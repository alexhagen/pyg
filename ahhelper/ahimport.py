# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 12:24:39 2014

@author: ahagen
"""

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
        self.wt = self.wt_data[self.wt_data>0.0].sum()/self.det_data[self.wt_data>0.0].sum();
        self.wt_sigma = self.wt/math.sqrt(self.det_data[self.wt_data>0.0].sum());
        self.p_sigma = np.std(self.p_data);
        self.p = np.mean(self.p_data);

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