import traceback

from .swift_messdata import SwiftComposedData

class SwiftSegment(SwiftComposedData):
	def __init__(self,name,root=None,parent=None,
			status='O',repeat_flg=False):
		if status=='O':
			opt_id = 0
		else:
			opt_id = -1
		super(SwiftSegment,self).__init__(name,root=root,
				parent=parent,formatstr='',
                                subnames=[],opt_id=opt_id)
		self.status = status
		self.repeat_flg = repeat_flg

	
	def isOptional(self):
		return self.status == 'O'

	def pack(self):
		self.textData = ''
		if self.repeat_flg:
			txt = ''
			for rec in self.innerData:
				for i,c in enumerate(self.children):
					v = rec.get(self.names[i])
					if v is None:
						if not c.isOptional():
						
							#print(self.innerData.keys(),self.names[i])
							raise Exception('(%s)not data error,inner data is None' % self.names[i])
						c.textData = ''
					else:
						c.setInnerData(v)
						c.pack()
						txt = txt + c.textData
			self.setTextData(txt)
		else:
			try:
				super(SwiftSegment,self).pack()
			except Exception as e:
				if self.isOptional():
					return
				raise e
	
	def unpack(self):
		print('unpack segment',self.name,'repeat=',self.repeat_flg)
		data = []
		if self.repeat_flg:
			leave = self.textData
			text = ''
			while leave != text:
				try:
					text = leave
					leave,rec = self._try(text)
					if leave != text:
						data.append(rec)
				except:
					break
			if len(data) == 0:
				print('unpack segment',self.name,'failed')
				return leave

			self.setInnerData(data)
			print('unpack segment',self.name,'finished')
			return leave
		else:
			text = self.textData
			try:
				txt,d = self._try(self.textData)
				if text!=txt:
					self.innerData = d
					print('unpack segment',self.name,'finished')
				else:
					print('unpack segment',self.name,'failed')
				return txt
			except Exception as e:
				print('unpack segment',self.name,'failed')
				if self.isOptional():
					return text
				msg = traceback.format_exc()
				print('e=',e,msg)
				raise e
