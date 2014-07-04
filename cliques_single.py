# Written 2/7/14 by dh4gan
# Generates a collection of civilisations with some distribution in space and arrival time
# Then calculates causally connected groups

import galaxy as gal
import params
from sys import argv

# Read in input parameters from file

if len(argv)==1:
    paramfile = raw_input("Enter the parameter file: ")
elif len(argv)==2:
    paramfile = argv[1]    

nciv, rinner,router,rscale, zmin,zmax, mu_life,sigma_life,mu_t,sigma_t = params.read_parameters_single(paramfile)

iseed = -45

# Generate a galaxy of civilisations - start with empty galaxy

myGalaxy = gal.galaxy(nciv, iseed)

# Place civilisations in space

myGalaxy.generate_uniform_GHZ(rinner, router, zmin, zmax)
#myGalaxy.generate_exponential_GHZ(rinner, router,rscale, zmin, zmax)

# Place civilisations in time

#myGalaxy.generate_uniform_arrival_time(tmin, tmax)
myGalaxy.generate_gaussian_arrival_time(mu_t,sigma_t)

# Distribution of civilisation lifetimes

myGalaxy.generate_fixed_lifetimes(mu_life)
#myGalaxy.generate_gaussian_lifetimes(mu_life, sigma_life)

# Now that Galaxy is set up, arrange civilisations by arrival time and construct groups

myGalaxy.sort_by_arrival_time()
myGalaxy.check_for_groups()
myGalaxy.count_groups()
myGalaxy.get_group_sizes()

print "There are ", myGalaxy.ngroups, " groups, with latest group established by civilisation ", myGalaxy.groupmax
print "Counts: ", myGalaxy.groupcount
print "Sizes: ", myGalaxy.groupsizes
# Plot this galaxy and its groups

myGalaxy.arrival_time_histogram()
myGalaxy.plot_spatial2D()

# Write data to outputfile
outputfile = 'output.single'

myGalaxy.output_group_statistics(outputfile)

