import sys
import os
sys.path.append(os.environ['HOME'] + '/code')
from pyg import twod as pyg2
import numpy as np

# first lets make some data with a numpy gaussian function
x = np.linspace(0., 5., 1000.)
mu = 2.5
sigma1 = 1.0
sigma2 = 0.5
y1 = np.exp(-np.power(x - mu, 2.) / (2. * np.power(sigma1, 2.)))
y2 = np.exp(-np.power(x - mu, 2.) / (2. * np.power(sigma2, 2.)))

# create a plot object
plot = pyg2.ah2d()

# add both of our lines to this object
plot.add_line(x, y1, linecolor='#285668', linestyle='-', name=r'$\sigma = 1$')
plot.add_line(x, y2, linecolor='#FC8D82', linestyle='-.', name=r'$\sigma =' +
              r'\frac{1}{2}$')

# make it pretty with labels and a legend
plot.markers_off()
plot.lines_on()
plot.xlabel(r'$x$')
plot.ylabel(r'$ y = \exp \left[\frac{\left( x - \mu \right)^{2}}' +
            r'{2 \sigma ^ {2}}\right]$')
plot.legend()

# export this to file
plot.export('../images/simple_linegraph', sizes=['2'],
            formats=['websvg', 'png'])
