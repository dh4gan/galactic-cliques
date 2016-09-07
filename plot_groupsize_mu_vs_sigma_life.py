# Written 1/8/14 by dh4gan
# Generates a collection of civilisations with some distribution in space and arrival time
# Then calculates causally connected groups
# Repeats this to allow MCR analysis
# Repeats MCR analysis over various values of the mean lifetime

import galaxy as gal
import params
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from sys import argv
from os.path import isfile


# Read in input parameters from file

#if len(argv)==1:
#    paramfile = raw_input("Enter the parameter file: ")
#elif len(argv)==2:
#    paramfile = argv[1]
        
#nruns,nciv, rinner,router,rscale, zmin,zmax, mu_life,sigma_life,mu_t,sigma_t = params.read_parameters_mcr(paramfile)

iseed = -47

# Override definitions of mu_life, sigma_life, specify the values to be explored
#nmu = 100
#mu_life_values = np.linspace(0.001, 5.0, num=nmu)

#nsigma = 100
#sigma_life_values = np.linspace(1.0e-1,1.0e0, num=nsigma)

#print "Surveying following parameter space:"
#print "mu: \n",mu_life_values
#print "sigma: \n",sigma_life_values

# Arrays to hold values of outputs for plotting

# mean_group_values = np.zeros((nmu,nsigma))
# sd_group_values = np.zeros((nmu,nsigma))
# mean_size_values = np.zeros((nmu,nsigma))
# sd_size_values = np.zeros((nmu,nsigma))
# mean_arrive_values = np.zeros((nmu,nsigma))
# sd_arrive_values =np.zeros((nmu,nsigma))

# Set up MCR output file

outputfile = 'output.MCR'


print 'Attempting to read ',outputfile
    
data = np.genfromtxt(outputfile, skiprows=1,usecols=(1,2,7,8))

nmu = 90
nsigma = 100

mu_life = data[:,0].reshape(nmu,nsigma).transpose()  
sigma_life = (data[:,1]/data[:,0]).reshape(nmu,nsigma).transpose()
mean_groupsize = data[:,2].reshape(nmu,nsigma).transpose()
sd_groupsize = data[:,3].reshape(nmu,nsigma).transpose()

mean_groupsize = ndimage.filters.gaussian_filter(mean_groupsize,1.0)
sd_groupsize = ndimage.filters.gaussian_filter(100.0*sd_groupsize/mean_groupsize,1.0)

#mu_life = data[:,0]  
#sigma_life = data[:,1]/data[:,0]
#mean_group = data[:,2]
#sd_group = data[:,3]

print mu_life
print sigma_life

# for i in range(len(mu_life)):
#     if(mu_life[i]>0.007 and mu_life[i]<0.02):
#         print mu_life[i],sigma_life[i],mean_group[i]
#     
contourlevels = [1,10,50,100,150,200,300,400,450,490,500]

fig1 = plt.figure()
plt.title('$\sigma_{arrive}$=100 Myr')
ax = fig1.add_subplot(111)
ax.set_xlabel('$\mu_{Life}$ (Myr)')
ax.set_ylabel('$\sigma_{Life}/\mu_{Life}$')
#ax.set_xscale('log')
#ax.set_yscale('log')
ax.set_xlim(0.0,4.0)
ax.set_ylim(0.1,1.0)
plt.pcolor(mu_life,sigma_life, mean_groupsize,vmin=1, vmax = 11)
#plt.hexbin(mu_life,sigma_life,C=mean_group, gridsize = 100)    
cb = plt.colorbar()
cb.set_label('Mean Group Size', fontsize=20)
#cb.ax.set_yticklabels(['1','2','3','4','5','6','7','8','9','10','>10'])
#cs = ax.contour(mu_life_values,sigma_life_values, mean_group_values.transpose(), levels=contourlevels, colors='k')
#ax.clabel(cs,contourlevels)


fig1.savefig('meangroupsize_mu_vs_sigma.png', format='png')

fig1 = plt.figure()
plt.title('$\sigma_{arrive}$=1 Myr')
ax = fig1.add_subplot(111)
ax.set_xlabel('$\mu_{Life}$ (Myr)')
ax.set_ylabel('$\sigma_{Life}/\mu_{Life}$')
#ax.set_xscale('log')
#ax.set_yscale('log')
ax.set_xlim(0.0,4.0)
ax.set_ylim(0.1,1.0)
plt.pcolor(mu_life,sigma_life, sd_groupsize)
#plt.hexbin(mu_life,sigma_life,C=mean_group, gridsize = 100)    
cb = plt.colorbar()
cb.set_label('Standard Error of Mean Group Size (%)', fontsize=20)
#cs = ax.contour(mu_life_values,sigma_life_values, mean_group_values.transpose(), levels=contourlevels, colors='k')
#ax.clabel(cs,contourlevels)
   
fig1.savefig('sdgroupsize_mu_vs_sigma.png', format='png')
plt.show()

