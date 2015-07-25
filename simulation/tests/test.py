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
rho_1 = ace.rho(325.,150000.);
p_1 = ace.p(325.,rho_1);
print p_1;

ace = ahf.fluid('acetone');
rho_1 = ace.rho(300.,101325.);
T = np.linspace(250.,350.,100);
P = np.linspace(1000.,200000.,100);

Ta,Pa = np.meshgrid(T,P);
T_rho_a = (Ta[:-1,1:] - Ta[:-1,:-1])/2.0 + Ta[1:,:-1];
P_rho_a = (Pa[1:,:-1] - Pa[:-1,:-1])/2.0 + Pa[:-1,1:];
rho_a = np.zeros_like(T_rho_a);
for i in range(len(P)-1):
    for j in range(len(T)-1):
        rho_a[j,i] = ace.rho(T_rho_a[j,i],P_rho_a[j,i]);

mask = ace.T_b_curve.at(P_rho_a) <= T_rho_a;
rho_a = np.ma.masked_where(mask,rho_a);

boiling = ace.T_b_curve;
boiling_plot = boiling.plot();
plt.pcolormesh(P_rho_a, T_rho_a, rho_a, \
    cmap=\
    mpl.colors.LinearSegmentedColormap.from_list('PU',["#ffffff","#7299C6"],\
    N=1024)
    );
cbar = plt.colorbar();
cbar.set_label('Density ($\\rho$) [$\\frac{kg}{m^{3}}$]')
boiling_plot.ylim(250.,350.);
boiling_plot.xlabel('Pressure ($p$) [$Pa$]');
boiling_plot.ylabel('Temperature ($T$) [$K$]');
boiling_plot.export('something',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);
