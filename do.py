import sys
sys.dont_write_bytecode=True
from model import *

class stats:
	def __init__(self, size=128):
		self.vals = []
		self.size = size
		self.n = self.m2 = self.mu = self.s = 0.0
	def add(self, val):
		if len(self.vals) == self.size:
			if rand() <= self.size/self.n:
				i = int(rand()*self.size)
				self.vals[i] = val
		else:
			self.vals.append(val)
		self.n += 1
		delta = val - self.mu
		self.mu += delta*1.0/self.n
		self.m2 += delta*(val - self.mu)
		if self.n > 1:
			self.s = (self.m2/(self.n-1))**0.5

'''
Automatically adds keys to dictionary 
Keys: "best" or ("every",era)
values: list of energy
'''
class Nums(dict):
	def __init__(self):
		self.default = stats
	def __getitem__(self, key):
		if key in self:
			return self.get(key)
		return self.setdefault(key, self.default())

class do:
	def __init__(self, 
							 iterator=xrange(100),
							 eps=0.005,
							 outer=None,
							 halt_on=None,
							 era=100,
							 cohen=0.2):
		self.iterator = iterator
		self.epsilon = eps
		self.outer = outer
		self.halt_on = halt_on
		self.era = era
		self.cohen = cohen
		self.all = Nums() #uses "best" and "every" as keys
		self.now = Nums() #uses ("best",era) as keys
	def get_era(self, i):
		return int(i/self.era)*self.era
	def early_stop(self, era):
		where = self.halt_on
		if where:
			if self.close_enough(where, era) \
						or not self.improving(where, era):
				return True
		return False
	def close_enough(self, where, era):
		return self.now[(where, era)] > (1-self.epsilon)
	def improving(self, where, era):
		before = era - self.era
	def seen(self, i, **val):
		era = get_era(i)
		for where,val in val.items():
			self.add(era, val, where)
	def add(self, era, val, where):
		if self.outer:
			self.outer.add(era, val, where)
		self.all[where]
	def loop(self):
		before = 0
		for i in self.iterator:
			now = self.get_era(i)
			if before and now != before:
				if self.early_stop(before):
					break
			before = now
			yield i, self


