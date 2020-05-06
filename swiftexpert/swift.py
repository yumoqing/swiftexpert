
import os
from .swift_messdata import SwiftComposedData
from .swift_field import SwiftXXXField, SwiftBlock, SwiftXXField
from .swiftxlsx_short import SwiftShortXlsx
from .assemblyline import AssemblyLine

def loadB4(msgtype,parent):
	xlsx = SwiftShortXlsx(f)
	d = xlsx.json()
	asm = AssemblyLine()
	b4 = asm.parse(d['Specification'],root=parent,parent=parent)
	parent.checkRules = d['CheckingRule']
	parent.fieldMappig = d['FieldMapping']
	parent.matchingRule = d['MatchingRule']
	return b4

class SwiftMessage(SwiftComposedData):
	def __init__(self,direction,msgtype):
		super(SwiftMessage,self).__init__(name=msgtype,
				root=None,parent=None,
				formatstr='',subnames=[])

def unpack(text):
	io = text[32]
	msgtype = 'MT' + text[33:36]
	msg = SwiftMessage(io,msgtype)
	try:
		msg.textData = text
		msg.unpack()
		return msg.innerData
	except Exception as e:
		print(e)
		return None

def pack(data):
	d = DictObject(data)
	io = d.b2.direction
	msgtype = d.b2.msgtype
	msg = SwiftMessage(io,msgtype)
	try:
		msg.innerData = data
		msg.pack()
		return msg.textData
	except Exception as e:
		print(e)
		return None

