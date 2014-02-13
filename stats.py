import sys
sys.dont_write_bytecode=True
from model import *

class run:
	def __init__(self, length=128):
		self.ave = []
		self.ind_ave = []
		self.best = []
		self.ind_best = []
		self.length = length
	def add(self, ave, best):
		if len(self.best) == self.length:
			i = int(rand()*self.length)
			self.ave[i] = ave[-1]
			self.ind_ave = ave[:-1]
			self.best[i] = best[-1]
			self.ind_best = best[:-1]
		else:
			self.ave.append(ave[-1])
			self.ind_ave.append(ave[:-1])
			self.best.append(best[-1])
			self.ind_best.append(best[:-1])
	def get_ind(self):
		return max(self.ind_best)
	def __repr__(self):
		ret = ""
		for e in self.best:
			ret += "%0.3f "%e
		return ret
	def __len__(self):
		return len(self.best)
	def sum(self):
		s = 0.0
		for e in self.best:
			s += e
		return s
	def mean(self):
		ave = 0.0
		for e in self.best:
			ave += e
		return ave/len(self.best)
	def calc_var(self,mean):
		var = 0.0
		for e in self.best:
			var += (mean - e)**2
		return var

class eras:
	def __init__(self, eps, coh):
		self.log = []
		self.epsilon = eps
		self.cohen = coh
	def add(self, l):
		self.log.append(l)
	def get_ind(self):
		if len(self.log) == 0:
			return None
		else:
			return self.log[-1].get_ind()
	def good_enough(self):
		ret = self.mean() > (1-self.epsilon)
		return ret
	def __len__(self):
		l = 0.0
		for c in self.log:
			l += len(c)
		return l
	def mean(self):
		m = 0.0
		for c in self.log:
			m += c.sum()
		return m/self.__len__()
	def std_dev(self):
		mean = 0.0
		length = self.__len__()
		for c in self.log:
			mean += c.sum()
		mean = mean/length
		var = 0.0
		for c in self.log:
			var += c.calc_var(mean)
		var = mean/length
		return var**.5
	def little_imp(self):
		prev = self.log[-2]
		curr = self.log[-1]
		val =  abs(prev.mean()-curr.mean())
		return val < self.cohen*self.std_dev()
	def get_list(self):
		best, ave = [], []
		for c in self.log:
			best.extend(c.best)
			ave.extend(c.ave)
		return best.append(ave)
