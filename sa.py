import sys
sys.dont_write_bytecode=True
from models import *
from do import *

def sa(m=kursawe, runs=50,
			 era=30, kmax=1000,
			 eps=0.01, p=0.33, cohen=0.2):
	def fiddle(model, ind):
		ret = []
		for i,d in enumerate(model.decs):
			if rand() < p:
				ret.append(d.get_val())
			else:
				ret.append(ind[i])
		return ret
	def maybe(old,new,t):
		x = math.e**((old - new)*1.0/max(t, 1))
		y = rand()
		return x < y
	outer = do(range(runs))
	ind_b = e_b = 0
	for run, outer in outer.loop():
		model = m()
		ind = ind_b = model.get_ind()
		dep = model.get_dep(ind)
		e = e_b = model.score(dep)
		inner = do(range(kmax),
							 eps=eps, halt_on="best",
							 era=era, also=outer, cohen=cohen)
		for k, inner in inner.loop():
			ind_n = fiddle(model,ind[:])
			dep_n = model.get_dep(ind_n[:])
			e_n = model.score(dep_n)
			if e_n > e_b:
				ind_b = ind_n[:]
				e_b = e_n
			if e_n > e:
				ind = ind_n[:]
				e = e_n
			elif maybe(e, e_n, float(k)/kmax):
				ind = ind_n[:]
				e = e_n
			inner.seen(k, best=e_b, every=e_n)
	done(outer, 0, 1,
			 key=lambda x: '%2d'%x,
			 value = lambda x: '%4.2f'%x)
	return ind_b, e_b
