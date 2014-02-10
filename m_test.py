import sys
sys.dont_write_bytecode=True
from models import *

m = golinski()
ind = m.get_ind()
print m.get_dep(ind)
