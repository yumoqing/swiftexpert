import sys
from swiftexpert.swiftxlsx_short import SwiftShortXlsx,pblock
from appPublic.dictObject import showData

for xf in sys.argv[1:]:
	x = SwiftShortXlsx(sys.argv[1],direction='O')
	d = x.json()
	print(showData(d))
	#pblock(d[0])
