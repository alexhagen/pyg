import math
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ah_py.plotting import twod as ahp
from ah_py.calc import func as ahm
from ah_py.simulation import fluids as ahf
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy import interpolate

ace = ahf.fluid('acetone');
T = np.linspace(275.,325.,90);
P = np.linspace(5000.,105000.,100);

Ta,Pa = np.meshgrid(T,P);
T_c_a = (Ta[:-1,1:] - Ta[:-1,:-1])/2.0 + Ta[1:,:-1];
P_c_a = (Pa[1:,:-1] - Pa[:-1,:-1])/2.0 + Pa[:-1,1:];
c_a = np.zeros_like(T_c_a);
for i in range(len(P)-1):
    for j in range(len(T)-1):
        c_a[i,j] = ace.c(T_c_a[i,j],P_c_a[i,j]);

mask = ace.T_b_curve.at(P_c_a) <= T_c_a;
c_a = np.ma.masked_where(mask,c_a);

### use azevedos correlation now
a = [ [ 2.55504E3,4.28692E1,-2.20070 ],\
    [ -8.34018,-3.19580E-1,1.28060E-2 ],\
    [ 6.31423E-3,7.35340E-4,-1.7663E-5 ] ];
b = [ [ 1.00000,6.32893E-2,-1.54202E-3 ],\
    [ -1.20021E-3,-5.01416E-4,9.37898E-6 ],\
    [ -1.08291E-6,1.06248E-6,-1.39463E-8 ] ];

top = np.zeros_like(T_c_a);
bottom = np.zeros_like(P_c_a);

for i in range(3):
    for j in range(3):
        top = top + a[i][j] * np.power(T_c_a,i) * np.power(P_c_a/1.0E6,j);
        bottom = bottom + b[i][j] * np.power(T_c_a,i) * np.power(P_c_a/1.0E6,j);

c_azev = np.divide(top,bottom);

boiling = ace.T_b_curve;
boiling_plot = boiling.plot();
boiling_plot.lines_on();
boiling_plot.markers_off();
residual = np.absolute((c_a-c_azev)/c_a)*100.;
c = interpolate.interp2d(T[:-1],P[:-1],residual);
plt.pcolormesh(P_c_a, T_c_a, residual, \
    cmap=\
    mpl.colors.LinearSegmentedColormap.from_list('PU',["#ffffff","#E3AE24"],\
    N=1024),edgecolors='face'
    );
cbar = plt.colorbar();
cbar.set_label(\
    'Residual Sound Velocity ($\\frac{|c_{tait}-c_{azev}|}{c_{tait}}$) [$\%$]')
boiling_plot.ylim(275.,325.);
boiling_plot.xlim(5000.,105000.);
boiling_plot.xlabel('Pressure ($p$) [$Pa$]');
boiling_plot.ylabel('Temperature ($T$) [$K$]');
c_stp = c(298.73,101325.);
print c_stp;
stp_str = '$\\frac{|c_{tait}-c_{azev}|}{c_{tait}} \left( STP \\right) = %5.3f \%% $' % (c_stp);
boiling_plot.add_data_pointer(101325.,point=298.73,\
    string=stp_str,\
    place=(60000.,310.))
boiling_plot.export('c_ace',
    formats=['png','pgf'],sizes=['2']);
