import numpy as np;
import math;

# decay:  https://t2.lanl.gov/nis/data/endf/decayVII.1.html
# photon: https://t2.lanl.gov/nis/data/endf/endfvii-g.html
# neutron: https://t2.lanl.gov/nis/data/endf/endfvii-n.html

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
		