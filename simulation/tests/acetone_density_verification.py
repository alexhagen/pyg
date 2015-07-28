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

T_mid = T[:-1] + (T[1:] - T[:-1])/2.;
P_mid = P[:-1] + (P[1:] - P[:-1])/2.;

Ta,Pa = np.meshgrid(T,P);
T_rho_a = (Ta[:-1,1:] - Ta[:-1,:-1])/2.0 + Ta[1:,:-1];
P_rho_a = (Pa[1:,:-1] - Pa[:-1,:-1])/2.0 + Pa[:-1,1:];
rho_a = np.zeros_like(T_rho_a);
for i in range(len(P)-1):
    for j in range(len(T)-1):
        rho_a[i,j] = ace.rho(T_rho_a[i,j],P_rho_a[i,j]);

mask = ace.T_b_curve.at(P_rho_a) <= T_rho_a;
rho_a = np.ma.masked_where(mask,rho_a);

### find density from NIST
arr = np.loadtxt('acetone_density_nist.csv',delimiter="\t");
T_nist = np.array(arr[:,0]); # temperature is in the first column
P_nist = np.array(arr[:,1])*1.0E3; # pressure is in the second column in kPa
rho_nist_data = np.array(arr[:,2]); # density is in the third column
rho_interp = interpolate.interp2d(T_nist,P_nist,rho_nist_data);
rho_nist = rho_interp(T_mid,P_mid);

boiling = ace.T_b_curve;
boiling_plot = boiling.plot();
boiling_plot.lines_on();
boiling_plot.markers_off();
residual = np.absolute((rho_a - rho_nist)/rho_a)*100.;
r = interpolate.interp2d(T_mid,P_mid,residual);
plt.pcolormesh(P_rho_a, T_rho_a, residual, \
    cmap=\
    mpl.colors.LinearSegmentedColormap.from_list('PU',["#ffffff","#E3AE24"],\
    N=1024),edgecolors='face'
    );
cbar = plt.colorbar();
cbar.set_label(\
    'Residual Density ($\\frac{|\\rho_{tait}-\\rho_{nist}|}{\\rho_{tait}}$) [$\%$]')
boiling_plot.ylim(275.,325.);
boiling_plot.xlim(5000.,105000.);
boiling_plot.xlabel('Pressure ($p$) [$Pa$]');
boiling_plot.ylabel('Temperature ($T$) [$K$]');
rho_stp = r(298.73,101325.);
stp_str = '$\\frac{|\\rho_{tait}-\\rho_{nist}|}{\\rho_{tait}} \left( STP \\right) = %5.3f \%% $' % (rho_stp);
boiling_plot.add_data_pointer(101325.,point=298.73,\
    string=stp_str,\
    place=(60000.,310.))
boiling_plot.export('rho_ace',
    formats=['png','pgf'],sizes=['2']);
