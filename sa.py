import sys
sys.dont_write_bytecode=True
from models import *
from do import *

def sa(m=kursawe, runs=50,
			 era=30, kmax=1000,
			 eps=0.1, p=0.33, cohen=0.2):
	def fiddle(model, ind):
		ret = []
		for i,d in enumerate(model.decs):
			if rand() < p:
				ret.append(d.get_val())
			else:
				ret.append(ind[i])
		return ret
	def maybe(old,new,t):
		x = math.e**((old - new)*1.0/t)
		y = rand()
		return x < y
	outer = do(range(runs))
	for run, outer in outer.loop():
		model = m()
		ind = ind_b = model.get_ind()
		dep = model.get_dep(ind)
		e = e_b = model.score(dep)
		inner = do(range(kmax),
							 eps=eps, halt_on="best",
							 era=era, also=outer, cohen=cohen)
		k = 0.0
		for _, inner in inner.loop():
			k+=1
			ind_n = fiddle(model,ind[:])
			dep_n = model.get_dep(ind_n[:])
			e_n = model.score(dep_n)
			if e_n > e_b:
				ind_b = ind_n[:]
				e_b = e_n
			if e_n > e:
				ind = ind_n[:]
				e = e_n
			elif maybe(e, e_n, k/kmax):
				ind = ind_n[:]
				e = e_n
			inner.seen(k, best=e_b, every=e)
	done(outer, 0, 1,
			 key=lambda x: '%2d'%x,
			 value = lambda x: '%4.2f'%x)
			
