import numpy as np;
import datetime as dt;
import math;
from matplotlib.pyplot import close
from ..plotting import twod as ahp
from ..calc import func as ahm
from scipy import stats

class ctmfd_pressure_data(object):
    def __init__(self):
        self.wt = 0.00;
        self.wt_sigma = 0.00;
        self.p = 0.00;
        self.p_sigma = 0.00;
        self.p_desired = 0.00;
        self.p_data = np.ndarray((1,1));
        self.wt_data = np.ndarray((1,1));
        self.det_data = np.ndarray((1,1));

    def __init__(self,_p_desired,_p_data,_p_sigma_data,_wt_data,_det_data):
        self.p_desired = _p_desired;
        self.p_data = _p_data;
        self.p_sigma = 0.00;
        self.p_sigma_data=_p_sigma_data;
        self.wt_data = _wt_data;
        self.det_data = _det_data;
        self.calc();

    def calc(self):
        # remove all those that cavitated before up to speed
        p_data = self.p_data[self.wt_data > 0.0];
        p_sigma_data = self.p_sigma_data[self.wt_data > 0.0];
        det_data = self.det_data[self.wt_data > 0.0];
        wt_data = self.wt_data[self.wt_data > 0.0];
        # calculate statistics
        self.wt = wt_data.sum()/det_data.sum();
        self.wt_sigma = self.wt/math.sqrt(det_data.sum());
        self.p_sigma = np.mean(p_sigma_data);
        self.p = np.mean(p_data);
        #return plt1,plt2

    def calc_meth_1(self):
        """ In this method, we concatenate tests into one long test with many
        events.  This removes any information from cavitations at speedup and
        performs poorly for those tests with long waiting times."""
        # remove all those that cavitated before up to speed
        p_data = self.p_data[self.wt_data > 0.0];
        det_data = self.det_data[self.wt_data > 0.0];
        wt_data = self.wt_data[self.wt_data > 0.0];
        # calculate and print statistics
        print 'counts'
        print det_data.sum()
        self.wt = wt_data.sum()/det_data.sum();
        self.wt_sigma = self.wt/math.sqrt(det_data.sum());
        print self.wt_sigma
        self.p_sigma = np.std(p_data);
        self.p = np.mean(p_data);
        # find the total time
        t_tot = np.sum(wt_data);
        # find the total cavitations
        det_tot = np.sum(det_data);
        # split the time into ~20 bins, then find number of cavs in each
        bin = np.linspace(0,t_tot,num=50);
        # have the times that each cavitation occurred
        t = [];
        i = 0
        runtime = 0.0;
        while i < len(p_data)-1:
            runtime += wt_data[i];
            if det_data[i]:
                t.append(runtime);
            i += 1;
        # find which cavitations happened in which bin
        plt = ahp.ah2d();
        n,bins = plt.add_hist(t,bin);
        rate = np.divide(n,(bins[1]-bins[0]));
        invrate = np.divide(1,rate);
        del plt;
        plt = ahp.ah2d();
        bin=np.linspace(np.min(rate),np.max(rate),num=20);
        n,bins = plt.add_hist(rate,bin);
        xdata = bins[:-1];
        ydata = n;
        curve = ahm.curve(xdata,ydata);
        scale = curve.integrate(np.min(xdata),np.max(xdata));
        x_samp = np.linspace(np.min(rate),np.max(rate),num=400);
        y_samp2 = scale*stats.norm.pdf(x_samp,*stats.norm.fit(rate));
        print 'mean is:'
        print 1.0/self.wt
        print 'std is'
        print self.wt_sigma/(self.wt**2.0)
        y_samp = scale*stats.norm.pdf(x_samp,loc=1.0/self.wt,scale=self.wt_sigma/(self.wt**2.0));
        samp_curve = ahm.curve(x_samp,y_samp);
        fit = stats.norm(*stats.norm.fit(rate));
        fit_param = stats.norm.fit(rate);
        print fit_param;
        print 'mean from fit param is:'
        print 1.0/fit_param[0];
        med = fit.median();
        mu = fit.mean();
        stderr = stats.norm.interval(0.95,loc=fit_param[0],scale=fit_param[1]);
        a = 1.0*np.array(rate)
        n = len(a)
        m, se = np.mean(a), stats.sem(a,ddof=1)
        h = se * stats.norm.ppf((1+0.95)/2.)
        print m, m-h, m+h
        print np.divide(1.0,m);
        print np.divide(1.0,m-h);
        print np.divide(1.0,m+h);
        low = stderr[0] - mu;
        high = stderr[1] - mu;
        rel_err = stderr[1] - mu;
        err = rel_err / (mu**2.0);
        print err;
        #mode = 15;
        #plt.add_data_pointer(mode,samp_curve,'$\mathrm{mode} = %6.4f$' % (mode));
        plt.title('$\mu = %f \pm %f, %f$' % (mu,low,high));
        plt.add_line(x_samp,y_samp,name='$\mu=\\frac{T}{N} \pm \\frac{T}{\sqrt{N}}$',linewidth=2.0,linestyle='solid');
        plt.add_line(x_samp,y_samp2,name='fitted normal distribution',linewidth=2.0,linestyle='dotted');
        plt.markers_off();
        plt.lines_on();
        plt.add_vline(mu,0,samp_curve.at(mu),ls='dashed',lw=2.0);
        plt.add_data_pointer(mu,samp_curve,'$\mu = %6.4f$' % (1.0/mu));
        plt.xlabel('Count Rate ($\dot{c}$) [$\mathrm{\\frac{1}{s}}$]');
        plt.ylabel('Frequency ($\\nu$) [ ]');
        plt.legend();
        return plt;

    def calc_meth_2(self,dist,trans=None,invtrans=None):
        """ In"""
        # remove all those that cavitated before up to speed
        p_data = self.p_data[self.wt_data > 0.0];
        det_data = self.det_data[self.wt_data > 0.0];
        wt_data = self.wt_data[self.wt_data > 0.0];
        p_desired = self.p_desired;
        # turn all the data into single event runs (even if longer than 60 seconds)
        wt = [];
        i = 0;
        runtime = 0;
        while i < len(p_data)-1:
            runtime += wt_data[i];
            if det_data[i]:
                wt.append(runtime);
                runtime = 0.0;
            i+=1;
        self.wt = wt;
        # then we make a histogram, delete it, and take the data from it
        plt = ahp.ah2d();
        bin = invtrans(np.linspace(trans(np.min(wt)),trans(np.max(wt))));
        n,bins = plt.add_hist(wt,bin);
        xdata = bins[:-1];
        ydata = n
        del plt;
        # Now we actually plot the data
        plt = ahp.ah2d();
        plt.add_bar(xdata,ydata,name='Frequency');
        plt.xlabel('Waiting Time ($t_{wait}$) [$\mathrm{s}$]');
        plt.ylabel('Frequency ($\\nu$) [ ]');
        # Fit a distribution to it
        curve = ahm.curve(xdata,ydata);
        scale = curve.integrate(np.min(xdata),np.max(xdata));
        x_samp = invtrans(np.linspace(trans(np.min(wt)),
                             trans(np.max(wt)),
                             num=400));
        y_samp = trans(scale)*invtrans(dist.pdf(trans(x_samp),*dist.fit(trans(wt))));
        samp_curve = ahm.curve(x_samp,y_samp);
        fit = dist(*dist.fit(trans(wt)));
        med = invtrans(fit.median());
        mu = invtrans(fit.mean());
        sigma = fit.std();
        plt.add_line(x_samp,y_samp,linewidth=2.0,linestyle='solid');
        plt.markers_off();
        plt.lines_on();
        plt.add_vline(med,0,samp_curve.at(med),ls='dotted',lw=2.0);
        plt.add_data_pointer(med,samp_curve,'$M = %6.4f$' % (med));
        plt.add_vline(mu,0,samp_curve.at(mu),ls='dashed',lw=2.0);
        plt.add_data_pointer(mu,samp_curve,'$\mu = %6.4f$' % (mu));
        return plt;

    def compare_dist(self,dist,distname='Distribution'):
        # clone the data to local variables
        p_data = self.p_data[self.wt_data > 0.0];
        det_data = self.det_data[self.wt_data > 0.0];
        wt_data = self.wt_data[self.wt_data > 0.0];
        p_desired = self.p_desired;
        # turn all the data into single event runs (even if longer than 60 seconds)
        wt = [];
        i = 0;
        runtime = 0;
        while i < len(p_data)-1:
            runtime += wt_data[i];
            if det_data[i]:
                wt.append(runtime);
                runtime = 0.0;
            i+=1;
        self.wt = wt;
        # make a plot
        plt = ahp.ah2d();
        # make two open arrays
        norm_samp_means = [];
        norm_samp_ci_l = [];
        norm_samp_ci_h = [];
        dist_samp_means = [];
        dist_samp_ci_l = [];
        dist_samp_ci_h = [];
        # now, construct a dataset using only the first k points of the dataset
        # growing iteratively
        n = len(wt);
        for k in range(1,n):
            # slice the data set to only the first k points
            working_wt = wt[:k];
            # fit a distribution to the data
            dist_fit = dist.fit(working_wt);
            dist_model = dist(*dist_fit);
            if dist_model.mean() > 1000.0:
                dist_mu = float('nan');
                dist_std = float('nan');
                dist_se = float('nan');
                dist_ci_l =  float('nan');
                dist_ci_h =  float('nan');
            else:
                # find the inverse gaussian mean
                dist_mu = dist_model.mean();
                # find the inverse gaussian standard error/confidence interval
                dist_std = dist_model.std();
                dist_se = dist_std / np.sqrt(k);
                dist_ci_l =  (dist_model.ppf(0.025)-dist_mu)/np.sqrt(k);
                dist_ci_h =  (dist_model.ppf(0.975)-dist_mu)/np.sqrt(k);
            # fit a normal distribution to the data
            norm_fit = stats.norm.fit(working_wt);
            norm_model = stats.norm(*norm_fit);
            if norm_model.mean() < 1000.0:
                # find the normal mean
                norm_mu = norm_model.mean();
                # find the normal standard error/confidence interval
                norm_std = norm_model.std();
                norm_se = norm_std / np.sqrt(k);
                norm_ci_l = (norm_model.ppf(0.025)-norm_mu)/np.sqrt(k);
                norm_ci_h = (norm_model.ppf(0.975)-norm_mu)/np.sqrt(k);
            else:
                # find the normal mean
                norm_mu = float('nan');
                # find the normal standard error/confidence interval
                norm_std = float('nan');
                norm_se = float('nan');
                norm_ci_l = float('nan');
                norm_ci_h = float('nan');
            # add these to an array
            norm_samp_means.append(norm_mu);
            norm_samp_ci_l.append(norm_mu+norm_ci_l);
            norm_samp_ci_h.append(norm_mu+norm_ci_h);
            dist_samp_means.append(dist_mu);
            dist_samp_ci_l.append(dist_mu+dist_ci_l);
            dist_samp_ci_h.append(dist_mu+dist_ci_h);
        # plot these
        plt.add_line(range(1,n),norm_samp_means,name='Normal Distribution - $\mu$');
        plt.fill_between(range(1,n),norm_samp_ci_l,norm_samp_ci_h,fc='#A7A9AC',\
                         name='Normal Distribution - $\pm 1$ Standard Error');
        plt.add_line(range(1,n),dist_samp_means,name=distname+' - $\mu$');
        plt.fill_between(range(1,n),dist_samp_ci_l,dist_samp_ci_h,fc='#E3AE24',\
                         name=distname+' Distribution - CI');
        plt.lines_on();
        plt.markers_on();
        #plt.ylim(0,200);
        plt.legend();
        return plt;


class ctmfd_data(object):
    def __init__(self):
        self.ctmfd = ''; # user defined
        self.fluid = ''; # from header of file
        self.density = 0.00; # from header of file
        self.year = 0;
        self.month = 0;
        self.day = 0;
        self.start = ''; # from header of file
        self.stop = ''; # from header of file
        self.pneg_desired = np.ndarray((1,1)); # this can change
        self.source = ''; # user defined
        self.source_dist_cm = 0.00; # user defined
        self.source_shielding = 'none'; # user defined
        self.meniscus = 0.00; # from header of file
        self.temperature = 0.00; # user defined
        self.det = np.ndarray((1,1)); # this can change
        self.data_split = {}; # this is hard
        # data stuff
        self.wt = [];
        self.wt_sigma = [];
        self.p = [];
        self.p_sigma = [];

    def add_data(self,filename):
        f = open(filename,'r')
        # check if the first line has a certain syntax
        l = f.readline();
        if "Start Date: " in l:
            self.read_jeff_ctmfd_file(filename);
        else:
            self.read_alex_ctmfd_file(filename);
        for key in self.data_split:
            self.wt.append(self.data_split[key].wt);
            self.wt_sigma.append(self.data_split[key].wt_sigma);
            self.p.append(self.data_split[key].p);
            self.p_sigma.append(self.data_split[key].p_sigma);

    def read_alex_ctmfd_file(self,filename):
        """ in reading alex's input files, there is a lot better structure to
        where things are put."""
        arr=np.loadtxt(filename,delimiter=',',usecols=(0,1,2,4,5))
        self.pneg_desired = arr[:,0]
        self.pneg = arr[:,1]
        self.u_pneg = arr[:,2];
        self.time = arr[:,3]
        det = arr[:,4]
        self.det = det

        # go through and dilute the data
        for i in np.unique(self.pneg_desired):
            pneg_desired_string = "%4.2f" % (i);
            wt = ctmfd_pressure_data(i,self.pneg[self.pneg_desired==i],
                self.u_pneg[self.pneg_desired==i],
                self.time[self.pneg_desired==i],self.det[self.pneg_desired==i]);
            if pneg_desired_string not in self.data_split:
                self.data_split[pneg_desired_string] = wt;
            else:
                wt = self.data_split[pneg_desired_string];
                np.append(wt.p_data,self.pneg[self.pneg_desired==i]);
                np.append(wt.p_sigma_data,self.u_pneg[self.pneg_desired==i]);
                np.append(wt.wt_data,self.time[self.pneg_desired==i]);
                np.append(wt.det_data,self.det[self.pneg_desired==i]);
                wt.calc();
                self.data_split[pneg_desired_string] = wt;

    def read_jeff_ctmfd_file(self,filename):
        f = open(filename,'r')
        # First line is header with the start date
        l = f.readline();
        startdate = l.strip("Start Date: ");
        # Second line is header with the start time
        l = f.readline();
        starttime = l.strip(" Start Time: ");
        self.start,self.year,self.month,self.day = timestamptodatetime(starttime,startdate);
        # Third line is header with end date
        l = f.readline();
        stopdate = l.strip("Save Date: ");
        # Fourth line is header with end time
        l = f.readline();
        stoptime = l.strip(" Save Time: ");
        self.stop,_,_,_ = timestamptodatetime(stoptime,stopdate);
        # Fifth line is blank
        f.readline()
        # Sixth line is the fluid name
        l = f.readline();
        self.fluid = l.strip("Fluid: ");
        # Seventh line is the fluid name
        f.readline()
        # Eight line is blank
        f.readline()
        # Ninth line is the density
        l = f.readline();
        densitystr = l.strip(" Density: ");
        arr = densitystr.split("kg");
        self.density = float(arr[0]);
        # Tenth line is diameter
        l = f.readline();
        meniscusstr = l.strip("Diameter: ");
        arr = meniscusstr.split(" c");
        self.meniscus = float(arr[0]);
        # Eleventh line is blank
        f.readline()
        # Twelth line is the headers
        l = f.readline()
        # Close the file, we've processed the header
        f.close()
        if "IR Temp" in l:
            print 'we have temp data'
            arr=np.loadtxt(filename,skiprows=13);
            arr=arr[0:-1,:];
            self.temperature = np.mean(arr[:,12]);
        else:
            # Now read the data
            arr=np.loadtxt(filename,skiprows=13)
            arr=arr[0:-1,:]
        self.pneg_desired = arr[:,1]
        self.rps = arr[:,2]
        self.pneg = arr[:,3]
        self.time = arr[:,4]
        cavs = arr[:,5]
        det = arr[:,6]
        for i in np.arange(0,len(cavs)):
            if self.pneg_desired[i-1] == self.pneg_desired[i]:
                if cavs[i] > cavs[i-1]:
                    det[i]=True
                else:
                    det[i]=False
        self.det = det

        # go through and dilute the data
        for i in np.unique(self.pneg_desired):
            pneg_desired_string = "%4.2f" % (i);
            wt = ctmfd_pressure_data(i,self.pneg[self.pneg_desired==i],self.time[self.pneg_desired==i],self.det[self.pneg_desired==i]);
            if pneg_desired_string not in self.data_split:
                self.data_split[pneg_desired_string] = wt;
            else:
                wt = self.data_split[pneg_desired_string];
                np.append(wt.p_data,self.pneg[self.pneg_desired==i]);
                np.append(wt.wt_data,self.time[self.pneg_desired==i]);
                np.append(wt.det_data,self.det[self.pneg_desired==i]);
                wt.calc();
                self.data_split[pneg_desired_string] = wt;

    def plot_waiting_times(self):
        self.vis = ahp.ah2d();
        for key in self.data_split:
            self.vis.add_waiting_time(self);
        self.vis.add_reg_line(self.p,self.wt,regtype='exp',xerr=self.p_sigma,yerr=self.wt_sigma);
        self.vis.xlabel("Pressure ($p$) [$\mathrm{bar}$]");
        self.vis.ylabel("Waiting Time ($t_{wait}$) [$\mathrm{s}$]");
        self.vis.add_wt_info_box(self);
        return self.vis;

    def generate_figure(self):
        self.plot_waiting_times();
        filename = "%s_%s_%scm_%s_(%d_%d_%d)" % (self.ctmfd,self.source,str(self.source_dist_cm).strip('[]'),self.source_shielding,self.month,self.day,self.year)
        #self.vis.export(filename);

def timestamptodatetime(timestr,datestr):
    arr = datestr.split("/");
    month = int(arr[0])
    day = int(arr[1])
    year = int(arr[2])
    arr = timestr.split(":");
    hour = int(arr[0]);
    arr = arr[1].split();
    minute = int(arr[0])
    ampm = arr[1]
    if "PM" in ampm:
        hour = hour + 12;
    # Convert to datetime
    datetime_obj = dt.datetime(year,month,day,hour,minute);
    return datetime_obj, year, month, day;
