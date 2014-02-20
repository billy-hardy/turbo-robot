import sys
sys.dont_write_bytecode=True
from models import *
from sa import *
from mws import *

print "schaffer"
print "simulated annealling"
sa(schaffer)
print "\nmax-walk-sat"
max_walk(schaffer)

print "\n\nkursawe"
print "simulated annealling"
sa(kursawe)
print "\nmax-walk-sat"
max_walk(kursawe)

print "\n\nzdt1"
print "simulated annealling"
sa(zdt1)
print "\nmax-walk-sat"
max_walk(zdt1)
