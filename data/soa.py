import numpy as np;
import datetime as dt;
import math;
import os;
import struct;
from matplotlib.pyplot import close
from datetime import datetime, timedelta
from ..plotting import twod as ahp
from ..calc import func as ahf

class ucs20(object):
	''' UCS20 is an object for interacting with the UCS20 output files saved in 
	comma separated value formats '''
	def __init__(self,filename = None ):
		if filename is not None:
			self.import_csv(filename);
	def import_csv(self,filename = None ):
		f = open(filename,'r');
		lineno=0;
		for line in f:
			# increment the line number
			lineno=lineno+1;
			# import lines to data structures until we get to "Channel Data"
			if "Channel Data:" in line:
				break;
		f.close();
		arr=np.genfromtxt(filename,skip_header=lineno+1,delimiter=",",
			usecols=[0,2]);
		self.channel = arr[:,0].copy();
		self.counts = arr[:,1].copy()
	def plot_spectrum(self,addto=None,xerr=None,yerr=None):
		self.line = ahf.curve(self.channel,self.counts,data='binned');
		self.plt = self.line.plot(addto=addto,xerr=xerr,yerr=yerr);
		return self.plt;


def calc_eff_ratio(eta_cf=None,sigma_eta_cf=None,eta_dd=None,sigma_eta_dd=None):
	r = eta_cf / eta_dd;
	sigma_r = math.sqrt( \
		(1.0/eta_dd)**2.0 * sigma_eta_dd**2.0 + \
		(-eta_cf/eta_dd**2.0)**2.0 * \
		sigma_eta_dd**2.0);
	return (r,sigma_r);

def calc_ls_eff(c_raw_src=None,c_raw_bkg=None,d_src=None,u_d_src=None,
	I_src=None,u_I_src=None,r_det=None,u_r_det=None,l_det=None,
	u_l_det=None,t_src=None,u_t_src=None,t_bkg=None,u_t_bkg=None):
	# first find all of the relative errors from the absolute error
	sigma_d_src = u_d_src / d_src;
	sigma_I_src = u_I_src / I_src;
	sigma_r_det = u_r_det / r_det;
	sigma_l_det = u_l_det / l_det;
	sigma_t_src = u_t_src / t_src;
	sigma_t_bkg = u_t_bkg / t_bkg;
	# calculate error in counts using poisson
	sigma_c_raw_src = math.sqrt(c_raw_src)/c_raw_src;
	# calculate error in background using poisson
	sigma_c_raw_bkg = math.sqrt(c_raw_bkg)/c_raw_bkg;
	# adjust background counts to match actual counts
	c_bkg = t_src * c_raw_bkg / t_bkg;
	# calculate the error in the background counts
	sigma_c_bkg = (c_raw_bkg/t_bkg)**2.0 * sigma_t_src**2.0 + \
	(-t_src*c_raw_bkg/t_bkg)**2.0 * sigma_t_bkg**2.0 + \
	(t_src/t_bkg)**2.0 * sigma_c_raw_bkg**2.0;
	# calculate efficiency using efficiency equation
	eta_src = 2*math.pi*(c_raw_src-c_bkg)*d_src*d_src/(I_src*r_det*l_det*t_src);
	# calculate propagated error using error propagation formula
	# squared term to the raw count error
	A = 2.0 * math.pi * d_src**2.0 / (I_src * r_det * l_det * t_src);
	# squared term to the background count error
	B = -2.0 * math.pi * d_src**2.0 / (I_src * r_det * l_det * t_src);
	# squared term to the distance to source error
	C = 4.0 * math.pi * (c_raw_src - c_bkg) * d_src / \
	(I_src * r_det * l_det * t_src);
	# squared term to the source intensity error
	D = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src**2.0 * r_det * l_det * t_src);
	# squared term to the detector radius error
	E = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det**2.0 * l_det * t_src);
	# squared term to the detector length error
	F = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det * l_det**2.0 * t_src);
	# squared term for the time error
	G = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det * l_det * t_src**2.0);
	sigma_eta_src = math.sqrt( A**2.0 * sigma_c_raw_src**2.0 + \
		B**2.0 * sigma_c_bkg**2.0 + C**2.0 * sigma_d_src**2.0 + \
		D**2.0 * sigma_I_src**2.0 + E**2.0 * sigma_r_det**2.0 + \
		F**2.0 * sigma_l_det**2.0 + G**2.0 * sigma_t_src**2.0);
	return eta_src,sigma_eta_src

def calc_cmb_ls_eff(c_raw_src=None,c_raw_bkg=None,d_src=None,u_d_src=None,
	I_src=None,u_I_src=None,r_det=None,u_r_det=None,l_det=None,
	u_l_det=None,t_src=None,u_t_src=None,t_bkg=None,u_t_bkg=None,
	c_raw_oppsrc=None,t_oppsrc=None,u_t_oppsrc=None):
	# first find all of the relative errors from the absolute error
	sigma_d_src = u_d_src / d_src;
	sigma_I_src = u_I_src / I_src;
	sigma_r_det = u_r_det / r_det;
	sigma_l_det = u_l_det / l_det;
	sigma_t_src = u_t_src / t_src;
	sigma_t_bkg = u_t_bkg / t_bkg;
	sigma_t_oppsrc = u_t_oppsrc / t_oppsrc;
	# calculate error in counts using poisson
	sigma_c_raw_src = math.sqrt(c_raw_src)/c_raw_src;
	# calculate error in background using poisson
	sigma_c_raw_bkg = math.sqrt(c_raw_bkg)/c_raw_bkg;
	# calculate error in the opposing source using poisson
	sigma_c_raw_oppsrc = math.sqrt(c_raw_oppsrc)/c_raw_oppsrc;
	# adjust background counts to match actual counts
	c_bkg = t_src * c_raw_bkg / t_bkg;
	# adjust opposing source counts to match actual counts
	c_oppsrc = (t_src * c_raw_oppsrc / t_oppsrc) - c_bkg;
	# calculate the error in the opposing source
	sigma_c_oppsrc = (c_raw_oppsrc/t_oppsrc)**2.0 * sigma_t_src**2.0 + \
	(-t_src*c_raw_oppsrc/t_oppsrc)**2.0 * sigma_t_oppsrc**2.0 + \
	(t_src/t_oppsrc)**2.0 * sigma_c_raw_oppsrc**2.0;
	# calculate the error in the background counts
	sigma_c_bkg = (c_raw_bkg/t_bkg)**2.0 * sigma_t_src**2.0 + \
	(-t_src*c_raw_bkg/t_bkg)**2.0 * sigma_t_bkg**2.0 + \
	(t_src/t_bkg)**2.0 * sigma_c_raw_bkg**2.0;
	# calculate efficiency using efficiency equation
	eta_src = 2*math.pi*(c_raw_src-c_oppsrc-c_bkg)*d_src*d_src/(I_src*r_det*l_det*t_src);
	# calculate propagated error using error propagation formula
	# squared term to the raw count error
	A = 2.0 * math.pi * d_src**2.0 / (I_src * r_det * l_det * t_src);
	# squared term to the background count error
	B = -2.0 * math.pi * d_src**2.0 / (I_src * r_det * l_det * t_src);
	# squared term to the distance to source error
	C = 4.0 * math.pi * (c_raw_src - c_bkg) * d_src / \
	(I_src * r_det * l_det * t_src);
	# squared term to the source intensity error
	D = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src**2.0 * r_det * l_det * t_src);
	# squared term to the detector radius error
	E = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det**2.0 * l_det * t_src);
	# squared term to the detector length error
	F = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det * l_det**2.0 * t_src);
	# squared term for the time error
	G = -2.0 * math.pi * (c_raw_src - c_bkg) * d_src**2.0 / \
	(I_src * r_det * l_det * t_src**2.0);
	sigma_eta_src = math.sqrt( A**2.0 * sigma_c_raw_src**2.0 + \
		B**2.0 * sigma_c_bkg**2.0 + C**2.0 * sigma_d_src**2.0 + \
		D**2.0 * sigma_I_src**2.0 + E**2.0 * sigma_r_det**2.0 + \
		F**2.0 * sigma_l_det**2.0 + G**2.0 * sigma_t_src**2.0);
	return eta_src,sigma_eta_src

class ls_test:
	something = '';
	def __init__(self,test_id='',source_str='',delt=0.0,t=None,counts=0,
		notes=None,bf3_files=[]):
		self.test_id = test_id; # set up the test id
		self.det_A = 25.0; # the Ne-213 has a 5cm OD x 5cm H
		# set up a list to list all the sources involved
		self.source = [];
		self.source_strength = [];
		self.source_dist = [];
		# read in each source separately
		sources = source_str.split(';');
		for src in sources:
			src_param = src.split('@');
			# determine the source
			self.source.append(src_param[0]); # source identifier
			# if we've listed a distance, add that to the source dist list
			if len(src_param) > 1:
				self.source_dist.append(float(src_param[1].strip('cm'))); 
				# source distance in cm
			# otherwise assume that it's right at the detector
			else:
				self.source_dist.append(0.0);
			# if we've listed a flux for the source, extract that
			if len(src_param) > 2:
				self.source_strength.append(float(src_param[2])); 
				# source strength in intensity
			# or use our known intensity for our isotope sources
			elif src_param[0] == 'Cf-252':
				self.source_strength.append(1.0E4);
			elif src_param[0] == 'Pu-Be':
				self.source_strength.append(2.0E6);
		# find out the time it took
		self.delt = delt;
		# amplify our accelerator sources by the level from the BF3 - if needed
		self.t = t;
		if t is not None:
			# import the times from bf3 files
			self.bf3_times = [];
			self.bf3_cpms = [];
			for key in bf3_files:
				self.add_bf3_counter_file(key);
			# find the start and stop time of the ls test
			delta = timedelta(seconds=self.delt);
			time_start = t - delta;
			averaging_cpms = []
			for i,time in enumerate(self.bf3_times):
				if time > time_start and time < t:
					averaging_cpms.append(self.bf3_cpms[i]);
			count_average = np.average(averaging_cpms);

		# import our number of counts
		self.counts = counts;
		# take any notes
		self.notes = notes;
		# calculate the efficiency for this test
		self.eff = self.calc_eff();
		print self.eff;
	def calc_phi(self):
		pass
	def calc_eff(self):
		incident_ns = 0.0;
		for i,src in enumerate(self.source):
			if self.source_dist[i] == 0.0:
				solid_angle = 1.0;
			else:
				solid_angle = self.det_A / (4.0*math.pi*self.source_dist[i]**2.0);
			print solid_angle;
			if i<len(self.source_strength):
				incident_ns = incident_ns + self.source_strength[i];
		if incident_ns > 0:
			eta = float(self.counts) / (incident_ns * self.delt);
		else:
			eta = None;
		return eta;
	def add_bf3_counter_file(self,filename):
		arr=np.genfromtxt(filename,skip_header=1,comments="#",dtype=None,
			usecols=np.arange(0,8));
		for row in arr:
			time = datetime(row[2],row[3],row[4],row[5],row[6],int(row[7]));
			cpm = 60.0*row[0]/row[1];
			self.bf3_times.append(time);
			self.bf3_cpms.append(cpm);
	def print_test(self):
		print "Test %s: %i s, giving %i counts from a %s source" % (self.test_id,self.delt,self.counts,self.source)
	
class ls_data(object):
	data = {};
	def __init__(self):
		#initialize here
		pass
	def import_dat(self,filename,bf3_files=[]):
		f = open(filename,'r')
		arr=np.genfromtxt(filename,comments="#",delimiter=",",
			dtype=None,usecols=np.arange(0,9));
		for row in arr:
			if row[7] != 'None':
				time_end = datetime.strptime(row[7],'%a %b %d %H:%M:%S %Y');
				if row[8] != 'None':
					time_add = datetime.strptime(row[8],'%H:%M:%S');
					delta = timedelta(hours=time_add.hour,minutes=time_add.minute,seconds=time_add.second);
					time_end = time_end + delta;
			test = ls_test(test_id=row[0],source_str=row[1],t=time_end,
				delt=row[2],counts=row[5],notes=row[6],bf3_files=bf3_files);
			self.data[row[0]] = test;
			del test;
		for key in self.data:
			self.data[key].print_test();