from pyg import twod as pyg2d

# we need to make a new empty plot to remove any chance that we don't set the
# rcparams correctly
plot = pyg2d.pyg2d()
plot.close()
del plot
