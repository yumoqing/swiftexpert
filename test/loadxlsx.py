
import sys
from swiftexpert.swiftxlsx import SwiftXlsx
from swiftexpert.assemblyline import AssemblyLine

def load():
	ret = []
	for f in sys.argv[1:]:
		x = SwiftXlsx(msgtype=f,direction='O')
		ret = ret + x.json()

	return ret

load()
