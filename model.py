import sys
sys.dont_write_bytecode=True
import math
import random

rand = random.random
urand = random.uniform
e = math.e
sin = math.sin
inf = 10.0**32
ninf = -1*inf
eps = 10.0**-32

class Num:
	def __init__(self, name, low, high):
		self.name = name
		self.low = low
		self.high = high
	def norm(self, val):
		return (val - self.low)*1.0/(self.high - self.low + eps)

class Dec(Num):
	def __init__(self, name, low=-5, high=5):
		Num.__init__(self, name, low, high)
	def get_val(self):
		self.val = urand(self.low, self.high)
		return self.val

class Obj(Num):
	def __init__(self, name, func, opt, low=0, high=1):
		Num.__init__(self, name, low, high)
		self.func = func
		self.opt = opt
	def calc(self, args):
		y = self.func(args)
		if y > self.high:
			self.high = y
		elif y < self.low:
			self.low = y
		return y
	def norm(self, val):
		return self.opt(Num.norm(self,val))

class Model:
	def __init__(self):
		self.decs = []
		self.objs = []
		self.const = []
	def add_vars(self): pass
	def get_ind(self):
		for _ in xrange(100):
			ret = []
			for d in self.decs:
				ret.append(d.get_val())
			if self.valid(ret):
				return ret
		return None
	def get_dep(self, ind):
		ret = []
		for o in self.objs:
			ret.append(o.calc(ind))
		return ret
	def baseline(self):
		for _ in xrange(100):
			ind = self.get_ind()
			self.get_dep(ind)
	def valid(self, args):
		for f in self.const:
			if not f(args):
				return False
		return True
	def score(self, s):
		ret = 0.0
		for i,o in enumerate(self.objs):
			ret += o.norm(s[i])
		return ret/(len(s)+eps)
	def stats(self, l):
		m = [0]*len(self.objs)
		for x in l[::len(self.objs)]:
			for i in xrange(len(self.objs)):
				m[i] += x[i]
		ret = ""
		for i,o in enumerate(self.objs):
			ret += "mean %s: %0.2f\n" % (o.name, m[i]/len(l[::len(self.objs)]))
		return ret

def to_str(ind, dep, e):
	args = []
	for i in xrange(len(ind)):
		args += ['%0.2f'% (ind[i])]
	for i in xrange(len(dep)):
		args += ['%0.2f'% (dep[i])]
	out = '(%s)' % (', '.join(args))
	return out + ' e = %0.2f' % (e)
