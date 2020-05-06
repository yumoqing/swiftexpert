
class SwiftException(Exception):
	def __init__(self,path,errcode):
		self.path = path,
		self.errcode = errcode

	def __str__(self):
		return f'swift error,path={self.path},errcode={self.errcode}'

if __name__ == '__main__':
	e = SwiftException('/b4/30a/A/p','T70')
	print(e)
