import sys
sys.dont_write_bytecode=True
from models import *
from do import *

def issamp(m=kursawe, max_tries=100):
    model = m()
    for _ in xrange(max_tries):
        ind = m.get_ind()
        
