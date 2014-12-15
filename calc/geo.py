import numpy as np
import math
import ..calc.math as ahmath

class coord_transform(object):
	def __init__(self,target='cartesian'):
		self.target = target;
	def cart_to_target(self,_input):
		pass;
	def spherical_to_target(self,_input):
		pass;
	def cyl_to_target(self,_input):
		pass;
	def to_target(self,_input,source='spherical'):
		return _input;

class shape(object):
	def __init__(self,coord='cartesian',shape='point',origin=(0,0,0),
		size=(1,1,1),_dir=(1,0,0)):
		# initialize my coordinate transform object
		coord_obj = coord_transform();
		self.shape = shape;
		# change the vectors to cartesian coordinates
		self.origin = coord_obj.to_target(origin,source=coord);
		self.size = coord_obj.to_target(size,source=coord);
		self.dir = coord_obj.to_target(_dir,source=coord);


class solid_angle(object):
	''' The solid_angle object uses a monte carlo method to calculate soild angle.

	More info here
	'''
	def __init__(self,coord='cartesian'):
		''' To initialize the solid_angle object, we add in the coordinate system

		The possible values for coordinate system are:
		-  cartesian (default): x,y,z
		-  spherical: r, \\theta, \\psi
		-  cylindrical: r, \\theta, z
		The values of coordinate system will not change the result, but will 
		instead help with input of the geometry
		'''
		# define our coordinate system
		self.coord = coord;
		# first we make a list of sources - initilized to empty
		sources = {};
		# then we make a list of detectors - initialized to empty
		dets = {};
		# start our random number generator
		mc = ahmath.rand_gen();
	def add_det(self,name='det',shape='cylinder',origin=(0,0,0),size=(1,1,1),
		_dir=(1,0,0)):
		''' We add the detector which will subtend the solid angle

		The input values needed are:
		-  shape: the shape of the detector.  possible values are:
			- 'cylinder'
			- 'rectangular-parallelpiped'
			- 'sphere'
		-  origin: tuple giving the center of the detector
		-  size:  tuple giving the size of the detector in coordinate system
		-  dir:  tuple giving vector direction of the detectors axis
		'''
		dets[name] = shape(coord=self.coord,shape=shape,origin=origin,size=size,
			dir=_dir);
	def add_source(self,shape='point',origin=(0,0,0),size=(1,1,1),_dir=(1,0,0)):
		''' We add a source which will emit the particles

		The input values needed are:
		-  shape: the shape of the source.  possible values are:
			- 'point' - all other input parameters but origin are ignored
			- 'cylinder'
			- 'rectangular-parallelpiped'
			- 'sphere'
		-  origin: tuple giving the center of the source
		-  size:  tuple giving the size of the source in coordinate system
		-  dir:  tuple giving vector direction of the source axis
		'''
		sources[name] = shape(coord=self.coord,shape=shape,origin=origin,
			size=size,dir=_dir);
	def calc_solid_angle(self):
		total_particles = 0;
		# sum the solid angle over all the dets from all the sources
		for source in sources:
			for det in dets:
				# perform the monte carlo simulation 1E9 times
				#######  WE COULD CHANGE THIS TO AUTO DETECT CONVERGENCE #######
				for i in range(0,1E9):
					# emit one particle from a random point in the current 
					# source, with arbitrary direction
					# find a random point inside the current source
					####### WE COULD MOVE THIS ROUTINE TO THE SHAPE CLASS ######
					if source.shape is 'point':
						particle_origin = source.shape.origin;
					elif source.shape is 'sphere':
						pass;
					elif source.shape is 'cylinder':
						pass;
					# find two angles defining the direction
					particle_dir = (math.pi*random.rand(),
						2*math.pi*random.rand());
					# determine if that particle crosses the detector
					##### WE COULD MOVE THIS ROUTINE TO THE SHAPE CLASS ########
					if det.shape is 'cylinder':
						pass;
					elif det.shape is 'sphere':
						pass;
					elif det.shape is 'rectangular-parallelpiped':
						pass;
		return sa;	