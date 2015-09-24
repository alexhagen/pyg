# AH Plot Library Class
By Alex Hagen

The AH Plot library is a small and simple library that allows for creation of consitent plots in python.  This is optimized to be published in writeups and two column article format, and probably shouldn't be used for large scale visualizations.

## Contents
1. Installation
2. Usage
3. To Do

## 1. Installation
Obviously, python (2.7) must be installed, but also, because the library depends on matplotlib, this must also be installed.  Then, just put the file `ah_plot.py` into whatever directory you're using.

## 2. Usage
Follow the steps below to use the ah_plot class.

* Lets say we want to create some data, plot it, and then use it in a latex file.  Here's a quick line plot demo program:

```python
# in file plot_line.py
from ah_plot import ahline
import numpy as np

# create a data set - for this we can use cos and sin
x = np.arange(0.0,6.28,0.01)
y = np.sin(x)
z = np.cos(x)

# create a new object with our first plot, and then add our
#  second plot to that object
plot = ahline(x,y,name='sin');
plot.add_plot(x,z,name='cos');

# label our axes and add a legend
plot.xlabel('Time ($t$) [$\\mathrm{s}$]')
plot.ylabel('Velocity ($v$) [$\\mathrm{\\frac{m}{s}}$]')
plot.add_legend()

# make sure we only have lines, no markers
plot.markers_off()
plot.lines_on()

# now export to a file
plot.export('plot_line')
```

* To run this, we use the line

```bash
$ python plot_line.py
```

* This should generate a file named `line_plot.pgf`, this can be included in a latex document such as

```latex
%% in file plot_line.tex
% set document type as article and set up encoding
\documentclass[english]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8x]{inputenc}

% import the pgf package in the preamble
\makeatletter
\usepackage{pgf}
\makeatother

% Use babel for the language package
\usepackage{babel}

% The only thing in the body is the image
\begin{document}
\input{plot_line_onecolumn.pgf}
\end{document}
```

* This document can be compiled using

```bash
$ pdflatex plot_line.tex
```

* and viewed!

## 3. To Do
- [ ] Absolute value support (added 10/16/14)
- [ ] "Smart" change, indicating if value was changed and is still at speed (added 10/16/14)