import numpy as np;
import datetime as dt;
import math;

class ctmfd_pressure_data:
    wt = 0.00;
    wt_sigma = 0.00;
    p = 0.00;
    p_sigma = 0.00;
    p_desired = 0.00;
    p_data = np.ndarray((1,1));
    wt_data = np.ndarray((1,1));
    det_data = np.ndarray((1,1));
    
    def __init__(self,_p_desired,_p_data,_wt_data,_det_data):
        self.p_desired = _p_desired;
        self.p_data = _p_data;
        self.wt_data = _wt_data;
        self.det_data = _det_data;
        self.calc();
    
    def calc(self):
        calc_meth_1(self);
        calc_meth_2(self);
        calc_meth_3(self);
        calc_meth_4(self);
        
    def calc_meth_1(self):
        """ In this method, we concatenate tests into one long test with many
        events.  This removes any information from cavitations at speedup and
        performs poorly for those tests with long waiting times."""
        # remove all those that cavitated before up to speed
        p_data = self.p_data[self.wt_data > 0.0]
        det_data = self.det_data[self.wt_data > 0.0]
        wt_data = self.wt_data[self.wt_data > 0.0]
        # assume the entire thing is one long run with multiple events, then
        # calculate and print those statistics
        wt = wt_data.sum()/det_data.sum();
        wt_sigma = wt/math.sqrt(det_data.sum());
        p_sigma = np.std(p_data);
        p = np.mean(p_data);
        # print out the waiting time and such
        print "The waiting time was %f $\pm$ %f s at pressure of %f $\pm$ %f s" % (wt, wt_sigma, p, p_sigma)
        # histogram the data
        # do a chi squared test
        # regress with a gaussian
        
    def calc_meth_2(self):
        """ In this method, we remove the assumption of a binomial test, and
        make every test successful, but of a different time.  Then, we should
        see a normal distribution around the true value of waiting time. This 
        removes any information from cavitations at speedup"""
        # remove all those that cavitated before up to speed
        p_data = self.p_data[self.wt_data > 0.0]
        det_data = self.det_data[self.wt_data > 0.0]
        wt_data = self.wt_data[self.wt_data > 0.0]
        p_desired = self.p_desired[self.wt_data > 0.0]
        # turn all the data into single event runs (even if longer than 60 seconds)
        # calculate the average run time
        # print out the waiting time and such
        print "The waiting time was %f $\pm$ %f s at pressure of %f $\pm$ %f s" % (wt, wt_sigma, p, p_sigma)
        # histogram
        # do a chi squared test
        # regress with a gaussian
        
    def calc_meth_3(self):
        """ In this method we assume that there is a value of pressure-seconds
        that gives the data available.  This allows us to retrieve information
        about runs that cavitation before startup. """
        # clone the data to local variables
        p_data = self.p_data;
        det_data = self.det_data;
        wt_data = self.wt_data;
        p_desired = self.p_desired;
        # determine the pressure seconds required for each run (speed up is triangular, then flat)
        # determine the error with the pressure seconds
        # print data
        # histogram
        # perform a chi squared test
        # regress with a gaussian
        
    def calc_meth_4(self):
        

class ctmfd_data:
    ctmfd = ''; # user defined
    fluid = ''; # from header of file
    density = 0.00; # from header of file
    start = ''; # from header of file
    stop = ''; # from header of file
    pneg_desired = np.ndarray((1,1)); # this can change
    source = ''; # user defined
    source_dist_cm = 0.00; # user defined
    source_shielding = ''; # user defined
    meniscus = 0.00; # from header of file
    temperature = 0.00; # user defined
    det = np.ndarray((1,1)); # this can change
    data_split = {}; # this is hard
    
    def add_data(self,filename):
        f = open(filename,'r')
        # check if the first line has a certain syntax
        l = f.readline();
        if "Start Date: " in l:
            self.read_jeff_ctmfd_file(filename);
    
    def read_jeff_ctmfd_file(self,filename):
        f = open(filename,'r')
        # First line is header with the start date
        l = f.readline();
        startdate = l.strip("Start Date: ");
        # Second line is header with the start time
        l = f.readline();
        starttime = l.strip(" Start Time: ");
        self.start = timestamptodatetime(starttime,startdate);
        # Third line is header with end date
        l = f.readline();
        stopdate = l.strip("Save Date: ");
        # Fourth line is header with end time
        l = f.readline();
        stoptime = l.strip(" Save Time: ");
        self.stop = timestamptodatetime(stoptime,stopdate);
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
        f.readline()
        # Close the file, we've processed the header
        f.close()
        # Now read the data
        arr=np.loadtxt(filename,skiprows=13)
        arr=arr[0:-1,:]
        self.pneg_desired = arr[:,1]
        self.rps = arr[:,2]
        self.pneg = arr[:,3]
        self.time = arr[:,4]
        cavs = arr[:,5]
        det = arr[:,6]
        for i in np.arange(1,len(cavs)):
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
            self.data_split[pneg_desired_string] = wt;
        
    
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
    return datetime_obj;