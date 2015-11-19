import sys
import os
sys.path.append(os.environ['HOME'] + '/code')
from pyg import twod as pyg2
import numpy as np

# first lets make some cool data with trigonometric functions
x = np.linspace(0., 4. * np.pi, 500.)
y1 = np.sin(x)
y2 = np.power(np.sin(x), 2.)

# create three plot objects, two for one column, and another for two column
plot1 = pyg2.ah2d()
plot2 = pyg2.ah2d()
plot3 = pyg2.ah2d()

# add one line each to our single column plots
plot1.add_line(x, y1, linecolor='#285668', linestyle='-', name=r'$\sin$')
plot2.add_line(x, y2, linecolor='#285668', linestyle='-', name=r'$\sin^{2}$')
# add both of them to our double width object
plot3.add_line(x, y1, linecolor='#285668', linestyle='-', name=r'$\sin$')
plot3.add_line(x, y2, linecolor='#FC8D82', linestyle='--', name=r'$\sin^{2}$')

# make them pretty with labels and a legend
for plot in [plot1, plot2, plot3]:
    plot.markers_off()
    plot.lines_on()
    plot.ylim(-1.1, 1.1)
    plot.xlabel(r'$x$')
    plot.ylabel(r'$y$')

# add a legend to our double width plot
plot3.legend()

# export this to file
plot1.export('../images/publication_figure1', sizes=['1'],
             formats=['websvg'])
plot2.export('../images/publication_figure2', sizes=['1'],
             formats=['websvg'])
plot3.export('../images/publication_figure3', sizes=['2'],
             formats=['websvg'])
