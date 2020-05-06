from swiftexpert.assemblyline import unpack

import sys

for fp in sys.argv[1:]:
	f = open(fp,'rb')
	txt = f.read().decode('utf-8')
	f.close()
	print('unpack ----',fp)
	x = unpack(txt)
	print(x)
