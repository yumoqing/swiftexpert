from swiftexpert.swiftxlsx import SwiftXlsx
from swiftexpert.assemblyline import AssemblyLine

def build(smdfile):
	smdf = SwiftXlsx(smdfile)
	data = smdf.json()
	asm = AssemblyLine()
	for d in data:
		asm.setDic(d.name,d)

def getText(f):
	with open(f,'rb') as f:
		b = f.read().decode('utf-8')
		return b

def pack(msgtype,data):
	asm = AssemblyLine()
	obj = asm.build(msgtype)
	if obj is None:
		print(msgtype,' message type object not found')
		sys.exit(1)
	obj.setInnerData(data)
	obj.pack()
	return obj.textData

def unpack(msgtype,text):
	asm = AssemblyLine()
	obj = asm.build(msgtype)
	if obj is None:
		print(msgtype,' message type object not found')
		print(asm.msgobjs.keys())
		sys.exit(1)
	obj.setTextData(text)
	obj.unpack()
	return obj.innerData
	
if __name__ == '__main__':
	import os
	import sys
	if len(sys.argv) < 1:
		print('usage\n%s smdfile msgtype_num' % sys.argv[0])
		sys.exit(1)
	
	for num in sys.argv[1:]:
		smdf = '../config/MT' + num + '.xlsx'
		if not os.path.isfile(smdf):
			print(smdf,'not exists')
			continue
		build(smdf)
		msgf = '../msgs/MT' + num + '.txt'
		if os.path.isfile(msgf):
			text = getText(msgf)
			d = unpack('MT' + num,text)
			print(d)
			txt = pack('MT' + num,d)
			print(txt)

