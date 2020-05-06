
class SwiftCharset:
	charsets = {
	"n": "1234567890",
	"a": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
	"c": "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ",
	"h": "1234567890ABCDEF",
	"d": ',1234567890',
	"e": ' ',
	"x": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ """,
	"y": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-()/='+:?!\"%&*<>; ",
	"z": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-()/='+:?!"%&*<>;{@#_ """,
	}
	
	def scope(self,name):
		return self.charsets.get(name,None)

	def isValid(self,name,c):
		return c in self.charsets.get(name,'')

	def express(self,name,s):
		if not name in "xyz":
			return s
		ret = ''
		for i in s:
			if self.isValid(name,i):
				ret = ret + i
			else:
				x = ord(i)
				ret = ret + '??%02x' % x
		return ret

