import pycurl
from StringIO import StringIO

def read_endf_line(line):
	#slice the first 66 characters
	line = line[0:65];
	#split the line into 11 width segments
	E = [];
	Edata = [];
	xs = [];
	xsdata = [];
	E.append(line[0:10]);
	xs.append(line[11:21]);
	E.append(line[22:32]);
	xs.append(line[33:43]);
	E.append(line[44:54]);
	xs.append(line[55:65]);
	for string in E:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			Edata.append(float(pre)*10.0**float(post));
	for string in xs:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			xsdata.append(float(pre)*10.0**float(post));
	return (np.array(Edata),np.array(xsdata));

def import_endf(filename):
	data = [line.strip() for line in open(filename, 'r')];
	#find the line ending with 099999
	(start_end,) = np.where([line.endswith("099999") for line in data]);
	#skip the next four lines
	data = np.array(data[start_end[0]+5:start_end[1]])
	#read in the lines between this and the next 099999
	
	E = [0.0];
	xs = [0.0];
	for line in data:
		(Edata,xsdata) = read_endf_line(line);
		for erg in Edata:
			E.append(erg);
		for sigma in xsdata:
			xs.append(sigma);
	E.append(np.max(E)+1.0);
	xs.append(0.0);
	E = np.array(E)/1.0E6; # convert to MeV
	return (E,np.array(xs));

# read in the data from endf
buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://t2.lanl.gov/nis/data/data/ENDFB-VII-gamma/H/2')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
if "<title>404 Not Found</title>" in body:
	raise Exception('ENDF has no entry for that reaction on that nuclide');
else:
	print(body)
