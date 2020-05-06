from .swift_messdata import SwiftComposedData

class SwiftRuleError(Exception):
	def __init__(self,errcode):
		Exception.__init__(self)
		self.errcode = errcode
		
	def __str__(self):
		return f'Error, Error Code={self.errcode}'

class SwiftChecker:
	def __init__(self):
		self.checkers = {
			"Not allowed":self.notAllowed,
			"Mandatory":self.mandatory,
			"Optional":self.optional,
			"Present":self.present,
			"Not present":self.notPresent,
		}

	def addChecker(self,name,func):
		self.checkers[name] = func

	def singleCheck(self,d,r):
		for k,v in r.items():
			if k is None or v is None:
				return True
			checker = self.checkers.get(v,None)
			if checker is None:
				return self.checkValue(d,k,v)
			# print(f'{k}:{v}:{checker}')
			return checker(d,k)

	def checkValue(self,d,e,v):
		d = self.getDataElement(d,e)
		if d is None:
			return False
		if ',' in v:
			return d in v.split(',')
		return d == v

	def getObjectElement(self,msgobj,e):
		keys = e.split(e)
		obj = msgobj
		for k in keys:
			obj = obj.getChild(k)
			if obj is None:
				return None
		return obj
			
	def getDataElement(self,data,e):
		keys = e.split('.')
		for k in keys:
			d = data.get(k,None)
			if d is None:
				return None
			data = d
		return d

	def present(self,d,e):
		return self.mandatory(d,e)

	def notPresent(self,d,e):
		return self.notAllowed(d,e)

	def optional(self,d,e):
		return True

	def notAllowed(self,d,e):
		d = self.getDataElement(d,e)
		if d is None:
			return True
		return False

	def mandatory(self,d,e):
		d = self.getDataElement(d,e)
		if d is None:
			return False
		return True

	def checkMandatory(self,msg):
		def _checkMandatory(obj,data):
			for c in obj.children:
				if not isinstance(c,SwiftComposedData):
					continue
				if c.isOptional() and data.get(c.name,None) is None:
					continue
				if not c.isOptional() and data.get(c.name,None) is None:
					raise Exception(f'{c.path()} is Mandatory but not data present')
				_checkMandatory(c,data.get(c.name))

			return True
		data = msg.innerData
		if data is None:
			raise Exception('innerData is None')
		return _checkMandatory(msg,data)

	def checkRules(self,msg,rules):
		for r in rules:
			errcode = r['errcode']
			for i, cr in enumerate(r['rules']):
				rez = self.singleCheck(msg.innerData,cr)
				print(f'{__file__}:{errcode},{cr},{rez}')
				if i==0 and not rez:
					break
				if not rez:
					return errcode
		return None
					
	def check(self,msg):
		try:
			self.checkMandatory(msg)
		except Exception as e:
			print(e)
			raise SwiftRuleError('C32')
		rules = msg.CheckingRule
		r = self.checkRules(msg,rules)
		if r is not None:
			print(f'{__file__},check error error code={r}')
			raise SwiftRuleError(r)
		return True
			
