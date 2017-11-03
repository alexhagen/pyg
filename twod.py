from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
import matplotlib
import string
import os
from matplotlib.patches import Ellipse, Polygon, Circle
from matplotlib.lines import Line2D
from colour import Color
import numpy as np
import platform
import shutil
import time
from copy import copy
from IPython.display import SVG, display, Latex, HTML, display_latex
import subprocess
import sys
import random
import weakref
import re
import __builtins__ as bi
import lyxithea.lyxithea as lyx
from itertools import count
import psgv.psgv as psgv
import pickle
import os.path

__context__ = psgv.psgv('__context__')
__context__.val = 'writeup'
__figures__ = psgv.psgv('__lyxfigures__')
__figures__.val = {}
__force__ = psgv.psgv('__pygforce__')
__force__.val = False

def ratio(ratio='golden'):
	if ratio is "golden":
		r = (1. + np.sqrt(5.)) / 2.
	elif ratio is "silver":
		r = 1. + np.sqrt(2.)
	elif ratio is "bronze":
		r = (3. + np.sqrt(13.)) / 2.
	elif ratio is "invgolden":
		r = 2. / (1. + np.sqrt(5.))
	elif ratio is "invsilver":
		r = 1. / (1. + np.sqrt(2.))
	elif ratio is "invbronze":
		r = 2. / (3. + np.sqrt(13.))
	return r

def context(ctx='writeup'):
	__context__.val = ctx

if "DISPLAY" not in os.environ.keys():
	import matplotlib
	matplotlib.use('Agg')
else:
	import matplotlib
	matplotlib.use('pgf')

import matplotlib.pyplot as plt

plt.close("all")
preamble = ['\usepackage{nicefrac}',
	'\usepackage{gensymb}',
	'\usepackage{xcolor}',
	'\definecolor{grey60}{HTML}{746C66}',
	'\definecolor{grey40}{HTML}{A7A9AC}',
	r'\usepackage{amsmath, amssymb}',
	r'\usepackage{stackrel}',
	'\\providecommand{\unit}[1]{\ensuremath{\\textcolor{grey60}' +
	'{\mathrm{#1}}}}']

def force(val=True):
	__force__.val = val

def load(fname, svg=False):
	_fig = pickle.load(file(os.path.expanduser('~') +
							'/.pyg/%s.pickle' % fname))
	if not svg:
		_fig.fig._cachedRenderer = None
		for ax in [_fig.ax, _fig.ax2]:
			if ax is not None:
				for axi in ax.images:
					axi._imcache = None
				ax._cachedRenderer = None
	_fig.loaded = True
	return _fig

class svg(object):
	def __init__(self, filename):
		self.filename = filename
		self.loaded = False

	@staticmethod
	def get_width(fname):
		if 'png' in fname:
			cmd = 'identify -format "%%[w]" %s' % fname
		else:
			cmd = 'inkscape --without-gui --query-width %s' % fname
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		try:
			width = float(out)
		except ValueError:
			print out
			print err
		return width

	@staticmethod
	def get_height(fname):
		if 'png' in fname:
			cmd = 'identify -format "%%[h]" %s' % fname
		else:
			cmd = 'inkscape --without-gui --query-height %s' % fname
		p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
		(out, err) = p.communicate()
		try:
			height = float(out)
		except ValueError:
			print out
			print err
		return height

	def show(self, caption='', label=None, scale=None, width=None,
			 convert=True, need_string=False, bbox=None):
		if label is not None and not self.loaded:
			pickle.dump(self, file(os.path.expanduser('~') +
									'/.pyg/%s.pickle' % label, 'w'))
		fig = None
		if label is None:
			label = caption
		html_widths = {'1': 400, '2': 600, '4': 800}
		if lyx.run_from_ipython() and not lyx.need_latex():
			__counter__ = random.randint(0, 2e9)
		curr_width = self.get_width(self.filename)
		curr_height = self.get_height(self.filename)
		if width is not None:
			if isinstance(width, int) or isinstance(width, float):
				fig_width = width
			elif isinstance(width, str):
				fig_width = html_widths[width]
		elif scale is not None:
			fig_width = curr_width * scale
		if not lyx.need_latex():
			fig_html = r"""
				<div class='figure' name='%s' style='align: center; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:800px; width:%fpx; height: auto;' src='%s?%d' />
					<div style='margin: auto; text-align: center;' class='figurecaption' name="%s"><b>Figure %d:</b> %s</div>
				</div>
			""" % (label, fig_width, self.filename, __counter__, label, bi.__figcount__, caption)
			__figures__.val[label] = bi.__figcount__
			bi.__figcount__ += 1
			return display(HTML(fig_html))
		else:
			if __context__.val == "writeup":
				widths = {"1": 3.25, "2": 6.25, "4": 12.50, "fp": 10.0, "cs": 0.0}
			elif __context__.val == "tufte":
				widths = {"1": 2.00, "2": 4.30, "4": 6.30, "fp": 10.0, "cs": 0.0}
			elif __context__.val == "thesis":
				widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
			else:
				widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
			if width is not None:
				if isinstance(width, float):
					fig_width = width
				else:
					fig_width = widths[width]
			else:
				fig_width = widths['2']
			if bbox is not None:
				if fig_width * curr_height / curr_width > bbox[1]:
					fig_width = bbox[1] * curr_width / curr_height
			svg_filename = self.filename
			pdf_filename = self.filename.replace('.svg', '.pdf')
			if convert:
				os.system('inkscape --without-gui -f {svg_filename} -A {pdf_filename}'.format(pdf_filename=pdf_filename, svg_filename=svg_filename))
				#os.system('rsvg-convert -f pdf -o {pdf_filename} {svg_filename}'.format(pdf_filename=pdf_filename, svg_filename=svg_filename))
			strlatex = r"""
			\begin{figure}
				\centering
				\includegraphics[width=%.2fin]{%s}
				\caption{%s\label{fig:%s}}
			\end{figure}""" % (fig_width, pdf_filename, caption, label)
			__figures__.val[label] = bi.__figcount__
			bi.__figcount__ += 1
			if need_string:
				return strlatex
			return Latex(strlatex)

def svg_show(filename, caption='', label=None, scale=None, width=None,
			 convert=True, need_string=False):
	_svg = svg(filename)
	return _svg.show(caption=caption, label=label, scale=scale, width=width,
					 convert=convert, need_string=need_string)


# make the line graphing class
class pyg2d(object):
	""" A ``pyg.pyg2d`` object plots many two-dimensional data types.

	The ``pyg2d`` class provides an access to ``matplotlib`` charting functions
	and some hook ins to making these functions easier to use and more
	repeatable.  The constructor itself takes only one optional argument,
	``env``.

	.. todo::

		Add more color schemes and the ability to define and hook in color
		schemes manually.

	:param str env: The environement option defines where you are going to use
		the generated plot, with the default option being plot (or printing).
		If you are using this to generate plots for a gui, define this option
		as ``gui`` and the class will choose a prettier parameter set for your
		chart. Default: ``plot``.
	:param str colors: The ``colors`` option defines the color scheme which
		will be used in the plotting.  The ability to hook in schemes will be
		added. Default: ``purdue``.
	:type env: ``plot``, ``gui``, or ``None``
	:type colors: ``pu``, ``purdue``, ``salabs``, or ``ah``
	:return: the ``pyg2d`` object.
	:rtype: ``pyg2d``
	"""
	leg_col_one_col = 2
	leg_col_two_col = 3
	leg_col_full_page = 4
	instances = []
	marker = {0: '+',
			  1: '.',
			  2: '1',
			  3: '2',
			  4: '3',
			  5: '4'}
	linestyle = {0: '-',
				 1: '--',
				 2: '-.',
				 3: ':'}
	sizestring = {'1': 'onecolumn',
				  '2': 'twocolumn',
				  'fp': 'fullpage',
				  'cs': 'customsize',
				  'none': ''}
	_figcount = count(0)

	def __init__(self, env='plot', polar=False, colors='purdue'):
		self.__class__.instances.append(weakref.proxy(self))
		self.__counter__ = self._figcount.next()
		self.fig = plt.figure(self.__counter__)
		self.ax = self.fig.add_subplot(111, polar=polar)
		self.ax_subp = []
		self.leg = False
		self.loaded = False
		self.ax2 = None
		self.polar = polar
		if not self.polar:
			self.ax.spines['top'].set_visible(False)
			self.ax.spines['right'].set_visible(False)
		self.ax.get_xaxis().tick_bottom()
		self.ax.get_yaxis().tick_left()
		self.artists = []
		self.landscape = True
		self.width = 3.25
		self.height = self.width / 1.61803398875
		self.plotnum = 0
		self.regnum = 0
		self.lines = {}
		self.bars = {}
		self.regs = {}
		self.reg_string = {}
		self.allartists = []
		self.pdf_filename = None
		self.html_filename = None
		self.data = []
		if colors is 'purdue' or colors is 'pu':
			import pyg.colors.pu as color
			self.colors = color.pu_colors
		else:
			import pyg.colors.pu as color
			self.colors = color.pu_colors
		if env is 'plot':
			self.rcparamsarray = {
				"pgf.texsystem": "lualatex",
				"pgf.rcfonts": False,
				"font.family": "sans",
				"font.size": 8.0,
				"axes.linewidth": 0.5,
				"axes.edgecolor": "#746C66",
				"xtick.major.width": 0.25,
				"xtick.major.size": 2,
				"xtick.direction": "in",
				"xtick.minor.width": 0.125,
				"xtick.color": "#746C66",
				"ytick.major.width": 0.25,
				"ytick.major.size": 2,
				"ytick.minor.width": 0.125,
				"ytick.color": "#746C66",
				"ytick.direction": "in",
				"text.color": "#746C66",
				"axes.facecolor": "none",
				"figure.facecolor": "none",
				"axes.labelcolor": "#746C66",
				"xtick.labelsize": "small",
				"ytick.labelsize": "small",
				"axes.labelsize": "medium",
				"legend.fontsize": "small",
				"legend.frameon": False,
				"axes.grid": False,
				"grid.color": "#A7A9AC",   # grid color
				"grid.linestyle": ":",       # dotted
				"grid.linewidth": 0.125,     # in points
				"grid.alpha": 0.5,     # transparency, between 0.0 and 1.0
				"savefig.transparent": True,
				"path.simplify": True,
				"text.usetex": True,
				"pgf.preamble": preamble,
				"text.latex.preamble": preamble
			}
		elif env is 'gui':
			self.rcparamsarray = {
				"pgf.texsystem": "lualatex",
				"pgf.rcfonts": False,
				"font.family": "sans",
				"font.size": 18.0,
				"axes.linewidth": 0.5,
				"axes.edgecolor": "#FFFFFF",
				"xtick.major.width": 0.25,
				"xtick.major.size": 2,
				"xtick.direction": "in",
				"xtick.minor.width": 0.125,
				"xtick.color": "#FFFFFF",
				"ytick.major.width": 0.25,
				"ytick.major.size": 2,
				"ytick.minor.width": 0.125,
				"ytick.color": "#FFFFFF",
				"ytick.direction": "in",
				"text.color": "#FFFFFF",
				"axes.facecolor": "black",
				"figure.facecolor": "black",
				"axes.labelcolor": "#FFFFFF",
				"xtick.labelsize": 12.0,
				"ytick.labelsize": 12.0,
				"axes.labelsize": 16.0,
				"legend.fontsize": "small",
				"legend.frameon": False,
				"axes.grid": False,
				"grid.color": "#A7A9AC",   # grid color
				"grid.linestyle": ":",       # dotted
				"grid.linewidth": 0.125,     # in points
				"grid.alpha": 0.5,     # transparency, between 0.0 and 1.0
				"savefig.transparent": True,
				"path.simplify": True,
				"pgf.preamble": preamble,
				"text.latex.preamble": preamble
			}
		matplotlib.rcParams.update(self.rcparamsarray)

	@staticmethod
	def change_context(context):
		__context__.val = context

	def xlabel(self, label, axes=None):
		r""" ``pyg2d.xlabel`` adds a label to the x-axis.

		``pyg2d.xlabel`` adds a label to the x-axis of the current axes (or
		other axis given by kwarg ``axes``).

		:param str label: The label added to the x-axis of the defined axis.
			The label can take LaTeX arguments and the ah style guide asks for
			labels given as 'Label ($variable$) [$unit$]'.
		:param axes: If not ``None``, this argument will apply the x-label
			to the provided axis.
		:type axes: axes, or ``None``
		:return: None
		"""
		if axes is None:
			axes = self.ax
		xlab = axes.set_xlabel(label)
		self.artists.append(xlab)
		self.allartists.append('xlab: ' + label)

	def add_subplot(self, subp=121, polar=False):
		""" ``pyg2d.add_subplot`` adds a grid in which you can make subplots.

		``pyg2d.add_subplot`` follows Matlab's lead and allows you to plot
		several axes on one plot. The newly created axes is saved as
		``pyg2d.ax2`` - this should be expanded for more axes later.

		.. todo::

			Expand subplotting to be able to use more than two axes total.

		:param int subp: If kwarg ``subp`` is not defined, the
			default is to add a second plot in a 1x2 array.  When ``subp`` is
			defined, it will follow that system (i.e. ``subp=234`` means you
			have two rows and three columns and you are plotting in the 4th
			postition ``(2,1)``).
		:return: None
		"""
		gsstr = str(subp)
		gs1 = int(gsstr[0])
		gs2 = int(gsstr[1])
		self.ax2 = self.fig.add_subplot(subp, polar=polar)
		self.ax.change_geometry(gs1, gs2, 1)
		self.ax2.change_geometry(gs1, gs2, 2)
		self.ax_subp.append(self.fig.add_subplot(subp))
		if not self.polar:
			self.ax2.spines['top'].set_visible(False)
			self.ax2.spines['right'].set_visible(False)
		self.ax2.get_xaxis().tick_bottom()
		self.ax2.get_yaxis().tick_left()

	def title(self, title, axes=None):
		""" ``pyg2d.title`` adds a title to the plot.

		:param str title: the title to be added to the plot. The title can take
			LaTeX arguments.
		:return: None
		"""
		if axes is None:
			axes = self.ax
		ttl = axes.set_title(title)
		self.artists.append(ttl)
		self.allartists.append(ttl)

	def ylabel(self, label, axes=None):
		""" ``pyg2d.ylabel`` adds a label to the y-axis.

		``pyg2d.ylabel`` adds a label to the y-axis of the current axes (or
		other axis given by kwarg ``axes``).  The label can take LaTeX
		arguments and the ah style guide asks for labels given as 'Label
		($variable$) [$unit$]'.

		:param str label: The label added to the y-axis of the defined axis.
			The label can take LaTeX arguments and the ah style guide asks for
			labels given as 'Label ($variable$) [$unit$]'.
		:param axes: If not ``None``, this argument will apply the x-label
			to the provided axis.
		:type axes: axes, or ``None``
		:return: None
		"""
		if axes is None:
			axes = self.ax
		ylab = axes.set_ylabel(label)
		self.artists.append(ylab)
		self.allartists.append('ylab: ' + label)

	def xlim(self, minx, maxx, axes=None):
		""" ``pyg2d.xlim`` limits the view of the x-axis to limits.

		:param float minx: The minimum value of x that will be shown.
		:param float maxx: The maximum value of x that will be shown.
		:param axes: If not ``None``, this argument will apply the x-limit
			to the provided axis.
		:type axes: axes, or ``None``
		:return: None
		"""
		if axes is None:
			axes = self.ax
		axes.set_xlim([minx, maxx])

	def ylim(self, miny, maxy, axes=None):
		""" ``pyg2d.ylim`` limits the view of the y-axis to limits.

		:param float miny: The minimum value of y that will be shown.
		:param float maxy: The maximum value of y that will be shown.
		:param axes: If not ``None``, this argument will apply the y-limit
			to the provided axis.
		:type axes: axes, or ``None``
		:return: None
		"""
		if axes is None:
			axes = self.ax
		axes.set_ylim([miny, maxy])

	def legend(self, loc=1, exclude='saljfdaljdfaslkjfd', axes=None):
		""" ``pyg2d.legend`` shows the legend on the plot.

		``pyg2d.legend`` toggles the legend showing on.  This is done by getting
		the included objects and titles from the ``matplotlib`` axis item, and
		then checking to see if there is the word 'connector' in that title. If
		there is that word, then the entry is discarded.

		:param int loc: The location of the legend in counter-clockwise
			notation.
		:param str exclude: Partial key string of legend entries to exclude
		:return: None
		"""
		if axes is None:
			axes = self.ax
		self.leg = axes.legend(loc=loc)
		(legobjs, legtitles) = axes.get_legend_handles_labels()
		inc_objs = []
		inc_titles = []
		for i in range(0, len(legtitles)):
			if 'connector' not in legtitles[i] and exclude not in legtitles[i]:
				inc_objs.append(legobjs[i])
				inc_titles.append(legtitles[i])
		axes.legend(inc_objs, inc_titles, loc=loc)

	def xticks(self, ticks, labels, axes=None):
		""" ``pyg2d.xticks`` changes the ticks and labels to provided values.

		``pyg2d.xticks`` will move the ticks on the abscissa to the
		locations given in ``ticks`` and place the labels in list ``labels`` at
		those locations, repsectively.

		:param list ticks: The values where the new tick labels will be placed
			on the x-axis.
		:param list labels: The string labels for each tick.
		:param axes axes: An axes to append these ticks to, if not current.
		:return: None
		"""
		if axes is not None:
			plt.sca(axes)
		else:
			axes = self.ax
		axes.set_xticks(ticks)
		axes.set_xticklabels(labels)

	def yticks(self, ticks, labels, axes=None):
		""" ``pyg2d.yticks`` changes the ticks and labels to provided values.

		``pyg2d.yticks`` will move the ticks on the ordinate axis to the
		locations given in ``ticks`` and place the labels in list ``labels`` at
		those locations, repsectively.

		:param list ticks: The values where the new tick labels will be placed
			on the y-axis.
		:param list labels: The string labels for each tick.
		:param axes axes: An axes to append these ticks to, if not current.
		:return: None
		"""
		if axes is not None:
			plt.sca(axes)
		else:
			axes = self.ax
		axes.set_yticks(ticks)
		axes.set_yticklabels(labels)

	def markers_on(self):
		""" ``pyg2d.markers_on`` turns on the data markers for all data sets.

		:return: None
		"""
		for key in self.lines:
			self.lines[key].set_alpha(1.0)
			self.lines[key].set_markersize(6)

	def markers_off(self):
		""" ``pyg2d.markers_off`` turns off the data markers for all data sets.

		:return: None
		"""
		for key in self.lines:
			self.lines[key].set_markersize(0)

	def fit_markers_off(self):
		""" ``pyg2d.fit_markers_off`` turns off the data markers for any
			fit lines that are plotted

		:return: None
		"""
		for key in self.lines:
			if "fit" in key:
				self.lines[key].set_markersize(0)

	def fit_lines_on(self):
		""" ``pyg2d.fit_lines_on`` turns on the connector lines for any
			regression fits that are plotted

		:return: None
		"""
		for key in self.lines:
			if "fit" in key:
				self.lines[key].set_linewidth(1.0)

	def lines_on(self):
		""" ``pyg2d.lines_on`` turns on the connector lines for all data sets.

		:return: None
		"""
		for key in self.lines:
			self.lines[key].set_linewidth(1.0)

	def lines_off(self):
		""" ``pyg2d.lines_off`` turns off the connector lines for all data sets.

		:return: None
		"""
		for key in self.lines:
			self.lines[key].set_linewidth(0.0)

	def add_vline(self, x, ymin=None, ymax=None, ls='solid', lw=1.5,
				  color='black', name=None, axes=None):
		""" ``pyg2d.add_vline`` draws a vertical line.

		``pyg2d.add_vline`` draws a vertical line from either the bottom axis
		to the top axis if ``ymin`` and ``ymax`` are not provided, otherwise
		it is drawn from ``ymin`` to ``ymax`` at ``x``.  Be careful not to
		change from linear to log scale AFTER using this function, as

		.. math::

			\log\left(0\\right)=-\infty

		and this means the line will extend past the extents of the latex page.

		.. todo::

			Fix the latex page extents problem with :math:`-\infty`

		:param float x:  The abscissa coordinate of the line.
		:param float ymin: The lower extent of the line.
		:param float ymax: The upper extent of the line.
		:param string ls: The style of the line, i.e. '-', '--', ':', etc.
		:param float lw: The width of the line in pt.
		:param string color: The color of the line.
		:param axes axes: The axes object the line should be added to, if not
			current.
		:return: None
		"""
		if axes is None:
			axes = self.ax
		if ymin == None:
			ymin = np.min(axes.get_ylim())
		if ymax == None:
			ymax = np.max(axes.get_ylim())
		if name is not None:
			self.add_to_legend(name=name, color=color, linestyle=ls)
		return axes.vlines(x, ymin, ymax, linestyles=ls, linewidths=lw,
						   color=color)

	def add_hline(self, y, xmin=None, xmax=None, ls='solid', lw=1.5,
				  color='black', axes=None):
		""" ``pyg2d.add_hline`` draws a horizontal line.

		``pyg2d.add_hline`` draws a horizontal line from either the left axis
		to the right axis if ``xmin`` and ``xmax`` are not provided, otherwise
		it is drawn from ``xmin`` to ``xmax`` at ``y``.  Be careful not to
		change from linear to log scale AFTER using this function, as

		.. math::

			\log\left(0\\right)=-\infty

		and this means the line will extend past the extents of the latex page.

		:param float y:  The ordinate axis coordinate of the line.
		:param float xmin: The left extent of the line.
		:param float xmax: The right extent of the line.
		:param string ls: The style of the line, i.e. '-', '--', ':', etc.
		:param float lw: The width of the line in pt.
		:param string color: The color of the line.
		:param axes axes: The axes object the line should be added to, if not
			current.
		:return: None
		"""
		if axes is None:
			axes = self.ax
		if xmin == None:
			xmin = np.min(axes.get_xlim())
		if xmax == None:
			xmax = np.max(axes.get_xlim())
		return axes.hlines(y, xmin=xmin, xmax=xmax, linestyle=ls,
							  linewidth=lw, color=color)

	def add_label(self, x, y, string, color='black'):
		curve_place = (x, y)
		ann = self.ax.annotate(string,
						 xy=curve_place,
						 xytext=curve_place, color=color)
		self.allartists.append(ann)

	def change_style(self, rcparamsarray):
		matplotlib.rcParams.update(rcparamsarray)

	def add_arrow(self, x1, x2, y1, y2, string='', axes=None, fc="0.5",
				  alpha=1.0, ha='center', va='center', arrowprops=None):
		if arrowprops is None:
			arrowprops = dict(arrowstyle="-|>", fc=fc, ec=fc, alpha=alpha)
		if axes is None:
			axes = self.ax
		ann = axes.annotate(string,
					  xy=(x2, y2),
					  xytext=(x1, y1),
					  color=fc, alpha=alpha,
					  horizontalalignment=ha,
					  verticalalignment=va,
					  arrowprops=arrowprops)
		self.allartists.append(ann)

	def add_text(self, x1, y1, string=None, ha='center', va='center',
				 color="#746C66", rotation=0, axes=None, fontsize=None):
		if axes is None:
			axes = self.ax
		if fontsize is not None:
			ann = axes.text(x1, y1, string, fontsize=fontsize, ha=ha, va=va, color=color,
					  rotation=rotation)
		else:
			ann = axes.text(x1, y1, string, ha=ha, va=va, color=color,
					  rotation=rotation)
		self.allartists.append(ann)

	def add_vmeasure(self, x1, y1, y2, string=None, place=None, offset=0.01,
					 axes=None, units='', log=False):
		if axes is None:
			axes = self.ax
		if string is None:
			string = r"$%.0f\,\mathrm{" % np.sqrt((y2 - y1)**2.0) + units + "}$"
		if place is None:
			place = "left"
		total_width = np.max(axes.get_xlim()) - np.min(axes.get_xlim())
		length = 0.05
		lw = 0.5
		h1 = self.add_hline(y1, x1 - offset * total_width,
					   x1 - offset * total_width - length * total_width,
					   lw=lw, axes=axes)
		h2 = self.add_hline(y2, x1 - offset * total_width,
					   x1 - offset * total_width - length * total_width,
					   lw=lw, axes=axes)
		if log:
			y_mid = np.sqrt(y2 * y1)
		else:
			y_mid = (y2 + y1) / 2.0
		x_mid = (x1 - offset * total_width +
				 x1 - offset * total_width - length * total_width) / 2.0
		h3 = self.add_arrow(x_mid, x_mid, y_mid, y1, string=self.latex_string(string), axes=axes)
		h4 = self.add_arrow(x_mid, x_mid, y_mid, y2, string=self.latex_string(string), axes=axes)
		self.allartists.append((h1, h2, h3, h4))

	def add_hmeasure(self, x1, x2, y1, string=None, place=None, offset=0.01,
					 axes=None, units='', log=False):
		if axes is None:
			axes = self.ax
		if string is None:
			string = r"$%.0f\,\mathrm{" % np.sqrt((x2 - x1)**2.0) + units + "}$"
		if place is None:
			place = "up"
		total_width = np.max(axes.get_ylim()) - np.min(axes.get_ylim())
		length = 0.05
		lw = 0.5
		h1 = self.add_vline(x1, y1 + offset * total_width,
					   y1 + offset * total_width + length * total_width,
					   lw=lw, axes=axes)
		h2 = self.add_vline(x2, y1 + offset * total_width,
					   y1 + offset * total_width + length * total_width,
					   lw=lw, axes=axes)
		if log:
			x_mid = np.sqrt(x1 * x2)
		else:
			x_mid = (x2 + x1) / 2.0
		y_mid = (y1 + offset * total_width +
				 y1 + offset * total_width + length * total_width) / 2.0
		h3 = self.add_arrow(x_mid, x1, y_mid, y_mid, string=self.latex_string(string), axes=axes)
		h4 = self.add_arrow(x_mid, x2, y_mid, y_mid, string=self.latex_string(string), axes=axes)
		self.allartists.append((h1, h2, h3, h4))

	def equal_aspect_ratio(self):
		self.ax.set_aspect('equal', 'datalim')

	@staticmethod
	def latex_string(string):
		try:
			power = int(re.search('(e([+-]?[0-9]+))', string).group(2))
			string = re.sub('e([+-]?[0-9]+)', (r'\times 10^{%d}' % power).encode('string-escape'), string)
		except AttributeError:
			pass
		return string

	def add_data_pointer(self, x, curve=None, point=None, string=None,
						 place='up-right', ha='left', axes=None, latex=True,
						 fc='0.3'):
		if axes is None:
			axes = self.ax
		if curve is not None:
			y = curve.at(x)
		elif point is not None:
			y = point
		else:
			raise Exception('No point for the arrow given in reference to ' +
							'data pointer.')
		if string is None:
			string = '$\left( %f,%f \\right)$' % (x, y)
		if place == 'up-right':
			curve_place = (4.0 * x / 3.0, 4.0 * y / 3.0)
		elif place == 'up-left':
			curve_place = (3.0 * x / 4.0, 4.0 * y / 3.0)
		elif place == 'down-right':
			curve_place = (4.0 * x / 3.0, 3.0 * y / 4.0)
		elif place == 'down-left':
			curve_place = (2.0 * x / 4.0, 3.0 * y / 4.0)
		elif type(place) is tuple:
			curve_place = place
		if latex:
			string = self.latex_string(string)
		ann = axes.annotate(string,
					  xy=(x, y),
					  xytext=curve_place,
					  ha=ha, color=fc,
					  arrowprops=dict(arrowstyle="fancy",
									  fc=fc, ec="none",
									  patchB=Ellipse((2, -1), 0.5, 0.5),
									  connectionstyle=
									  "angle3,angleA=0,angleB=-90")
					  )
		self.allartists.append(ann)

	def add_reg_line(self, x, y, regtype='lin', name='reg', xerr=None,
					 yerr=None, axes=None):
		if axes is None:
			axes = self.ax
		self.regnum = self.regnum + 1
		if name is 'reg':
			name = 'reg%d' % (self.regnum);
		# set up the error bounds
		if yerr is None:
			y_err_up = None
			y_err_down = None
		else:
			y_err_up = yerr[0, :]
			y_err_down = yerr[1, :]
			print y_err_up
			print y
		# determine the regression
		if regtype.isdigit():
			# determine the coefficients of degree regtype
			coeffs = np.polyfit(x,y,regtype);
			print coeffs
			# determine a fine grid of values
			x_fit = np.linspace(min(x),max(x),num=1000);
			y_fit = np.polyval(coeffs,x_fit);
			self.coeffs = coeffs;
			name = '$y\left( x \\right) = ';
			for i in range(0,int(regtype)):
				if coeffs[i] > 0:
					name += '+ %f' % (abs(coeffs[i]));
					if i > 0:
						name += 'x^{%d}' % (i);
				elif coeffs[i] < 0:
					name += '- %f' % (abs(coeffs[i]));
					if i > 0:
						name += 'x^{%d}' % (i);
			name += '$';
			print name;
		elif regtype is 'exp':
			x_np = np.array(x);
			x_err_np = np.array(xerr);
			y_np = np.array(y);
			y_err_np = np.array(yerr);
			def exp_func(B,x):
				return B[0]*np.exp(B[1]*x);

			exp_model = Model(exp_func);
			exp_data = RealData(x_np,y_np,sx=x_err_np,sy=y_err_np);
			odr = ODR(exp_data,exp_model,beta0=[0.,1.])
			out = odr.run();
			if out.res_var > 1.0 and out.beta[1] < 0.0:
				x_fit = np.linspace(min(x),max(x),num=1000);
				y_fit = exp_func(out.beta,x_fit);
				self.reg_string[name] = '$t_{wait} = e^{%.2f \cdot p} + %.2f$' % (out.beta[1],out.beta[0]);
				if out.sum_square < 20:
					y_err_up = exp_func(out.beta+out.sd_beta,x_fit);
					y_err_down = exp_func(out.beta-out.sd_beta,x_fit);
					if y_err_up[0] > 120:
						y_err_up = None;
						y_err_down = None;
				else:
					y_err_up = None;
					y_err_down = None;
					print "showing the exponential error will occlude data";
			else:
				y_fit = None;
				x_fit = None;
				y_err_up = None;
				y_err_down = None;
				print "the exponential does not fit to the data";
		elif regtype is 'log':
			print 'I haven\'t yet completed the log fitting!';
			#do something;
		elif regtype is 'gaussian':
			def gaus(x,a,x0,sigma):
				return a*exp(-(x-x0)**2/(2*sigma**2));
			pop,pcov = curve_fit(gaus,x,y,p0=[1,np.mean(y),np.std(y)]);
			x_fit = x_fit = np.linspace(min(x),max(x),num=1000);
			y_fit = gaus(x_fit);
		# plot the regression
		if x_fit is not None and y_fit is not None:
			self.x_fit = x_fit;
			self.y_fit = y_fit;
			lines = axes.plot(x_fit, y_fit, label=name, color='#A7A9AC',
							  ls='--')
			self.regs[name] = lines[0];
			# make sure these are lines
			lines[0].set_markersize(0);
			lines[0].set_lw(1.0);
		if y_err_up is not None and y_err_down is not None:
			uperrlines = plt.plot(x_fit,y_err_up,color='#D1D3D4',ls='--');
			downerrlines = plt.plot(x_fit,y_err_down,color='#D1D3D4',ls='--');
			axes.fill_between(x_fit,y_err_up,y_err_down,facecolor='#D1D3D4',alpha=0.5,lw=0.0);
			# add the regression to the dict of regressions

	def fill_under_curve(self, curve, scale=0., *args, **kwargs):
		if curve.data == 'binned':
			self.fill_between(curve.binned_data_x,
							  scale * np.ones_like(curve.binned_data_y),
							  curve.binned_data_y, **kwargs)
		else:
			self.fill_between(curve.x, scale * np.ones_like(curve.y), curve.y,
							  **kwargs)

	def fill_between(self, x, y1, y2=None, fc='red', name='plot', ec='None', leg=True,
					 axes=None, alpha=0.5, xmin=None, xmax=None, log=False):
		if axes is None:
			axes = self.ax
		self.plotnum = self.plotnum + 1
		if name is 'plot':
			name = 'plot%d' % (self.plotnum)
		p = axes.fill_between(x, y1, y2, facecolor=fc, alpha=alpha, edgecolor=ec, linewidth=0.001)
		self.allartists.append(p)
		if leg:
			patch = axes.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
								   facecolor=fc, alpha=alpha, label=name))
			self.bars[name] = patch


	def add_to_legend(self, name=None, line=True, color=None, linestyle=None,
					  alpha=1.0, axes=None):
		if axes is None:
			axes = self.ax
		if not line:
			patch = axes.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
								   color=color, alpha=alpha, label=name))
			self.bars[name] = patch
		else:
			line = axes.add_line(Line2D([0, 0], [0, 0],
								 color=color, alpha=alpha,
								 linestyle=linestyle, label=name))
			self.lines[name] = line

	def fill_betweenx(self, x1, x2, y, fc='red', name='plot', ec='None',
					  leg=True, axes=None, alpha=0.5):
		if axes is None:
			axes = self.ax;
		self.plotnum=self.plotnum+1;
		if name is 'plot':
			name = 'plot%d' % (self.plotnum);
		idx = np.argsort(x1);
		x1 = np.array(x1);
		x2 = np.array(x2);
		y = np.array(y);
		x1 = x1[idx];
		x2 = x2[idx];
		y = y[idx];
		p = axes.fill_betweenx(y,x1,x2,facecolor=fc,edgecolor=ec,alpha=alpha)
		self.allartists.append(p)


	def semi_log_y(self, axes=None):
		if axes is None:
			axes = self.ax
		axes.set_yscale('log', nonposy='mask')
		self.allartists.append('logy')

	def semi_log_x(self, axes=None):
		if axes is None:
			axes = self.ax
		axes.set_xscale('log', nonposx='mask')
		self.allartists.append('logx')

	def log_log(self):
		self.semi_log_x()
		self.semi_log_y()

	def add_circle(self, x, y, r, fc='red', ec='None', alpha=0.5, axes=None,
				   name='plot'):
		if axes is None:
			axes = self.ax
		self.plotnum = self.plotnum + 1
		if name is 'plot':
			name = 'plot%d' % (self.plotnum)
		patch = axes.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec,
							   alpha=alpha, label=name))
		self.bars[name] = patch
		self.allartists.append(patch)

	def add_line(self, x, y, name='plot', xerr=None, yerr=None, linewidth=0.5,
				 linestyle=None, linecolor='black', legend=True, axes=None,
				 error_fill=False):
		if axes is None:
			axes = self.ax
		self.data.extend([[x, y]])
		self.plotnum = self.plotnum + 1
		if name == 'plot':
			name = 'plot%d' % (self.plotnum)
		if linestyle is None:
			_ls = '-'
		else:
			_ls = linestyle
		if xerr is None and yerr is None:
			line = axes.plot(x, y, label=name, color=linecolor,
							 marker=self.marker[self.plotnum % 5],
							 ls=_ls, lw=linewidth, solid_capstyle='butt')
			for i in range(0, len(line)):
				self.lines[name + '%d' % (i)] = (line[i])
		else:

			if linecolor == 'black':
				ecolor = '#A7A9AC'
			else:
				col = Color(linecolor)
				col.saturation = 0.5
				col.luminance = 0.75
				ecolor = col.hex
			if not error_fill:
				line, caplines, barlinecols = axes.errorbar(x, y, label=name,
															color=linecolor,
															xerr=xerr,
															yerr=yerr,
															marker=self.marker[self.plotnum % 5],
															ls=_ls,
															ecolor=ecolor,
															lw=linewidth,
															clip_on=True)
				self.lines[name] = (line)
			else:
				self.add_line(x, y, xerr=None, yerr=None, name=name, linewidth=0.5,
							  linestyle=linestyle, linecolor=linecolor,
							  legend=legend, axes=axes)
				self.fill_between(x, np.array(y) - np.array(yerr),
								  np.array(y) + np.array(yerr), leg=False,
								  fc=linecolor, name=name + 'err')
				line = self.lines[name + '0']
		self.markers_on()
		self.lines_on()
		self.allartists.append(line)

	def add_line_yy(self, x, y, name='plot', xerr=None, yerr=None,
					linecolor='black', linewidth=0.5, linestyle=None,
					legend=True, axes=None):
		# make new axis
		if axes is None:
			self.ax2 = self.ax.twinx()
		else:
			self.ax2 = axes.twinx()
		line = self.add_line(x, y, name=name + 'yy', xerr=xerr, yerr=yerr,
					  linewidth=linewidth,
					  linecolor=linecolor,
					  linestyle=linestyle,
					  legend=legend, axes=self.ax2)
		self.allartists.append(line)
		if legend:
			self.add_line([0., 0.], [np.nan, np.nan], name=name, linewidth=linewidth,
						  linecolor=linecolor, linestyle=linestyle, axes=self.ax)

	def add_line_xx(self, x, y, name='plot', xerr=None, yerr=None,
					linecolor='black', linewidth=0.5, linestyle=None,
					legend=True):
		# make new axis
		self.ax2 = self.ax.twiny()
		line = self.add_line(x, y, name=name, xerr=xerr, yerr=yerr,
							   linewidth=linewidth,
							   linecolor=linecolor,
							   linestyle=linestyle,
							   legend=legend, axes=self.ax2)
		self.allartists.append(line)

	def add_xx(self,calfunc):
		self.ax2 = self.ax.twiny()
		mini = calfunc(np.min(self.ax.get_xlim()))
		maxi = calfunc(np.max(self.ax.get_xlim()))
		self.ax2.set_xlim(mini,maxi)
		self.ax2.get_xaxis().tick_top()
		self.allartists.append(self.ax2)

	def add_yy(self,calfunc):
		self.ax2 = self.ax.twinx();
		self.calfunc = calfunc;
		self.update_yy()
		self.allartists.append(self.ax2)

	def update_yy(self):
		mini = self.calfunc(np.min(self.ax.get_ylim()));
		maxi = self.calfunc(np.max(self.ax.get_ylim()));
		self.ax2.set_ylim(mini,maxi);
		self.ax2.get_yaxis().tick_right();

	def add_hist(self, y, bins, facecolor='gray', alpha=0.5, name='plot'):
		self.plotnum = self.plotnum + 1
		if name is 'plot':
			name = 'plot%d' % (self.plotnum)
		n, bins, patches = self.ax.hist(y, bins=bins, label=name,
									facecolor=facecolor, alpha=alpha,
									normed=False)
		self.bars[name] = patches
		self.allartists.append(self.bars[name])
		return n, bins

	def add_bar(self, x, y, hold=True, facecolor='gray', alpha=0.5,
				name='plot'):
		self.plotnum = self.plotnum + 1
		self.data.extend([[x, y]])
		if name is 'plot':
			name = 'plot%d' % (self.plotnum)
		delta = [j - i for i, j in zip(x[:-1], x[1:])]
		delta.append(delta[-1])
		# x = [j - (i/2) for i, j in zip(delta, x)];
		patches = self.ax.bar(x, y, width=delta, label=name, facecolor=facecolor,
						  alpha=alpha)
		self.bars[name] = patches
		self.allartists.append(self.bars[name])
		return x, y, delta

	def add_legend(self, axes=None):
		if axes is None:
			axes = self.ax
		self.leg = True
		leg = axes.legend()
		self.artists.append(leg)

	def det_height(self, ratio="golden"):
		if ratio is "golden":
			r = (1. + np.sqrt(5.)) / 2.
		elif ratio is "silver":
			r = 1. + np.sqrt(2.)
		elif ratio is "bronze":
			r = (3. + np.sqrt(13.)) / 2.
		elif ratio is "invgolden":
			r = 2. / (1. + np.sqrt(5.))
		elif ratio is "invsilver":
			r = 1. / (1. + np.sqrt(2.))
		elif ratio is "invbronze":
			r = 2. / (3. + np.sqrt(13.))
		else:
			r = float(ratio)
		if self.landscape:
			self.height = self.width / r
		else:
			self.height = self.width * r

	def remove_font_sizes(self,filename):
		f=open(filename,'r')
		fstring = "\\centering \n" + f.read()
		f.close()
		f=open(filename,'w')
		fstring=fstring.replace("\\rmfamily\\fontsize{8.328000}{9.993600}\\selectfont","\\scriptsize")
		fstring=fstring.replace("\\rmfamily\\fontsize{12.000000}{14.400000}\\selectfont","\\normalsize")
		fstring = filter(lambda x: x in string.printable, fstring);
		f.write(fstring)
		f.close()

	def add_math_jax(self, filename):
		f = open(filename, 'r')
		fstring = \
			"<script type=\"text/x-mathjax-config\">\n" + \
			"MathJax.Hub.Config({\n" + \
			"  tex2jax: {\n" + \
			"    inlineMath: [ ['$','$'], ['\\\\(','\\\\)'] ],\n" + \
			"  },\n" + \
			"  \"HTML-CSS\": {\n" + \
			"    linebreaks: {\n" + \
			"      automatic: true,\n" + \
			"      width: \"80% container\",\n" + \
			"    }\n" + \
			"  },\n" + \
			"  SVG: {\n" + \
			"    linebreaks: {\n" + \
			"      automatic: true,\n" + \
			"      width: \"80% container\",\n" + \
			"    }\n" + \
			"  },\n" + \
			"  TeX: {\n" + \
			"    equationNumbers: {\n" + \
			"      autoNumber: \"all\"\n" + \
			"    },\n" + \
			"  },\n" + \
			"    showMathMenu: false\n" + \
			"});\n" + \
			"\n" + \
			"</script>\n" + \
			"\n" + \
			"<script type=\"text/javascript\"" + \
			"     src=\"http://cdn.mathjax.org/mathjax/latest/MathJax.js?" + \
			"config=TeX-AMS-MML_HTMLorMML\">" + \
			"</script>" + f.read()
		f.close()
		f = open(filename, 'w')
		f.write(fstring)
		f.close()


	def long_name(self):
		self.leg_col_one_col = 1
		self.leg_col_two_col = 1
		self.leg_col_full_page = 1

	def set_size(self, size, sizeofsizes, customsize=None, legloc=None,
				 tight=True, ratio="golden", width=None):
		#global __context__.val
		if __context__.val == "writeup":
			widths = {"1": 3.25, "2": 6.25, "4": 12.50, "fp": 10.0, "cs": 0.0}
		elif __context__.val == "tufte":
			widths = {"1": 2.00, "2": 4.30, "4": 6.30, "fp": 10.0, "cs": 0.0}
		elif __context__.val == "thesis":
			widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
		else:
			widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
		if width is None:
			self.width = widths[size]
		elif isinstance(width, basestring):
			self.width = widths[width]
		else:
			self.width = width
		if size is '1':
			self.det_height(ratio=ratio)
		elif size is '2':
			self.det_height(ratio=ratio)
			self.fig.set_size_inches(self.width, self.height)
		elif size is '4':
			self.det_height(ratio=ratio)
			self.fig.set_size_inches(self.width, self.height)
		elif size is 'fp':
			self.width=10;
			self.det_height();
			self.fig.set_size_inches(self.width,self.height);
			if self.leg:
				self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
							   ncol=self.leg_col_full_page, mode="expand",
							   borderaxespad=0.);
		elif size is 'cs':
			if customsize is not None:
				self.width=customsize[0];
				self.height=customsize[1];
				if legloc is not None:
					self.ax.legend(loc=legloc,ncol=2);
		self.fig.set_size_inches(self.width, self.height)
		if tight:
			plt.tight_layout()

	def export_fmt(self, filename, size, sizeofsizes, format):
		if sizeofsizes == 1:
			size = 'none'
		if format is 'png':
			add = '.png'
		elif format is 'pgf':
			add = '.pgf'
		elif format is 'pdf':
			add = '.pdf'
		elif format is 'svg':
			# save as pdf, then pdf2svg
			if not os.path.isfile(filename + self.sizestring[size] + '.svg') \
				or self.force_export or __force__.val:
				self.fig.savefig(filename + self.sizestring[size] + '.pdf',
							bbox_extra_artists=self.artists, bbox_inches='tight',
							transparent=True, dpi=1200)
				os.system('pdf2svg ' + filename + self.sizestring[size] + '.pdf ' +
						  filename + self.sizestring[size] + '.svg')
				os.remove(filename + self.sizestring[size] + '.pdf')
			self.svg_filename = filename + self.sizestring[size] + '.svg'
		elif format is 'websvg':
			add = 'web.svg'
			self.svg_filename = filename + self.sizestring[size] + add
		if (format is not 'svg') and (format is not 'html'):
			if not os.path.isfile(filename + self.sizestring[size] + add) \
				or self.force_export or __force__.val:
				self.fig.savefig(filename + self.sizestring[size] + add,
							bbox_extra_artists=self.artists, bbox_inches='tight',
							transparent=True)
		if format is 'html':
			add = '.html'
			import mpld3
			from mpld3 import plugins
			import plotly.plotly as py
			import plotly.tools as tls
			import plotly.offline as offline
			from plotly.offline.offline import _plot_html
			plotly_fig = tls.mpl_to_plotly(self.fig)
			plot_file = offline.plot(plotly_fig)
			js_string = '<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG"></script>'
			self.html_filename = filename + add
			os.system('cp temp-plot.html ' + filename + add)
			scriptstring = \
				"MathJax.Hub.Config({\n" + \
				"  tex2jax: {\n" + \
				r"    inlineMath: [ ['$','$'], ['\\(','\\)'] ]," + "\n" + \
				"  }\n" + \
				"});\n"
			from bs4 import BeautifulSoup as bs
			with open(filename + add, 'r') as f:
				soup = bs(f.read(), "lxml")
				title = soup.find('meta')
				script = soup.new_tag('script')
				script2 = soup.new_tag('script')
				script['type'] = "text/javascript"
				script['src'] = "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG"
				script2['type'] = "text/x-mathjax-config"
				script2.append(scriptstring)
				# script['src'] = "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG"
				title.insert_after(script2)
				script2.insert_after(script)
			with open(filename + '2' + add, 'wb') as f:
				f.write(soup.prettify('utf-8'))
			os.system("cp " + filename + "2" + add + " " + filename + add)
		if format is 'pgf':
			self.remove_font_sizes(filename + self.sizestring[size] + add)
			self.pgf_filename = filename + self.sizestring[size] + add

	def show(self, caption='', label=None, scale=None, interactive=False,
			 need_string=False):
		if label is not None and not self.loaded:
			plt.ioff()
			pickle.dump(self, file(os.path.expanduser('~') +
									'/.pyg/%s.pickle' % label, 'w'))
		fig = None
		if label is None:
			label = str([''.join(ch for ch in caption if ch.isalnum())])
		self.label = label
		if scale is None and lyx.run_from_ipython() and not lyx.need_latex():
			scale = 2.0
		elif scale is None:
			scale = 1.0
		if caption is not None:
			self.caption = caption
		if interactive:
			plt.ion()
			plt.show(block=True)
		elif not lyx.need_latex():
			__counter__ = random.randint(0, 2e9)
			fig_width = self.fig.get_figwidth() * self.fig.dpi * scale
			fig_html = r"""
				<div class='pygfigure' name='%s' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%%; width:%fpx; height: auto;' src='%s?%d' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure %d:</b> %s</div>
				</div>
			""" % (label, fig_width, self.svg_filename, __counter__, bi.__figcount__, self.caption)
			__figures__.val[label] = bi.__figcount__
			bi.__figcount__ += 1
			fig = HTML(fig_html)
			self.close()
			if need_string:
				return fig_html
		elif lyx.need_latex():
			if self.force_pdf:
				include_line = '\includegraphics{%s}' % self.pdf_filename
			else:
				include_line = '\input{%s}' % (self.pgf_filename)
			if __context__.val == 'tufte' and self.width > 5.0:
				figfloat = 'figure*'
				centering = ''
			elif __context__.val == 'tufte' and self.width < 4:
				figfloat = 'marginfigure'
				centering = ''
			else:
				figfloat = 'figure'
				centering = r'\centering'
			strlatex = r"""
				\begin{%s}
					%s
					%s
					\caption{%s\label{fig:%s}}
				\end{%s}""" % (figfloat, centering, include_line, self.caption,
							   self.label, figfloat)
			__figures__.val[label] = bi.__figcount__
			bi.__figcount__ += 1
			fig = Latex(strlatex)
			self.close()
			if need_string:
				return strlatex
		else:
			if self.pdf_filename is not None:
				if platform.system() == "Darwin":
					os.system("open -a Preview " + self.pdf_filename)
				if platform.system() == "Linux":
					os.system("evince " + self.pdf_filename + " &")
			if self.html_filename is not None:
				os.system("google-chrome " + self.html_filename + " &")
		display(fig)

	def export(self, filename, sizes=None, formats=None,
			   customsize=None, legloc=None, tight=True, ratio="golden",
			   width=None, caption='', force_pdf=False, force=False):
		self.force_pdf = force_pdf
		self.force_export = force
		self.caption = caption
		#global __context__.val
		if sizes is None:
			if __context__.val == "writeup":
				sizes = ['1']
			elif __context__.val == "thesis":
				sizes = ['2']
			if lyx.run_from_ipython():
				sizes = ['2']
		for size in sizes:
			if formats is None:
				if lyx.run_from_ipython():
					formats = ['svg']
					if lyx.need_latex() and not force_pdf:
						formats = ['pgf']
					elif lyx.need_latex() and force_pdf:
						formats = ['pdf']
				else:
					formats = ['pdf']
			for format in formats:
				if format == 'html':
					tight = False
				self.set_size(size, len(sizes), customsize=customsize,
							  legloc=legloc, tight=tight, ratio=ratio,
							  width=width)
				self.export_fmt(filename, size, len(sizes), format)
				if format == 'pdf':
					self.pdf_filename = filename + '.pdf'
				elif format == 'pgf':
					self.pgf_filename = filename + '.pgf'
				elif format == 'png':
					self.png_filename = filename + '.png'

	def close(self):
		plt.close(self.fig)

	def add_metadata(self, filename):
		os.system("setfattr -n user.creation_script -v \'%s\' %s" % (__file__, filename))
		os.system("setfattr -n user.creation_date -v \'%s\' %s" % (time.strftime("%d/%m/%Y"), filename))

	def publish_to(self, directory):
		if directory not in bi.__exported_files__:
			bi.__exported_files__[directory] = []
		if hasattr(self, 'pgf_filename'):
			self.add_metadata(self.pgf_filename)
			shutil.copy(self.pgf_filename, directory)
			bi.__exported_files__[directory].extend([os.path.basename(self.pgf_filename)])
		if hasattr(self, 'pdf_filename'):
			self.add_metadata(self.pdf_filename)
			shutil.copy(self.pdf_filename, directory)
			bi.__exported_files__[directory].extend([os.path.basename(self.pdf_filename)])
		if hasattr(self, 'png_filename'):
			self.add_metadata(self.png_filename)
			shutil.copy(self.png_filename, directory)
			bi.__exported_files__[directory].extend([os.path.basename(self.png_filename)])

def commit_publications(message='automated commit'):
	for key, val in bi.__exported_files__.iteritems():
		os.chdir(key)
		for filename in val:
			os.system('git add %s' % filename)
		os.system('git commit -am "%s"' % message)
