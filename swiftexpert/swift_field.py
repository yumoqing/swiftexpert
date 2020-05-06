from appPublic.dictObject import DictObject
from .swift_messagedata import BaseData
from .swift_messdata import SwiftComposedData,SwiftXorData
from .identifier import tag_xor

class SwiftField(SwiftComposedData):
	def __init__(self,tag,name='',label='',
			root=None,parent=None,
			opt_flg=False,formatstr='',
				subnames=[]):
		super(SwiftField,self).__init__(name,root=root,
				parent=parent,formatstr=formatstr,
				subnames=subnames,opt_id=-1)
		self.tag = tag
		self.label = label
		self.opt_flg = opt_flg

	def isOptional(self):
		return self.opt_flg
	
class IMessage(SwiftField):
	def __init__(self):
		super(IMessage,self).__init__('imessage',
				name='imessage',root=None,
				parent=None,formatstr='',subnames=[])
		self.b1 = SwiftBlock(tag='1',name='b1',
					root = self,parent=self,
					formatstr='1!a2!n12!c4!n6!n',
					subnames=['appIdentifier',
							'du_identifier',
							'local_addr',
							'session_id',
							'series_id'])
		self.b2 = SwiftBlock(tag='2',name='b2',
					root=self,parent=self,
					formatstr='I3!n12!c1!a1!n3!n',
					subnames=['',
							'msgtype',
							'remote_addr',
							'priority',
							'transfer_status',
							'timeout'])
		self.b3 = SwiftBlock(tag='3',name='b3',
					root=self,parent=self,
					formatstr='',subnames=[])
		self.b5 = SwiftBlock(tag='5',name='b5',
					root=self,parent=self,
					formatstr='',subnames=[])
class OMessage(SwiftField):
	def __init__(self):
		super(IMessage,self).__init__('imessage',
				name='imessage',root=None,
				parent=None,formatstr='',subnames=[])
		self.b1 = SwiftBlock(tag='1',name='b1',
					root = self,parent=self,
					formatstr='1!a2!n12!c4!n6!n',
					subnames=['appIdentifier',
							'du_identifier',
							'local_addr',
							'session_id',
							'series_id'])
		self.b2 = SwiftBlock(tag='2',name='b2',
					root=self,parent=self,
					formatstr='O3!n4!n6!n12!c4!n6!n6!n4!n1a',
					subnames=['',
							'msgtype',
							'send_time',
							'send_date',
							'remote_addr',
							'session_id',
							'series_id',
							'receive_date',
							'receive_time',
							'priority'])
		self.b3 = SwiftBlock(tag='3',name='b3',
					root=self,parent=self,
					formatstr='',subnames=[])
		self.b5 = SwiftBlock(tag='5',name='b5',
					root=self,parent=self,
					formatstr='',subnames=[])

class SwiftBlock(SwiftField):
	def __init__(self,tag='',name='',root=None,
				parent=None,
				formatstr='',
				subnames=[],
				opt_flg=False):
		if tag not in '12345':
			raise Exception('block id(%s) Error' % tag)

		super(SwiftBlock,self).__init__(tag,name=name,root=root,
				parent=parent,
				formatstr=formatstr,subnames=subnames,
				opt_flg=opt_flg)
		ss = '\r\n' if tag == '4' else ''
		self.tag = tag
		self.startword = '{' + tag + ':' + ss
		self.endword = '-}' if tag=='4' else '}'

	def pack(self):
		text = self.startword
		super(SwiftBlock,self).pack()
		text = text + self.textData
		text = text + self.endword
		self.textData = text

	def unpack(self):
		print('unpack block',self.tag)
		text = self.textData
		if not text.startswith(self.startword):
			raise Exception('unpack failed, error at (%s),startword=:%s:' % (text,self.startword))
		text = text[len(self.startword):]
		txt, d = self._try(text)
		if not txt.startswith(self.endword):
			print('unpack block',self.tag,'failed')
			raise Exception('unpack failed,error at '+txt)
		self.innerData = d
		txt = txt[len(self.endword):]
		print('unpack block',self.tag,'finished')
		return txt

class SwiftXXField(SwiftField):
	def __init__(self,tag,name='',label='',
				root='',parent=None,status="O",
				formatstr='',subnames=[],pack_name=''):
		self.xor_flg = False
		self.checkTag(tag,name)
		opt_flg = False
		if status == 'O':
			opt_flg = True
		super(SwiftXXField,self).__init__(tag,name=name,
				label=label,
				root=root,
				parent=parent,
				formatstr='' if self.xor_flg else formatstr,
				subnames=subnames,
				opt_flg=opt_flg)
		if len(tag)==3 and tag[2] == 'a':
			d = tag_xor(tag,formatstr)
			d.kwargs.root = root
			d.kwargs.parent = self
			# print('SwiftXXField.__init__(),d=',d)
			self + (SwiftXorData(**d.kwargs),d.name)
		self.tag = tag
		self.startword = ':%s:'% tag
		self.endword = '\r\n'
		# print('99field.__init__(),tag=',self.tag,'name=',self.name)

	def checkTag(self,tag,name):
		self.tag = tag
		tlen = len(tag)
		if tlen not in [2,3]:
			raise Exception('name=%s Tag(%s) length error' % (name,tag))
		if tlen == 3 and tag[2] not in 'aABCDEFGHIJKLMNOPQRSTUVWXYZ':
			raise Exception('Tag(%s) invalid' % tag)
		if tlen == 3 and tag[2] == 'a':
			self.xor_flg = True

	def pack(self):
		self.textData = ''
		text = self.startword
		if self.xor_flg:
			keys = [i for i in self.innerData.keys()]
			pack_name = keys[0]
			text = text[:3] + pack_name + text[4:]
			self.children[0].name = pack_name
		super(SwiftXXField,self).pack()
		text = text + self.textData
		text = text + self.endword
		self.textData = text

	def unpack(self):
		print('unpack 99field',self.tag,self.name)
		def optionalReturnText(txt):
			if self.isOptional():
				return txt
			raise Exception('unpack error,tag=%s,startword=%s,txt=%s' \
				% (self.tag,
					self.startword,
					txt))

		text = self.textData
		if not self.xor_flg and not text.startswith(self.startword):
			print('unpack 99field',self.tag,'failed 1')
			return optionalReturnText(text)
		if self.xor_flg:
			if not text.startswith(self.startword[:3]):
				print('unpack 99field',self.tag,'failed 2')
				return optionalReturnText(text)
			if text[4] != ':':
				print('unpack 99field',self.tag,'failed 3')
				return optionalReturnText(text)
			self.children[0].name = text[3]
		self.textData = self.textData[len(self.startword):]
		txt = super(SwiftXXField,self).unpack()
		if txt is None:
			self.innerData = DictObject()
			print('unpack 99field',self.tag,'failed 4')
			return optionalReturnText(self.textData)
		if not txt.startswith(self.endword):
			print('unpack 99field',self.tag,'failed 5')
			self.innerData = DictObject()
			return optionalReturnText(text)

		print('unpack 99field',self.tag,'finished')
		return txt[len(self.endword):]

class SwiftXXXField(SwiftField):
	def __init__(self,tag,name='',label='',root='',parent=None,status="O",
				formatstr='',subnames=[],pack_name=''):
		self.xor_flg = False
		self.checkTag(tag)
		opt_flg = False
		if status == 'O':
			opt_flg = True
		super(SwiftXXXField,self).__init__(tag,name=name,label=label,root=root,
				parent=parent,formatstr=formatstr,
				subnames=subnames,
				opt_flg=opt_flg)
		self.startword = '{%s:'% tag
		self.endword = '}'

	def checkTag(self,tag):
		tlen = len(tag)
		if tlen != 3:
			raise Exception('Tag(%s) length error' % tag)

	def pack(self):
		text = self.startword
		super(SwiftXXXField,self).pack()
		text = text + self.textData
		text = text + self.endword
		self.textData = text

	def unpack(self):
		print('unpack 999field',self.tag,self.name)
		text = self.textData
		if not text.startswith(self.startword):
			print('unpack 999field',self.tag,self.name,'failed')
			return text
		self.textData = self.textData[len(self.startword):]
		txt = super(SwiftXXXField,self).unpack()
		if not txt.startswith(self.endword):
			print('unpack 999field',self.tag,self.name,'failed')
			return text

		print('unpack 999field',self.tag,self.name,'finished')
		return txt[len(self.endword):]


