#import modules
from ..ahhelper import ahimport
#set svg as export
import matplotlib
matplotlib.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
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
#import numpy as np
#import matplotlib.animation as animation

#make the line graphing class
class ah2d:
    landscape = True;
    width = 3.25;
    height = 3.25/1.61803398875;
    plotnum = 0;
    lines = {};
    bars = {};
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
