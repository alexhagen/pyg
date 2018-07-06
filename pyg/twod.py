from __future__ import print_function
import os
import psgv.psgv as psgv
__context__ = psgv.psgv('__context__')
__context__.val = 'writeup'
def context(ctx='writeup'):
    __context__.val = ctx
import matplotlib
if False:#bi.is_interactive():
    #print 'using interactive backend'
    matplotlib.use('Qt5Agg', warn=False)
else:
    #print 'using non interactive backend'
    if "DISPLAY" not in os.environ.keys():
        matplotlib.use('Agg', warn=False)
    else:
        matplotlib.use('pgf', warn=False)

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
import matplotlib
import string
import gc
from colour import Color
import numpy as np
import platform
import shutil
import time
from copy import copy
import subprocess
import sys
import random
import weakref
import re
import __builtins__ as bi
#import builtins as bi
from lyxithea import lyxithea as lyx
from itertools import count

import pickle
import os.path
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

if lyx.run_from_ipython():
    from IPython.display import SVG, display, Latex, HTML, display_latex


__figures__ = psgv.psgv('__lyxfigures__')
__figures__.val = {}
__force__ = psgv.psgv('__pygforce__')
__force__.val = False

def metal_dim(ratio='golden'):
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
    elif ratio is 'square':
        r = 1.0
    return r

def w(width):
    if __context__.val == "writeup":
        widths = {"1": 3.25, "2": 6.25, "4": 12.50, "fp": 10.0, "cs": 0.0}
    elif __context__.val == "tufte":
        widths = {"1": 2.00, "2": 4.30, "4": 6.30, "fp": 10.0, "cs": 0.0}
    elif __context__.val == "thesis":
        widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
    else:
        widths = {"1": 3.0, "2": 6.0, "4": 12.00, "fp": 9.0, "cs": 0.0}
    return widths[width]

def res(w=1080., ratio='golden'):
    h = w * metal_dim(ratio)
    return (h, w)

plt.close("all")
preamble = [
            r"\usepackage{fontspec}",
            r"\setmainfont{AvenirLTStd-Light.otf}",
            r"\setsansfont{AvenirLTStd-Light.otf}",
            r'\usepackage{nicefrac}',
            r'\usepackage{gensymb}',
            r'\usepackage{xcolor}',
            r'\definecolor{grey60}{HTML}{746C66}',
            r'\definecolor{grey40}{HTML}{A7A9AC}',
            r'\usepackage{amsmath, amssymb}',
            r'\usepackage{stackrel}',
            r'\providecommand{\unit}[1]{\ensuremath{' +
            r'{\mathrm{#1}}}}'
           ]

def force(val=True):
    __force__.val = val


def load(fname, svg=False):
    _fig = pickle.load(file(os.path.expanduser('~') +
                            '/.pyg/%s.pickle' % fname))
    if not svg:
        _fig.set_rcparams('plot')
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
        from sys import platform
        import os
        if platform == "darwin":
            self.filename = os.path.abspath(filename)
            self.show_filename = filename
        else:
            self.filename = filename
            self.show_filename = filename
        self.loaded = False

    @staticmethod
    def get_width(fname):
        from sys import platform
        if platform == "linux" or platform == "linux2":
            command = 'inkscape'
        elif platform == "darwin":
            command = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
        elif platform == "win32":
            pass
        if 'png' in fname:
            cmd = 'identify -format "%%[w]" %s' % fname
        else:
            cmd = '%s --without-gui --query-width %s' % (command, fname)
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        (out, err) = p.communicate()
        try:
            width = float(out)
        except ValueError:
            print (out)
            print (err)
        return width

    @staticmethod
    def get_height(fname):
        from sys import platform
        if platform == "linux" or platform == "linux2":
            command = 'inkscape'
        elif platform == "darwin":
            command = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
        elif platform == "win32":
            pass
        if 'png' in fname:
            cmd = 'identify -format "%%[w]" %s' % fname
        else:
            cmd = '%s --without-gui --query-width %s' % (command, fname)
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        (out, err) = p.communicate()
        try:
            height = float(out)
        except ValueError:
            print (out)
            print (err)
        return height

    def show(self, caption='', label=None, scale=None, width=None,
             convert=True, need_string=False, bbox=None, sideways=False,
             only_graphic=False, scalef=1.0, here_definitely=False,
             **kwargs):
        """Show an SVG as a figure or just as a picture

        :param str caption: Caption to go under the figure
        :param str label: Label to cross reference the figure
        :param float scale: Ratio to scale the figure - useful in HTML contexts
        :param width: Width in inches, or a string defining the number of
            columns to span: ``'1'``, ``'2'``, or ``'fp'`` (full page)
        :param bool convert: Whether to convert to PDF from SVG - default
            ``True``
        """
        from sys import platform
        if platform == "linux" or platform == "linux2":
            command = 'inkscape'
        elif platform == "darwin":
            command = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
        elif platform == "win32":
            pass
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
            """ % (label, fig_width, self.show_filename, __counter__, label, bi.__figcount__, caption)
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
                os.system('{command} --without-gui -f {svg_filename} -A {pdf_filename}'.format(command=command, pdf_filename=pdf_filename, svg_filename=svg_filename))
                #os.system('rsvg-convert -f pdf -o {pdf_filename} {svg_filename}'.format(pdf_filename=pdf_filename, svg_filename=svg_filename))
            if sideways:
                env = 'sidewaysfigure'
            else:
                env = 'figure'
            if not only_graphic:
                if here_definitely:
                    pos = '[H]'
                else:
                    pos = ''
                strlatex = r"""
                \begin{%s}%s
                    \centering
                    \includegraphics[width=%.2fin]{%s}
                    \caption{%s\label{fig:%s}}
                \end{%s}""" % (env, pos,
                               scalef * fig_width, pdf_filename,
                               caption, label,
                               env)
            else:
                strlatex = r"""
                    \includegraphics[width=%.2fin]{%s}
                """ % (scalef * fig_width, pdf_filename)
            __figures__.val[label] = bi.__figcount__
            bi.__figcount__ += 1
            fig = Latex(strlatex)
            if need_string:
                return strlatex
        display(fig)

def svg_show(filename, caption='', label=None, scale=None, width=None,
             convert=True, need_string=False, sideways=False, **kwargs):
    _svg = svg(filename)
    return _svg.show(caption=caption, label=label, scale=scale, width=width,
                     convert=convert, need_string=need_string,
                     sideways=sideways, **kwargs)


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
        self.__counter__ = next(self._figcount)
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
        self.set_rcparams(env)

    def set_rcparams(self, env):
        if env is 'gui':
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
        else:
            fsize = 10
            mathfont = 'cm'
            labelsize='medium'
            if 'bruce' in env:
                preamble.append(r'\usepackage{sansmath}')
                preamble.append(r'\sansmath')
                preamble.append(r'\usepackage{helvet}')
                fsize = 12
                labelsize='large'
                mathfont = 'stixsans'
            self.rcparamsarray = {
                "font.sans-serif": "Helvetica",
                "font.family": "sans-serif",
                "mathtext.fontset": mathfont,
                "font.size": fsize,
                "axes.linewidth": 0.5,
                "axes.edgecolor": "#000000",
                "xtick.major.width": 0.25,
                "xtick.major.size": 2,
                "xtick.direction": "in",
                "xtick.minor.width": 0.125,
                "xtick.color": "#000000",
                "ytick.major.width": 0.25,
                "ytick.major.size": 2,
                "ytick.minor.width": 0.125,
                "ytick.color": "#000000",
                "ytick.direction": "in",
                "text.color": "#000000",
                "axes.facecolor": "none",
                "figure.facecolor": "none",
                "axes.labelcolor": "#000000",
                "xtick.labelsize": "small",
                "ytick.labelsize": "small",
                "axes.labelsize": labelsize,
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
                "text.latex.preamble": preamble,
                "pgf.texsystem": "lualatex",
                "pgf.rcfonts": False
            }
            if __context__.val == 'pres':
                self.rcparamsarray["font.size"] = 14.0
        matplotlib.rcParams.update(self.rcparamsarray)

    def add_to_preamble(self, line):
        preamble = self.rcparamsarray['pgf.preamble']
        preamble += '\n' + line + '\n'
        self.rcparamsarray['pgf.preamble'] = preamble
        self.rcparamsarray['text.latex.preamble'] = preamble
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

    def xticks(self, ticks, labels, axes=None, rotation='horizontal'):
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
        axes.set_xticklabels(labels, rotation=rotation)
        if rotation is 'vertical':
            plt.margins(0.2)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.15)

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

    def markers_on(self, markersize=1, alpha=1.0):
        """ ``pyg2d.markers_on`` turns on the data markers for all data sets.

        :return: None
        """
        for key in self.lines:
            self.lines[key].set_alpha(alpha)
            self.lines[key].set_markersize(markersize)

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
        """``pyg2d.add_hline`` draws a horizontal line.

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
                  alpha=1.0, ha='center', va='center', arrowprops=None,
                  rotation=0):
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
                      rotation=rotation,
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

    def add_detail_circ(self, x, y, r, string, r2=None, fc='0.5', axes=None):
        if axes is None:
            axes = self.ax
        if r2 is None:
            r1 = r
            r2 = r
        else:
            r1 = r
        ha='left'
        # add one arrow from left around to right
        axes.annotate('',
                      xy=(x, y + r2), xycoords='data',
                      xytext=(x - r1, y), textcoords='data',
                      arrowprops=dict(arrowstyle='-', fc=fc, ec=fc,
                                      connectionstyle="angle, angleA=-90, angleB=180, rad=%f" % (1.)))
        axes.annotate(string,
                      xy=(x, y + r2), xycoords='data',
                      xytext=(x + r1, y), textcoords='data', color=fc,
                      horizontalalignment=ha,
                      arrowprops=dict(arrowstyle='<|-', fc=fc, ec=fc,
                                      connectionstyle="angle, angleA=90, angleB=180, rad=%f" % (1.)))
        # add another arrow from right around to bottom
        axes.annotate(string,
                      xy=(x, y - r2), xycoords='data',
                      xytext=(x + r1, y), textcoords='data', color=fc,
                      horizontalalignment=ha,
                      arrowprops=dict(arrowstyle='<|-', fc=fc, ec=fc,
                                      connectionstyle="angle, angleA=-90, angleB=180, rad=%f" % (1.)))
        axes.annotate('',
                      xy=(x, y - r2), xycoords='data',
                      xytext=(x - r1, y), textcoords='data',
                      arrowprops=dict(arrowstyle='-', fc=fc, ec=fc,
                                      connectionstyle="angle, angleA=90, angleB=180, rad=%f" % (1.)))

    def add_hmeasure(self, x1, x2, y1, string=None, place=None, offset=0.01,
                     axes=None, units='', log=False, rotation=0):
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
        h3 = self.add_arrow(x_mid, x1, y_mid, y_mid, string=self.latex_string(string), axes=axes, rotation=rotation)
        h4 = self.add_arrow(x_mid, x2, y_mid, y_mid, string=self.latex_string(string), axes=axes, rotation=rotation)
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
                         fc='0.3', rel_place=False):
        if isinstance(x, int):
            x = float(x)
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
            ha = 'left'
        elif place == 'up-left':
            curve_place = (3.0 * x / 4.0, 4.0 * y / 3.0)
            ha = 'right'
        elif place == 'down-right':
            curve_place = (4.0 * x / 3.0, 3.0 * y / 4.0)
            ha = 'left'
        elif place == 'down-left':
            curve_place = (2.0 * x / 4.0, 3.0 * y / 4.0)
            ha = 'right'
        elif type(place) is tuple:
            if rel_place:
                curve_place = (x + place[0], y + place[1])
            else:
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


    def callout(self, x, curve=None, point=None, string=None, place='up-right',
                    ha='left', axes=None, latex=True, fc='0.3'):
        if axes is None:
            axes = self.ax
        if point is None:
            y = curve.at(x)
        else:
            y = point
        if string is None:
            string = curve.name
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
                      arrowprops=dict(arrowstyle='-', fc=fc, ec=fc,
                                      connectionstyle="arc, rad=0, angleA=90")
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
            print (y_err_up)
            print (y)
        # determine the regression
        if regtype.isdigit():
            # determine the coefficients of degree regtype
            coeffs = np.polyfit(x,y,regtype);
            print (coeffs)
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
            print (name)
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
                    print ("showing the exponential error will occlude data")
            else:
                y_fit = None;
                x_fit = None;
                y_err_up = None;
                y_err_down = None;
                print ("the exponential does not fit to the data")
        elif regtype is 'log':
            print ('I haven\'t yet completed the log fitting!')
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

    def contour(self, X, Y, Z, cmap, levels=25):
        self.cmin = np.nanmin(Z)
        self.cmax = np.nanmax(Z)
        levels = np.linspace(self.cmin, self.cmax, levels)
        self.cmap = cmap
        plt.contourf(X, Y, Z, levels=levels, cmap=self.cmap)
        return self

    def colorbar(self):
        self.cax = self.fig.add_axes([0.95, 0.05, 0.04, 0.9])
        self.cax.set_position([1.02, 0., 0.04, 1.0])
        norm = matplotlib.colors.Normalize(vmin=self.cmax,
                                           vmax=self.cmin)
        self.cb = matplotlib.colorbar.ColorbarBase(self.cax, cmap=self.cmap,
                                                   norm=norm)
        return self

    def clabel(self, label):
        self.ylabel(label, axes=self.cax)
        return self

    def fill_under_curve(self, curve, scale=0., *args, **kwargs):
        if curve.data == 'binned':
            if curve.binned_data_x is None:
                curve.prepare_binned_data()
            self.fill_between(curve.binned_data_x,
                              scale * np.ones_like(curve.binned_data_y),
                              curve.binned_data_y, name=curve.name,
                              **kwargs)
        else:
            self.fill_between(curve.x, scale * np.ones_like(curve.y), curve.y,
                              name=curve.name, **kwargs)
        return self

    def fill_between(self, x, y1, y2=None, fc='red', name='plot', ec='None', leg=True,
                     axes=None, alpha=0.5, xmin=None, xmax=None, log=False,
                     hatch=None, **kwargs):
        if axes is None:
            axes = self.ax
        self.plotnum = self.plotnum + 1
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        if hatch is None:
            if ec is not 'None' and ec is not None:
                lw = 0.5
            else:
                lw = 0.001
            mask = [np.isfinite(_y1) and np.isfinite(_y2) for _y1, _y2 in zip(y1, y2)]
            x = [float(_x) for _x in x[mask]]
            y1 = [float(_y1) for _y1 in y1[mask]]
            y2 = [float(_y2) for _y2 in y2[mask]]
            p = axes.fill_between(x, y1, y2, facecolor=fc, alpha=alpha,
                                  edgecolor=ec, linewidth=lw)
            self.allartists.append(p)
        else:
            _xb = x[-1::-1]
            _x = np.append(x, _xb)
            _x = np.append(_x, [x[0]])
            _y = np.append(y2, y1)
            _y = np.append(_y, [y2[0]])
            if ec is not None:
                kwargs['ec'] = ec
            patch = Polygon([[__x, __y] for __x, __y in zip(_x, _y)],
                            closed=True, fill=False, hatch=hatch,
                            **kwargs)
            p = axes.add_patch(patch)
        if leg:
            patch = axes.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
                                   facecolor=fc, alpha=alpha, label=name))
            self.bars[name] = patch
        return self


    def add_to_legend(self, name=None, line=True, color=None, linestyle=None,
                      linewidth=0.5, alpha=1.0, axes=None):
        if axes is None:
            axes = self.ax
        if not line:
            patch = axes.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
                                   color=color, alpha=alpha, label=name))
            self.bars[name] = patch
        else:
            line = axes.add_line(Line2D([0, 0], [0, 0],
                                 color=color, alpha=alpha,
                                 linestyle=linestyle, linewidth=linewidth,
                                 label=name))
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

    def stackplot(self, x, y, baseline='zero', axes=None, name='stackplot',
                  **kwargs):
        if axes is None:
            axes = self.ax
        self.plotnum = self.plotnum + 1
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        stack = axes.stackplot(x, y, baseline=baseline, **kwargs)

    def add_line(self, x, y, name='plot', xerr=None, yerr=None, linewidth=0.5,
                 linestyle=None, linecolor='black', markerstyle=None, legend=True, axes=None,
                 alpha=1.0, error_fill=False, asymerr=False, differr=True,
                 markevery=None, **kwargs):
        if axes is None:
            axes = self.ax
        self.data.extend([[x, y]])
        self.plotnum = self.plotnum + 1
        if markerstyle is None:
            markerstyle = self.marker[self.plotnum % 5]
        if name == 'plot':
            name = 'plot%d' % (self.plotnum)
        if linestyle is None:
            _ls = '-'
        else:
            _ls = linestyle
        if xerr is None and yerr is None:
            line = axes.plot(x, y, label=name, color=linecolor, alpha=alpha,
                             marker=markerstyle,
                             ls=_ls, lw=linewidth, solid_capstyle='butt',
                             markevery=markevery, **kwargs)
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
                                                            alpha=alpha,
                                                            marker=markerstyle,
                                                            ls=_ls,
                                                            ecolor=ecolor,
                                                            lw=linewidth,
                                                            clip_on=True,
                                                            markevery=markevery)
                self.lines[name] = (line)
            else:
                self.add_line(x, y, xerr=None, yerr=None, name=name,
                              linewidth=0.5, linestyle=linestyle,
                              linecolor=linecolor, markerstyle=markerstyle,
                              alpha=alpha, legend=legend, axes=axes,
                              markevery=markevery, **kwargs)
                if asymerr:
                    if differr:
                        yerr1 = yerr[:, 0]
                        yerr2 = yerr[:, 1]
                    else:
                        yerr1 = y - yerr[:, 0]
                        yerr2 = yerr[:, 1] - y
                else:
                    yerr1 = yerr
                    yerr2 = yerr
                self.fill_between(x, np.array(y) - np.array(yerr1),
                                  np.array(y) + np.array(yerr2), leg=False,
                                  fc=linecolor, name=name + 'err')
                line = self.lines[name + '0']
        self.markers_on()
        self.lines_on()
        self.allartists.append(line)

    def y_axis_off(self):
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def surf(self, x, y, tri, vector=False):
        """Create a surface plot on a two-d chart.
        """
        if vector:
            triangles = tri.get_masked_triangles()
            for _t in triangles:
                self.add_line(x[_t], y[_t])
        else:
            pass
        return self

    def add_line_yy(self, x, y, name='plot', xerr=None, yerr=None,
                    linecolor='black', linewidth=0.5, linestyle=None,
                    legend=True, alpha=1.0, axes=None, markerstyle=None,
                    **kwargs):
        # make new axis
        if axes is None:
            self.ax2 = self.ax.twinx()
        else:
            self.ax2 = axes.twinx()
        line = self.add_line(x, y, name=name + 'yy', xerr=xerr, yerr=yerr,
                             linewidth=linewidth,
                             linecolor=linecolor,
                             linestyle=linestyle,
                             legend=legend, alpha=alpha, axes=self.ax2,
                             markerstyle=markerstyle, **kwargs)
        self.allartists.append(line)
        if legend:
            self.add_line([0., 0.], [np.nan, np.nan], name=name,
                          linewidth=linewidth, linecolor=linecolor,
                          linestyle=linestyle, axes=self.ax,
                          markerstyle=markerstyle, **kwargs)

    def add_line_xx(self, x, y, name='plot', xerr=None, yerr=None,
                    linecolor='black', linewidth=0.5, linestyle=None,
                    legend=True, axes=None, markerstyle=None, **kwargs):
        # make new axis
        if axes is None:
            self.ax2 = self.ax.twiny()
        else:
            self.ax2 = axes.twiny()
        line = self.add_line(x, y, name=name, xerr=xerr, yerr=yerr,
                             linewidth=linewidth,
                             linecolor=linecolor,
                             linestyle=linestyle,
                             legend=legend, axes=self.ax2,
                             markerstyle=markerstyle, **kwargs)
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
        r = metal_dim(ratio)
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

    def set_size(self, size, sizeofsizes=1, customsize=None, legloc=None,
                 tight=True, ratio="golden", width=None):
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
            self.width = 10
            self.det_height()
            self.fig.set_size_inches(self.width, self.height)
            if self.leg:
                self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                               ncol=self.leg_col_full_page, mode="expand",
                               borderaxespad=0.)
        elif size is 'cs':
            if customsize is not None:
                self.width = customsize[0]
                self.height = customsize[1]
                if legloc is not None:
                    self.ax.legend(loc=legloc, ncol=2)
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
             need_string=False, span_columns=False, just_graphics=False,
             here_definitely=False):
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
            return self
        elif not lyx.need_latex():
            try:
                use_filename = self.svg_filename
            except AttributeError:
                use_filename = self.png_filename
            __counter__ = random.randint(0, 2e9)
            fig_width = self.fig.get_figwidth() * self.fig.dpi * scale
            fig_html = r"""
                <div class='pygfigure' name='%s' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
                    <img style='margin: auto; max-width:100%%; width:%fpx; height: auto;' src='%s?%d' />
                    <div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure %d:</b> %s</div>
                </div>
            """ % (label, fig_width, use_filename, __counter__, bi.__figcount__, self.caption)
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
                if span_columns:
                    figfloat = 'figure*'
                else:
                    figfloat = 'figure'
                centering = r'\centering'
            if here_definitely:
                pos = '[H]'
            else:
                pos = ''
            if just_graphics:
                strlatex = include_line
            else:
                strlatex = r"""
                    \begin{%s}%s
                        %s
                        %s
                        \caption{%s\label{fig:%s}}
                    \end{%s}""" % (figfloat, pos, centering, include_line,
                                   self.caption, self.label, figfloat)
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
               width=None, caption='', force_pdf=False, force=False,
               context=None):
        self.force_pdf = force_pdf
        self.force_export = force
        self.caption = caption
        '''ticks_font = 'Helvetica'
        for label in ax.get_xticklabels():
            label.set_fontproperties(ticks_font)

        for label in ax.get_yticklabels():
            label.set_fontproperties(ticks_font)'''
        #global __context__.val
        if context is not None:
            __context__.val = context
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

plot = pyg2d()
plt.cla()
plt.clf()
plt.close()
plot.fig.clear()
plt.close(plot.fig)
plot.close()
del plot.fig
del plot
plt.close()
gc.collect(2)
