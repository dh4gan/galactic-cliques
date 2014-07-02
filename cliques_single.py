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

mu_life = 0.5
sigma_life = 1.0e-3

mu_t = 5000.0
sigma_t = 10.0

myGalaxy = gal.galaxy(nciv)

# Spatial distribution of civilisations
#myGalaxy.generate_uniform_spatial_distribution(xmax,ymax,zmax)
myGalaxy.generate_uniform_GHZ(rinner, router, zmin, zmax)
#myGalaxy.generate_exponential_GHZ(rinner, router,rscale, zmin, zmax)


# Distribution of civilisation arrival times
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
outputfile = 'single.output'

myGalaxy.output_group_statistics(outputfile)

