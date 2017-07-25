import twod
import numpy as np
from colour import Color
import os
import svgutils.compose as sc
from matplotlib.transforms import Bbox

class asset(object):
	def __init__(self, filename, width, height, x, y, scale):
		self.filename = filename
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.scale = scale

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

	@staticmethod
	def get_dpi(fname):
		return 200.0

	def add_asset(self, filename, wh=[10.0, 10.0], pos=(0., 0.), above=True):
		# first we have to calculate the bounding box while keeping aspect
		# ratio
		# then, we create an asset
		asst = asset(filename, set_width, set_height,
					 1.25 * pos[0], self.fig.dpi * self.fig.get_figheight() - pos[1],
					 scale)
		if above:
			self.above.extend([asst])
		else:
			self.below.extend([asst])

	def calc_scale(self):
		width = self.get_width(filename)
		height = self.get_height(filename)
		aspect_ratio = width / height
		self.dpi = self.get_dpi(filename)
		bb_data = Bbox.from_bounds(pos[0], pos[1],
								   wh[0], wh[1])
		disp_coords = self.ax.transData.transform(bb_data)
		fig_coords = self.fig.transFigure.inverted().transform(disp_coords)
		pos = self.ax.transData.transform((pos[0], pos[1]))
		print pos

		# Our first option is to make the width the full of the bounding box
		set_width = wh[0]
		set_height = set_width / aspect_ratio
		scale = wh[0] / width * self.dpi
		if set_height > wh[1]:
			set_height = wh[1]
			set_width = set_height * aspect_ratio
			scale = wh[1] / height * self.dpi
		#print scale
		#print disp_coords
		#print fig_coords
		print "fig_width: %f" % (self.fig.dpi * self.fig.get_figwidth())
		print "fig_height: %f" % (self.fig.dpi * self.fig.get_figheight())
		print "pos: %f, %f" % (pos[0], pos[1])

	def calc_pos(self, asst):
		pass

	def export(self, *args, **kwargs):
		kwargs['formats'] = ['svg']
		super(composite, self).export(*args, **kwargs)
		below_panels = []
		for asst in self.above:
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			below_panels.extend([x])
		panel = [sc.Panel(sc.SVG(self.svg_filename).scale(1.25))]
		above_panels = []
		for asst in self.above:
			x = sc.Panel(sc.SVG(asst.filename).scale(asst.scale)\
				.move(asst.x, asst.y))
			above_panels.extend([x])
		panels = below_panels + panel + above_panels
		print panels
		sc.Figure("%fcm" % (2.54 * self.width), "%fcm" % (2.54 * self.height),
		    *panels
		).save(self.svg_filename)
