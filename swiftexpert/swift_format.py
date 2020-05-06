
from appPublic.dictObject import DictObject

from .swift_charset import SwiftCharset

class FormatOptions:
	def __init__(self):
		self.datatype = 'x'
		self.cnt = 0
		self.min_cnt = 1
		self.fixlength = False
		self.lines = 0
		self.opt_id = -1
		self.v = 0
		self.datatype_finished = False
		self.all_finished = False

	def finished(self):
		return self.all_finished

	def dict(self):
		return {
			"datatype":self.datatype,
			"cnt":self.cnt,
			"min_cnt":self.min_cnt,
			"opt_id":self.opt_id,
			"fixlength":self.fixlength,
			"lines":self.lines,
		}
	
	def parse(self,fmt):
		for i, c in enumerate(fmt):
			if c in '*-!nacdhexyz':
				ret = self.eatMeanChar(c)
			elif c <= '9' and c >= '0':
				ret = self.eatNumber(c)
			else:
				#print('1 invalided char(%s) found at (%d)' % (c,i))
				return None, fmt
			if not ret:
				#print('2 invalided char(%s) found at (%d)' % (c,i))
				return None, fmt

			if self.finished():
				return self.dict(),fmt[i+1:]
		return None, fmt

	def eatMeanChar(self,c):
		if c == '-':
			self.min_cnt = self.v
			self.v = 0
			return True
		if c == '!':
			self.cnt = self.v
			self.v = 0
			self.fixlength = True
			return True
		if c == '*':
			self.lines = self.v
			self.v = 0
			return True
		if c in 'nachdxyze':
			if self.v == 0 and self.cnt == 0:
				return False
			if self.cnt == 0:
				self.cnt = self.v
			self.datatype = c
			self.all_finished = True
			return True

	def eatNumber(self,n):
		self.v = self.v * 10 + int(n)
		return True
		
class SwiftDelimiter:
	def __init__(self,delimiter,root=None,parent=None,opt_id=-1):
		self.opt_id = opt_id
		self.root = root
		self.parent = parent
		self.delimiter = delimiter
		self.innerData = delimiter
		self._disable = False
		self.textData = delimiter

	def disable(self,f):
		self._disable = f

	def isDisabled(self):
		return self._disable

	def isOptional(self):
		return False

	def pack(self):
		return self.delimiter

	def unpack(self):
		self.innerData = self.textData

	def check(self):
		return True,None

	def setInnerData(self,v):
		pass

	def setTextData(self,v):
		pass

class SwiftCrNl(SwiftDelimiter):
	def isOptional(self):
		return True
	
class SwiftDataFormat:
	def __init__(self, 
				datatype='x', 
				cnt=0,
				min_cnt = 1,
				fixlength=False,
				lines=1,
				opt_id=-1):
		self.dt = datatype
		self.cnt = cnt
		self.min_cnt = min_cnt
		self.fixlength = fixlength
		self.lines = lines
		self.opt_id = opt_id
		self.charset = SwiftCharset()

	def isOptional(self):
		return self.opt_id > -1

	def setOptionID(self,f):
		self.opt_id = f

	def info(self):
		print('dt=',self.dt)
		print('cnt=',self.cnt)
		print('min_cnt=',self.min_cnt)
		print('fixlength=',self.fixlength)
		print('lines=',self.lines)
		print('opt_id=',self.opt_id)

	def unpack(self,text):
		saved_text = text
		def handlerFloat(v,t):
			if self.dt == 'd':
				v = v.split(',')
				if len(v)!=2:
					return None,saved_text
				v = '.'.join(v)
				f = float(v)
				return f,t
			return v,t

		if text == '':
			return '',text
		value = ''
		line = 0
		x = ''
		nxt = 0
		stop = False
		total_len = len(text)
		for i,c in enumerate(text):
			if c == '\n':
				continue
			if c in self.charset.scope(self.dt):
				x = x + c
				if len(x) >= self.cnt:
					stop = True
				nxt = i + 1
			else:
				# print('char=',ord(c))
				stop = True
				nxt = i

			if not stop:
				continue

			value = value + x

			if self.lines < 2:
				if self.fixlength and len(x) < self.cnt:
					# print('here 3')
					return None, saved_text
				if len(x)<self.min_cnt:
					# print('here 4')
					return None,saved_text
				# print('--here---5')
				return handlerFloat(value, text[nxt:])

			if text[nxt:].startswith('\r\n'):
				# print('eeeeeeeeeeeeeeeeeee')
				if text[nxt:].startswith('\r\n:'):
					# print('--here---6')
					return handlerFloat(value, text[nxt:])
				if text[nxt:].startswith('\r\n-}'):
					# print('--here---7')
					return handlerFloat(value, text[nxt:])
				if text[nxt:].startswith('\r\n}'):
					# print('--here---8')
					return handlerFloat(value, text[nxt:])
				line = line + 1
				if line >= self.lines:
					# print('--here---9')
					return handlerFloat(value, text[nxt:])
				value = value + '\r\n'

			# print('c=',ord(c),'next=',ord(text[nxt]),ord(text[nxt-1]),nxt)
			stop = False
			x = ''
				
		if self.fixlength:
			# print('here 1')
			return None, saved_text
		value = value + x
		# print('--here---10')
		return handlerFloat(value,'')

	def pack(self,value):
		if value is None:
			return ''
		if self.dt == 'd':
			value = self.amount2string(value)
		return self.pack_string(value)
			
	def amount2string(self,value):
		f = str(value)
		if '.' in f:
			f = ','.join(f.split('.'))
		else:
			f = f + ','
		return f

	def pack_string(self,value):
		value = self.charset.express(self.dt,value)
		s = ''.join(value.split('\r'))
		f = '\r\n'.join(s.split('\n'))
		d,t = self.unpack(f)
		if t != '':
			return None
		return f


if __name__ == '__main__':
	#f = '{15d:[[/12d/5x]3!a//3!n]}'
	#x = formatsplit(f)
	#print(f,x)
	pass
