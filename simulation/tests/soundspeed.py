import math
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ah_py.plotting import twod as ahp
from ah_py.calc import func as ahm
from ah_py.simulation import fluids as ahf
from matplotlib import pyplot as plt
import matplotlib as mpl

ace = ahf.fluid('acetone');
T = np.linspace(275.,325.,100);
P = np.linspace(5000.,105000.,100);

Ta,Pa = np.meshgrid(T,P);
T_c_a = (Ta[:-1,1:] - Ta[:-1,:-1])/2.0 + Ta[1:,:-1];
P_c_a = (Pa[1:,:-1] - Pa[:-1,:-1])/2.0 + Pa[:-1,1:];
c_a = np.zeros_like(T_c_a);
for i in range(len(P)-1):
    for j in range(len(T)-1):
        c_a[j,i] = ace.c(T_c_a[j,i],P_c_a[j,i]);

mask = ace.T_b_curve.at(P_c_a) <= T_c_a;
c_a = np.ma.masked_where(mask,c_a);

boiling = ace.T_b_curve;
boiling_plot = boiling.plot();
plt.pcolormesh(P_c_a, T_c_a, c_a, \
    cmap=\
    mpl.colors.LinearSegmentedColormap.from_list('PU',["#ffffff","#E3AE24"],\
    N=1024)
    );
cbar = plt.colorbar();
cbar.set_label('Sound Velocity ($c$) [$\\frac{m}{s}$]')
boiling_plot.ylim(275.,325.);
boiling_plot.xlim(5000.,105000.);
boiling_plot.xlabel('Pressure ($p$) [$Pa$]');
boiling_plot.ylabel('Temperature ($T$) [$K$]');
boiling_plot.export('c_ace',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);
