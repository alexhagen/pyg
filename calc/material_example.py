# example of usage for ndata module

# create a material object
cargo = new ndata.material();
# alternative usage
#	cargo = new ndata.material(mass='1900 g');
#   cargo = new ndata.material(volume='1500 cc');

# define it physically by weight
cargo.set_mass(1900,unit='g');
#cargo.set_mass('1900 g');

# add a nuclide by weight percent or volume percent 
# or weight or volume
cargo.add_nuclide('H-2',rho='1.00 g/cc',wo=100);
# alternative usage
#	cargo.add_nuclide('H-2',rho='1.00 g/cc',vo=100);
#   cargo.add_nuclide('H-2',rho='1.00 g/cc',mass='1900 g');
#   cargo.add_nuclide('H-2',rho='1.00 g/cc',volume='1500 cc');

# add a reaction of interest
cargo.add_reaction('g,n');

# export the cross section
E,xs = cargo.get_micro_xs();
# alternative usage
#	E,xs = cargo.get_micro_xs(Emin=0,Emax=10);

# export an MCNP card
print cargo.get_mcnp_card();

# get a spectrum
E,theta = loadtxt("/some/path/to/some/spectrum.txt");

# determine a spectrum averaged cross section
E,xs = cargo.get_sa_micro_xs(E,theta);