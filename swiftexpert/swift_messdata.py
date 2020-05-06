
from appPublic.dictObject import DictObject
from .swift_format import FormatOptions,SwiftDelimiter,SwiftCrNl
from .swift_messagedata import SwiftData, BaseData

class SwiftComposedData(BaseData):
	def __init__(self,name,root=None,parent=None,formatstr='',subnames=[],opt_id=-1):
		super(SwiftComposedData,self).__init__(name,root=root,
				parent=parent,opt_id=opt_id)
		self.names = subnames
		self.formatstr = formatstr
		self.children = []
		self.children_dic = {}
		if formatstr!='':
			#print('formatstr=',formatstr)
			self.children = formatsplit(formatstr,root=root,parent=self)
			self.naming_sub()

	def naming_sub(self):
		if len(self.names) < len(self.children):
			self.names = [ "field%d" % i for i in range(len(self.children)) ]
		for i,c in enumerate(self.children):
			c.name = self.names[i]
			self.children_dic[self.names[i]] = c

	def getDescendant(self,identifycode):
		names = identifycode.split('.')
		obj = self
		for n in names:
			obj = obj.getChild(n)
			if obj is None:
				return None
		return obj

	def getChild(self,name):
		return self.children_dic[name]
			
	def __add__(self,m):
		a,name = m
		if type(a) == type(''):
			self.children += formatsplit(a,root=root,parent=self)
			self.names = self.names + name
		else:
			self.children.append(a)
			self.names.append(name)
		self.naming_sub()
		return self

	def addChild(self,data):
		self.children.append(data)

	def optioncheck(self):
		return True, None
			
	def pack(self):
		self.textData = ''
		txt = ''
		if self.innerData is None:
			self.text = ''
			if not self.isOptional():
				raise Exception('data(%s) is not optional' % self.name)
			return

		if type(self.innerData) == type(''):
			self.textData = self.innerData
			self.innerData = {}
			txt = self.unpack()
			if txt != '':
				raise Exception('Data error(%s)' % (self.textData))
		status = []
		for i,c in enumerate(self.children):
			if c.__class__  == SwiftCrNl:
				if txt != '':
					txt = txt + c.delimiter
					status.append(True)
				else:
					status.append(False)

			elif c.__class__  == SwiftDelimiter:
				txt = txt + c.delimiter
				status.append(True)
			else:
				v = self.innerData.get(c.name)
				if v is None:
					c.textData = ''
					status.append(False)
				else:
					c.setInnerData(v)
					try:
						c.pack()
						status.append(True)
					except:
						status.append(False)
				txt = txt + c.textData
		allstatus=[]
		for i,t in enumerate(status):
			if t:
				allstatus.append(True)
			else:
				if self.children[i].isOptional():
					allstatus.append(True)
				else:
					allstatus.append(False)
		if all(allstatus):
			self.textData = txt
		else:
			selftextData = ''

	def debug(self,*args,**kw):
		if self.name!="b4":
			return
		print(*args,**kw)

	def _try(self,text):
		# text = self.textData
		oldtext = text
		data = DictObject()
		status = []
		for i,c in enumerate(self.children):
			if c.isDisabled():
				status.append(False)
				continue
			if c.__class__ in [ SwiftCrNl, SwiftDelimiter ]:
				if not text.startswith(c.delimiter):
					status.append(False)
				else:
					text = text[len(c.delimiter):]
					status.append(True)
				continue

			c.setTextData(text)
			text_old=text
			c.innerData = None
			text = c.unpack()
			if text is None:
				print(f'{c.path()} unpack return None')
				raise Exception(f'{c.path()} return None')
			if text_old == text:
				status.append(False)
			else:
				data[c.name] = c.innerData
				status.append(True)

		allstatus = []
		for i,t in enumerate(status):
			if t:
				allstatus.append(t)
			elif self.children[i].isOptional():
				allstatus.append(True)
			elif self.children[i].__class__ == SwiftCrNl and \
				all([not i for i in status[i+1:]]):
				allstatus.append(True)
			else:
				allstatus.append(False)
		if all(allstatus):
			return text, data
		else:
			return oldtext, DictObject()
			
	def unpack(self):
		self.innerData = DictObject()
		options = [[i,c] for i,c in enumerate(self.children) if c.isOptional() ]
		ret_buf = []
		ret_buf.append(self._try(self.textData))
		for i,c in options:
			c.disable(True)
			ret_buf.append(self._try(self.textData))
	
		for i,c in options:
			c.disable(False)
		txt = self.textData
		data = DictObject()
		for t,d in ret_buf:
			if t is None or d is None:
				print(f'-----t={t},d={d}---{ret_buf}---textdata={self.textData}----')
				continue
			if len(t) < len(txt):
				txt = t
				data = d
			
		self.innerData = data
		return txt

class SwiftXorData(BaseData):
	def __init__(self,name='',fmtdic={},root=None,parent=None,opt_id=-1):
		super(SwiftXorData,self).__init__(name,root=root,
					parent=parent,opt_id = opt_id)
		self.fmtdic = fmtdic
		self.xorchildren = []
		self.unpack_name = None
		self.pack_name = None
		self._build()

	def _build(self):
		try:
			for n,(f , names) in self.fmtdic.items():
				self.xorchildren.append(SwiftComposedData(n,
					formatstr=f,subnames=names))
		except Exception as e:
			print(self.name,self.parent.name,
				'parent.formatstr=',self.parent.formatstr,'fmtdic=',self.fmtdic,e)
			raise e
		
	def setUnpackName(self,name):
		self.unpack_name = name

	def setPackName(self,name):
		self.pack_name = name

	def pack(self):
		self.textData = ''
		for d in self.xorchildren:
			if d.name == self.name:
				d.setInnerData(self.innerData)
				d.pack()
				self.setTextData(d.textData)

	def unpack(self):
		for d in self.xorchildren:
			if d.name == self.name:
				d.setTextData(self.textData)
				txt = d.unpack()
				self.setInnerData(d.innerData)
				return txt
		return self.textData
		# names=[d.name for d in self.xorchildren ]
		# raise Exception(f'{self.name} not defined {names}')


def findRightBrackets(s):
	l = len(s)
	pair = 0
	for i,c in enumerate(s):
		if c==']' and pair == 0:
			if i + 1 >= l:
				return s[:i],None
			return s[:i],s[i+1:]
		if c==']' and pair > 0:
			pair = pair - 1
		if c=='[':
			pair = pair + 1
	return None,None

def formatsplit(txt,root=None,parent=None):
	fmtcharset = "0123456789-!*nacdhxyze"

	def parseformat(txt,opt_id):
		sd = SwiftData(root=root,parent=parent,
				formatstr=txt,opt_id=opt_id)
		return sd

	def parseDelimiter(txt,opt_id):
		if txt == '\r\n':
			return SwiftCrNl(txt,root=root,parent=parent,opt_id=opt_id)
		sd = SwiftDelimiter(txt,root=root,parent=parent,opt_id = opt_id)
		return sd
		
	opt_flg = False
	opt_id = -1
	delimiter = ''
	fmttxt = ''
	rets = []
	skip = -1
	for i,c in enumerate(txt):
		if i < skip:
			continue
		if c == '[':
			if delimiter != '':
				sd = parseDelimiter(delimiter,opt_id)
				rets.append(sd)
				delimiter = ''
			subs,sibling = findRightBrackets(txt[i+1:])
			if subs == None:
				raise Exception("'[' invalid")
			sd = SwiftComposedData('',root=root,parent=parent,formatstr=subs,opt_id=1)
			rets.append(sd)
			if sibling is None:
				break
			skip = len(txt) - len(sibling)
			continue

		if c==']':
			raise Exception("']' invalid")

		o_id = -1
		if opt_flg:
			o_id = opt_id
		if c not in fmtcharset:
			if fmttxt != '':
				raise Exception('%s not stoped' % fmttxt)
			delimiter = delimiter + c
		else:
			if delimiter != '':
				sd = parseDelimiter(delimiter,opt_id)
				rets.append(sd)
				delimiter = ''
			fmttxt = fmttxt + c
			if c in 'nachxyzde':
				dic = parseformat(fmttxt,o_id)
				rets.append(dic)
				fmttxt = ''
	if fmttxt != '':
		raise Exception("(%s) is invalid swift format" % fmttxt)
	if delimiter != '':
		rets.append(parseDelimiter(delimiter,opt_id))
	return rets
	
if __name__ == '__main__':
	fmt = '[/1a][/34x]\r\n4!a2!a2!c[3!c]'
	text = '/0000\r\nWWWWKK99'
	c = SwiftComposedData('test',formatstr=fmt,opt_id=-1)
	c.textData = text
	c.unpack()
	print(c.innerData)

