# Written 25/2/16 by dh4gan
# Code plots outputs from 3 runs of the cliques_MCR_vs_nciv.py script

import numpy as np
import matplotlib.pyplot as plt

filenames = ['sdarrive_1/output.MCR','sdarrive_10/output.MCR','sdarrive_100/output.MCR']
labels = [r'$\sigma_{arrive}=1$ Myr',r'$\sigma_{arrive}=10$ Myr',r'$\sigma_{arrive}=100$ Myr']
colours = ['red', 'blue','green']

fig1 = plt.figure()
ax = fig1.add_subplot(111)

for i in range(3):
    print 'Reading file ',filenames[i]
    data = np.genfromtxt(filenames[i], skiprows=1,usecols=(0,5,6))    
    
    ax.plot(data[:,0],data[:,1], label=labels[i], color=colours[i])
    #ax.errorbar(data[:,0],data[:,1],yerr=data[:,2],c=colours[i])
    ax.fill_between(data[:,0],data[:,1]-data[:,2], data[:,1]+data[:,2], alpha=0.5,color=colours[i])
    
lims = [np.amin([ax.get_xlim(),ax.get_ylim()]), np.amax([ax.get_xlim(),ax.get_ylim()])]

plt.legend(bbox_to_anchor=(0.,1.02,1.,1.02),loc=3,ncol=3,mode="expand",borderaxespad=0)
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlim(0,4000)
ax.plot(ax.get_xlim(),ax.get_xlim(), 'k--')
ax.set_ylabel(r'$N_{group}$',fontsize=20)
ax.set_xlabel(r'$N_{civ}$',fontsize=20)
fig1.savefig('ngroup_vs_nciv.png', format='png')

    
    