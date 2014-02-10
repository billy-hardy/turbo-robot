import sys
sys.dont_write_bytecode=True
from models import *
from cache import *

def max_walk():
	sol = None
	for i in xrange(tries):
		sol = fiddle()
		for j in xrange(changes):
			if sol.score() > threshold:
				return sol
			c = part_of(sol)
			if p < rand():
				change(c)
			else:
				max_change(c)
	return fail, sol
