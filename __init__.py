from pyg import twod as pyg2d
import matplotlib.pyplot as plt

# we need to make a new empty plot to remove any chance that we don't set the
# rcparams correctly
plot = pyg2d.pyg2d()
plt.cla()
plt.clf()
plt.close()
plot.fig.clear()
plt.close(plot.fig)
plot.close()
del plot.fig
del plot
plt.close()
