from appPublic.dictObject import DictObject
from .swift_format import FormatOptions, SwiftDataFormat

class BaseData:
	def __init__(self,name='',root=None,parent=None,opt_id=-1):
		self.name = name
		self.parent = parent
		self.root = root
		self.innerData = None
		self.textData = None
		self.checks = {}
		self.status = 'O'
		self.opt_id = opt_id
		self.pack_stack = []
		self.unpack_stack = []
		self._disable = False

	def path(self):
		if self.parent is None:
			return self.name
		else:
			return self.parent.path() + '/' + self.name

	def disable(self,f):
		self._disable = f

	def isDisabled(self):
		return self._disable

	def isOptional(self):
		# print("hahah ---- here",self.opt_id)
		return self.opt_id > -1

	def setInnerData(self,data):
		self.innerData = data

	def setTextData(self,text):
		self.textData = text

	def pack(self):
		"""
		data to text
		"""
		pass
		#self.textData = self.parser.pack(self.innerData)

	def unpack(self):
		return ''

	def setChecker(self,n,f):
		self.checks[n] = f

	def check(self):
		"""
		return result,(data_name,funcname)
		"""
		for n,f in self.checks.items():
			r = f(self.innerData)
			if not r:
				return False,(self.name,n)
		if hasattr(self,'children'):
			r,loc = self.optioncheck()
			if not r:
				return False, loc
			for c in self.children:
				if type(c) == type(''):
					continue
				r,loc = c.check()
				if not r:
					return False,loc
		return True,None

class SwiftData(BaseData):
	def __init__(self,root=None,parent=None,formatstr='',name='',opt_id=-1):
		super(SwiftData,self).__init__(name,root=root,
				parent=parent,opt_id=opt_id)
		self.formatstr = formatstr
		self.name = name
		if formatstr != '':
			fo = FormatOptions()
			opts,fmts = fo.parse(formatstr)
			if opts is None:
				raise Exception('data format error(%s)' % formatstr)	
			self.parser = SwiftDataFormat(**opts)

	def setParser(self,parser):
		self.parser = parser

	def pack(self):
		self.textData = self.parser.pack(self.innerData)

	def unpack(self):
		v,txt = self.parser.unpack(self.textData)
		self.innerData = v
		return txt

