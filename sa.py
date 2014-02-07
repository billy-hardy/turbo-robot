import sys
sys.dont_write_bytecode=True
from models import *
from cache import *


def sa(m=kursawe, era=200, eps=0.2, p=0.33, initial=None):
	def fiddle(model, ind):
		ret = []
		for i,d in enumerate(model.decs):
			if rand() < p:
				ret.append(d.get_val())
			else:
				ret.append(ind[i])
		return ret
	def maybe(old,new,t):
		x = e**((old - new)*1.0/t)
		y = rand()
		return x < y
	model = m()
	c = Cache()
	ind = ind_b = model.get_ind()
	dep = dep_b = model.get_dep(ind)
	e = e_b = model.score(dep)
	c.add(ind+[e], ind_b+[e_b])
	stagger = 1.0
	k = 0.0
	for _ in xrange(era):
		k += 1
		ind_n = fiddle(model,ind[:])
		dep_n = model.get_dep(ind_n[:])
		e_n = model.score(dep_n)
		if e_n > e_b:
			ind_b, dep_b = ind_n[:], dep_n[:]
			e_b = e_n
			c.add(ind+[e], ind_b+[e_b])
		if e_n > e:
			ind, dep = ind_n[:], dep_n[:]
			e = e_n
			c.add(ind+[e], ind_b+[e_b])
		elif maybe(e, e_n, (k/era)**stagger):
			ind, dep = ind_n[:], dep_n[:]
			e = e_n
			c.add(ind+[e], ind_b+[e_b])
	return c
