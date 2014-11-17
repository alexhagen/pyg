# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 19:29:29 2014

@author: ahagen
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "font.serif": [],
    "axes.edgecolor": "#746C66",
    "xtick.color": "#746C66",
    "ytick.color": "#746C66",
    "text.color": "#746C66",
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "axes.labelcolor": "black",
    "xtick.labelsize": "x-small",
    "ytick.labelsize": "x-small",
    "axes.linewidth": 0.5,
    "axes.labelsize": "medium",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
}
matplotlib.rcParams.update(pgf_with_pdflatex)
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
plt.close("all")
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

fig.set_size_inches(3.25,3.25/1.6);
plt.savefig('something'+'_onecolumn.pgf')