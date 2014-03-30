import sys
sys.dont_write_bytecode=True
from models import *
from do import *

def isamp(model=kursawe, max_tries=100):
	era = 100
	bin_num = 100
	base = 0.9
	jiggle = 0.2
	m = model()
	ans = None
	for _ in xrange(max_tries):
		constraints = [None]*len(m.decs)
		before = 0
		for _ in m.decs:
			sum = 0
			bias = {}
			for i in xrange(len(m.decs)):
				for j in xrange(bin_num):
					bias[i,j] = 0
			for k in xrange(era):
				ind = m.get_ind()
				for i,c in enumerate(constraints):
					if c:
						ind[i] = m.decs[i].get_val(c[0],c[1])
				s = m.score(m.get_dep(ind))
				sum += s
				for i,d in enumerate(ind):
					bin_size = (m.decs[i].high - m.decs[i].low)/bin_num
					r = int(bin_size*(d-m.decs[i].low))
					bias[i,r] += s*(base + jiggle*rand())
			b_1, b_2 = -1,-1
			for i in xrange(len(ind)):
				if not constraints[i]:
					for j in xrange(bin_num):
						if b_1 == -1 \
							     or bias[b_1,b_2] < bias[i,j]:
							b_1,b_2 = i,j
			n_dec = m.decs[b_1]
			n_const = [float(b_2)/bin_num, float(b_2+1)/bin_num]
			constraints[b_1] = n_const[:]
			now = sum/len(m.decs)
			ans = ind[:]
			if now < before:
				break
			else:
				before = now
		print m.score(m.get_dep(ans))
isamp()

'''
class range:
	def __init__(self, length, hi, lo):
		self.length = length
		self.hi = hi
		self.lo = lo
	

def bias(model=kursawe,
				 bins = 5,
				 era = 30):
	def get_bin(n, r):
		return int((n-r.lo)*1.0/r.length)
	def get_ranges(model):
		tmp = model()
		s = Nums()
		for _ in xrange(era):
			


def bias(model=kursawe,
				 seed = 1,
				 bins = 5,
				 era  = 30):
	def num2bin(n,about):
		return int((n - about.lo)*1.0/about.div)
	def range2num(r):
		return any(r[0], r[1])
	def theDivs(model):
		tmp = model()
		for _ in range(era): tmp.any()
		out = {}
		for h in tmp.t.nums:
			div    = (h.hi - h.lo)*1.0/bins
			breaks = {}
			for bin in range(bins):
				lo = h.lo + bin*div
				breaks[bin] = (lo, lo+div)
			out[h.pos] = Thing(div=div,lo=h.lo,
												 hi=h.hi,breaks=breaks)
		return out
  #--------------------
  #resetSeed(seed)
	divs = theDivs(model)
	m    = model()
	bias = {}
	for _ in range(era):
		m.any()
		old = m.t.rows[-1]
		s = old.score()
		for h in m.t.nums:
			pos = h.pos
			n   = old.cells[pos]
			bin = num2bin(n,divs[pos])
			key = (pos,bin)
			bias[key] = bias.get(key,0) + s
    ordered = []
    for k in bias:
      ordered += [(bias[k],k)]
    ordered = sorted(ordered,reverse=True)
    for score,(pos,bin) in ordered[:5]:
      print "best",score,':pos',pos,':bin',bin
    for score,(pos,bin) in ordered[-5:]:
      print "worst",score,':pos',pos,':bin',bin
    plot2d([x for x in range(len(ordered))],
           [x[0] for x in ordered],
           xlabel="bins",
           ylabel="scores",
           title=m.name(),
           file="~/ai/%s.png" % m.name())

def plot2d(x,y,xlabel="x",ylabel="y",
					 title="Plot",file=None,
					 width=3,
					 height=3):
    "Print a 2d plot. If 'file' not given, show on screen"
    print title,file
    import matplotlib.pyplot as plt
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gcf().set_size_inches(width,height)
    plt.plot(x, y, 'ro')
    plt.subplots_adjust(bottom=0.2,left=0.2)
    plt.savefig(file) if file else plt.show()
'''
