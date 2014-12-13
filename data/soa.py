import numpy as np;
import datetime as dt;
import math;
from matplotlib.pyplot import close
from datetime import datetime, timedelta
from ..plotting import twod as ahp

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