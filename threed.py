from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
import matplotlib
import string
import os
from matplotlib.patches import Ellipse, Polygon
from colour import Color
import numpy as np
matplotlib.use('pgf')
import matplotlib.pyplot as plt
import platform

plt.close("all")


# make the line graphing class
class ah3d(object):
    """ A ``pyg.ah3d`` object plots many three-dimensional data types.

    The ``ah3d`` class provides an access to ``matplotlib`` charting functions
    and some hook ins to making these functions easier to use and more
    repeatable.  The constructor itself takes only one optional argument,
    ``env``.

    :param str env: The environement option defines where you are going to use
        the generated plot, with the default option being plot (or printing).
        If you are using this to generate plots for a gui, define this option
        as ``gui`` and the class will choose a prettier parameter set for your
        chart. Default: ``plot``.
    :type env: ``plot``, ``gui``, or ``None``
    :return: the ``ah3d`` object.
    :rtype: ``ah3d``
    """
