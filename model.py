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
tiny = 10.0**-32


class Dec:
	def __init__(self, low=-5, high=5):
		self.low = low
		self.high = high
	def get_val(self, lo=0, hi=1):
		off_low = (self.high-self.low)*lo
		off_high = (self.high-self.low)*hi
		val = self.low+urand(off_low, off_high)
		return val
	def tighten(self, val):
		return max(self.low, min(val, self.high))

class Obj:
	def __init__(self, func, opt):
		self.func = func
		self.opt = opt
		self.high = self.low = None
	def calc(self, args):
		y = self.func(args)
		self.high = y if self.high is None else self.high
		self.low = y if self.low is None else self.low
		if y > self.high:
			self.high = y
		elif y < self.low:
			self.low = y
		return y
	def norm(self, val):
		return self.opt((val - self.low)*1.0/(self.high - self.low + tiny))

class Model:
	def __init__(self):
		self.decs = []
		self.objs = []
		self.const = []
	def add_vars(self): pass
	def get_ind(self):
		while True:
			ret = []
			for d in self.decs:
				ret.append(d.get_val())
			if self.valid(ret):
				return ret
		return None
	def fiddle(self, ind, k, lo=0, hi=1):
		for _ in xrange(1000):
			ret = ind[:]
			ret[k] = self.decs[k].get_val(lo, hi)
			if self.valid(ret):
				return ret
		return ind
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
		return ret/(len(s)+tiny)
	def stats(self, l):
		m = [0]*len(self.objs)
		for x in l[::len(self.objs)]:
			for i in xrange(len(self.objs)):
				m[i] += x[i]
		ret = ""
		for i,o in enumerate(self.objs):
			ret += "mean %s: %0.2f\n" % (o.name, m[i]/len(l[::len(self.objs)]))
		return ret
	def tighten(self, i, val):
		return self.decs[i].tighten(val)

def to_str(ind, dep, e):
	args = []
	for i in xrange(len(ind)):
		args += ['%0.2f'% (ind[i])]
	for i in xrange(len(dep)):
		args += ['%0.2f'% (dep[i])]
	out = '(%s)' % (', '.join(args))
	return out + ' e = %0.2f' % (e)
