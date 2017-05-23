
# pyg - A graphics class

By Alex Hagen

``pyg`` started as a simple wrapper around ``matplotlib`` to help me keep my style the same in plotting, but now it's expanded to a full graphics suite.

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

The simplest plotting in ``pyg`` is line plotting, so I've crafted a little exam


```python
import numpy as np

x = np.linspace(0.0, 4.0 * np.pi, 1000)
y = np.sin(x)
u_y = 0.1

plot = pyg2d.pyg2d()
plot.add_line(x, y, linestyle='-', linecolor='#285668', yerr=u_y, name=r'$\sin \left( \theta \right)$')

plot.xlabel('x-coordinate ($x$) [$\unit{cm}$]')
plot.ylabel('y-coordinate ($y$) [$\unit{cm}$]')

plot.lines_on()
plot.markers_off()

plot.export('_static/line', ratio='silver')
plot.show('some caption')
```



                <div class='pygfigure' name='some caption' style='text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;'>
                    <img style='margin: auto; max-width:100%; width:1250.000000px; height: auto;' src='_static/line.svg?32706518' />
                    <div style='margin: auto; text-align: center;' class='figurecaption'><b>Figure 1:</b> some caption</div>
                </div>
            


### Dual Axis Plotting


```python
# coming soon
```

### Cross Referencing


```python
# coming soon
```

### Three Dimensional Plotting


```python
# coming soon
```

### Two to Three Dimensional Plotting


```python
# coming soon
```
