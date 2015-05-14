import numpy as np;
import math;
'''
class matl(object):
	def __init__(self,nuclides={}):
		self.nuclides=nuclides;

# decay:  https://t2.lanl.gov/nis/data/endf/decayVII.1.html
# photon: https://t2.lanl.gov/nis/data/endf/endfvii-g.html
# neutron: https://t2.lanl.gov/nis/data/endf/endfvii-n.html
class nuclide(object):
	name = '';
	t_1_2 = None;
	d_const = None;
	

class ndata(object):
	nuclide = '';
	txtfile = '';
	nuclides = {};
	possible_nuclides = [];
	def __init__(self):
		# make a folder for the data files
	def add_component(self,nuclide,wo=None,ndens=None):
		# add to the dict with the specified weight percent or number density
	def export_mcnp_entry(self):
		# print out an entry for a material card in mcnp
	def t_1_2(self):
		# check if single component
		# return half life if so
	def d_const(self):
		# get half life
		# return decay constant
	def xs(self,rxn='N,N',E=None):
		# return the cross section for a specified reaction at energies E or self.E
'''
# Helper Functions

def read_endf_line(line):
	#slice the first 66 characters
	line = line[0:65];
	#split the line into 11 width segments
	E = [];
	Edata = [];
	xs = [];
	xsdata = [];
	E.append(line[0:10]);
	xs.append(line[11:21]);
	E.append(line[22:32]);
	xs.append(line[33:43]);
	E.append(line[44:54]);
	xs.append(line[55:65]);
	for string in E:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			Edata.append(float(pre)*10.0**float(post));
	for string in xs:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			xsdata.append(float(pre)*10.0**float(post));
	return (np.array(Edata),np.array(xsdata));

def import_endf(filename):
	data = [line.strip() for line in open(filename, 'r')];
	#find the line ending with 099999
	(start_end,) = np.where([line.endswith("099999") for line in data]);
	#skip the next four lines
	data = np.array(data[start_end[0]+5:start_end[1]])
	#read in the lines between this and the next 099999
	
	E = [0.0];
	xs = [0.0];
	for line in data:
		(Edata,xsdata) = read_endf_line(line);
		for erg in Edata:
			E.append(erg);
		for sigma in xsdata:
			xs.append(sigma);
	E.append(np.max(E)+1.0);
	xs.append(0.0);
	E = np.array(E)/1.0E6; # convert to MeV
	return (E,np.array(xs));