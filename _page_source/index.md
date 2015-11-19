---
layout: post
title: pyg
description: "a graphing library in python"
category: code
tags: [python, visualization]
image:
  feature: "http://alexhagen.github.io/pyg/images/pyg_banner_1.png"
---

# pyg - A graphing library in python

Last Updated on 11/2/15

Written by [Alex Hagen](http://alexhagen.github.io)

Hosted at [github.com/alexhagen/pyg](http://github.com/alexhagen/pyg)

Documentation at [alexhagen.github.io/pyg/docs](docs/)

`pyg` (pronounced <i>pig</i>) is my graphing library for `python`, building off of
`matplotlib`.  Realistically, it only is very useful for a couple cases.

- If you're using my [`pym`](http://alexhagen.github.io/pym/) library for
interpolation, decimation, or other operations on data sets, `pyg` is a lazy
and easy way to create graphs from these objects.
- If you've got a specific style in mind, and you want to pass that in as an
`rc.Params` object, `pyg` can help you keep that style consistent.
- If you're wanting to publish, `pyg` has some exporting features that make
figures exported as 1-column, 2-column, or full-page look
great in journal articles.
- If you want to tinker, `pyg` is a good starting point for making functions
to consistently graph data with the same annotations, such as measurements,
data-pointers, and other features.

If one of those cases are something you're interested in, you can look below
for samples and demos or take a look at the [documentation](docs/).

## Pyg Demonstrations and Screenshots

### A simple pyg linegraph

<figure>
    <img src="http://alexhagen.github.io/pyg/images/simple_linegraphweb.svg">
    <figcaption>A simple linegraph plotted with pyg</figcaption>
</figure>

The above figures shows the basic interface to `pyg`. In general, the function
plot will give us what we want, and we can send a bunch of parameters to this
function, such as x error, y error, line color, and line style.  The source for
creating the above graph is shown below:

```python
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
```

### Publication figures with pyg

<figure style="text-align:center;">
    <img style="width:48%; display:inline-block;" src="http://alexhagen.github.io/pyg/images/publication_figure1web.svg">
    <img style="width:48%; display:inline-block;" src="http://alexhagen.github.io/pyg/images/publication_figure2web.svg">
    <figcaption>Two one column figures plotted with pyg</figcaption>
</figure>

<figure>
    <img src="http://alexhagen.github.io/pyg/images/publication_figure3web.svg">
    <figcaption>One two column figure plotted with pyg</figcaption>
</figure>

For publishing, often you want to put things in two column format.  The `pyg`
library has a built in interface for this, setting the width to a typical ASME
column size and changing the height with the golden ratio.  This makes for some
pretty beautiful figures, and shown above, you can decide whether you want the
figure to span the whole width or not.  The source code for this follows

```python
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

```

### Pyg and Pym integration, data pointers, and fill

See the page for [pym](/pym) for an illustration on how to use `pyg` and `pym`
together.  This example also shows how to add data_pointers on your plots, and
to fill spaces for even prettier plots.

### Dual axes

<figure>
    <img src="http://alexhagen.github.io/pyg/images/dual_axesweb.svg">
    <figcaption>Dual y axis graph plotted with pyg</figcaption>
</figure>

The `pyg` library also allows for plotting on dual axes, so that you can show
correlations between data on different scales, or on linear and log scales.
Currently, the library only allows for one extra axis to be added, which can be
accessed through `pyg_object.ax2`, but in the future, a third access will be
added (only three are needed, because you can only have one extra in the y and x
direction).  The code below shows the interface for using these axes:

```python
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
```
