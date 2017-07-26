import twod
import numpy as np
from colour import Color
import os
import svgutils.compose as sc
from matplotlib.transforms import Bbox

class asset(object):
	def __init__(self, filename, bbox, parent):
		self.filename = filename
		self.bbox = bbox
		self.parent = parent

	def calc_pos(self):
		width = self.parent.get_width(self.filename)
		height = self.parent.get_height(self.filename)
		aspect_ratio = width / height
		dpi = 200.
		bbox = self.parent.ax.transData.transform(self.bbox)
		max_width = bbox[1, 0] - bbox[0, 0]
		max_height = bbox[1, 1] - bbox[0, 1]
		# Our first option is to make the width the full of the bounding box
		set_width = max_width
		set_height = set_width * aspect_ratio
		self.scale = 1.0/(set_width / width)
		if set_height > max_height:
			set_height = max_height
			set_width = set_height / aspect_ratio
			self.scale = 1.0 / (set_height / height)
		self.x = bbox[0, 0]
		self.y = bbox[1, 1]
		#print scale
		#print disp_coords
		#print fig_coords
		#self.scale = 1.0
		print "scale: %f" % (self.scale)
		print "fig_width: %f" % (self.parent.fig.dpi * self.parent.fig.get_figwidth())
		print "fig_height: %f" % (self.parent.fig.dpi * self.parent.fig.get_figheight())
		self.fig_height = self.parent.fig.dpi * self.parent.fig.get_figheight()
		#self.y = self.fig_height - (self.y + (set_height / 2.0))/1.25
		#self.x = (self.x - (set_width / 2.0))/1.25
		print "pos: %f, %f" % (self.x, self.y)

class composite(twod.pyg2d):
	def __init__(self):
		super(composite, self).__init__()
		self.above = []
		self.below = []

	@staticmethod
	def get_width(fname):
		width = float(os.system('inkscape --without-gui -query-width %s' % fname))
		return width

	@staticmethod
	def get_height(fname):
		height = float(os.system('inkscape --without-gui -query-height %s' % fname))
		return height

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
		kwargs['formats'] = ['svg']
		super(composite, self).export(*args, **kwargs)
		below_panels = []
		for asst in self.above:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			below_panels.extend([x])
		panel = [sc.Panel(sc.SVG(self.svg_filename).scale(1.25))]
		above_panels = []
		for asst in self.above:
			asst.calc_pos()
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			above_panels.extend([x])
		panels = below_panels + panel + above_panels
		print panels
		sc.Figure("%fcm" % (2.54 * self.width), "%fcm" % (2.54 * self.height),
		    *panels
		).save(self.svg_filename)
