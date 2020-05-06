import traceback

from appPublic.Singleton import SingletonDecorator
from appPublic.dictObject import DictObject

from .swift_messdata import SwiftComposedData,SwiftXorData
from .swift_field import SwiftBlock,SwiftXXField,SwiftXXXField
from .swift_segments import SwiftSegment
from .swiftxlsx_short import SwiftShortXlsx
from .swift_checker import SwiftChecker

class SwiftMessage(SwiftComposedData):
	def __init__(self,name,root=None,parent=None):
		super(SwiftMessage,self).__init__(name=name,
				root=None,parent=None,
				formatstr='',subnames=[])

classmapping = {
	"message":SwiftMessage,
	"block":SwiftBlock,
	"segment":SwiftSegment,
	"99field":SwiftXXField,
	"999field":SwiftXXXField,
	"composed":SwiftComposedData,
	"xor":SwiftXorData,
}

@SingletonDecorator
class AssemblyLine:
	def __init__(self):
		self.msgdic = {}
 
	def setDic(self,msgtype,dic):
		self.msgdic[msgtype] = dic

	def build(self,msgtype,direction='I'):
		dic = self.msgdic.get(msgtype+direction,None)
		if dic is None:
			xlsx = SwiftShortXlsx(msgtype,direction=direction)
			dic = xlsx.json()
			self.msgdic[msgtype+direction] = dic
		msgdic = DictObject(name='swiftmsg',object="message",children=dic['Specification'])
		swiftmsg = self.parse(msgdic,root=None,parent=None)
		swiftmsg.CheckingRule = dic['CheckingRule']
		swiftmsg.fieldMapping = dic['FieldMapping']
		swiftmsg.matchingRule = dic['MatchingRule']
		return swiftmsg

	def parse(self,dic,root=None,parent=None):
		if parent is None:
			root = None
		klass = classmapping[dic.get('object')]
		kwargs = dic.get('kwargs',{})
		kwargs['root'] = root
		kwargs['parent'] = parent
		kwargs['name'] = dic['name']
		print('name=',dic['name'])
		obj = klass(**kwargs)
		children =  dic.get('children',[])
		if parent is None:
			root = obj
		parent = obj
		for i,c in enumerate(children):
			obj = obj + (self.parse(c,root=root,parent=parent),c.get('name'))
		return obj

def unpack(text,needCheck=True):
	io = text[32]
	msgtype = 'MT' + text[33:36]
	asm = AssemblyLine()
	print(io,msgtype)
	msg = asm.build(msgtype,io)
	try:
		print(msg.children[1].formatstr)
		msg.textData = text
		msg.unpack()
		if needCheck:
			checker = SwiftChecker()
			checker.check(msg)
		return msg.innerData
	except Exception as e:
		print(e,traceback.format_exc())
		return None

def pack(data):
	d = DictObject(data)
	io = d.b2.direction
	msgtype = d.b2.msgtype
	asm = AssemblyLine()
	msg = asm.build(msgtype,io)
	try:
		msg.innerData = data
		if needCheck:
			checker = SwiftChecker()
			checker.check(msg)
		msg.pack()
		return msg.textData
	except Exception as e:
		print(e)
		return None

