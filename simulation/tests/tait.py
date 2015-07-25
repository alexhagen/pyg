import math
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ahpy.plotting import twod as ahp
from ahpy.calc import func as ahm
from ahpy.calc import ndata as ahs

# USE SI UNITS

# some values from NIST WEBBOOK for density at pressure and temperature
p_l_275 = [ 20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,
  170.,180.,190.,200.,210.,220.,230.,240.,250. ];
p_l_275 = np.array(p_l_275)*1.0E3;
rho_l_275 = [ 810.1,810.1,810.1,810.1,810.1,810.1,810.2,810.2,810.2,810.2,810.2,
  810.2,810.2,810.2,810.2,810.2,810.2,810.3,810.3,810.3,810.3,810.3,810.3,
  810.3 ];
p_l_325 = [ 90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,210.,
  220.,230.,240.,250. ];
p_l_325 = np.array(p_l_325)*1.0E3;
rho_l_325 = [ 753.9,753.9,754.0,754.0,754.0,754.0,754.0,754.0,754.0,754.0,754.1,
  754.1,754.1,754.1,754.1,754.1,754.1 ];
p_l = [ 40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,
  170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0 ];
p_l = np.array(p_l)*1.0E3;
rho_l = [ 782.57,782.58,782.59,782.60,782.61,782.62,782.63,782.64,782.65,782.66,
  782.67,782.68,782.69,782.70,782.71,782.72,782.73,782.74,782.75,782.76,
  782.77,782.78 ];
u_rho_l = [ 0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,
    0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62 ];
P_b = [ 0.0000010543,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,
  140.,150.,160.,170.,180.,190.,200.,210.,220.,230.,240.,250. ];
P_b = np.array(P_b)*1.0E3;
T_b = [ 140.0,274.0,287.7,296.5,303.2,308.7,313.3,317.4,321.0,324.3,327.3,330.0,
  332.6,335.0,337.3,339.5,341.5,343.5,345.4,347.1,348.9,350.5,352.1,353.7,355.2,
  356.6 ];
T_b_curve = ahm.curve(P_b,T_b);
M = 58.0791/1000.0;

p_l_250 = [ 40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,
    160.0,170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0 ];
p_l_250 = np.array(p_l_250)*1.0E3;
rho_l_250 = [ 837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,
    837.0,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1];
V_l_250 = np.divide(M,rho_l_250);

################################### Tait #######################################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 275.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);
omega = 0.625;

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
e = np.exp(f + g*omega + h*omega**2);
B = P_c * (-1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));
C = j + k*omega**2;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;
f = 0.386914;
g = -0.0427258;
h = -0.0480645;
V_r_0 = 1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));

V_r_delta = (e + f*T_r + g*T_r**2 + h*T_r**3)/(T_r - 1.0001);
a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;
V_s = V_o * V_r_0 * (1.-omega*V_r_delta);

#T_bo = np.array([ T_b_curve.at(P_o) for P_o in P ]);
T_br = 329.23/T_c;
psi_b = -35. + 36./T_br + 42.*np.log(T_br) - T_br**6;
#K = 0.0838;
h = T_br * np.log(P_c*1.E-5/1.01325)/(1.-T_br);
K = 0.373-0.030*h;
alpha_c = (3.758*K*psi_b + np.log(P_c*1.E-5/1.01325))/(K*psi_b - np.log(T_br));
Q = K*(3.758 - alpha_c);
A_ant = -35.*Q;
B_ant = -36.*Q;
C_ant = 42.*Q + alpha_c;
D_ant = -Q;
P_s = np.exp(A_ant - (B_ant/T_r) + C_ant*np.log(T_r) + D_ant*T_r**6);

V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
rho = M/np.array(V);
rho_l_curve = ahm.curve(rho_l_275,p_l_275,name='$\\rho_{l,275}$');
tb_plot = rho_l_curve.plot();
tb = ahm.curve(rho,P,name='TB275');
tb_plot = tb.plot(addto=tb_plot);

################################### Tait #######################################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 300.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
e = np.exp(f + g*omega + h*omega**2);
B = P_c * (-1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));
C = j + k*omega**2;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;
f = 0.386914;
g = -0.0427258;
h = -0.0480645;
V_r_0 = 1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));

V_r_delta = (e + f*T_r + g*T_r**2 + h*T_r**3)/(T_r - 1.0001);
a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;
V_s = V_o * V_r_0 * (1.-omega*V_r_delta);

#T_bo = np.array([ T_b_curve.at(P_o) for P_o in P ]);
T_br = 329.23/T_c;
psi_b = -35. + 36./T_br + 42.*np.log(T_br) - T_br**6;
#K = 0.0838;
h = T_br * np.log(P_c*1.E-5/1.01325)/(1.-T_br);
K = 0.373-0.030*h;
alpha_c = (3.758*K*psi_b + np.log(P_c*1.E-5/1.01325))/(K*psi_b - np.log(T_br));
Q = K*(3.758 - alpha_c);
A_ant = -35.*Q;
B_ant = -36.*Q;
C_ant = 42.*Q + alpha_c;
D_ant = -Q;
P_s = np.exp(A_ant - (B_ant/T_r) + C_ant*np.log(T_r) + D_ant*T_r**6);

V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
rho = M/np.array(V);
rho_l_curve = ahm.curve(rho_l,p_l,name='$\\rho_{l,300}$');
tb_plot = rho_l_curve.plot(addto=tb_plot);
tb = ahm.curve(rho,P,name='TB300');
tb_plot = tb.plot(addto=tb_plot);

################################### Tait #######################################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 325.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
e = np.exp(f + g*omega + h*omega**2);
B = P_c * (-1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));
C = j + k*omega**2;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;
f = 0.386914;
g = -0.0427258;
h = -0.0480645;
V_r_0 = 1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));

V_r_delta = (e + f*T_r + g*T_r**2 + h*T_r**3)/(T_r - 1.0001);
a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;
V_s = V_o * V_r_0 * (1.-omega*V_r_delta);

#T_bo = np.array([ T_b_curve.at(P_o) for P_o in P ]);
T_br = 329.23/T_c;
psi_b = -35. + 36./T_br + 42.*np.log(T_br) - T_br**6;
#K = 0.0838;
h = T_br * np.log(P_c*1.E-5/1.01325)/(1.-T_br);
K = 0.373-0.030*h;
alpha_c = (3.758*K*psi_b + np.log(P_c*1.E-5/1.01325))/(K*psi_b - np.log(T_br));
Q = K*(3.758 - alpha_c);
A_ant = -35.*Q;
B_ant = -36.*Q;
C_ant = 42.*Q + alpha_c;
D_ant = -Q;
P_s = np.exp(A_ant - (B_ant/T_r) + C_ant*np.log(T_r) + D_ant*T_r**6);

V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
rho = M/np.array(V);
rho_l_curve = ahm.curve(rho_l_325,p_l_325,name='$\\rho_{l,325}$');
tb_plot = rho_l_curve.plot(addto=tb_plot);
tb = ahm.curve(rho,P,name='TB325');
tb_plot = tb.plot(addto=tb_plot);

################################### Tait #######################################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 250.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
e = np.exp(f + g*omega + h*omega**2);
B = P_c * (-1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));
C = j + k*omega**2;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;
f = 0.386914;
g = -0.0427258;
h = -0.0480645;
V_r_0 = 1. + a*np.power((1.-T_r),(1./3.)) + b*np.power((1.-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));

V_r_delta = (e + f*T_r + g*T_r**2 + h*T_r**3)/(T_r - 1.0001);
a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;
V_s = V_o * V_r_0 * (1.-omega*V_r_delta);

#T_bo = np.array([ T_b_curve.at(P_o) for P_o in P ]);
T_br = 329.23/T_c;
psi_b = -35. + 36./T_br + 42.*np.log(T_br) - T_br**6;
#K = 0.0838;
h = T_br * np.log(P_c*1.E-5/1.01325)/(1.-T_br);
K = 0.373-0.030*h;
alpha_c = (3.758*K*psi_b + np.log(P_c*1.E-5/1.01325))/(K*psi_b - np.log(T_br));
Q = K*(3.758 - alpha_c);
A_ant = -35.*Q;
B_ant = -36.*Q;
C_ant = 42.*Q + alpha_c;
D_ant = -Q;
P_s = np.exp(A_ant - (B_ant/T_r) + C_ant*np.log(T_r) + D_ant*T_r**6);

V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
rho = M/np.array(V);
rho_l_curve = ahm.curve(rho_l_250,p_l_250,name='$\\rho_{l,250}$');
tb_plot = rho_l_curve.plot(addto=tb_plot);
tb = ahm.curve(rho,P,name='TB250');
tb_plot = tb.plot(addto=tb_plot);
tb_plot.lines_on();
tb_plot.markers_off();
tb_plot.lines['$\\rho_{l,325}$0'].set_linewidth(0.0);
tb_plot.lines['$\\rho_{l,325}$0'].set_markersize(6);
tb_plot.lines['$\\rho_{l,300}$0'].set_linewidth(0.0);
tb_plot.lines['$\\rho_{l,300}$0'].set_markersize(6);
tb_plot.lines['$\\rho_{l,275}$0'].set_linewidth(0.0);
tb_plot.lines['$\\rho_{l,275}$0'].set_markersize(6);
tb_plot.lines['$\\rho_{l,250}$0'].set_linewidth(0.0);
tb_plot.lines['$\\rho_{l,250}$0'].set_markersize(6);
tb_plot.xlabel('Density ($\\rho$) [$\\nicefrac{kg}{m^{3}}$]');
tb_plot.ylabel('Pressure ($p$) [$Pa$]');
tb_plot.legend();
tb_plot.export('tait_l',
    formats=['png','pgf'],sizes=['cs'],customsize=[10.0,5.0]);
