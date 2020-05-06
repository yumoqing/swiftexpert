from swiftexpert.swift_messdata import SwiftComposedData

"""
"""
def unpack(fmtstr,text,subnames=[]):
	s = SwiftComposedData('test',formatstr=fmtstr,subnames=subnames)
	for i,c in enumerate(s.children):
		print(s.names[i],c.name,c.__class__)
	print('childrens=',len(s.children),'innerData=',s.innerData)
	s.setTextData(text)
	txt = s.unpack()
	print('text=',text,':\nunpacked_data=',s.innerData,':\nremain_text=',txt,':')
	
#fmtstr="[ISIN1!e12!c]\r\n[4*35x]"
#data="ISIN US3135G0BA00\r\nBONDFNMA-NEW 2.375\r\n11APR16/0D/2016/04/11/2.375PCT"
#unpack(fmtstr,data)
#unpack('4!c[/30x]','TRRR')
#unpack(fmtstr,'/AT GG (GT) TR')
fmtstr="1!a3!n4!n6!n12!c4!n6!n6!n4!n1!a"
data="O5350000110104CEDELULLAXXX00000000001101980000N"
unpack(fmtstr,data)
