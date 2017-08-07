import twod
import numpy as np
from colour import Color
import os
import os.path
import svgutils.compose as sc
from sys import platform
import subprocess

gscale = 0.96

class asset(object):
	def __init__(self, filename, bbox, parent):
		self.filename = filename
		self.bbox = bbox
		self.parent = parent
		self.cwd = os.getcwd()
		self.gscale = 1.144117591

	def calc_pos(self):
		width = self.parent.get_width(self.filename)
		height = self.parent.get_height(self.filename)
		aspect_ratio = width / height
		bbox = self.parent.ax.transData.transform(self.bbox)
		max_width = np.abs(bbox[1, 0] - bbox[0, 0])/self.gscale
		max_height = np.abs(bbox[1, 1] - bbox[0, 1])/self.gscale
		self.fig_height = self.parent.fig.dpi * self.parent.fig.get_figheight() / self.gscale
		top_margin = self.fig_height - self.parent.get_height(self.parent.svg_filename) - self.parent.get_y(self.parent.svg_filename)
		set_width = max_width
		set_height = set_width * aspect_ratio
		self.scale = (set_width / width)
		if set_height > max_height:
			set_height = max_height
			set_width = set_height / aspect_ratio
			self.scale = (set_height / height)
		self.x = ((bbox[0, 0] + bbox[1, 0])/2.0 - (set_width/2.0))/self.gscale - self.parent.get_x(self.parent.svg_filename)
		self.y = ((bbox[1, 1] + bbox[0, 1])/2.0 + (set_height/2.0))/self.gscale - top_margin
		self.y = self.parent.get_height(self.parent.svg_filename) - self.y

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
		y = float(out)
		return y

	def get_dpi(self, fname):
		return self.fig.dpi

	def add_asset(self, filename, wh=[10.0, 10.0], pos=(0., 0.), above=True):
		x1 = pos[0] - wh[0]/2.0
		x2 = pos[0] + wh[0]/2.0
		y1 = pos[1] - wh[1]/2.0
		y2 = pos[1] + wh[1]/2.0
		#self.add_line([x1, x1, x2, x2, x1], [y1, y2, y2, y1, y1])
		bbox = np.array([[x1, y1], [x2, y2]])
		asst = asset(filename, bbox, self)
		if above:
			self.above.extend([asst])
		else:
			self.below.extend([asst])

	def export(self, *args, **kwargs):
		super(composite, self).export(*args, formats=['websvg'], **kwargs)
		os.system('inkscape -z --export-area-drawing --export-pdf=temp.pdf %s' % (self.svg_filename))
		os.system('inkscape -z --export-plain-svg=%s temp.pdf' % (self.svg_filename))
		below_panels = []
		for asst in self.below:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			below_panels.extend([x])
		x = sc.Panel(sc.SVG(self.svg_filename))
		x.scale(gscale)
		panel = [x]
		above_panels = []
		for asst in self.above:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			above_panels.extend([x])
		panels = below_panels + panel + above_panels
		sc.Figure("%fpx" % (self.get_width(self.svg_filename)),
				  "%fpx" % (self.get_height(self.svg_filename)),
			*panels
		).save(self.svg_filename)
