import sys
sys.dont_write_bytecode=True
from models import *

class sample:
	id = 0
	def __init__(self, model):
		self.id = sample.id = sample.id+1
		self.model = model
		self.vals = self.model.get_ind()
		dep = self.model.get_dep(self.vals)
		self.score = self.model.score(dep)
	def __getitem__(self, i):
		return self.vals[i]
	def __setitem__(self, i, val):
		self.vals[i] = self.model.tighten(i, val)
		dep = self.model.get_dep(self.vals)
		self.score = self.model.score(dep)
	def __len__(self):
		return len(self.vals)
	def __repr__(self):
		return repr(self.vals)

def r(max):
	return int(random.uniform(0,max))

def de(m=kursawe, max_rep=100,
			 pop=100, f=0.75, cf=0.3,
			 eps=0.01, era=30, cohen=0.2):
	def update(f,cf,frontier,total=0.0,n=0):
		for x in frontier:
			new = extrapolate(frontier, x, f, cf)
			if new.score > x.score:
				x.vals = new.vals[:]
				x.score = new.score
				total += x.score
				n += 1
		return total, n
	def extrapolate(frontier, one, f, cf):
		out = sample(one.model)
		out.id = one.id
		two,three,four = some(frontier, one)
		changed = False
		for i in xrange(len(model.decs)):
			x,y,z = two.vals[i], three.vals[i], four.vals[i]
			if rand() < cf:
				new = x + f*(y-z)
				out[i] = new
				changed = True
		if not changed:
			i = r(len(out))
			out[i] = two[i]
		return out
	def some(lst, avoid):
		def other():
			x = one(lst)
			while x.id in seen:
				x = one(lst)
			seen.append(x.id)
			return x
		def one(lst):
			return lst[r(len(lst))]
		seen = [avoid.id]
		return other(), other(), other()	 
	outer = do(xrange(runs))
	for i,outer in outer.loop():
		model = m()
		pareto = [sample(model) for _ in xrange(pop)]
		inner = do(xrange(max_rep),
							 eps=eps,halt_on="best",
							 era=era,also=outer,cohen=cohen)
		for k in xrange(max_rep):
			total, n = update(f, cf, pareto)
			if total/(n+(1/inf)) > (1-eps):
				break
		return pareto
