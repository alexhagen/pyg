#import modules
#from ..data import ctmfd
from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
#set svg as export
import matplotlib
matplotlib.use('pgf')
pgf_with_pdflatex = {
    "font.family": "serif",
    "font.serif": [],
    "axes.edgecolor": "#746C66",
    "xtick.color": "#746C66",
    "ytick.color": "#746C66",
    "text.color": "#746C66",
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "axes.labelcolor": "black",
    "xtick.labelsize": "x-small",
    "ytick.labelsize": "x-small",
    "axes.linewidth": 0.5,
    "axes.labelsize": "medium",
    "legend.fontsize": "x-small",
    "legend.frameon": False
}
matplotlib.rcParams.update(pgf_with_pdflatex)
import matplotlib.pyplot as plt
plt.close("all")
import numpy as np
#import matplotlib.animation as animation

#make the line graphing class
class ah2d:
    landscape = True;
    width = 3.25;
    height = 3.25/1.61803398875;
    plotnum = 0;
    regnum = 0;
    lines = {};
    bars = {};
    regs = {};
    leg=False;
    marker = {0: '.',
              1: ',',
              2: '+',
              3: '1',
              4: '2',
              5: '3',
              6: '4'}
    linestyle = {0: '-',
            1: '--',
            2: '-.',
            3: ':'}
    def __init__(self):
        self.fig = plt.figure();
        self.ax = self.fig.add_subplot(111);
    def xlabel(self,label):
        self.ax.set_xlabel(label);
    def ylabel(self,label):
        self.ax.set_ylabel(label);
    def legend(self):
        self.ax.legend();
    def markers_on(self):
        for key in self.lines:
            self.lines[key].set_markersize(6)
    def markers_off(self):
        for key in self.lines:
            self.lines[key].set_markersize(0)
    def lines_on(self):
        for key in self.lines:
            self.lines[key].set_lw(1.0)
    def lines_off(self):
        for key in self.lines:
            self.lines[key].set_lw(0.0)
    def add_reg_line(self,x,y,regtype='lin',name='reg',xerr=None,yerr=None):
        self.regnum = self.regnum+1;
        if name is 'reg':
            name = 'reg%d' % (self.regnum);
        # determine the regression
        if regtype.isdigit():
            # determine the coefficients of degree regtype
            coeffs = np.polyfit(x,y,regtype);
            # determine a fine grid of values
            x_fit = np.linspace(min(x),max(x),num=1000);
            y_fit = np.polyval(coeffs,x_fit);
        elif regtype is 'exp':
            x_np = np.array(x);
            x_err_np = np.array(xerr);
            y_np = np.array(y);
            y_err_np = np.array(yerr);
            #coeffs = np.polyfit(x,y_log,1);
            #x_fit = np.linspace(min(x),max(x),num=1000);
            #y_fit_log = np.polyval(coeffs,x_fit);
            #y_fit = np.exp(y_fit_log);
            def exp_func(B,x):
                return B[0]*np.exp(B[1]*x);
            
            exp_model = Model(exp_func);
            exp_data = RealData(x_np,y_np,sx=x_err_np,sy=y_err_np);
            odr = ODR(exp_data,exp_model,beta0=[0.,1.])
            out = odr.run();
            if out.res_var > 1.0 and out.beta[1] < 0.0:
                x_fit = np.linspace(min(x),max(x),num=1000);
                y_fit = exp_func(out.beta,x_fit);
                if out.sum_square < 20:
                    y_err_up = exp_func(out.beta+out.sd_beta,x_fit);
                    y_err_down = exp_func(out.beta-out.sd_beta,x_fit);
                else:
                    y_err_up = None;
                    y_err_down = None;
                    print "showing the exponential error will occlude data";
            else:
                y_fit = None;
                x_fit = None;
                y_err_up = None;
                y_err_down = None;
                print "the exponential does not fit to the data";
        elif regtype is 'log':
            print 'I haven\'t yet completed the log fitting!';            
            #do something;
        elif regtype is 'gaussian':
            def gaus(x,a,x0,sigma):
                return a*exp(-(x-x0)**2/(2*sigma**2));
            pop,pcov = curve_fit(gaus,x,y,p0=[1,np.mean(y),np.std(y)]);
            x_fit = x_fit = np.linspace(min(x),max(x),num=1000);
            y_fit = gaus(x_fit);
        # plot the regression
        if x_fit is not None and y_fit is not None:
            lines = plt.plot(x_fit,y_fit,label=name,color='#A7A9AC',ls='--');
            self.regs[name] = lines[0];
            # make sure these are lines
            lines[0].set_markersize(0);
            lines[0].set_lw(1.0);
        if y_err_up is not None and y_err_down is not None:
            uperrlines = plt.plot(x_fit,y_err_up,color='#D1D3D4',ls='--');
            downerrlines = plt.plot(x_fit,y_err_down,color='#D1D3D4',ls='--');
            self.ax.fill_between(x_fit,y_err_up,y_err_down,facecolor='#D1D3D4',alpha=0.5,lw=0.0);
            # add the regression to the dict of regressions
    def add_wt_info_box(self,ctmfd_data):
        textstr = "ctmfd: $%s$\nfluid: %s\nsource: %s at $%s\,\mathrm{cm}$\ntemperature: $%.1f\,\mathrm{\,^{o}C}$\nperformed on: %d/%d/%d" % (ctmfd_data.ctmfd,ctmfd_data.fluid,ctmfd_data.source,str(ctmfd_data.source_dist_cm).strip('[]'),ctmfd_data.temperature,ctmfd_data.month,ctmfd_data.day,ctmfd_data.year);
        posx = 1 - (0.05/1.61803398875);
        posy = 1 - (0.05);
        self.ax.text(posx, posy, textstr, transform=self.ax.transAxes, fontsize='xx-small',
        verticalalignment='top',ha='right')
    def add_line(self,x,y,name='plot',xerr=None,yerr=None):
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        line,caplines,barlinecols=plt.errorbar(x,y,label=name,color='black',xerr=xerr,yerr=yerr,marker=self.marker[self.plotnum%7],ls=self.linestyle[self.plotnum%4])
        self.lines[name] = (line)
        self.markers_on();
        self.lines_off();
    def add_bar(self,y,bins,name='plot'):
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        n,bins,patches=plt.hist(y,bins=bins,label=name,facecolor='gray',alpha=0.5);
        self.bars[name] = patches;
    def add_waiting_time(self,ctmfd_data,name='plot'):
        p = [];
        perr = [];
        wt = [];
        wterr = [];
        for key in ctmfd_data.data_split:
            p.append(ctmfd_data.data_split[key].p);
            perr.append(2*ctmfd_data.data_split[key].p_sigma);
            wt.append(ctmfd_data.data_split[key].wt);
            wterr.append(2*ctmfd_data.data_split[key].wt_sigma);
        self.add_line(p,wt,xerr=perr,yerr=wterr,name=name)
    def add_legend(self):
        self.leg=True
        self.ax.legend();
    def det_height(self):
        if self.landscape:
            self.height = self.width/1.61803398875;
        else:
            self.height = self.width*1.61803398875;
    def remove_font_sizes(self,filename):
        f=open(filename,'r')
        string = f.read()
        f.close()
        f=open(filename,'w')
        string=string.replace("\\rmfamily\\fontsize{8.328000}{9.993600}\\selectfont","\\scriptsize")
        string=string.replace("\\rmfamily\\fontsize{12.000000}{14.400000}\\selectfont","\\normalsize")       
        f.write(string)
        f.close()
    def export(self,filename):
        self.width=3.25;
        self.det_height();
        self.fig.set_size_inches(self.width,self.height);
        if self.leg:        
            self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                           ncol=2, mode="expand", borderaxespad=0.)        
        plt.savefig(filename+'_onecolumn.pgf');
        self.remove_font_sizes(filename+'_onecolumn.pgf');
        plt.savefig(filename+'_onecolumn.svg');
        self.width=6.25;
        self.det_height();
        self.fig.set_size_inches(self.width,self.height);
        if self.leg:        
            self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                           ncol=3, mode="expand", borderaxespad=0.)        
        plt.savefig(filename+'_twocolumn.pgf');
        self.remove_font_sizes(filename+'_twocolumn.pgf');
        plt.savefig(filename+'_twocolumn.svg');
        self.width=10;
        self.det_height();
        self.fig.set_size_inches(self.width,self.height);
        if self.leg:        
            self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                           ncol=4, mode="expand", borderaxespad=0.)        
        plt.savefig(filename+'_fullpage.pgf');
        self.remove_font_sizes(filename+'_fullpage.pgf');
        plt.savefig(filename+'_fullpage.svg');
