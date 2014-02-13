import sys
sys.dont_write_bytecode=True
from models import *
from sa import *
from stats import *

def loop(era=100, epsilon=0.2, cohen=0.2):
	results = eras(epsilon, cohen)
	for i in xrange(50):
		c = sa(kursawe, era, epsilon, results.get_ind())
		results.add(c)
		if i!= 0:
			if results.good_enough() or results.little_imp():
				break
		print "era: %i" % i
		print xtile(c.best)
		print xtile(c.ave)

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

def _tile() :
	nums = [x*0.5 for x in range(0,100)]
	print xtile(nums,
							lo=0, hi=100,
							width=25,
							show= lambda s:" %3.2f" % s)


loop(50)
