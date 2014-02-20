import sys
sys.dont_write_bytecode=True
from sa import *

print "kursawe, runs=50, era=30, eps=0.01, cohen=0.2"
sa(m=kursawe, runs=50, era=30, eps=0.01, cohen=0.2)
print "kursawe, runs=50, era=30, eps=0.2, cohen=0.2"
sa(m=kursawe, runs=50, era=30, eps=0.2, cohen=0.2)
print "kursawe, runs=50, era=30, eps=0.01, cohen=0.01"
sa(m=kursawe, runs=50, era=30, eps=0.01, cohen=0.01)
print ""
print "fonseca, runs=50, era=30, eps=0.01, cohen=0.2"
sa(m=fonseca, runs=50, era=30, eps=0.01, cohen=0.2)
print "fonseca, runs=50, era=30, eps=0.2, cohen=0.2"
sa(m=fonseca, runs=50, era=30, eps=0.2, cohen=0.2)
print "fonseca, runs=50, era=30, eps=0.01, cohen=0.01"
sa(m=fonseca, runs=50, era=30, eps=0.01, cohen=0.01)
