import sys
sys.dont_write_bytecode=True
from model import *

minimize = lambda x: (1-x)
maximize = lambda x: x

class schaffer(Model):
	def __init__(self):
		Model.__init__(self)
		schaffer.add_vars(self)
	def add_vars(self):
		f1 = lambda args: args[0]**2
		f2 = lambda args: (args[0]-2)**2
		self.decs = [Dec("x1",-(10**5),10**5)]
		self.objs = [Obj("f1", f1, maximize, 0.0, 10.0),
								 Obj("f2", f2, maximize, 0.0, 10.0)]

class kursawe(Model):
	def __init__(self):
		Model.__init__(self)
		kursawe.add_vars(self)
	def add_vars(self):
		def f1(args):
			ret = 0.0
			for n,one in enumerate(args[:-1]):
				two = args[n+1]
				ret += 10.0*e**(-0.2*(one**2 + two**2)**0.5)
				return ret
		def f2(args):
			ret = 0.0
			for one in args:
				ret += abs(one)**0.8 + 5*sin(one**3)
			return ret
		self.decs = [Dec("x1",-5,5), 
								 Dec("x2",-5,5), 
								 Dec("x3",-5,5)]
		self.objs = [Obj("f1", f1, maximize, 0.0, 10.0),
								 Obj("f2", f2, maximize, 0.0, 10.0)]

class fonseca(Model):
	def __init__(self):
		Model.__init__(self)
		fonseca.add_vars(self)
	def add_vars(self):
		def f1(args):
			temp = 0.0
			for i,x in enumerate(args):
				temp += (x - ((i+1)**-.5))**2
			ret = e**(-temp)
			return 1 - ret
		def f2(args):
			temp = 0.0
			for i,x in enumerate(args):
				temp += (x + 1/((i+1)**.5))**2
			ret = e**(-temp)
			return 1 - ret
		self.decs = [Dec("x1",-4,4),
								 Dec("x2",-4,4),
								 Dec("x3",-4,4)]
		self.objs = [Obj("f1",f1, minimize, 0.0, 1.0),
								 Obj("f2",f2, maximize, 0.0, 1.0)]

class zdt1(Model):
	def __init__(self):
		Model.__init__(self)
		zdt1.add_vars(self)
	def add_vars(self):
		def f1(args):
			return args[0]
		def f2(args):
			return g(args)*(1-(args[0]/g(args))**.5)
		def g(args):
			ret = 0
			for x in args:
				ret += x
			ret = 9*(ret)/(len(args)-1)
			return ret + 1
		for i in xrange(30):
			self.decs.append(Dec("x%i"%(i+1),0,1))
		self.objs = [Obj("f1",f1,minimize,0,1),
								 Obj("f2",f2,minimize,-10,10)]

class zdt2(Model):
	def __init__(self):
		Model.__init__(self)
		zdt2.add_vars(self)
	def add_vars(self):
		def f1(args):
			return args[0]
		def f2(args):
			return g(args)*(1-(args[0]/g(args))**2)
		def g(args):
			ret = 0
			for x in args:
				ret += x
			ret = 9*(ret)/(len(args)-1)
			return ret + 1
		self.decs = []
		for i in xrange(30):
			self.decs.append(Dec("x%i"%(i+1),0,1))
		self.objs = [Obj("f1",f1,minimize,0,1),
								 Obj("f2",f2,minimize,-10,10)]

class golinski(Model):
	def __init__(self):
		Model.__init__(self)
		golinski.add_vars(self)
	def add_vars(self):
		def f1(args):
			ret = 1.0
			ret *= 0.7854*args[0]*(args[1])**2
			ret *= 10*(args[2]**2)/3 + 14.933*args[2] - 43.0934
			ret += -1.508*args[0]*(args[5]**2 + args[6]**2)
			ret += 7.477*(args[5]**3 + args[6]**3)
			ret += 0.7854*(args[3]*(args[5]**2) + args[4]*(args[6]**2))
			return ret
		def f2(args):
			ret = 745.0*args[3]/(args[1]*args[2])
			ret += 1.69*(10**7)
			ret = ret**.5
			ret /= 0.1*(args[5]**3)
			return ret
		self.decs = [Dec("x1", 2.6, 3.6),
								 Dec("x2", 0.7, 0.8),
								 Dec("x3", 17.0, 28.0),
								 Dec("x4", 7.3, 8.3),
								 Dec("x5", 7.3, 8.3),
								 Dec("x6", 2.9, 3.9),
								 Dec("x7", 5.0, 5.5)]
		self.objs = [Obj("f1", f1, minimize, 0.0, 10.0),
								 Obj("f2", f2, minimize, 0.0, 10.0)]
		self.const = [lambda args: 0 <= args[0] + args[1] - 2,
									lambda args: 0 <= 6 - args[0] - args[1],
									lambda args: 0 <= 2 - args[1] + args[0],
									lambda args: 0 <= 2 - args[0] + 3*args[1],
									lambda args: 0 <= 4 - (args[2]-3)**2 - args[3],
									lambda args: 0 <= (args[4]-3)**3 + args[5] - 4]


