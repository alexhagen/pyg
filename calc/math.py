import numpy as np

class rand_gen(object):
	def __init__(self):
		n = 0;
		rands = [];
	def rand(self):
		# sample a random value
		r = np.random.rand();
		# add these rands into our list of rands
		self.rands.append(r);
		# increment the number of rands used
		self.n = self.n + 1;
		return r;
	def check_randomness(self):
		# check the average and std of the rands used
		r_bar = np.average(self.rands);
		r_std = np.std(self.rands);
		return (r_bar,r_std);
