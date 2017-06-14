
# pyg - A graphics class

By Alex Hagen

``pyg`` started as a simple wrapper around ``matplotlib`` to help me keep my style the same in plotting, but now it's expanded to a full graphics suite.  If you get bored reading through the first two examples, skip to the bottom. Those examples are a bit cooler.

## Installation

For ``pyg``, we need quite a few requirements.  Installation right now is pretty manual, but this should do the trick on unix systems:

```bash
pip install numpy scipy matplotlib colours
mkdir ~/util
cd ~/util
git clone https://github.com/alexhagen/pyg -b master pyg
sudo echo "export PYTHONPATH=${PYTHONPATH}:~/util" >> ~/.bashrc
source ~/.bashrc
```

and then we can just import pyg whenever with


```python
from pyg import twod as pyg2d
```

## Usage

``pyg`` has one main class, a ``twod`` plot type, and it has several other classes. The ``table`` module has some table printing help for Jupyter notebooks and some LaTeX publication helper functions.  The ``threed`` module has some ``matplotlib`` three dimensional plotting (this is good for surface plotting, if you're doing geometric visualization, use my [``pyb``](github.com/alexhagen/pyb) class, which I'll include into ``pyg`` soon), ``three2twod`` is a class for annotating three dimensional plotting (if you have the transformation matrix from 3-d to 2-d).  I've created some informative examples of these below.

### Line Plotting

The simplest plotting in ``pyg`` is line plotting, and the following two figures show the api for plotting a line with its associated uncertainty.


```python
import numpy as np

x = np.linspace(0.0, 4.0 * np.pi, 1000)
y = np.sin(x)
u_y = 0.1

plot = pyg2d.pyg2d()
plot.add_line(x, y, linestyle='-', linecolor='#285668', yerr=u_y, error_fill=True,
              name=r'$\sin \left( \theta \right)$')

plot.xlabel('x-coordinate ($x$) [$\unit{cm}$]')
plot.ylabel('y-coordinate ($y$) [$\unit{cm}$]')

plot.lines_on()
plot.markers_off()

plot.export('_static/line', ratio='silver')
plot.show(caption='some caption')
```



				<div class='pygfigure' name='['somecaption']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/line.svg?387964143' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 1:</b> some caption</div>
				</div>
			



```python
x = np.linspace(0.0, 4.0 * np.pi, 1000)
y = 5.0 * np.cos(x)
u_y = 1.0
x_sparse = np.linspace(0.0, 4.0 * np.pi, 10)
y_sparse = 5.0 * np.cos(x_sparse)
u_y_sparse = 1.0

plot = pyg2d.pyg2d()
plot.add_line(x, y, linestyle='-', linecolor='#fc8d82', yerr=u_y, error_fill=True,
              name=r'$\sin \left( \theta \right)$')
plot.add_line(x_sparse, y_sparse, linecolor='#000000', yerr=u_y_sparse,
              name=r'sparse')
plot.lines_on()
plot.markers_off()
plot.lines['sparse'].set_alpha(1.0)
plot.lines['sparse'].set_markersize(6)
plot.lines['sparse'].set_linewidth(0.0)

plot.export('_static/err', ratio='silver')
plot.show(caption='Sinusoid with uncertainty and a sparsely sampled sinusoid with uncertainty')
```



				<div class='pygfigure' name='['Sinusoidwithuncertaintyandasparselysampledsinusoidwithuncertainty']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/err.svg?175877497' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 2:</b> Sinusoid with uncertainty and a sparsely sampled sinusoid with uncertainty</div>
				</div>
			


### Dual Axis Plotting

The following figure shows the API for plotting data on concurrent axes.  There are two different APIs to this:  the first requires you to plot your data, and then define a function that converts one axis to another.  The other API requires you to plot two different data sets on axes with different limits.


```python
x = np.linspace(0., 4.0 * np.pi, 1000)
y1 = 1.0 * np.sin(x)
y2 = 5.0 * np.cos(x)

plot = pyg2d.pyg2d()
plot.add_line(x, y1, linecolor='#fc8d82', name='$y_{1}$')
plot.add_line_yy(x, y2, linecolor='#285668', name='$y_{2}$')
plot.markers_off()

plot.xlabel('x coordinate ($x$)')
plot.ylabel('y coordinate ($y_{1}$)')
plot.ylabel('y coordinate ($y_{2}$)', axes=plot.ax2)
plot.legend(loc=3)

plot.export('_static/dual', ratio='silver')
plot.show('Sinusoids with the same $x$ axis, on different $y$ axes')
```



				<div class='pygfigure' name='['Sinusoidswiththesamexaxisondifferentyaxes']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/dual.svg?226024080' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 3:</b> Sinusoids with the same $x$ axis, on different $y$ axes</div>
				</div>
			


The next figure shows how you can compare a single function against different ordinate axes.  This would be useful if you are comparing different units, but I particularly use it when there is some electrical measurement that is calibrated non-linearly (for example, in gamma spectroscopy).


```python
x = np.linspace(0., 4.0 * np.pi, 1000)
y = 1.0 * np.sin(x)

plot = pyg2d.pyg2d()
plot.add_line(x, y, linecolor='#285668', name='$y$')
plot.markers_off()

def pi_div(x):
    return x / np.pi
plot.add_xx(pi_div)

plot.xlabel('x coordinate ($x$) [$\unit{cm}$]')
plot.xlabel('x coordinate in terms of $\pi$ ($x$) [$\unit{\pi}$]', axes=plot.ax2)
plot.ylabel('y coordinate ($y$) [$\unit{cm}$]')

plot.export('_static/dualx', ratio='silver')
plot.show('Sinusoid in terms of radians and in terms of $\pi$')
```



				<div class='pygfigure' name='['Sinusoidintermsofradiansandintermsofpi']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/dualx.svg?931079291' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 4:</b> Sinusoid in terms of radians and in terms of $\pi$</div>
				</div>
			


### Three Dimensional Plotting

The following shows an example for 3d plotting using ``pyg``, which is generally simple except for the conversion from matrix data into a form that can be plotted.  Below shows a simple example for a power fit, but an API is soon coming for converting data into the right formats.


```python
from pyg import threed as pyg3d

plot = pyg3d.pyg3d()
x = np.linspace(0.0, 5.0)
y = np.linspace(0.0, 5.0)
X, Y = np.meshgrid(x, y)
z = np.power(X, 2.0) - np.power(Y, 3.0)
plot.surf(x, y, z)
plot.export('_static/threed_surf')
plot.show(caption='An arbitrary three dimensional surface')
```



				<div class='pygfigure' name='['Anarbitrarythreedimensionalsurface']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/threed_surf.svg?775124085' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 5:</b> An arbitrary three dimensional surface</div>
				</div>
			


### Two to Three Dimensional Plotting

The description of 3 dimensional geometry by annotation is difficult in the best circumstances, but very few things are "best circumstances".  Most of the field of visualization relies on software specifically designed for visualization, such as ``VTK`` and its derivatives.  This is very powerful, but for someone analyzing data or writing simulations, the last thing they want to do is write an interface to these programs.  So, I've written a quick and easy API to keep all the data in Python and visualize the geometry in Blender.  Then, I have an interface for which the code can extract the camera parameters of an exported render, and then the user can plot two dimensional annotations overtop of the three-dimensional geometry, in place.  A more advanced example is coming, but a rudimentary example is shown below.


```python
from pyg.pyb import pyb
from pyg import three2twod as pyg32d

scene = pyb.pyb()
scene.rpp(c=(0., 0., 0.), l=(100., 100., 100.), name='cube')
scene.flat(color="#E3AE24", name='newgold')
scene.set_matl(obj='cube', matl='newgold')
scene.rpp(c=(0., 0., -65.), l=(500., 500., 30.), name='floor')
scene.flat(color='#888888', name='gray')
scene.set_matl(obj='floor', matl='gray')
scene.run('_static/blenderrender.png')
plot = pyg32d.ann_im('_static/blenderrender.png')
plot.add_data_pointer(0., 0., 0., string=r'$\vec{c} = \left( 0, 0, 0 \right)$',
                   place=(-500., 200.))
plot.add_legend_entry(color="#E3AE24", name='Cube')\
    .add_legend_entry(color='#888888', name='Floor')
plot.legend(loc=2)
plot.export('_static/ann_im', ratio='golden')
plot.show('Using two dimensional annotations on a three dimensional geometric plot')
```



				<div class='pygfigure' name='['Usingtwodimensionalannotationsonathreedimensionalgeometricplot']' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
					<img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/ann_im.svg?1230673266' />
					<div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 6:</b> Using two dimensional annotations on a three dimensional geometric plot</div>
				</div>
			

