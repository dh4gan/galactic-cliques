# Written 1/8/14 by dh4gan
# Generates a collection of civilisations with some distribution in space and arrival time
# Then calculates causally connected groups
# Repeats this to allow MCR analysis
# Repeats MCR analysis over various values of the mean lifetime

import galaxy as gal
import params
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from os.path import isfile

# Read in input parameters from file

if len(argv)==1:
    paramfile = raw_input("Enter the parameter file: ")
elif len(argv)==2:
    paramfile = argv[1]
        
nruns,nciv, rinner,router,rscale, zmin,zmax, mu_life,sigma_life,mu_t,sigma_t = params.read_parameters_mcr(paramfile)

iseed = -47

# Override definitions of mu_life, sigma_life, specify the values to be explored
nmu = 10
mu_life_values = np.linspace(0.01, 5.0, num=nmu)

nsigma = 10
sigma_life_values = np.linspace(1.0e-3,1.0e-1, num=nsigma)

print "Surveying following parameter space:"
print "mu: \n",mu_life_values
print "sigma: \n",sigma_life_values

# Arrays to hold values of outputs for plotting

mean_group_values = np.zeros((nmu,nsigma))
sd_group_values = np.zeros((nmu,nsigma))
mean_size_values = np.zeros((nmu,nsigma))
sd_size_values = np.zeros((nmu,nsigma))
mean_arrive_values = np.zeros((nmu,nsigma))
sd_arrive_values =np.zeros((nmu,nsigma))

# Set up MCR output file

outputfile = 'output.MCR'

# Detect if this file exists - if it does, and user wishes, then simply read out the data and skip the calculation

plot_instead = "n"

if(isfile(outputfile)):
    plot_instead = raw_input("Outputfile "+ outputfile+ " detected - do you want to skip calculation and plot this instead? ")

if plot_instead=="n":
    print 'Outputting to new file ', outputfile

    f_obj = open(outputfile,'w')

    line = 'Nciv  meanLife  sdLife  meanArrive  sdArrive '
    line += 'meanNgroup  sdNgroup  meanGroupSize  sdGroupSize  meanGroupArrive  sdGroupArrive \n'

    f_obj.write(line)

    imu = 0


    for mu_life in mu_life_values:

        isigma = 0
        for sigma_life in sigma_life_values:
        
            # Now loop over runs

            mcr_ngroups = np.empty(0)
            mcr_groupcounts = np.empty(0)
            mcr_groupsizes = np.empty(0)
            mcr_grouparrive = np.empty(0)

            for irun in range(nruns):

                #print 'Beginning run ', irun+1
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

                #print "There are ", myGalaxy.ngroups, " groups, with latest group established by civilisation ", myGalaxy.groupmax
        
                # Plot this galaxy and its groups

                #myGalaxy.arrival_time_histogram()
                #myGalaxy.plot_spatial2D()

                # Write data to outputfile
                #outputfile = 'output.'+str(irun)
                #myGalaxy.output_group_statistics(outputfile)
    
                #print 'Run ',irun+1, ' complete'
    
                # Store the data in an array?
    
                mcr_ngroups = np.append(mcr_ngroups,np.asarray(myGalaxy.ngroups))
                mcr_groupcounts = np.append(mcr_groupcounts,np.asarray(myGalaxy.groupcount))
                mcr_groupsizes = np.append(mcr_groupsizes,np.asarray(myGalaxy.groupsizes))
                mcr_grouparrive = np.append(mcr_grouparrive,np.asarray(myGalaxy.grouparrive))
    
            #print 'MCR complete - now producing means and standard deviations for ', mu_life, sigma_life


            # Groups with a single member have zero size - remove them
            mcr_groupsizes = mcr_groupsizes[np.nonzero(mcr_groupsizes)]

            # Calculate means and standard deviations
            mean_ngroups = np.mean(mcr_ngroups)
            sd_ngroups = np.std(mcr_ngroups)

            mean_groupsize = np.mean(mcr_groupsizes)
            sd_groupsize = np.std(mcr_groupsizes)

            mean_grouparrive = np.mean(mcr_grouparrive)
            sd_grouparrive = np.std(mcr_grouparrive)
  
            # Write MCR data to output file

            print "Writing data for mu_life ", mu_life, "  sigma_life ",sigma_life, "to file ",outputfile

            line = str(nciv)+'\t'+str(mu_life)+'\t'+str(sigma_life)+'\t'+str(mu_t)+'\t'+str(sigma_t)+'\t'
            line += str(mean_ngroups)+'\t'+str(sd_ngroups)+'\t'+str(mean_groupsize)+'\t'+str(sd_groupsize)+'\t'+str(mean_grouparrive)+'\t'+str(sd_grouparrive)+'\n'

            f_obj.write(line)

            # Add data to output arrays
        
            mean_group_values[imu,isigma] = mean_ngroups
            sd_group_values[imu,isigma] = sd_ngroups
            mean_size_values[imu,isigma] = mean_groupsize
            sd_size_values[imu,isigma] = sd_groupsize
            mean_arrive_values[imu,isigma] = mean_grouparrive
            sd_arrive_values[imu,isigma] = sd_grouparrive

            isigma = isigma+1
            # End of loop over sigma values
            
        imu = imu +1
        # End of loop over mu values
        
    print "MCR complete for all values of mu_life, sigma_life "
    f_obj.close()

if(plot_instead=="y"):
    
    # Read data from outputfile
    f_obj= open(outputfile, "r")
    
    # Read header line
    
    line = f_obj.readline()

    for imu in range(nmu):
        isigma = 0
        
        for isigma in range(nsigma):
    
            # Read line, break up into individual values
            
            line = f_obj.readline()
            
            values = str.split(line)
            
            # Add data to output arrays
            
            if(float(values[1])!=mu_life_values[imu]):
                print "WARNING: mu mismatch: ", values[1], mu_life_values[imu]
            
            if(float(values[2])!=sigma_life_values[isigma]):
                print "WARNING: sigma mismatch: ", values[2], sigma_life_values[isigma]
                
            mean_group_values[imu,isigma] = float(values[5])
            sd_group_values[imu,isigma] = float(values[6])
            mean_size_values[imu,isigma] = float(values[7])
            sd_size_values[imu,isigma] = float(values[8])
            mean_arrive_values[imu,isigma] = float(values[9])
            sd_arrive_values[imu,isigma] = float(values[10])
            
            # End of loop over sigma values
        # End of loop over mu values

    f_obj.close()
# Now Plot data

contourlevels = [10,50,100,150,200,250]

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('$\mu$')
ax.set_ylabel('$\sigma$')
ax.set_xscale('log')
ax.set_yscale('log')
cs = ax.contour(mu_life_values,sigma_life_values, mean_group_values.transpose(), levels=contourlevels)
ax.clabel(cs,contourlevels)
plt.savefig('contour.png', format='png')   


