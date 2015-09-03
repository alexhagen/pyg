import math
import numpy as np
from ..plotting import twod as ahp
from scipy import nanmean
from scipy.optimize import curve_fit
from scipy.odr import *

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

class curve(object):
	def __init__(self,x,y,name='',u_x=None,u_y=None,data='smooth'):
		self.name = name;
		self.data = data;
		# assert that x and y are 1d lists of same size
		if isinstance(x,list):
			self.x = np.array(x);
		else:
			self.x = x;
		if isinstance(y,list):
			self.y = np.array(y);
		else:
			self.y = y;
		if isinstance(u_x,list):
			self.u_x = np.array(u_x);
		else:
			self.u_x = u_x;
		if isinstance(u_y,list):
			self.u_y = np.array(u_y);
		else:
			self.u_y = u_y;
		self.sort();
	def sort(self):
		""" ``ah_py.curve.sort()`` sorts the list depending on the **x** coordinate."""
		idx = self.x.argsort();
		self.x = self.x[idx];
		self.y = self.y[idx];
		if self.u_x is not None:
			self.u_x = self.u_x[idx];
		if self.u_y is not None:
			self.u_y = self.u_y[idx];
	def add_data(self,x,y):
		""" ``ah_py.curve.add_data(x,y)`` adds data to the already populated x and y."""
		self.x = np.append(self.x,x);
		self.y = np.append(self.y,y);
		self.sort();
	def inrange(self,x):
		""" ``ah_py.curve.inrange(x)`` checks if input ``x`` is in the range of the
	covered by the ``ah_py.curve`` instance's array ``x``."""
		if x >= self.x.min() and x <= self.x.max():
			return True;
		else:
			return False;
	def at(self,x):
		""" ``ah_py.curve.at(x)`` interpolates or extrapolates the curve to give a y
	value for the curve at input ``x``."""
		y = np.ones_like(x);
		for index, xi in np.ndenumerate(x):
			if xi >= self.x.min() and xi <= self.x.max():
				# if it is in the data range, interpolate
				y[index] = self.interpolate(xi);
			else:
				# if it is not in the data range, extrapolate
				y[index] = self.extrapolate(xi);
		return y;
	def normalize(self,xmin=None,xmax=None,norm='max'):
		if norm is 'max':
			self.y = self.y / self.y.max();
		elif norm is 'int':
			if xmin is None:
				xmin = self.x.min();
			if xmax is None:
				xmax = self.x.max();
			self.y = self.y / \
				self.integrate(xmin,xmax);
	def average(self,xmin=None,xmax=None):
		if xmin is None:
			xmin = self.x.min();
		if xmax is None:
			xmax = self.x.max();
		mean = self.integrate(xmin,xmax) \
			/ (xmax - xmin);
		return mean;
	def interpolate(self,x):
		# if not, we have to do linear interpolation
		# find closest value below
		x_down,y_down = self.find_nearest_down(x);
		# find the closest value above
		x_up,y_up = self.find_nearest_up(x);
		# find the percentage of x distance between
		x_dist = (x-x_down);
		# find the slope
		m = (y_up-y_down)/(x_up-x_down);
		# find the y value
		y = y_down + x_dist * m;
		return y;
	def extrapolate(self,x):
		#print "You need to write the extrapolate method!";
		if x < self.x.min():
			x1 = self.x[0];
			x2 = self.x[1];
		elif x > self.x.max():
			x1 = self.x[-1];
			x2 = self.x[-2];
		# now find the slope
		m = (self.at(x1) - self.at(x2))/(x1 - x2);
		# find the y change between closest point and new point
		dy = m * (x - x1);
		# find the new point
		return self.at(x1) + dy;
	def find_nearest_down(self,x):
		idx = (np.abs(x-self.x)).argmin()
		return (self.x[idx-1], self.y[idx-1])
	def find_nearest_up(self,x):
		idx = (np.abs(x-self.x)).argmin()
		return (self.x[idx], self.y[idx])
	def integrate(self,x_min,x_max,quad='lin'):
		# for now, we'll just do simpsons rule until I write
		# more sophisticated
		return self.trapezoidal(x_min,x_max,quad);
	def trapezoidal(self,x_min,x_max,quad='lin'):
		# first we assert that all values are in the region
		# then, we find a bunch of x's between these values
		numpoints = 61;
		if quad is 'lin':
			x_sub = np.linspace(x_min,x_max,numpoints);
		elif quad is 'log':
			x_sub = np.logspace(np.log10(x_min),np.log10(x_max),num=numpoints);
		# then, between each x, we find the value there
		y_sub = [ self.at(x_i) for x_i in x_sub ];
		# then, we do the trapezoidal rule
		return np.sum([ ((x_sub[i+1]-x_sub[i])*y_sub[i]) + \
			((x_sub[i+1]-x_sub[i])*(y_sub[i+1]-y_sub[i]))/2 \
			for i in np.arange(0,len(x_sub)-1) ]);
	def plot(self,x=None,y=None,addto=None,linestyle=None,linecolor='black',
		yy=False,xerr=None,yerr=None):
		if addto is None:
			plot = ahp.ah2d();
		else:
			plot = addto;
		if x is None and y is None:
			x = self.x;
			y = self.y;
		if self.data is 'binned':
			# plot the bins
			# setup a matix
			# preallocate this later ***********************************
			plot_x = np.array([]);
			plot_y = np.array([]);
			# plot the thick bars
			for i in np.arange(0,len(x)-1):
				plot_x = np.append(plot_x,x[i]);
				plot_y = np.append(plot_y,y[i]);
				plot_x = np.append(plot_x,x[i+1]);
				plot_y = np.append(plot_y,y[i]);
				plot_x = np.append(plot_x,np.nan);
				plot_y = np.append(plot_y,np.nan);
			plot.add_line(plot_x,plot_y,name=self.name,linewidth=4.0,linecolor=linecolor,
				linestyle='-');
			conn_x = np.array([]);
			conn_y = np.array([]);
			for i in np.arange(1,len(x)):
				conn_x = np.append(conn_x,x[i]);
				conn_y = np.append(conn_y,y[i-1]);
				conn_x = np.append(conn_x,x[i]);
				conn_y = np.append(conn_y,y[i]);
				conn_x = np.append(conn_x,np.nan);
				conn_y = np.append(conn_y,np.nan);
			plot.add_line(conn_x,conn_y,name=self.name+'connectors',linewidth=0.1,linestyle='-',linecolor=linecolor);
			plot.markers_off();
			plot.lines_on();
		elif self.data is 'smooth':
			if yy is False:
				plot.add_line(x,y,xerr=self.u_x,yerr=self.u_y,name=self.name,linestyle=linestyle,linecolor=linecolor);
			else:
				plot.add_line_yy(x,y,xerr=self.u_x,yerr=self.u_y,name=self.name,linestyle=linestyle,linecolor=linecolor);
		return plot;
	def decimate(self,R):
		pad_size = pymath.ceil(float(self.x.size)/R)*R - self.x.size;
		arr_x_padded = np.append(self.x, np.zeros(pad_size)*np.NaN);
		self.x = nanmean(arr_x_padded.reshape(-1,R), axis=1);
		arr_y_padded = np.append(self.y, np.zeros(pad_size)*np.NaN);
		self.y = nanmean(arr_y_padded.reshape(-1,R), axis=1);
	def fit_exp(self):
		def exp_func(coeffs=None,x=None):
			return np.exp(np.polyval(coeffs,x));
		coeffs = np.polyfit(self.x,np.log(self.y),1);
		self.fun = exp_func;
		self.coeffs = coeffs;
		self.fit_exp_bool = True;
	def fit_gen(self,fun,guess=None,u_y=None):
		self.fun = fun;
		fit = curve_fit(fun, self.x, self.y, p0 = guess,sigma=u_y,absolute_sigma=True);
		self.coeffs = fit[0];
		self.fit_exp_bool = False;
	def fit_at(self,x):
		if self.fit_exp_bool:
			return self.fun(self.coeffs,x);
		else:
			return self.fun(x,*self.coeffs);
	def fit_square(self):
		def square_func(coeffs,x):
			return np.polyval(coeffs,x);
		coeffs = np.polyfit(self.x,self.y,2);
		self.fun = square_func;
		self.coeffs = coeffs;
	def plot_fit(self,xmin=None,xmax=None,addto=None,linestyle=None):
		if addto is None:
			plot = ahp.ah2d();
		else:
			plot = addto;
		if xmin is None:
			xmin = self.x.min();
		if xmax is None:
			xmax = self.x.max();
		x = np.linspace(xmin,xmax,num=1000);
		y = self.fit_at(x);
		plot.add_line(x,y,name=self.name+'fit',linestyle=linestyle);
		return plot;
