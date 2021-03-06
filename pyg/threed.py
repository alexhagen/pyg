from __future__ import print_function, division
from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
import matplotlib
import string
import os
from colour import Color
import numpy as np
#matplotlib.use('pgf')
if "DISPLAY" not in os.environ.keys():
    matplotlib.use('Agg')
else:
    matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import platform
from matplotlib import cm
from pyg.colors import pnnl as color
from copy import copy
from IPython.display import SVG, display, Latex, HTML, display_latex
import subprocess
import sys
import random
import weakref
import re
import lyxithea.lyxithea as lyx
from pyg import twod as pyg2d
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import art3d
import matplotlib.pyplot as plt

global context
context = 'writeup'
global __figcount__
__figcount__ = 1
exported_files = {}

plt.close("all")
preamble = [r'\usepackage{nicefrac}',
	r'\usepackage{gensymb}',
	r'\usepackage{xcolor}',
	r'\definecolor{grey60}{HTML}{746C66}',
	r'\definecolor{grey40}{HTML}{A7A9AC}',
	r'\usepackage{amsmath, amssymb}',
	r'\usepackage{stackrel}',
	r'\providecommand{\unit}[1]{\ensuremath{' +
	r'{\mathrm{#1}}}}']

# make the line graphing class
class pyg3d(pyg2d.pyg2d):
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
        super(pyg3d, self).__init__(env=env, polar=False, colors=colors)
        self.rcparamsarray['_internal.classic_mode'] = True
        self.rcparamsarray['grid.color'] = '#ffffff'
        self.rcparamsarray['grid.alpha'] = 0.5
        self.rcparamsarray['axes.grid'] = False
        matplotlib.rcParams.update(self.rcparamsarray)
        matplotlib.rcParams['_internal.classic_mode'] = True
        self.ax = self.fig.gca(projection='3d')
        self.cax = []
        self.surfs = {}
        self.contours = {}
        self.annotations = []
        self.ax.view_init(30, 245)
        #print dir(self.ax.w_zaxis.gridlines)
        self.ax.w_xaxis.gridlines.set_lw(2)
        self.ax.w_yaxis.gridlines.set_lw(2)
        self.ax.w_zaxis.gridlines.set_lw(2)
        for _ax in [self.ax.w_xaxis, self.ax.w_yaxis, self.ax.w_zaxis]:
            _ax._axinfo[u'tick'] = {u'color': u'k', u'outward_factor': 0.1, u'linewidth': 0.5, u'inward_factor': 0.0}
            _ax.set_clip_on(True)
        self.ax.w_xaxis._axinfo['axisline'] = {u'color': (1, 1, 1, 1), u'linewidth': 0.5}
        self.ax.w_yaxis._axinfo['axisline'] = {u'color': (1, 1, 1, 1), u'linewidth': 0.5}
        self.ax.w_zaxis._axinfo['axisline'] = {u'color': (1, 1, 1, 1), u'linewidth': 0.5}
        self.ax.w_xaxis._axinfo['grid'] = {u'color': (1.0, 1.0, 1.0, 1.0), u'linewidth': 1.0, u'linestyle': u'-'}
        self.ax.w_yaxis._axinfo['grid'] = {u'color': (1.0, 1.0, 1.0, 1.0), u'linewidth': 1.0, u'linestyle': u'-'}
        self.ax.w_zaxis._axinfo['grid'] = {u'color': (1.0, 1.0, 1.0, 1.0), u'linewidth': 1.0, u'linestyle': u'-'}
        pane_color = (0.9, 0.9, 0.9, 0.1)
        self.ax.w_xaxis.set_pane_color(pane_color)
        self.ax.w_yaxis.set_pane_color(pane_color)
        self.ax.w_zaxis.set_pane_color(pane_color)
        self.ax.set_autoscale_on(True)
        self.ax.tick_params(pad=0.0)

    def xlim(self, x1, x2):
        self.ax.set_xlim3d(x1, x2)
        super(pyg3d, self).xlim(x1, x2)
        self.xmin = x1
        self.xmax = x2

    def ylim(self, y1, y2):
        self.ax.set_ylim3d(y1, y2)
        super(pyg3d, self).ylim(y1, y2)
        self.ymin = y1
        self.ymax = y2

    def zlim(self, z1, z2):
        self.ax.set_zlim3d(z1, z2)
        super(pyg3d, self).zlim(z1, z2)
        self.zmin = z1
        self.zmax = z2

    def orthogonal_proj(self, zfront, zback):
        a = (zfront+zback)/(zfront-zback)
        b = -2*(zfront*zback)/(zfront-zback)
        return np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,a,b],
                         [0,0,-1.0e-9,zback]])

    def add_line(self, x, y, z, name='', addto=None, axes=None, **kwargs):
        if addto is None:
            axes = self.ax
        else:
            axes = addto.ax
        line = axes.plot(x, y, z, **kwargs)
        for i in range(0, len(line)):
            self.lines[name + '%d' % (i)] = (line[i])
        self.allartists.append(line)

    def upright_orthogonal_proj(self, zfront, zback):
        a = (zfront+zback)/(zfront-zback)
        b = -2*(zfront*zback)/(zfront-zback)
        return np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,a,b],
                         [0,0,1.0e-9,zback]])

    def surf2d(self, x, y, z, c, cmap=color.brand_cmap, addto=None, name='plot',
               **kwargs):
        from matplotlib.collections import PolyCollection
        if addto is None:
            axes = self.ax
        else:
            axes = addto.ax
        cmaplist = [_c.rgb for _c in cmap]
        self.cmap = matplotlib.colors.ListedColormap(cmaplist,
                                                name='brand_cmap')
        m = np.ma.masked_where(np.isnan(c), c)
        levels = np.linspace(np.min(c), np.max(c), 50)
        if len(x) == 1:
            #print 'x'
            Y, Z = np.meshgrid(y, z)
            zdir = 'x'
            zs = x[0]
            self.cax.extend([axes.contourf(c, Y, Z, cmap=self.cmap, offset=zs, zdir='x',
                                     levels=levels, linestyle='-', **kwargs)])
        elif len(y) == 1:
            #print 'y'
            Z, X = np.meshgrid(z, x)
            zdir = 'y'
            zs = y[0]
            self.cax.extend([axes.contourf(X, c.T, Z, cmap=self.cmap, offset=zs, zdir='y',
                                     levels=levels, linestyle='-', **kwargs)])
        elif len(z) == 1:
            #print 'z'
            X, Y = np.meshgrid(x, y)
            zdir = 'z'
            zs = z[0]
            self.cax.extend([axes.contourf(X, Y, c, cmap=self.cmap, offset=zs, zdir='z',
                                     levels=levels, linestyle='-', **kwargs)])

    def colorbar2(self):
        self.norm = self.cax[0].norm
        maxes = []
        mins = []
        for c in self.cax:
            c.set_norm = self.norm
            maxes.extend([c.levels[-1]])
            mins.extend([c.levels[0]])
        levels = np.linspace(np.nanmin(mins), np.nanmax(maxes))
        for c in self.cax:
            c.vmin = np.nanmin(mins)
            c.vmax = np.nanmax(maxes)
        self.cbar = self.fig.colorbar(self.cax[0])
    #self.artists.append(self.cbar)

    def add_arrow(self, x1, x2, y1, y2, z1, z2, *args, axes=None, **kwargs):
        if axes is None:
            axes = self.ax
        _x1, _y1, _ = proj3d.proj_transform(x1, y1, z1, axes.get_proj())
        _x2, _y2, _ = proj3d.proj_transform(x2, y2, z2, axes.get_proj())
        super(pyg3d, self).add_arrow(_x1, _x2, _y1, _y2, *args, **kwargs)


    def surf(self, x, y, z, c=None, cmap=color.brand_cmap, addto=None,
             name='surf', zmin=None, zmax=None, **kwargs):
        if addto is None:
            axes = self.ax
        else:
            axes = addto.ax
        X, Y = np.meshgrid(x, y)
        # z = np.nan_to_num(z)
        #m = np.ma.masked_where(np.isnan(z), z)
        m = np.ma.masked_where(~np.isfinite(z), z)
        cmaplist = [_c.rgb for _c in cmap]
        cmap = matplotlib.colors.ListedColormap(cmaplist,
                                                name='brand_cmap')
        if zmax is None:
            zmax = np.nanmax(z)
        if zmin is None:
            zmin = np.nanmin(z)
        surf = axes.plot_surface(X, Y, m, cmap=cmap,
                                 linewidth=0, antialiased=False,
                                 rstride=1, cstride=1,
                                 vmin=zmin, vmax=zmax,
                                 **kwargs)
        self.surfs[name] = surf
        return self

    def wireframe(self, x, y, z, c=None, cmap=color.brand_cmap, addto=None,
                  name='surf', zmin=None, zmax=None, stride=10, **kwargs):
        if addto is None:
            axes = self.ax
        else:
            axes = addto.ax
        X, Y = np.meshgrid(x, y)
        Z = z
        wire = axes.plot_wireframe(X, Y, Z, rstride=stride, cstride=stride,
                                   cmap=cmap, **kwargs)

        # Retrive data from internal storage of plot_wireframe, then delete it
        #nx, ny, _  = np.shape(wire._segments3d)
        #wire_x = np.array(wire._segments3d)[:, :, 0].ravel()
        #wire_y = np.array(wire._segments3d)[:, :, 1].ravel()
        #wire_z = np.array(wire._segments3d)[:, :, 2].ravel()
        #wire.remove()
#
        ## create data for a LineCollection
        #wire_x1 = np.vstack([wire_x, np.roll(wire_x, 1)])
        #wire_y1 = np.vstack([wire_y, np.roll(wire_y, 1)])
        #wire_z1 = np.vstack([wire_z, np.roll(wire_z, 1)])
        #to_delete = np.arange(0, nx*ny, ny)
        #wire_x1 = np.delete(wire_x1, to_delete, axis=1)
        #wire_y1 = np.delete(wire_y1, to_delete, axis=1)
        #wire_z1 = np.delete(wire_z1, to_delete, axis=1)
        #scalars = np.delete(wire_z, to_delete)
#
        #segs = [list(zip(xl, yl, zl)) for xl, yl, zl in \
        #                 zip(wire_x1.T, wire_y1.T, wire_z1.T)]
#
        ## Plots the wireframe by a  a line3DCollection
        #my_wire = art3d.Line3DCollection(segs, cmap=cmap)
        #my_wire.set_array(scalars)
        #axes.add_collection(my_wire)

        return self

    def contour(self, x, y, z, name='countour', addto=None, **kwargs):
        if addto is None:
            axes = self.ax
        else:
            axes = addto.ax
        X, Y = np.meshgrid(x, y)
        # z = np.nan_to_num(z)
        m = np.ma.masked_where(np.isnan(z),z)
        #cmaplist = [_c.rgb for _c in cmap]
        #cmap = matplotlib.colors.ListedColormap(cmaplist, name='brand_cmap')
        cs = axes.contour(X, Y, m, **kwargs)
        self.contours[name] = cs
        return self

    def legend(self):
        surfs = []
        labels = []
        for key, val in self.surfs.iteritems():
            labels.extend([key])
            surfs.extend([val])
        self.ax.legend(surfs, labels, numpoints=1)


    def view(self, phi, theta, perspective=False, upright=False):
        if not perspective:
            if upright:
                proj3d.persp_transformation = self.upright_orthogonal_proj
            else:
                proj3d.persp_transformation = self.orthogonal_proj
        self.ax.view_init(phi, theta)
        return self

    def cylinder(self, center, h, r, color, planes=True, lines=False,
                 axes=None):
        try:
            self.c_data
        except AttributeError:
            self.c_data = []
        try:
            self.c_data.extend([center[2]])
        except AttributeError:
            pass
        if isinstance(planes, float):
            planes_alpha = planes
        elif planes:
            planes_alpha = 0.1
        else:
            planes_alpha = 0.0
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if lines:
            linewidth = 0.01
        else:
            linewidth = 0.0
        # draw the cylindrical surface
        t = np.linspace(0, 2.0 * np.pi, 100)
        if h[0] > h[1] and h[0] > h[2]:
            cz = center[0]
            cx = center[2]
            cy = center[1]
        elif h[2] > h[1] and h[2] > h[0]:
            cz = center[2]
            cx = center[0]
            cy = center[1]
        x = cx + r * np.cos(t)
        y = cy + r * np.sin(t)
        z = cz + np.linspace(- np.max(h) / 2, np.max(h) / 2, 100)
        Tc, Zc =np.meshgrid(t, z)
        Xc = cx + r * np.cos(Tc)
        Yc = cy + r * np.sin(Tc)
        rstride = 20
        cstride = 10
        if h[0] > h[1] and h[0] > h[2]:
            cylsurface = axes.plot_surface(Zc, Yc, Xc, alpha=planes_alpha,
                                           rstride=rstride, cstride=cstride,
                                           color=color, shade=False,
                                           linewidth=linewidth)
        elif h[2] > h[1] and h[2] > h[0]:
            cylsurface = axes.plot_surface(Xc, Yc, Zc, alpha=planes_alpha,
                                           rstride=rstride, cstride=cstride,
                                           color=color, shade=False,
                                           linewidth=linewidth)

        t = np.linspace(0.0, 2.0 * np.pi, 100)
        radius = np.linspace(0.0, r, 100)
        R, Theta = np.meshgrid(radius, t)
        Xc, Yc = cx + R * np.cos(Theta), cy + R * np.sin(Theta)
        Zc = cz + np.max(h) / 2.0
        if h[0] > h[1] and h[0] > h[2]:
            top = axes.plot_surface(Zc, Yc, Xc, alpha=planes_alpha, rstride=100,
                                    cstride=100, color=color, shade=False,
                                    linewidth=linewidth, edgecolor='black')
        elif h[2] > h[1] and h[2] > h[0]:
            top = axes.plot_surface(Xc, Yc, Zc, alpha=planes_alpha, rstride=100,
                                    cstride=100, color=color, shade=False,
                                    linewidth=linewidth, edgecolor='black')
        Zc = cz - np.max(h) / 2.0
        if h[0] > h[1] and h[0] > h[2]:
            bottom = axes.plot_surface(Zc, Yc, Xc, alpha=planes_alpha, rstride=100,
                                    cstride=100, color=color, shade=False,
                                    linewidth=linewidth, edgecolor='black')
        elif h[2] > h[1] and h[2] > h[0]:
            bottom = axes.plot_surface(Xc, Yc, Zc, alpha=planes_alpha, rstride=100,
                                    cstride=100, color=color, shade=False,
                                    linewidth=linewidth, edgecolor='black')
        return self

    def sphere(self, center, r, color='gray', planes=True, lines=False,
             axes=None):
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if isinstance(planes, float):
            planes_alpha = planes
        elif planes:
            planes_alpha = 0.1
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
        return self

    def box(self, corner, d1, d2, d3, color='gray', planes=True, lines=False,
            axes=None):
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if isinstance(planes, float):
            planes_alpha = planes
        elif planes:
            planes_alpha = 0.1
        else:
            planes_alpha = 0.0
        if lines:
            linewidth = 0.5
        else:
            linewidth = 0.0
        rstride = 10
        cstride = 10
        l1 = np.sqrt(d1[0]**2 + d1[1]**2 + d1[2]**2)
        l2 = np.sqrt(d2[0]**2 + d2[1]**2 + d2[2]**2)
        l3 = np.sqrt(d3[0]**2 + d3[1]**2 + d3[2]**2)
        numpts = 10
        planes = []
        top_corner = np.array(corner) + np.array(d1) + np.array(d2) + \
            np.array(d3)
        for ds in [(d1, d2), (d2, d3), (d1, d3)]:
            a1 = ds[0]
            a2 = ds[1]
            xx = np.zeros((numpts, numpts))
            yy = np.zeros((numpts, numpts))
            zz = np.zeros((numpts, numpts))
            for i in range(0, numpts):
                for j in range(0, numpts):
                    xx[i, j] = corner[0] + a1[0] * float(i) / float(numpts - 1) + \
                        a2[0] * float(j) / float(numpts - 1)
                    yy[i, j] = corner[1] + a1[1] * float(i) / float(numpts - 1) + \
                        a2[1] * float(j) / float(numpts - 1)
                    zz[i, j] = corner[2] + a1[2] * float(i) / float(numpts - 1) + \
                        a2[2] * float(j) / float(numpts - 1)
            planes.extend([axes.plot_surface(xx, yy, zz,
                                       rstride=cstride, cstride=rstride,
                                       color=color, alpha=planes_alpha, shade=False,
                                       linewidth=linewidth)])
            for i in range(0, numpts):
                for j in range(0, numpts):
                    xx[i, j] = top_corner[0] - \
                        a1[0] * float(i) / float(numpts - 1) - \
                        a2[0] * float(j) / float(numpts - 1)
                    yy[i, j] = top_corner[1] - \
                        a1[1] * float(i) / float(numpts - 1) - \
                        a2[1] * float(j) / float(numpts - 1)
                    zz[i, j] = top_corner[2] - \
                        a1[2] * float(i) / float(numpts - 1) - \
                        a2[2] * float(j) / float(numpts - 1)
            planes.extend([axes.plot_surface(xx, yy, zz,
                                       rstride=cstride, cstride=rstride,
                                       color=color, alpha=planes_alpha, shade=False,
                                       linewidth=linewidth)])
        #top = axes.plot_surface(Xc, Yc, )
        return self

    def add_plane(self, xmin=None, xmax=None, ymin=None, ymax=None,
                  zmin=None, zmax=None, axes=None):
        if axes is None:
            axes = self.ax
        if zmax is None:
            dir = 'z'
            args = [0, 1, 2, 3]
            dims = [0, 1]
            z = 2
        elif ymax is None:
            dir = 'y'
            args = [0, 1, 4, 5]
            dims = [0, 2]
            z = 1
        elif xmax is None:
            dir = 'x'
            args = [2, 3, 4, 5]
            dims = [1, 2]
            z = 0
        maxes = [xmin, xmax, ymin, ymax, zmin, zmax]
        chis, etas = np.meshgrid(np.linspace(maxes[args[0]],
                                         maxes[args[1]], 3),
                             np.linspace(maxes[args[2]],
                                         maxes[args[3]], 3))
        phis = maxes[2*z] * np.ones_like(etas)
        surf = [[], [], []]
        surf[dims[0]] = chis
        surf[dims[1]] = etas
        surf[z] = phis
        top = axes.plot_surface(*surf,
                                color='none', shade=False,
                                linewidth=0.5, edgecolor='black')

    def cube(self, center, dx, dy, dz, color='gray', planes=True, lines=False,
             axes=None):
        if axes is None:
            axes = self.ax
        else:
            axes = axes.ax
        if isinstance(planes, float):
            planes_alpha = planes
        elif planes:
            planes_alpha = 0.1
        else:
            planes_alpha = 0.0
        if lines:
            linewidth = 1.0
        else:
            linewidth = 0.0
        rstride = 100
        cstride = 100
        Xc, Yc = np.meshgrid(np.linspace(center[0] - dx/2.,
                                         center[0] + dx/2., 100),
                             np.linspace(center[1] - dy/2.,
                                         center[1] + dy/2., 100))
        top = axes.plot_surface(Xc, Yc, (center[2] + dz/2.) * np.ones_like(Yc),
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth, edgecolor='black')
        bottom = axes.plot_surface(Xc, Yc, (center[2] - dz/2.) * np.ones_like(Yc),
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth, edgecolor='black')
        Xc, Zc = np.meshgrid(np.linspace(center[0] - dx/2.,
                                         center[0] + dx/2., 100),
                             np.linspace(center[2] - dz/2.,
                                         center[2] + dz/2., 100))
        left = axes.plot_surface(Xc, (center[1] + dy/2.) * np.ones_like(Xc), Zc,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth, edgecolor='black')
        right = axes.plot_surface(Xc, (center[1] - dy/2.) * np.ones_like(Xc), Zc,
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth, edgecolor='black')
        Yc, Zc = np.meshgrid(np.linspace(center[1] - dy/2.,
                                         center[1] + dy/2., 100),
                             np.linspace(center[2] - dz/2.,
                                         center[2] + dz/2., 100))
        front = axes.plot_surface((center[0] + dx/2.) * np.ones_like(Yc), Yc, Zc,
                                rstride=cstride, cstride=rstride,
                                color=color, alpha=planes_alpha, shade=False,
                                linewidth=linewidth, edgecolor='black')
        back = axes.plot_surface((center[0] - dx/2.) * np.ones_like(Yc), Yc, Zc,
                                   rstride=cstride, cstride=rstride,
                                   color=color, alpha=planes_alpha, shade=False,
                                   linewidth=linewidth, edgecolor='black')
        return self

    def add_data_pointer(self, x, y, z, string=None,
                         place='up-right', axes=None, **kwargs):
        if axes is None:
            axes = self.ax
        _x, _y, _ = proj3d.proj_transform(x, y, z, axes.get_proj())
        super(pyg3d, self).add_data_pointer(_x, point=_y, string=string,
                                            place=place, axes=None,
                                            **kwargs)

    def add_text(self, x, y, z, string=None, ha='center', va='center',
                 color="#746C66", rotation=0, axes=None, fontsize=None,
                 backgroundcolor=None, backgroundalpha=None):
        if axes is None:
            axes = self.ax
        if axes is None:
            axes = self.ax
        if backgroundcolor is None and backgroundalpha is None:
            backgroundcolor = '#FFFFFF00'
        if backgroundcolor is not None and backgroundalpha is not None:
            _bgc = colour(backgroundcolor).hex
            backgroundcolor = _bgc + hex(int(255 * backgroundalpha))[-2:]
        if fontsize is not None:
            ann = axes.text(x1, y1, string, fontsize=fontsize, ha=ha, va=va,
                            color=color, rotation=rotation,
                            backgroundcolor=backgroundcolor)
        else:
            ann = axes.text(x, y, z, string, ha=ha, va=va, color=color,
                            rotation=rotation, backgroundcolor=backgroundcolor)
        self.allartists.append(ann)
        return self
        #_x, _y, _ = proj3d.proj_transform(x, y, z, self.ax.get_proj())
        #super(pyg3d, self).add_text(_x, _y, string=string,
        #                                    axes=None, **kwargs)

    def update_data_pointers(self):
        for ann in self.annotations:
            x = ann[0]
            y = ann[1]
            z = ann[2]
            _x, _y, _ = proj3d.proj_transform(x, y, z, self.ax.get_proj())
            ann[3].xy = (_x, _y)

    '''
    def colorbar(self):#, cmap, cmap_name='Color Map'):
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
    '''

    def find_best_lims(self, xs, ys, ratio='golden'):
        r = pyg2d.metal_dim(ratio)
        xmin = np.min(xs)
        xmax = np.max(xs)
        dx = xmax - xmin
        ymin = np.min(ys)
        ymax = np.max(ys)
        dy = ymax - ymin
        xchange = -1.
        ychange = -1.
        perc = 0.
        while xchange < 0. and ychange < 0.:
            dx += dx * perc
            xchange = (dy * r) - dx
            ychange = (dx / r) - dy
            if xchange > 0 and xchange < ychange:
                dx = dx + xchange
            elif ychange > 0:
                dy = dy + ychange
            perc += 0.1
        self.xlim(xmin, xmin + dx)
        self.ylim(ymin, ymin + dy)

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
        return self

    def clabel(self, label, axes=None):
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
        self.clab = self.cbar.set_label(label)
        #self.artists.append(self.clab)

    def zlim(self, minz, maxz, axes=None):
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
        axes.set_zlim([minz, maxz])

    def zticks(self, ticks, labels, axes=None, rotation='horizontal'):
        """ ``pyg2d.zticks`` changes the ticks and labels to provided values.

        ``pyg2d.zticks`` will move the ticks on the abscissa to the
        locations given in ``ticks`` and place the labels in list ``labels`` at
        those locations, repsectively.

        :param list ticks: The values where the new tick labels will be placed
            on the z-axis.
        :param list labels: The string labels for each tick.
        :param axes axes: An axes to append these ticks to, if not current.
        :return: None
        """
        if axes is not None:
            plt.sca(axes)
        else:
            axes = self.ax
        axes.set_zticks(ticks)
        axes.set_zticklabels(labels, rotation=rotation)
        if rotation is 'vertical':
            plt.margins(0.2)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.15)
        return self
