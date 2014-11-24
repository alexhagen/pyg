# AH Python Library

An object oriented library to do lots of useful things around the MFARL.

## Features

This library contains a couple big divisions

- Data methods
	- import of data from CTMFD programs for waiting time plotting
	- import of data from pulse counter programs for comparison of radiation levels
	- import of Liquid Scintillation data files for determination of spectra
- Plotting methods
	- plotting of everything exports straight to pgf, which allows for plotting in LaTeX
	- plotting of
		- histograms
		- waiting time curves with and without regression
- Simulation methods
	- an object oriented way to model in MCNP5 for good portability and agreement across models used in the lab

## Tutorial

To install this library, make sure you have Python 2.7.3 installed, with matplotlib, pyplot, and some other packages.  For Windows, the best way is to download Anaconda python and install that (again, ensure you get 2.7.*).  For linux, the best way will be to install Spyder Python with

```bash
$ sudo apt-get -y spyder
```

Then, ensure you have Git.  For windows, download and install git bash.  For linux, you should already have git.
Then, clone this library.  Go to a directory and clone it with

```bash
$ cd /path/to/parent/dir # pick a directory to keep everything in, I use ~/code
$ git clone ssh://git@githost.ecn.purdue.edu/alexhagen/ahpy.git
```

Everytime you start writing code, you should make sure you have updated sources, so always make sure to go into the directory and pull when you start writing:

```bash
$ cd /path/to/parent/dir # go to the head of the master branch, same dir you chose
$ # before
$ git pull
```

Then, you can use it in any python file by putting the following lines or something similar in your file:

```python
# we have to add the path to find ahpy
import sys
sys.path.append("/path/to/parent/dir/");
# import only the methods you want from each submodule
from ahpy.data import ctmfd

# now you can write whatever code you want using the
# methods you imported
...
```

The current submodules and their methods are:

- data
	- ctmfd
- simulation
	- mcnp
- ahplot
	- twod

## To-Do

There's currently too much to do to write a list.  I'll fill this in as I get more comfortable with making to do lists for this project.