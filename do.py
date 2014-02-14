import sys
sys.dont_write_bytecode=True
from model import *

class stats:
	def __init__(self, size=128):
		self.vals = []
		self.size = size
		self.n = self.m2 = self.mu = self.s = 0.0
	def __len__(self):
		return len(self.vals)
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
							 also=None,
							 halt_on=None,
							 era=100,
							 cohen=0.01):
		self.iterator = iterator
		self.epsilon = eps
		self.outer = also
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
	def small(self, where):
		return self.all[where].s*self.cohen
	def close_enough(self, where, era):
		return self.now[(where, era)].mu > (1-self.epsilon)
	def improving(self, where, era):
		last = era - self.era
		curr = self.now[(where, era)]
		prev = self.now[(where, last)]
		return curr.mu - prev.mu > self.small(where)
	def seen(self, i, **val):
		era = self.get_era(i)
		for where,val in val.items():
			self.add(era, val, where)
	def add(self, era, val, where):
		if self.outer:
			self.outer.add(era, val, where)
		self.all[where].add(val)
		self.now[(where, era)].add(val)
	def loop(self):
		before = 0
		for i in self.iterator:
			now = self.get_era(i)
			if before and now != before:
				if self.early_stop(before):
					break
			before = now
			yield i, self

def gen(iterator, epsilon, where, era, also):
	for i, g in do(xrange(kmax),
							 eps, "best",
							 era, also=outer).loop():
		yield i, g

def done(doings, lo, hi,
				 key  =lambda z:'%10s' %  z,
				 value=lambda z: '%2d' %  z):
	d = doings.now
	wheres= {}
	whens = {}
	for where,when in d.keys():
		wheres[where] = 1
		whens[ when ] = 1
	wheres = sorted(wheres.keys())
	whens  = sorted(whens.keys())
	for where in wheres:
		print '\n------|',str(where),'|'+'-'*75,'\n'
		for when in whens:
			if (where,when) in d:
				all = d[(where,when)].vals
				if len(all) > 5:
					s=   xtile(all,show = value,
										 lo=lo,hi=hi,width=25)
					print '%10s' % key(when),\
							'[%5s]' % len(all), s

def xtile(lst,lo=0,hi=100,width=25,
					chops=[0.1 ,0.3,0.5,0.7,0.9],
					marks=["-" ," "," ","-"," "],
					bar="|",star="*",show= lambda s:" %0.2f" % s):
	def pairs(lst):
		last=lst[0]
		for i in lst[1:]:
			yield last,i
			last = i
	def pos(p)   : return ordered[int(len(lst)*p)]
	def place(x) :
		tmp= int(width*float((x - lo))/(hi - lo))
		if tmp == width: tmp += -1
		return tmp
	def pretty(lst) :
		return ', '.join([show(x) for x in lst])
	ordered = sorted(lst)
	lo      = min(lo,ordered[0])
	hi      = max(hi,ordered[-1])
	what    = [pos(p)   for p in chops]
	where   = [place(n) for n in  what]
	out     = [" "] * width
	for one,two in pairs(where):
		for i in range(one,two):
			out[i] = marks[0]
		marks = marks[1:]
	out[int(width/2)]    = bar
	loc = place(pos(0.5))
	#print loc, len(out)
	out[loc] = star
	return ''.join(out) +  "," +  pretty(what)
