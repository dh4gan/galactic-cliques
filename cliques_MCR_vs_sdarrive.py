# Written 1/8/14 by dh4gan
# Generates a collection of civilisations with some distribution in space and arrival time
# Then calculates causally connected groups
# Repeats this to allow MCR analysis
# Repeats MCR analysis over various values of the standard deviation of arrival time

import galaxy as gal
import params
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

# Read in input parameters from file

if len(argv)==1:
    paramfile = raw_input("Enter the parameter file: ")
elif len(argv)==2:
    paramfile = argv[1]
        
nruns,nciv, rinner,router,rscale, zmin,zmax, mu_life,sigma_life,mu_t,sigma_t = params.read_parameters_mcr(paramfile)

iseed = -47

# Override definition of sigma_t, and specify the nciv values to be explored

sigma_t_values = [0.1, 0.5, 1, 5, 10]

# Set up MCR output file

outputfile = 'output.MCR'

print 'Outputting to file ', outputfile

f_obj = open(outputfile,'w')

line = 'Nciv  meanLife  sdLife  meanArrive  sdArrive '
line += 'meanNgroup  sdNgroup  meanGroupSize  sdGroupSize  meanGroupArrive  sdGroupArrive \n'

f_obj.write(line)


for sigma_t in sigma_t_values:

    # Now loop over runs

    mcr_ngroups = np.empty(0)
    mcr_groupcounts = np.empty(0)
    mcr_groupsizes = np.empty(0)
    mcr_grouparrive = np.empty(0)

    for irun in range(nruns):

        print 'Beginning run ', irun+1
        # Generate a galaxy of civilisations

        myGalaxy = gal.galaxy(nciv,iseed)

        # Spatial distribution of civilisations

        #myGalaxy.generate_uniform_GHZ(rinner, router, zmin, zmax)
        myGalaxy.generate_exponential_GHZ(rinner, router,rscale, zmin, zmax)


        # Distribution of civilisation arrival times
    
        #myGalaxy.generate_uniform_arrival_time(tmin, tmax)
        myGalaxy.generate_gaussian_arrival_time(mu_t,sigma_t)

        # Distribution of civilisation lifetimes

        myGalaxy.generate_fixed_lifetimes(mu_life)
        #myGalaxy.generate_gaussian_lifetimes(mu_life, sigma_life)

        # Arrange civilisations by arrival time and construct groups

        myGalaxy.sort_by_arrival_time()
        myGalaxy.check_for_groups()
        myGalaxy.count_groups()
        myGalaxy.get_group_sizes()

        print "There are ", myGalaxy.ngroups, " groups, with latest group established by civilisation ", myGalaxy.groupmax
        
        # Plot this galaxy and its groups

        #myGalaxy.arrival_time_histogram()
        #myGalaxy.plot_spatial2D()

        # Write data to outputfile
        #outputfile = 'output.'+str(irun)
        #myGalaxy.output_group_statistics(outputfile)
    
        print 'Run ',irun+1, ' complete'
    
        # Store the data in an array?
    
        mcr_ngroups = np.append(mcr_ngroups,np.asarray(myGalaxy.ngroups))
        mcr_groupcounts = np.append(mcr_groupcounts,np.asarray(myGalaxy.groupcount))
        mcr_groupsizes = np.append(mcr_groupsizes,np.asarray(myGalaxy.groupsizes))
        mcr_grouparrive = np.append(mcr_grouparrive,np.asarray(myGalaxy.grouparrive))
    
    print 'MCR complete - now producing means and standard deviations'


    # Groups with a single member have zero size - remove them
    mcr_groupsizes = mcr_groupsizes[np.nonzero(mcr_groupsizes)]

    # Calculate means and standard deviations
    mean_ngroups = np.mean(mcr_ngroups)
    sd_ngroups = np.std(mcr_ngroups)

    mean_groupsize = np.mean(mcr_groupsizes)
    sd_groupsize = np.std(mcr_groupsizes)

    mean_grouparrive = np.mean(mcr_grouparrive)
    sd_grouparrive = np.std(mcr_grouparrive)

    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.set_ylabel('Relative Frequency')
    ax.set_xlabel('Group Population')
    ax.hist(mcr_groupcounts, bins=100, normed=True)
    plt.show()

    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.set_ylabel('Relative Frequency')
    ax.set_xlabel('Group Size (kpc)')
    ax.hist(mcr_groupsizes, bins=100)
    plt.show()

    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.set_ylabel('Relative Frequency')
    ax.set_xlabel('Group Arrival Time (Myr)')
    ax.hist(mcr_grouparrive, bins=100)
    plt.show()
  
    # Write MCR data to output file

    print "Writing data for sdArrive ", sigma_t, "to file ",outputfile

    line = str(nciv)+'\t'+str(mu_life)+'\t'+str(sigma_life)+'\t'+str(mu_t)+'\t'+str(sigma_t)+'\t'
    line += str(mean_ngroups)+'\t'+str(sd_ngroups)+'\t'+str(mean_groupsize)+'\t'+str(sd_groupsize)+'\t'+str(mean_grouparrive)+'\t'+str(sd_grouparrive)+'\n'

    f_obj.write(line)

print "MCR complete for all values of nciv"

f_obj.close()
    

