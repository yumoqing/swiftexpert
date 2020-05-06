import os
import sys
sys.path.append('.')
import openpyxl as xlsx

from appPublic.dictObject import extend,showData

from appPublic.dictObject import DictObject
from appPublic.folderUtils import folderList
from .identifier import tag_xor


def nl2crnl(s):
	if type(s) != type(''):
		return ''
	a = ''.join(s.split('\r'))
	b = '\r\n'.join(s.split('\n'))
	return b

def psegment(level,j):
	print('\t' * level,j.object,j.name,j.kwargs.repeat_flg,j.kwargs.status)
	for c in j.children:
		pchild(level+1,c)

def p99field(level,j):
	print('\t' * level,j.object,j.name,j.kwargs.tag,j.kwargs.formatstr)

def pchild(l,j):
	if j.object=='segment':
		psegment(l,j)
	else:
		p99field(l,j)

def pblock(j):
	print('block',j.name)
	for c in j.children:
		pchild(1,c)

class CheckingRule:
	def __init__(self,wb):
		self.wb = wb

	def checkrules(self,row,checkfields,rules):
		rule = {
			'errcode':row[0].value,
			'rules':[]
		}
		for i,c in enumerate(row[1:]):
			if c is None:
				break
			r = {checkfields[i]:c.value}
			rule['rules'].append(r)
		rules.append(rule)
		return rules
		
	def checkingfields(self,row):
		fields = []
		for c in row[1:]:
			if c is None:
				break
			fields.append(c.value)
		return fields

	def json(self):
		checkrules = []
		self.lifo = []
		ws = self.wb['CheckingRule']
		checkfields = []
		for row in ws.rows:
			if row[0].value=='errcode':
				checkfields = self.checkingfields(row)
			else:
				checkrules = self.checkrules(row,checkfields,checkrules)
		
		return {'CheckingRule':checkrules}
		
class FieldMapping:
	def __init__(self,wb):
		self.wb = wb

	def json(self):
		return {'FieldMapping':[]}

class MatchingRule:
	def __init__(self,wb):
		self.wb = wb
	
	def json(self):
		return {'MatchingRule':[]}

class Specification:
	def __init__(self,wb):
		self.wb = wb
		self.name = 'Specification'
		self.actions={
			"block":self.block,
			"endblock":self.endblock,
			"segment":self.segment,
			"endsegment":self.endsegment,
			"99field":self._99field,
			"appendfield":self.appendField,
		}

	def getkey(self,row):
		if row is None:
			return None
		s = row[0].value
		if s is None and self.lastobj.object=='99field':
			return 'appendfield'
		if s is None:
			print('lastobj=',self.lastobj)
			return None
		if s.startswith('M = Mandatory'):
			return None
		if s == 'block':
			return 'block'
		if s == 'endblock':
			return 'endblock'
		if s in 'MO':
			self.defaultCurObj()
			return '99field'
		if s.startswith('Mandatory') or \
					s.startswith('Optional') or \
					s.startswith('----->'):
			self.defaultCurObj()
			return 'segment'
		if s.startswith('End of') or s.startswith('-----|'):
			return 'endsegment'

	def block(self,row):
		ns = [] if row[4].value is None else row[4].value.split(',')
		block = DictObject(object='block',
			name=row[1].value,
			kwargs=DictObject(
			tag=str(row[2].value),
			formatstr='' if row[3].value is None else row[3].value,
			subnames=ns
			),
			children=[],
			schildren=[]
		)
		self.curobj.children.append(block)
		self.lifo.append(self.curobj)
		self.curobj = block

	def endblock(self,row):
		return self._end(row,'block')

	def getSegmentName(self):
		x = len(self.curobj.schildren)
		if self.curobj.object == 'block':
			name = 'seg_' + chr(ord('a') + x)
			# print('self.curobj=',self.curobj.name,name)
			return name
		m = len(self.curobj.name[4:])
		if m % 2 == 0:
			name = self.curobj.name + chr(ord('a') + x)
		else:
			name = self.curobj.name + str(x)
		return name

	def appendField(self,row):
		_fmt = 3
		if len(row) == 7:
			_fmt = 5
		s = self.lastobj.kwargs.formatstr
		self.lastobj.kwargs.formatstr = s + '\r\n' + row[_fmt].value

	def _99field(self,row):
		_status=0
		_tag = 1
		_label = 2
		_fmt = 3
		if len(row) == 7:
			_label = 4
			_fmt = 5

		tag = str(row[_tag].value)
		fmtstr = nl2crnl(row[_fmt].value)
		if fmtstr.startswith('copy'):
			fmtstr = ''
		if fmtstr.startswith('Empty'):
			fmtstr = ''
		if ' ' in tag:
			tag = tag.split(' ')[0]
		if tag[-1]!='a' and ' ' in fmtstr:
			fmtstr = fmtstr.split(' ')[0]
		name='f_' + str(tag)
		object = '99field'
		if self.curobj.name == 'b3' or self.curobj.name == 'b5':
			object = '999field'
		field = DictObject(object=object,
			name=name,
			kwargs=DictObject(status=row[_status].value,
				tag=tag,
				label=row[_label].value,
				subnames=[],
				formatstr=fmtstr
			),
			children=[]
		)
		self.curobj.children.append(field)
		self.lastobj = field

	def segment(self,row):
		name = self.getSegmentName()
		status = 'M' if 'Mandatory' in row[0].value else 'O'
		repeat_flg = False
		if row[0].value == '----->' or 'Repetitive' in row[0].value:
			repeat_flg = True
		seg = DictObject(object='segment',
			name=name,
			kwargs=DictObject(status=status,
				repeat_flg=repeat_flg),
			children=[],
			schildren=[],
		)
		self.curobj.children.append(seg)
		self.curobj.schildren.append(seg)
		self.lifo.append(self.curobj)
		self.curobj = seg
		self.lastobj = seg

	def _end(self,row,objtype):
		if self.curobj.object != objtype:
			raise Exception('mismatch type(%s)-(%s)' % ( self.curobj,objtype))
		self.curobj = self.lifo[-1]
		self.lifo = self.lifo[:-1]

	def endsegment(self,row):
		return self._end(row,'segment')

	def defaultCurObj(self):
		if self.curobj is self:
			msgdic = DictObject(name='b4',
				object="block",children=[],
				kwargs=DictObject(tag='4'),
				schildren=[])
			self.children.append(msgdic)
			self.curobj = msgdic
			self.lastobj = msgdic

	def init(self):
		self.lifo = []
		self.children = []
		self.curobj = self
		self.lastobj = self
		self.object = 'container'

	def json(self):
		self.init()
		ws = self.wb['Specification']
		for i,row in enumerate(ws.rows):
			k = self.getkey(row)
			act = self.actions.get(k,None)
			if act is None:
				print('ignore...',[i.value for i in row])
				continue
			act(row)
			print([i.value for i in row],
					'lifo=','None' if len(self.lifo) == 0 else 'name=%s type=%s' % (self.lifo[-1].name,self.lifo[-1].object),
					'curobj=(%s,%s)' % (self.curobj.name,self.curobj.object))
		if len(self.lifo) > 0:
			print(self.lifo,'not finished')
			raise Exception('stack not empty')
		
		return {'Specification':self.children}

class SpecificationWithDefault(Specification):
	def __init__(self,wb,defdata):
		Specification.__init__(self,wb)
		self.defchildren = defdata['Specification']

	def init(self):
		self.lifo = []
		self.children = self.defchildren
		self.curobj = self
		self.lastobj = self
		self.object = 'container'

	def block(self,row):
		for b in self.children:
			if b.name == row[1].value:
				self.lifo.append(self.curobj)
				self.curobj = b
				self.lastobj = b
				return
		raise Exception('block error(%s)',row[1].value)

	def defaultCurObj(self):
		if self.curobj.object == 'container':
			for b in self.children:
				if b.name == 'b4':
					self.curobj = b
					self.lastobj = b
					return
			raise Exception('block error(%s)',row[1].value)

class SwiftShortXlsx:
	def __init__(self,msgtype='MT300',direction='I'):
		self.direction = direction
		self.defaultFile = self.getDefaultFile()
		self.dwb = xlsx.load_workbook(self.defaultFile)
		self.def_spec = Specification(self.dwb)
		self.xlsxfile = self.getXlsxFile(msgtype)
		self.wb = xlsx.load_workbook(self.xlsxfile)
		self.spec = SpecificationWithDefault(self.wb,self.def_spec.json())
		self.cr = CheckingRule(self.wb)
		self.fm = FieldMapping(self.wb)
		self.mr = MatchingRule(self.wb)

	def getDefaultFile(self):
		basePath = os.path.join(os.path.dirname(__file__),'conf')
		fp = os.path.join(basePath,self.direction + '.xlsx')
		if os.path.isfile(fp):
			return fp
		raise Exception(f'{fp} is not exist')
		
	def getXlsxFile(self,msgtype):
		basePath = os.path.join(os.path.dirname(__file__),'conf')
		folders = [i for i in folderList(basePath)]
		folders.sort()
		folders.reverse()
		for f in folders:
			fp = os.path.join(f,msgtype + '.xlsx')
			if os.path.isfile(fp):
				return fp
		raise Exception(f'{msgtype} is not configure')
		
	def json(self):
		ret = {}
		ret.update(self.spec.json())
		ret.update(self.cr.json())
		ret.update(self.fm.json())
		ret.update(self.mr.json())
		return ret

if __name__ == '__main__':
	import sys

	xlsx = SwiftXlsx(sys.argv[1])
	data = xlsx.json()
	print(data)
	sys.exit(0)
