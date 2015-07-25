import math
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ah_py.plotting import twod as ahp
from ah_py.calc import func as ahm
from ah_py.calc import ndata as ahs

def tait_p(T,rho,P_c,T_c,M):

def tait_t(P,rho,P_c,T_c,T_b,M):

def tait_rho(T,P,P_c,T_c,T_b,M):
    M = M / 1000.0;
    R = 8.3145; # Common definitions in m^3 Pa / mol K

    T_r = np.divide(T,T_c);
    omega = 0.62;

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
    T_br = T_b/T_c;
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
    return rho;

T=[ 250.,275.,300.,325. ];
P=[ 2380.,10600.,34900.,92400. ];
rho = [ 0.,0.,0.,0. ];
for i in range(len(P)):
    rho[i]=tait(T=T[i],P=P[i],P_c=2070000.,T_c=457.,T_b=T[i],M=252.055032);
print rho;
