import math
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ahpy.plotting import twod as ahp
from ahpy.calc import func as ahm
from ahpy.calc import ndata as ahs

# USE SI UNITS

# some values from NIST WEBBOOK for density at pressure and temperature
p_g = [ 0.7,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,
  16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,
  31.0,32.0,33.0 ];
p_g = np.array(p_g)*1.0E3;
u_rho_g = [ 1.1e-6,2.2e-6,8.7e-6,2.0e-5,3.5e-5,5.5e-5,7.9e-5,0.00011,0.00014,
  0.00018,0.00022,0.00027,0.00032,0.00038,0.00044,0.00051,0.00058,0.00065,
  0.00073,0.00082,0.00091,0.0010,0.0011,0.0012,0.0013,0.0014,0.0016,0.0017,
  0.0018,0.0020,0.0021,0.0023,0.0024,0.0026 ];
rho_g = [ 0.0163079,0.0233024,0.0466412,0.070016,0.093428,0.116877,0.140363,
  0.16389,0.18745,0.21105,0.23468,0.25836,0.28207,0.30582,0.32961,0.35344,
  0.37731,0.40121,0.42516,0.44915,0.47317,0.4972,0.5213,0.5455,0.5697,
  0.5939,0.6182,0.6425,0.6669,0.6913,0.7157,0.7402,0.7647,0.7893 ];
p_l = [ 40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,
  170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0 ];
p_l = np.array(p_l)*1.0E3;
rho_l = [ 782.57,782.58,782.59,782.60,782.61,782.62,782.63,782.64,782.65,782.66,
  782.67,782.68,782.69,782.70,782.71,782.72,782.73,782.74,782.75,782.76,
  782.77,782.78 ];
u_rho_l = [ 0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,
    0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62 ];
M = 58.0791/1000.0;
V_g = np.divide(M,rho_g);
V_l = np.divide(M,rho_l);
u_V_g = - np.multiply(u_rho_g,np.divide(M,np.power(rho_g,2.0)));
u_V_l = - np.multiply(u_rho_l,np.divide(M,np.power(rho_l,2.0)));

p_l_250 = [ 40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,
    160.0,170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0 ];
p_l_250 = np.array(p_l_250)*1.0E3;
rho_l_250 = [ 837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,837.0,
    837.0,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1,837.1];
V_l_250 = np.divide(M,rho_l_250);

'''
########################## ONLY WORKS FOR GAS PHASE ############################
rho_val = np.linspace(np.min(rho_g),np.max(rho_g),5000);
R = 8.3145; # Common definitions in m^3 Pa / mol K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

a = 27.0 * np.power(R,2.0) * np.power(T_c,2.0) / (64.0 * P_c);
# [ Pa * m^6 / mol^2]
b = R * T_c / (8.0 * P_c); # [ m^3 / mol ]

# calculating a and b correctly!!
M = 58.0791/1000.0; # [ kg / mol ]

T = 300.0; # [ K ]

V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V-b)) - (a/(np.power(V,2.0))) \
    for V in V_val ];

rho_g_curve = ahm.curve(V_g,p_g,u_x=u_V_g,name='$\\rho_{g}$');
vdw_plot = rho_g_curve.plot();
vdw = ahm.curve(V_val,P,name='VDW');
vdw_plot = vdw.plot(addto=vdw_plot);
vdw_plot.lines_on();
vdw_plot.markers_off();
vdw_plot.lines['$\\rho_{g}$'].set_linewidth(0.0);
vdw_plot.lines['$\\rho_{g}$'].set_markersize(6);
vdw_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
vdw_plot.ylabel('Pressure ($p$) [$Pa$]');
vdw_plot.legend();
vdw_plot.export('vdw_g',
    formats=['png','pgf'],sizes=['cs'],customsize=[10.0,5.0]);

########################## Liquid phase inaccurate ############################
rho_val = np.linspace(np.min(rho_l),np.max(rho_l),5000);
R = 8.3145; # Common definitions in m^3 Pa / mol K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

a = 27.0 * np.power(R,2.0) * np.power(T_c,2.0) / (64.0 * P_c);
# [ Pa * m^6 / mol^2]
b = R * T_c / (8.0 * P_c); # [ m^3 / mol ]

# calculating a and b correctly!!
M = 58.0791/1000.0; # [ kg / mol ]

T = 300.0; # [ K ]

V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V-b)) - (a/(np.power(V,2.0))) \
    for V in V_val ];
rho_l_curve = ahm.curve(V_l,p_l,name='$\\rho_{l}$');
vdw_plot = rho_l_curve.plot();
vdw = ahm.curve(V_val,P,name='VDW');
vdw_plot = vdw.plot(addto=vdw_plot);
vdw_plot.lines_on();
vdw_plot.markers_off();
vdw_plot.lines['$\\rho_{l}$0'].set_linewidth(0.0);
vdw_plot.lines['$\\rho_{l}$0'].set_markersize(6);
vdw_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
vdw_plot.ylabel('Pressure ($p$) [$Pa$]');
vdw_plot.legend();
vdw_plot.export('vdw_l',
    formats=['png','pgf'],sizes=['cs'],customsize=[10.0,5.0]);

################################### PRSV #######################################

rho_val = np.linspace(np.min(rho_g),np.max(rho_g),5000);
omega = 0.30667;
T_r = np.divide(T,T_c);

# We get the kappa, alpha, and kappa_0 definitions from Stryjek
kappa_1 = -0.00888;      # Stryjek for T_r > 0.7

kappa_0 = 0.378893 + 1.4897153*omega - 0.17131848 * np.power(omega,2.0) + \
    0.0196554 * np.power(omega,3.0);
kappa = kappa_0 + kappa_1 * (1.0 - np.sqrt(T_r)) * (0.7 - T_r);
alpha = np.power((1.0 + kappa * (1.0-np.sqrt(T_r))),2.0);
a = (0.457235 * (np.power(R,2.0) * np.power(T_c,2.0) / P_c)) * alpha;
b = 0.077796 * (R * T_c / P_c);
#P = ((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)));
T = ((V-b)*(P + (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)))))/R;

#print '---------- Stryjek -------------';
#print "T(%f kPa, %f kg/m^3) = %e K" % (P,782.73,T);

T = 300.0;
V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0))) \
    for V in V_val ];

rho_g_curve = ahm.curve(V_g,p_g,u_x=u_V_g,name='$\\rho_{g}$');
prsv_plot = rho_g_curve.plot();
prsv = ahm.curve(V_val,P,name='PRSV');
prsv_plot = prsv.plot(addto=prsv_plot);
prsv_plot.lines_on();
prsv_plot.markers_off();
prsv_plot.lines['$\\rho_{g}$'].set_linewidth(0.0);
prsv_plot.lines['$\\rho_{g}$'].set_markersize(6);
prsv_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
prsv_plot.ylabel('Pressure ($p$) [$Pa$]');
prsv_plot.legend();
prsv_plot.export('prsv_g',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);

################################### PRSV #######################################

rho_val = np.linspace(np.min(rho_l),np.max(rho_l),5000);
omega = 0.30667;
T_r = np.divide(T,T_c);

# We get the kappa, alpha, and kappa_0 definitions from Stryjek
kappa_1 = -0.00888;      # Stryjek for T_r > 0.7

kappa_0 = 0.378893 + 1.4897153*omega - 0.17131848 * np.power(omega,2.0) + \
    0.0196554 * np.power(omega,3.0);
kappa = kappa_0 + kappa_1 * (1.0 - np.sqrt(T_r)) * (0.7 - T_r);
alpha = np.power((1.0 + kappa * (1.0-np.sqrt(T_r))),2.0);
a = (0.457235 * (np.power(R,2.0) * np.power(T_c,2.0) / P_c)) * alpha;
b = 0.077796 * (R * T_c / P_c);
#P = ((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)));
T = ((V-b)*(P + (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)))))/R;

#print '---------- Stryjek -------------';
#print "T(%f kPa, %f kg/m^3) = %e K" % (P,782.73,T);

T = 300.0;
V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0))) \
    for V in V_val ];

rho_l_curve = ahm.curve(V_l,p_l,name='$\\rho_{l}$');
prsv_plot = rho_l_curve.plot();
prsv = ahm.curve(V_val,P,name='PRSV');
prsv_plot = prsv.plot(addto=prsv_plot);
prsv_plot.lines_on();
prsv_plot.markers_off();
prsv_plot.lines['$\\rho_{l}$0'].set_linewidth(0.0);
prsv_plot.lines['$\\rho_{l}$0'].set_markersize(6);
prsv_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
prsv_plot.ylabel('Pressure ($p$) [$Pa$]');
prsv_plot.legend();
prsv_plot.export('prsv_l',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);
'''
'''
##################### volume translated peng-robinson ##########################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 300.0;
# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa
rho_val = np.linspace(np.min(rho_g),np.max(rho_g),50);
omega = 0.30667;
T_r = np.divide(T,T_c);

k_3 = 0.05648;
N = 0.14457;
M = 0.20473 + 0.83548*omega - 0.18470*omega**2.0 + 0.16675*omega**3.0 - \
    0.09881*omega**4.0;
alpha = np.power((1.0+M*(1.0-T_r)+N*(1.0-T_r)*(0.7-T_r)),2.0);
k_1 = 0.00185 + 0.00438*omega + 0.36322*omega**2.0 - 0.90831*omega**3.0 + \
    0.55885*omega**4.0;
k_2 = -0.00542 - 0.51112*k_3 + 0.04533*k_3**2.0 + 0.07447*k_3**3.0 - \
    0.03831*k_3**4.0;
t = R*T_c * (k_1 + k_2*(1.0-np.power(T_r,(2.0/3.0))) + \
    k_3*np.power((1.0-np.power(T_r,(2.0/3.0))),2.0))/P_c;
a = (0.45724 * (np.power(R,2.0) * np.power(T_c,2.0) / P_c)) * alpha;
b = 0.07780 * (R * T_c / P_c);

M = 58.0791/1000.0;
V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V+t-b)) - \
    (a/((V+t)*(V+t+b)+b*(V+t-b))) \
    for V in V_val ];

rho_l_curve = ahm.curve(V_g,np.array(p_g)/1.0E3,name='$\\rho_{g}$');
vtpr_plot = rho_l_curve.plot();
vtpr = ahm.curve(V_val,np.array(P)/1.0E3,name='VTPR');
vtpr_plot = vtpr.plot(addto=vtpr_plot);
vtpr_plot.lines_on();
vtpr_plot.markers_off();
vtpr_plot.lines['$\\rho_{g}$0'].set_linewidth(0.0);
vtpr_plot.lines['$\\rho_{g}$0'].set_markersize(6);
vtpr_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
vtpr_plot.ylabel('Pressure ($p$) [$kPa$]');
vtpr_plot.legend();
vtpr_plot.export('vtpr_g',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);


########################## Perturbed Hard Sphere Chain #########################
T = 300.00;  # [ K ]

M = 58.0791/1000.0; # [ kg / mol ]
k = 1.38065E-23; # common definitions in [ m^3 Pa / K ]
R = 8.3145; # Common definitions in [ m^3 Pa / mol K ]
N_A = 6.022E23; # common definitions in [ atoms / mol ]

rho_val = np.linspace(np.min(rho_g),np.max(rho_g),5000);
N_val = [ N_A * rho / M for rho in rho_val ]; # [ atom / m^3 ]

# NIST Webbook
deltaH_vap = 30920.0; # [ m^3 Pa /mol ] at 300 K

# Bondi
#A_vdw = 1.0E9 * (1.0 * 1.60 + 2.0 * 2.12)/1.0E4;  # [ m^2 / mol ]
#V_vdw = (1.0 * 11.70 + 2.0 * 13.67)/1.0E6; # [ m^3 / mol ]
# Fermeglia 1997-a
#E_coh = deltaH_vap - R * T;

# Fermeglia 1998
#m_A = 0.943; q_A = 1.355; # for refrigerants
#A_star = m_A * A_vdw + q_A;
#m_V = 0.869; q_V = 2.781;
#V_star = m_V * V_vdw + q_V;
#m_E = 2.77; q_E = -3.746;
#E_star = m_E * E_coh + q_E;
A_star = 7.226; # [ m^2 / mol ]
V_star = 43.79; # [ m^3 / mol ]
E_star = 63.630; # [ Pa m^3 / mol ]

# Solve for the three parameters
sigma = 6.0*V_star/A_star;
r = 6.0*V_star/(3.14159*sigma**3.0*N_A);
epsilon = E_star*k/(r*R);
print sigma
print r
print epsilon

# Solve for F_a, F_b
alpha_1 = 1.8681;
alpha_2 = 0.0619;
alpha_3 = 0.6715;
alpha_4 = 1.7317;
F_a = alpha_1*np.exp(-alpha_2*(k*T/epsilon)) + \
    alpha_3*np.exp(-alpha_4*np.power((k*T/epsilon),1.5));
beta_1 = 0.7303;
beta_2 = 0.1649;
beta_3 = 0.2697;
beta_4 = 2.3973;
F_b = beta_1*np.exp(-beta_2*np.sqrt((k*T/epsilon))) + \
    beta_4*np.exp(-beta_4*np.power((k*T/epsilon),1.5));

# solve for a,b
a = 2.0*3.14159*np.power(sigma,3.0)*epsilon*F_a/3.0;
b = 2.0*3.14159*np.power(sigma,3.0)*F_b/3.0;

# solve for g(d+)
b_d = np.array([ r*sigma*N/4.0 for N in N_val ]);
eta = np.array([ r*b*N/4.0 for N in N_val ]);
g_d = np.divide((1.0-np.divide(eta,2.0)),np.power((1.0-eta),3.0));

# solve for P
term1 = np.array([(r**2.0*b*N*g) for N,g in zip(N_val,g_d)]);
term2 = np.array([((r-1.0)*(g-1.0)) for g in g_d ]);
term3 = np.array([(r**2.0*a*N/(k*T)) for N in N_val ]);
denom = np.array([ (N*k*T) for N in N_val ]);
print term1
print term2
print term3
print denom
P = (1.0 + term1 - term2 - term3)*denom;

V_val = [ N/N_A for N in N_val ];

rho_g_curve = ahm.curve(V_g,p_g,u_x=u_V_g,name='$\\rho_{g}$');
phsc_plot = rho_g_curve.plot();
phsc = ahm.curve(V_val,1.0E4*P,name='PHSC');
phsc_plot = phsc.plot();
phsc_plot.lines_on();
phsc_plot.markers_off();
#phsc_plot.lines['$\\rho_{g}$'].set_linewidth(0.0);
#phsc_plot.lines['$\\rho_{g}$'].set_markersize(6);
phsc_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
phsc_plot.ylabel('Pressure ($p$) [$Pa$]');
phsc_plot.legend();
phsc_plot.export('phsc_g',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);


################################### Soave ######################################
T = 300.0;
P = 100.0;
V = M/782.73; # [ kg / mol ] / [ kg / m^3 ] [=] [ m^3 / mol ]

omega = 0.30667;
T_r = np.divide(T,T_c);
# Soave uses different definitions for kappa and alpha
kappa = 0.480 + 1.574 * omega - 0.176 * np.power(omega,2.0);
alpha = np.power((1.0 + kappa * (1.0-np.sqrt(T_r))),2.0);
a = (0.42747 * (np.power(R,2.0) * np.power(T_c,2.0) / P_c)) * alpha;
b = 0.08664 * (R * T_c / P_c);
#P = ((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)));
T = ((V-b)*(P + (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0)))))/R;
print '---------- Soave -------------';
#print "T(%f kPa, %f kg/m^3) = %e K" % (P,782.73,T);

T = 300.0;
V_val = [ M/rho for rho in rho_val ];
P = [((R*T)/(V-b)) - (a/(np.power(V,2.0) + 2.0*b*V - np.power(b,2.0))) \
    for V in V_val ];

########################## compressed liquid densities #########################
T = 300.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa
# critical density in kg/m^3
rho_c = 272.9;

omega = 0.30667;
z_c = 0.291-0.080*omega;

T_r = np.divide(T,T_c);
P_r = np.divide(P,P_c);
P_rs = np.divide(P_s,P_c);
Delta_P_r = P_r - P_rs;

E_27 = 0.714 - 1.626*np.power((1.-T_r),(1./3.)) - \
    0.646*np.power((1.0-T_r),(2./3.)) + 3.699*(1.-T_r) - \
    2.198*np.power((1.0-T_r),(4./3.));
F_27 = 0.268*np.power(T_r,2.0967) / (1.0+0.8*np.power((-np.log(T_r)),0.441));
G_27 = 0.05 + 4.221*np.power((1.01-T_r),0.75)*np.exp(-7.848*(1.01-T_r));
H_27 = -10.6 - 45.22*np.power((1.-T_r),(1./3.)) - \
    103.79*np.power((1.0-T_r),(2./3.)) + 114.44*(1.-T_r) - \
    47.38*np.power((1.0-T_r),(4./3.));
delta_rho_r_27 = E_27+F_27*np.log(Delta_P_r) + G_27*np.exp(H_27*Delta_P_r);

A = 17.4425 - 214.578*z_c + 989.625*z_c**2.0 - 1522.06*z_c**3.0;
B = -3.28257 + 13.6377*z_c + 107.4844*z_c**2.0 - 384.211*z_c**3.0;
if z_c <= 0.26:
    B = 60.2091 - 402.063*z_c + 501.0*z_c**2.0 + 641.0*z_c**3.0;
if z_c > 0.26:
    D = 0.93 - B;
else:
    D = 0.0;
rho_rs = 1.0 + A*np.power((1.-T_r),(1./3.)) + B*np.power((1.-T_r),(2./3.)) + \
    D*np.power((1.-T_r),(4./3.));

if z_c >= 0.28:
    a1 = -0.0817;
    a2 = 0.3274;
    a3 = -0.5014;
    a4 = 0.3870;
    a5 = -0.1342;
    b1 = -0.0230;
    b2 = -0.0124;
    b3 = 0.1625;
    b4 = -0.2135;
    b5 = 0.08643;
    c1 = 0.05626;
    c2 = -0.3518;
    c3 = 0.6194;
    c4 = -0.3809;
    d1 = -21.0;
    d2 = 55.174;
    d3 = -33.637;
    d4 = -28.109;
    d5 = 26.277;
elif z_c < 0.26 and z_c > 0.24:
    a1=0.0933;
    a2=-0.3445;
    a3=0.4042;
    a4=-0.2083;
    a5=0.05473;
    b1=0.0220;
    b2=-0.003363;
    b3=-0.07960;
    b4=0.08546;
    b5=-0.02170;
    c1=0.01937;
    c2=-0.03055;
    c3=0.06310;
    c4=0.0;
    d1=-16.0;
    d2=30.699;
    d3=19.645;
    d4=-81.305;
    d5=47.031;
elif z_c <= 0.24:
    a1=0.0890;
    a2=-0.4344;
    a3=0.7915;
    a4=-0.7654;
    a5=0.3367;
    b1=0.0674;
    b2=-0.06109;
    b3=0.06261;
    b4=-0.2378;
    b5=0.1665;
    c1=-0.01393;
    c2=-0.003459;
    c3=-0.1611;
    c4=0.0;
    d1=-6.550;
    d2=7.8027;
    d3=15.344;
    d4=-37.04;
    d5=20.169;
else:
    a1=0.;
    a2=0.;
    a3=0.;
    a4=0.;
    a5=0.;
    b1=0.;
    b2=0.;
    b3=0.;
    b4=0.;
    b5=0.;
    c1=0.;
    c2=0.;
    c3=0.;
    c4=0.;
    d1=0.;
    d2=0.;
    d3=0.;
    d4=0.;
    d5=0.;

I = a1 + a2*np.power((1.-T_r),(1./3.)) + \
    a3*np.power((1.0-T_r),(2./3.)) + a4*(1.-T_r) + \
    a5*np.power((1.0-T_r),(4./3.));
J = b1 + b2*np.power((1.-T_r),(1./3.)) + \
    b3*np.power((1.0-T_r),(2./3.)) + b4*(1.-T_r) + \
    b5*np.power((1.0-T_r),(4./3.));
K = c1 + c2*T_r + c3*np.power(T_r,2.0) + c4*np.power(T_r,3.0);
L = d1 + d2*np.power((1.-T_r),(1./3.)) + \
    d3*np.power((1.0-T_r),(2./3.)) + d4*(1.-T_r) + \
    d5*np.power((1.0-T_r),(4./3.));
delta_z_c = I + J*np.log(Delta_P_r) + K*np.exp(L*Delta_P_r);

rho_r = rho_rs + delta_rho_r_27 + delta_z_c;
rho_val = rho_r * rho_c;
print rho_rs * rho_c;
print delta_rho_r_27 * rho_c;
print delta_z_c * rho_c;

M = 58.0791/1000.0;

rho_l_curve = ahm.curve(p_l,rho_l,name='$\\rho_{l}$');
yw_plot = rho_l_curve.plot();
yw = ahm.curve(P,rho_val,name='YW');
yw_plot = yw.plot(addto=yw_plot);
yw_plot.lines_on();
yw_plot.markers_off();
yw_plot.lines['$\\rho_{l}$0'].set_linewidth(0.0);
yw_plot.lines['$\\rho_{l}$0'].set_markersize(6);
yw_plot.ylabel('Density ($\\rho$) [$\\nicefrac{kg}{m^{3}}$]');
yw_plot.xlabel('Pressure ($p$) [$Pa$]');
yw_plot.legend();
yw_plot.export('yw_l',
    formats=['png'],sizes=['cs'],customsize=[10.0,5.0]);
'''

############################### Thomson Brobst #################################
R = 8.3145; # Common definitions in m^3 Pa / mol K
T = 300.0; # K
P = np.linspace(np.min(p_l),np.max(p_l),50);
P_s = 33260.0; # Pa saturated pressure at 300 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);
P_r = np.divide(P,P_c);

omega = 0.30667;

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
C = j + k*omega;
e = np.exp(f + g*omega + h*omega**2.0);
B = P_c * (-1.0 + a*np.power((1.0-T_r),(1./3.)) + \
    b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));

M = 58.0791/1000.0;
a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;

V_r_delta = (e + f*T_r + g*T_r**2.0 + h*T_r**3.0)/(T_r - 1.00001);
V_r_0 = 1.0 + a*np.power((1.0-T_r),(1./3.)) + b*np.power((1.0-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));
V_s = V_o * (V_r_0)*(1.0-omega*V_r_delta);
V_val = V_s * (1.0 - C * np.log((B+P)/(B+P_s)));

rho_l_curve = ahm.curve(V_l,p_l,name='$\\rho_{l,300}$');
tb_plot = rho_l_curve.plot();
tb = ahm.curve(V_val,P,name='TB300');
tb_plot = tb.plot(addto=tb_plot);
tb_plot.lines_on();
tb_plot.markers_off();
tb_plot.lines['$\\rho_{l,300}$0'].set_linewidth(0.0);
tb_plot.lines['$\\rho_{l,300}$0'].set_markersize(6);

############################### T-B 400 C ######################################
############################### Thomson Brobst #################################
T = 250.0; # K
P = np.linspace(np.min(p_l_250),np.max(p_l_250),50);
P_s = 2382.0; # Pa saturated pressure at 400 K

# critical temperature in K
T_c = 508.100; # +/- 0.071
# critical pressure in Pa
P_c = 4690000.0; # NIST Webbook converted from 4690 +/- 150 kPa

T_r = np.divide(T,T_c);
P_r = np.divide(P,P_c);

omega = 0.30667;

a = -9.070217
b = 62.45326;
d= -135.1102;
f = 4.79594;
g = 0.250047;
h = 1.14188;
j = 0.0861488;
k = 0.0344483;
C = j + k*omega;
e = np.exp(f + g*omega + h*omega**2.0);
B = P_c * (-1.0 + a*np.power((1.0-T_r),(1./3.)) + \
    b*np.power((1.-T_r),(2./3.)) + \
    d*(1.-T_r) + e*np.power((1.-T_r),(4./3.)));

M = 58.0791/1000.0;


a = 0.2851686;
b = -0.06379110;
c = 0.01379173;
V_o = R*T_c * (a + b*omega +c*omega**2.0)/P_c;

a = -1.52816;
b = 1.43907;
c = -0.81446;
d = 0.190454;
e = -0.296123;

V_r_delta = (e + f*T_r + g*T_r**2.0 + h*T_r**3.0)/(T_r - 1.00001);
V_r_0 = 1.0 + a*np.power((1.0-T_r),(1./3.)) + b*np.power((1.0-T_r),(2./3.)) + \
    c*(1.-T_r) + d*np.power((1.-T_r),(4./3.));
V_s = V_o * (V_r_0)*(1.0-omega*V_r_delta);
V_val = V_s * (1.0 - C * np.log((B+P)/(B+P_s)));

#rho_l_curve = ahm.curve(V_l_250,p_l_250,name='$\\rho_{l,250}$');
#tb_plot = rho_l_curve.plot();
#tb = ahm.curve(V_val,P,name='TB250');
#tb_plot = tb.plot(addto=tb_plot);
#tb_plot.lines_on();
#tb_plot.markers_off();
#tb_plot.lines['$\\rho_{l,250}$0'].set_linewidth(0.0);
#tb_plot.lines['$\\rho_{l,250}$0'].set_markersize(6);
tb_plot.xlabel('Molar Volume ($\\nicefrac{M}{\\rho}$) [$\\nicefrac{m^{3}}{mol}$]');
tb_plot.ylabel('Pressure ($p$) [$Pa$]');
tb_plot.legend();
tb_plot.export('tb_l',
    formats=['png','pgf'],sizes=['cs'],customsize=[10.0,5.0]);
