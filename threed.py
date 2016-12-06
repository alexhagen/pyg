from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
import matplotlib
import string
import os
from colour import Color
import numpy as np
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import platform

plt.close("all")


# make the line graphing class
class pyg3d(object):
    """ A ``pyg.pyg3d`` object plots many three-dimensional data types.

    The ``pyg3d`` class provides an access to ``matplotlib`` charting functions
    and some hook ins to making these functions easier to use and more
    repeatable.  The constructor itself takes only one optional argument,
    ``env``.

    :param str env: The environement option defines where you are going to use
        the generated plot, with the default option being plot (or printing).
        If you are using this to generate plots for a gui, define this option
        as ``gui`` and the class will choose a prettier parameter set for your
        chart. Default: ``plot``.
    :type env: ``plot``, ``gui``, or ``None``
    :return: the ``pyg3d`` object.
    :rtype: ``pyg3d``
    """
    leg_col_one_col = 2
    leg_col_two_col = 3
    leg_col_full_page = 4
    marker = {0: '+',
              1: '.',
              2: '1',
              3: '1',
              4: '2',
              5: '3',
              6: '4'}
    linestyle = {0: '-',
                 1: '--',
                 2: '-.',
                 3: ':'}
    sizestring = {'1': 'onecolumn',
                  '2': 'twocolumn',
                  'fp': 'fullpage',
                  'cs': 'customsize',
                  'none': ''}

    def __init__(self, env='plot', colors='purdue'):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax_subp = []
        self.leg = False
        self.ax2 = None
        #self.ax.get_xaxis().tick_bottom()
        #self.ax.get_yaxis().tick_left()
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
        if colors is 'purdue' or colors is 'pu':
            import pyg.colors.pu as color
            self.colors = color.pu_colors
        else:
            import pyg.colors.pu as color
            self.colors = color.pu_colors
        if env is 'plot':
            rcparamsarray = {
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
                "pgf.preamble": "\usepackage{nicefrac}"
            }
        elif env is 'gui':
            rcparamsarray = {
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
                "pgf.preamble": "\usepackage{nicefrac}"
            }
        matplotlib.rcParams.update(rcparamsarray)

    def cylinder(self, center, h, r, color, alpha=0.5, axes=None):
        try:
            self.c_data
        except AttributeError:
            self.c_data = []
        try:
            self.c_data.extend([center[3]])
        except AttributeError:
            pass
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        # draw the cylindrical surface
        t = np.linspace(0, 2.0 * np.pi, 100)
        x = center[0] + r * np.cos(t)
        y = center[1] + r * np.sin(t)
        z = center[2] + np.linspace(- h / 2, h / 2, 100)
        Tc, Zc =np.meshgrid(t, z)
        Xc = center[0] + r * np.cos(Tc)
        Yc = center[1] + r * np.sin(Tc)
        rstride = 20
        cstride = 10
        cylsurface = axes.plot_surface(Xc, Yc, Zc, alpha=alpha,
                                       rstride=rstride, cstride=cstride,
                                       color=color, shade=False,
                                       linewidth=0.0)
        t = np.linspace(0.0, 2.0 * np.pi, 100)
        radius = np.linspace(0.0, r, 100)
        R, Theta = np.meshgrid(radius, t)
        Xc, Yc = center[0] + R * np.cos(Theta), center[1] + R * np.sin(Theta)
        Zc = center[2] + h / 2.0
        top = axes.plot_surface(Xc, Yc, Zc, alpha=alpha, rstride=100,
                                cstride=100, color=color, shade=False,
                                linewidth=0.0)
        Zc = center[2] - h / 2.0
        bottom = axes.plot_surface(Xc, Yc, Zc, alpha=alpha, rstride=100,
                                   cstride=100, color=color,
                                   shade=False, linewidth=0.0)

    def sphere(self, center, r, color='gray', planes=True, lines=False,
             axes=None):
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if planes:
            planes_alpha = 0.5
        else:
            planes_alpha = 0.0
        if lines:
            linewidth = 0.01
        else:
            linewidth = 0.0
        rstride = 20
        cstride = 20
        theta = np.linspace(0., 2. * np.pi, 100)
        phi = np.linspace(0., np.pi, 100)
        x = center[0] + r * np.outer(np.cos(theta), np.sin(phi))
        y = center[1] + r * np.outer(np.sin(theta), np.sin(phi))
        z = center[2] + r * np.outer(np.ones(np.size(theta)), np.cos(phi))

        sph = axes.plot_surface(x, y, z,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth)

    def cube(self, center, dx, dy, dz, color='gray', planes=True, lines=False,
             axes=None):
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if planes:
            planes_alpha = 0.1
        else:
            planes_alpha = 0.0
        if lines:
            linewidth = 0.5
        else:
            linewidth = 0.0
        rstride = 100
        cstride = 100
        Xc, Yc = np.meshgrid(np.linspace(center[0] - dx/2.,
                                         center[0] + dx/2., 100),
                             np.linspace(center[1] - dy/2.,
                                         center[1] + dy/2., 100))
        top = axes.plot_surface(Xc, Yc, center[2] + dz/2.,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth)
        bottom = axes.plot_surface(Xc, Yc, center[2] - dz/2.,
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth)
        Xc, Zc = np.meshgrid(np.linspace(center[0] - dx/2.,
                                         center[0] + dx/2., 100),
                             np.linspace(center[2] - dz/2.,
                                         center[2] + dz/2., 100))
        left = axes.plot_surface(Xc, center[1] + dy/2., Zc,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth)
        right = axes.plot_surface(Xc, center[1] - dy/2., Zc,
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth)
        Yc, Zc = np.meshgrid(np.linspace(center[1] - dy/2.,
                                         center[1] + dy/2., 100),
                             np.linspace(center[2] - dz/2.,
                                         center[2] + dz/2., 100))
        front = axes.plot_surface(center[0] + dx/2., Yc, Zc,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth)
        back = axes.plot_surface(center[0] - dx/2., Yc, Zc,
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth)

    def colorbar(self, cmap, cmap_name='Color Map'):
        if cmap.__class__.__name__ == "list" and \
            cmap[0].__class__.__name__ == "Color":
            colors = [c.rgb for c in cmap]
            ax1 = self.fig.add_axes([0.95, 0.05, 0.04, 0.9])
            self.ax_subp.extend([ax1])
            cm = LinearSegmentedColormap.from_list(
                cmap_name, colors, N=len(cmap))
            norm = matplotlib.colors\
                .Normalize(vmin=np.min(self.c_data), vmax=np.max(self.c_data))
            cb1 = matplotlib.colorbar \
                .ColorbarBase(ax1, cmap=cm, norm=norm)
            ax1.set_ylabel(cmap_name)

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

    def ylabel(self, label, axes=None):
        r""" ``pyg2d.ylabel`` adds a label to the x-axis.

        ``pyg2d.ylabel`` adds a label to the x-axis of the current axes (or
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
        ylab = axes.set_ylabel(label)
        self.artists.append(ylab)

    def zlabel(self, label, axes=None):
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
        zlab = axes.set_zlabel(label)
        self.artists.append(zlab)

    def det_height(self, ratio="golden"):
        if ratio is "golden":
            r = (1. + np.sqrt(5.)) / 2.
        elif ratio is "silver":
            r = 1. + np.sqrt(2.)
        elif ratio is "bronze":
            r = (3. + np.sqrt(13.)) / 2.
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
                 tight=True, ratio="golden"):
        if size is '1':
            self.width = 3.25
            self.det_height(ratio=ratio)
            # if self.leg:
            #    self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            #        ncol=self.leg_col_one_col, mode="expand",
            #        borderaxespad=0.);
        elif size is '2':
            self.width = 6.25
            self.det_height()
            self.height = self.height / 2.0
            self.fig.set_size_inches(self.width, self.height)
            # if self.leg:
            #    self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            #                   ncol=self.leg_col_two_col, mode="expand",
            #                   borderaxespad=0.)
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
        elif format is 'html':
            add = '.html'
        elif format is 'svg':
            # save as pdf, then pdf2svg
            self.fig.savefig(filename + self.sizestring[size] + '.pdf',
                        bbox_extra_artists=self.artists, bbox_inches='tight',
                        transparent=True)
            os.system('pdf2svg ' + filename + self.sizestring[size] + '.pdf ' +
                      filename + self.sizestring[size] + '.svg')
            os.remove(filename + self.sizestring[size] + '.pdf')
        elif format is 'websvg':
            add = 'web.svg'
        if (format is not 'svg') and (format is not 'html'):
            self.fig.savefig(filename + self.sizestring[size] + add,
                        bbox_extra_artists=self.artists, bbox_inches='tight',
                        transparent=True)
        if format is 'html':
            add = '.html'
            mpld3.save_html(self.fig, filename + add)
            self.add_math_jax(filename + add)
        if format is 'pgf':
            self.remove_font_sizes(filename + self.sizestring[size] + add)

    def show(self):
        if self.pdf_filename:
            if platform.system() == "Darwin":
                os.system("open -a Preview " + self.pdf_filename)
            if platform.system() == "Linux":
                os.system("evince " + self.pdf_filename + " &")

    def export(self, filename, sizes=['1'], formats=['pgf'],
               customsize=None, legloc=None, tight=True, ratio="golden"):
        zaxis = self.ax.zaxis
        draw_grid_old = zaxis.axes._draw_grid
        # disable draw grid
        zaxis.axes._draw_grid = False
        tmp_planes = zaxis._PLANES
        zaxis._PLANES = (tmp_planes[2], tmp_planes[3],
                         tmp_planes[0], tmp_planes[1],
                         tmp_planes[4], tmp_planes[5])
        zaxis._PLANES = tmp_planes
        zaxis.axes._draw_grid = draw_grid_old

        self.ax.xaxis._axinfo['tick']['outward_factor'] = 0
        self.ax.yaxis._axinfo['tick']['outward_factor'] = 0
        self.ax.zaxis._axinfo['tick']['outward_factor'] = 0
        self.ax.view_init(30, 240)
        self.ax.w_xaxis.gridlines.set_lw(0.1)
        self.ax.w_yaxis.gridlines.set_lw(0.1)
        self.ax.w_zaxis.gridlines.set_lw(0.1)
        self.ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.set_aspect('equal')
        self.ax.set_xlim([-60, 60])
        self.ax.set_ylim([-60, 60])
        self.ax.set_zlim([-60, 60])
        # self.ax.set_position([0.0, 0.0, 1.5, 1.0])
        for size in sizes:
            for format in formats:
                self.set_size(size, len(sizes), customsize=customsize,
                              legloc=legloc, tight=tight, ratio=ratio)
                self.export_fmt(filename, size, len(sizes), format)
                if format is 'pdf':
                    self.pdf_filename = filename + '.pdf'

    def close(self):
        plt.close(self.fig)
