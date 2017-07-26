import twod
import numpy as np
from colour import Color
import os
import os.path
import svgutils.compose as sc
from sys import platform
import subprocess

gscale = 1.00

class asset(object):
	def __init__(self, filename, bbox, parent):
		self.filename = filename
		self.bbox = bbox
		self.parent = parent
		self.cwd = os.getcwd()
		self.gscale = 1.5

	def calc_pos(self):
		width = self.parent.get_width(self.filename)
		height = self.parent.get_height(self.filename)
		aspect_ratio = width / height
		dpi = 96.
		bbox = self.parent.ax.transData.transform(self.bbox)
		print bbox
		max_width = (bbox[1, 0] - bbox[0, 0])/self.gscale
		max_height = (bbox[1, 1] - bbox[0, 1])/self.gscale
		# Our first option is to make the width the full of the bounding box
		set_width = max_width
		set_height = set_width * aspect_ratio
		self.scale = (set_width / width)
		if set_height > max_height:
			set_height = max_height
			set_width = set_height / aspect_ratio
			self.scale = (set_height / height)
		self.x = ((bbox[0, 0] + bbox[1, 0])/2.0 - (set_width/2.0))/self.gscale
		self.y = ((bbox[1, 1] + bbox[0, 1])/2.0 + (set_height/2.0))/self.gscale
		#print scale
		#print disp_coords
		#print fig_coords
		#self.scale = 1.0
		print "set_width: %f set_height: %f" % (set_width, set_height)
		print "width: %f height: %f" % (width, height)
		print "scale: %f" % (self.scale)
		print "fig_width: %f" % (self.parent.fig.dpi * self.parent.fig.get_figwidth())
		print "fig_height: %f" % (self.parent.fig.dpi * self.parent.fig.get_figheight())
		self.fig_height = gscale * self.parent.fig.dpi * self.parent.fig.get_figheight()
		self.y = self.fig_height - self.y
		#self.x = (self.x - (set_width / 2.0))/1.25
		print "pos: %f, %f" % (self.x, self.y)

class composite(twod.pyg2d):
	def __init__(self):
		super(composite, self).__init__()
		self.above = []
		self.below = []
		self.cwd = os.getcwd()

	def get_width(self, fname):
		if platform == "linux" or platform == "linux2":
			inkscape_bin = 'inkscape'
		elif platform == "darwin":
			inkscape_bin = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
		elif platform == "win32":
			pass
		cmd = '%s --without-gui --query-width %s' % (inkscape_bin, os.path.join(self.cwd,fname))
		#print cmd
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		#print out,err
		width = float(out)
		return width

	def get_height(self, fname):
		if platform == "linux" or platform == "linux2":
			inkscape_bin = 'inkscape'
		elif platform == "darwin":
			inkscape_bin = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
		elif platform == "win32":
			pass
		cmd = '%s --without-gui --query-height %s' % (inkscape_bin, os.path.join(self.cwd,fname))
		#print cmd
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		#print out,err
		height = float(out)
		return height

	def get_x(self, fname):
		if platform == "linux" or platform == "linux2":
			inkscape_bin = 'inkscape'
		elif platform == "darwin":
			inkscape_bin = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
		elif platform == "win32":
			pass
		cmd = '%s --without-gui --query-x %s' % (inkscape_bin, os.path.join(self.cwd,fname))
		#print cmd
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		#print out,err
		x = float(out)
		return x

	def get_y(self, fname):
		if platform == "linux" or platform == "linux2":
			inkscape_bin = 'inkscape'
		elif platform == "darwin":
			inkscape_bin = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
		elif platform == "win32":
			pass
		cmd = '%s --without-gui --query-y %s' % (inkscape_bin, os.path.join(self.cwd,fname))
		#print cmd
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		#print out,err
		y = float(out)
		return y

	def get_dpi(self, fname):
		return self.fig.dpi

	def add_asset(self, filename, wh=[10.0, 10.0], pos=(0., 0.), above=True):
		x1 = pos[0] - wh[0]/2.0
		x2 = pos[0] + wh[0]/2.0
		y1 = pos[1] - wh[1]/2.0
		y2 = pos[1] + wh[1]/2.0
		self.add_line([x1, x1, x2, x2, x1], [y1, y2, y2, y1, y1])
		bbox = np.array([[x1, y1], [x2, y2]])
		asst = asset(filename, bbox, self)
		if above:
			self.above.extend([asst])
		else:
			self.below.extend([asst])

	def export(self, *args, **kwargs):
		super(composite, self).export(*args, formats=['svg'], **kwargs)
		below_panels = []
		for asst in self.below:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			below_panels.extend([x])
		x = sc.Panel(sc.SVG(self.svg_filename))
		x.moveto(0., 0., gscale)
		panel = [x]
		above_panels = []
		for asst in self.above:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			above_panels.extend([x])
		panels = below_panels + panel + above_panels
		print panels
		sc.Figure("%fpx" % (self.get_width(self.svg_filename)),
				  "%fpx" % (self.get_height(self.svg_filename)),
			*panels
		).save(self.svg_filename)
