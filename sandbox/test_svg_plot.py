from xml.dom import minidom
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import pyplot
import os
from svg.path import parse_path
import numpy as np

filename = 'dd_setup'

doc = minidom.parse(filename + "poly.svg")

path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()
xs = []
ys = []
for path_string in path_strings:
    path = parse_path(path_string)
    for segment in path._segments:
        for pos in np.linspace(0, segment.length()):
            point = segment.point(pos)
            x = np.real(point)
            y = np.imag(point)
            xs = np.append(xs, x)
            ys = np.append(ys, y)
        pyplot.plot(xs, ys)
        xs = []
        ys = []

pyplot.plot(xs, ys)

pyplot.show()
