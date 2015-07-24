import math
import numpy as np
from ..plotting import twod as ahp
from ..calc import func as ahm

class fluid(object):
    # a limit of error in iteration to find pressure
    epsilon_p = 1.0E-1;
    # a limit of error in iteration to find temperature
    epsilon_T = 1.0E-5;
    R = 8.3145;
    def __init__(self,name=None):
        if name.lower() == 'acetone':
            self.P_c = 4690000.0;
            self.T_c = 508.100;
            P_b = [ 1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.,16.,17.,
                18.,19.,20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,31.,32.,33.,
                34.,35.,36.,37.,38.,39.,40.,41.,42.,43.,44.,45.,46.,47.,48.,49.,
                50.,51.,52.,53.,54.,55.,56.,57.,58.,59.,60.,61.,62.,63.,64.,65.,
                66.,67.,68.,69.,70.,71.,72.,73.,74.,75.,76.,77.,78.,79.,80.,81.,
                82.,83.,84.,85.,86.,87.,88.,89.,90.,91.,92.,93.,94.,95.,96.,97.,
                98.,99.,100.,101.,102.,103.,104.,105.,106.,107.,108.,109.,110.,
                111.,112.,113.,114.,115.,116.,117.,118.,119.,120.,121.,122.,
                123.,124.,125.,126.,127.,128.,129.,130.,131.,132.,133.,134.,
                135.,136.,137.,138.,139.,140.,141.,142.,143.,144.,145.,146.,
                147.,148.,149.,150.,151.,152.,153.,154.,155.,156.,157.,158.,
                159.,160.,161.,162.,163.,164.,165.,166.,167.,168.,169.,170.,
                171.,172.,173.,174.,175.,176.,177.,178.,179.,180.,181.,182.,
                183.,184.,185.,186.,187.,188.,189.,190.,191.,192.,193.,194.,
                195.,196.,197.,198.,199.,200. ];
            T_b = [ 237.48,247.36,253.59,258.25,262.00,265.17,267.91,270.35,
                272.54,274.53,276.36,278.06,279.65,281.14,282.54,283.87,285.12,
                286.32,287.47,288.57,289.62,290.63,291.61,292.55,293.45,294.33,
                295.19,296.01,296.82,297.60,298.36,299.10,299.82,300.52,301.21,
                301.88,302.53,303.18,303.80,304.42,305.02,305.61,306.19,306.76,
                307.32,307.87,308.41,308.94,309.46,309.97,310.47,310.97,311.46,
                311.94,312.41,312.88,313.34,313.80,314.24,314.69,315.12,315.55,
                315.98,316.40,316.81,317.22,317.62,318.02,318.42,318.81,319.19,
                319.57,319.95,320.32,320.69,321.06,321.42,321.77,322.13,322.48,
                322.83,323.17,323.51,323.85,324.18,324.51,324.84,325.16,325.48,
                325.80,326.12,326.43,326.74,327.05,327.35,327.65,327.96,328.25,
                328.55,328.84,329.13,329.42,329.71,329.99,330.27,330.55,330.83,
                331.10,331.38,331.65,331.92,332.19,332.45,332.71,332.98,333.24,
                333.50,333.75,334.01,334.26,334.51,334.76,335.01,335.26,335.50,
                335.75,335.99,336.23,336.47,336.71,336.94,337.18,337.41,337.64,
                337.87,338.10,338.33,338.56,338.78,339.01,339.23,339.45,339.67,
                339.89,340.11,340.33,340.54,340.76,340.97,341.18,341.39,341.60,
                341.81,342.02,342.23,342.43,342.64,342.84,343.04,343.25,343.45,
                343.65,343.85,344.04,344.24,344.44,344.63,344.83,345.02,345.21,
                345.40,345.59,345.78,345.97,346.16,346.35,346.53,346.72,346.90,
                347.09,347.27,347.45,347.63,347.82,348.00,348.17,348.35,348.53,
                348.71,348.88,349.06,349.23,349.41,349.58,349.76,349.93,350.10,
                350.27,350.44,350.61 ]
            self.T_b_curve = ahm.curve(np.array(P_b)*1.0E3,np.array(T_b));
            self.M = 58.0791/1000.0;
            self.omega = 0.625;
        if name.lower() in ['dfp','decafluoropentane']:
            self.P_c = 2070000.;
            self.T_c = 457.;
            self.T_b_curve = ahm.curve();
            self.M = 252.055032;
            self.omega = 0.62;
    def tait_const(self,T_r):
        a = -9.070217
        b = 62.45326;
        d= -135.1102;
        f = 4.79594;
        g = 0.250047;
        h = 1.14188;
        j = 0.0861488;
        k = 0.0344483;
        e = np.exp(f + g*self.omega + h*self.omega**2);
        B = self.P_c * (-1. + a*np.power((1.-T_r),(1./3.)) + \
            b*np.power((1.-T_r),(2./3.)) + d*(1.-T_r) + \
            e*np.power((1.-T_r),(4./3.)));
        C = j + k*self.omega**2;
        return (B,C);

    def hankinson_thomson(self):
        a = 0.2851686;
        b = -0.06379110;
        c = 0.01379173;
        V_o = self.R*self.T_c * (a + b*self.omega +c*self.omega**2.0)/self.P_c;
        return V_o;

    def tait_vs(self,T_r,V_o):
        a = -1.52816;
        b = 1.43907;
        c = -0.81446;
        d = 0.190454;
        e = -0.296123;
        f = 0.386914;
        g = -0.0427258;
        h = -0.0480645;
        V_r_0 = 1. + a*np.power((1.-T_r),(1./3.)) + \
            b*np.power((1.-T_r),(2./3.)) + c*(1.-T_r) + \
            d*np.power((1.-T_r),(4./3.));
        V_r_delta = (e + f*T_r + g*T_r**2 + h*T_r**3)/(T_r - 1.0001);
        V_s = V_o * V_r_0 * (1.-self.omega*V_r_delta);
        return V_s;

    def riedel(self,T_r,T_br):
        psi_b = -35. + 36./T_br + 42.*np.log(T_br) - T_br**6;
        h = T_br * np.log(self.P_c*1.E-5/1.01325)/(1.-T_br);
        K = 0.373-0.030*h;
        alpha_c = (3.758*K*psi_b + \
            np.log(self.P_c*1.E-5/1.01325))/(K*psi_b - np.log(T_br));
        Q = K*(3.758 - alpha_c);
        A_ant = -35.*Q;
        B_ant = -36.*Q;
        C_ant = 42.*Q + alpha_c;
        D_ant = -Q;
        P_s = np.exp(A_ant - \
            (B_ant/T_r) + C_ant*np.log(T_r) + D_ant*T_r**6);
        return P_s;

    def rho(self,T,P):
        # determine the reduced temperature from common definitions
        T_r = np.divide(T,self.T_c);
        # determine the constats using tait's definitions
        (B,C) = self.tait_const(T_r);
        # determine the characteristic volume from hankinson-thomson's
        # correlation
        V_o = self.hankinson_thomson();
        # determine the saturation volume from tait's definition
        V_s = self.tait_vs(T_r,V_o);

        T_b = self.T_b_curve.at(P);
        T_br = T_b/self.T_c;
        # determine the saturation pressure from the riedel equation
        P_s = self.riedel(T_r,T_br);
        # finally use the tait equation to determine the molar volume
        V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
        # calculate the density from that molar volume and return it
        rho = self.M/np.array(V);
        return rho;
    def p(self,T,rho):
        # determine the reduced temperature from common definitions
        T_r = np.divide(T,self.T_c);
        # determine the constats using tait's definitions
        (B,C) = self.tait_const(T_r);
        # determine the characteristic volume from hankinson-thomson's
        # correlation
        V_o = self.hankinson_thomson();
        # determine the saturation volume from tait's definition
        V_s = self.tait_vs(T_r,V_o);
        # assume P is atmospheric so we can iterate
        P = 101325.0;
        P_last = 0.0;
        while np.sqrt((P - P_last)**2) > self.epsilon_p:
            self.T_b = self.T_b_curve.at(P);
            # determine the reduced boiling temperature from common definitions
            T_br = self.T_b/self.T_c;
            # determine the saturation pressure from the riedel equation
            P_s = self.riedel(T_r,T_br);
            # finally use the tait equation to determine the molar volume
            V = V_s * (1.0 - C * np.log((B + P)/(B + P_s)));
            # save the pressure for our iteration
            P_last = P;
            P = ((B + P_s)*np.exp((1.-(V/V_s))/C)) - B;
        return P;
