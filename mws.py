import sys
sys.dont_write_bytecode=True
from models import *
from do import *

def max_walk(m=kursawe, tries=50,
						 threshold=0.99999, p=0.5,
						 era=30, eps=0.01, cohen=0.2):
	def calc(model, do, i, ind_old, k, lo=0, hi=1):
		ind = model.fiddle(ind_old, k, lo, hi)
		dep = model.get_dep(ind)
		e = model.score(dep)
		return ind, e
	outer = do(range(tries))
	for run, outer in outer.loop():
		model = m()
		model.baseline()
		ind_b = ind = model.get_ind()
		dep_b = dep = model.get_dep(ind)
		e_b = e = model.score(dep)
		inner = do(range(100), eps=eps,
							 halt_on="best", era=era,
							 also=outer, cohen=cohen)
		for i, inner in inner.loop():
#			if e_b > threshold:
#				return ind
			k = int(rand()*len(model.decs))
			if p < rand():
				ind_n, e_n = calc(model, inner, i, ind, k)
				if e_n > e_b:
					ind_b, e_b = ind_n[:], e_n
				if e_n > e:
					ind, e = ind_n[:], e_n
				inner.seen(i, best=e_b, every=e_n)
			else:
				for l in xrange(10):
					ind_n, e_n = calc(model, inner, i, ind, k, l/10.0, (l+1)/10.0)
					if e_n > e_b:
						ind_b, e_b = ind_n[:], e_n
					if e_n > e:
						ind, e = ind_n[:], e_n
					inner.seen(i, best=e_b, every=e_n)
	done(outer, 0, 1,
			 key=lambda x: '%2d'%x,
			 value = lambda x: '%4.2f'%x)

def say(*lst):
	sys.stdout.write(','.join(map(str,lst)))
	sys.stdout.flush()

#max_walk(kursawe)
max_walk(fonseca)
#max_walk(schaffer)
