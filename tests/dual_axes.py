import sys
import os
sys.path.append(os.environ['HOME'] + '/code')
from pyg import twod as pyg2
import numpy as np

# first lets make some data which relates to each other, but is way off scale
x = np.linspace(0., 4. * np.pi, 500.)
y1 = np.sin(x)
y2 = np.exp(np.sin(x))

# create three plot objects, two for one column, and another for two column
plot = pyg2.ah2d()

# add one line each to our single column plots
plot.add_line(x, y1, linecolor='#285668', linestyle='-', name=r'$\sin$')
plot.fill_between(x, np.zeros_like(y1), y1, fc='#ccccff', name=r'$\int y dx$')
plot.add_line_yy(x, y2, linecolor='#FC8D82', linestyle='-',
                 name=r'$\exp \left( \sin \right)$')
plot.fill_between(x, np.zeros_like(y2), y2, fc='#ffcccc', name=r'$\int y dx$',
                  axes=plot.ax2)

# make them pretty with labels and a legend
plot.markers_off()
plot.lines_on()
plot.xlim(0., 4. * np.pi)
plot.ylim(-1.5, 1.5)
plot.ylim(0.0, 4.0, axes=plot.ax2)
plot.xlabel(r'$x$')
plot.ylabel(r'$y = \sin$')
plot.ylabel(r'$y = \exp \left( \sin \right)$', axes=plot.ax2)

# add a legend to our double width plot
plot.legend()
plot.legend(loc=4, axes=plot.ax2)

# export this to file
plot.export('../images/dual_axes', sizes=['2'],
            formats=['png', 'websvg'])
