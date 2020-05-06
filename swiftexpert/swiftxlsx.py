import openpyxl as xlsx

from appPublic.dictObject import DictObject
from .identifier import tag_xor

from .assemblyline import AssemblyLine


def nl2crnl(s):
	a = ''.join(s.split('\r'))
	b = '\r\n'.join(s.split('\n'))
	return b

class SwiftXlsx:
	def __init__(self,xlsxfile):
		self.xlsxfile = xlsxfile
		self.wb = xlsx.load_workbook(self.xlsxfile)
		self.actions={
			"segment":self.segment,
			"endsegment":self.endsegment,
			"block":self.block,
			"endblock":self.endblock,
			"99field":self._99field,
			"999field":self._999field,
		}

	def json(self):
		configs = []
		for  name in self.wb.sheetnames:
			msgdic = DictObject(name=name,
				object="message",children=[])
			self.lifo = []
			self.curobj = msgdic
			ws = self.wb[name]
			print('sheet=',name)
			self.readBlocks(ws)
			if len(self.lifo) > 0:
				print(self.lifo,'not finished')
				raise Exception('stack not empty')
			configs.append(msgdic)
			ws = self.wb[name]
		return configs

	def readBlocks(self,ws):
		self.curobj.children = []
		self.curtype = 'message'
		for i,row in enumerate(ws.rows):
			print([i.value for i in row])
			act = self.actions.get(row[0].value,None)
			if act is None:
				continue
			act(row)

	def _999field(self,row):
		field = DictObject(object='999field',
			name='f_' + str(row[2].value),
			kwargs=DictObject(status=row[1].value,
				tag=str(row[2].value),
				label=row[3].value,
				subnames=[],
				formatstr=nl2crnl(row[4].value)
			),
			children=[]
		)
		if field.kwargs.formatstr.startswith('Empty'):
			field.formatstr = ''

		self.curobj.children.append(field)

	def _99field(self,row):
		field = DictObject(object='99field',
			name='f_' + str(row[2].value),
			kwargs=DictObject(status=row[1].value,
				tag=str(row[2].value),
				label=row[3].value,
				subnames=[],
				formatstr=nl2crnl('' if row[4].value is None else row[4].value)
			),
			children=[]
		)
		if field.kwargs.formatstr.startswith('Empty'):
			field.kwargs.formatstr = ''

		#if len(field.kwargs.tag)==3 and field.kwargs.tag[2] == 'a':
		#	d = tag_xor(field.kwargs.tag,field.kwargs.formatstr)
		#	field.children.append(d)
		v = [c.value for c in row ]
		self.curobj.children.append(field)

	def segment(self,row):
		seg = DictObject(object='segment',
			name=row[1].value,
			kwargs=DictObject(status=row[2].value,
				repeat_flg=row[3].value),
			children=[]
		)
		self.curobj.children.append(seg)
		self.lifo.append(self.curobj)
		self.curobj = seg

	def block(self,row):
		block = DictObject(object='block',
			name=row[1].value,
			kwargs=DictObject(
			tag=str(row[2].value),
			formatstr='' if row[3].value is None else row[3].value
			),
			children=[]
		)
		self.curobj.children.append(block)
		self.lifo.append(self.curobj)
		self.curobj = block

	def _end(self,row,objtype):
		if self.curobj.object != objtype:
			raise Exception('mismatch type(%s)-(%s)' % ( self.curobj,objtype))
		self.curobj = self.lifo[-1]
		self.lifo = self.lifo[:-1]

	def endsegment(self,row):
		return self._end(row,'segment')

	def endblock(self,row):
		return self._end(row,'block')

if __name__ == '__main__':
	import sys

	SwiftObjs = []
	asm = AssemblyLine()
	xlsx = SwiftXlsx(sys.argv[1])
	data = xlsx.json()
	for d in data:
		m = asm.parse(d)
		SwiftObjs.append(m)
	with open('../test/msgs/MT300.txt','rb') as f:
		txt = f.read().decode('utf-8')
		x = SwiftObjs[0]
		x.setTextData(txt)
		print(txt)
		print('==================')
		x.unpack()
		print(x.innerData)
		print('==================')
		x.pack()
		print(x.textData)
		print('==================')
