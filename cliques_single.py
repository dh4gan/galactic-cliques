# Written 2/7/14 by dh4gan
# Generates a collection of civilisations with some distribution in space and arrival time
# Then calculates causally connected groups

import galaxy as gal

# Generate a galaxy of civilisations

nciv = 500
xmax = ymax = 5.0 
zmax = 0.0

rinner = 6.0
router = 10.0
rscale = 3.0

zmin = 0.0


mu_t = 5000.0
sigma_t = 1.0

tmin = mu_t - 5.0*sigma_t
tmax = mu_t + 5.0*sigma_t


myGalaxy = gal.galaxy(nciv)
#myGalaxy.generate_uniform_spatial_distribution(xmax,ymax,zmax)
myGalaxy.generate_uniform_GHZ(rinner, router, zmin, zmax)
#myGalaxy.generate_exponential_GHZ(rinner, router,rscale, zmin, zmax)
#myGalaxy.generate_uniform_arrival_time(tmin, tmax)
myGalaxy.generate_gaussian_arrival_time(tmin, tmax,mu_t,sigma_t)

myGalaxy.sort_by_arrival_time()

# Loop over all possible civilisation pairs and check for connections

myGalaxy.check_for_groups()
myGalaxy.count_groups()

print "There are ", myGalaxy.ngroups, " groups, with latest group established by civilisation ", myGalaxy.groupmax

print len(myGalaxy.groupcount)
print len(myGalaxy.groupID)

# Plot this galaxy and its groups

myGalaxy.arrival_time_histogram()
myGalaxy.plot_spatial2D()

# Write data to outputfile
outputfile = 'single.output'

myGalaxy.output_group_statistics(outputfile)

