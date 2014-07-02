# Written 2/7/14 by dh4gan
# This object is essentially a collection of civilisations
# Methods generate distributions of civilisations in space and time

import civilisation as civ
import numpy as np
import matplotlib.pyplot as plt

class galaxy(object):
    
    '''
    This object is essentially a collection of civilisations
    Methods generate distributions of civilisations in space and time
    '''


    def __init__(self, ncivs):
        '''
        
        '''
        self.N = ncivs
        self.civs = [] # Array to hold all civilisations
        self.ngroups= 0 # Total number of groups
        self.groupmax = 0 # Largest civilisation rank to start a group
        self.groupID = [] # For groups 1 to ngroups, this gives the civilisation that started the group
        self.groupcount = [] # Population of each group from 1 to ngroups
        
        self.generate_empty_galaxy()
        
    def generate_empty_galaxy(self):
        '''Called upon setup, creates numpy array of civilisations'''
        i=0
        while i<self.N:        
            self.civs.append(civ.civilisation([0.0,0.0,0.0], 0.0,0.0,0, 0))
            i+=1
            
    def generate_uniform_spatial_distribution(self,xmax,ymax,zmax):
        '''Generates a uniform cuboid of civilisations, with limits xmax,ymax,zmax'''
        for civ in self.civs:
            civ.r[0] = -xmax + 2.0*np.random.random()*xmax
            civ.r[1] = -ymax + 2.0*np.random.random()*ymax
            civ.r[2] = -zmax + 2.0*np.random.random()*zmax
        
        
    def generate_uniform_GHZ(self,rinner,router, zmin,zmax):
        '''Generates a uniform GHZ annulus of civilisations, with annular limits rinner, router'''
        
        for civ in self.civs:
            
            r = rinner + np.random.random()*(router-rinner)
            phi = 2.0*np.pi*np.random.random()
            z = zmin + np.random.random()*(zmax-zmin)
            
            civ.r[0] = r*np.cos(phi)
            civ.r[1] = r*np.sin(phi)
            civ.r[2] = z
            
        
    def generate_exponential_GHZ(self,rinner,router, rscale, zmin,zmax):
        '''Generates a GHZ annulus of civilisations, with annular limits rinner, router, exponentially distributed in r'''
        
        sigma0 = np.exp(-rinner/rscale) - np.exp(-router/rscale)
        
        for civ in self.civs:
            
            r = np.exp(-rinner/rscale) - np.random.random()*sigma0
            r = -np.log(r)*rscale
            
            print r
            #r = rinner + np.random.random()*(router-rinner)
            phi = 2.0*np.pi*np.random.random()
            z = zmin + np.random.random()*(zmax-zmin)
            
            civ.r[0] = r*np.cos(phi)
            civ.r[1] = r*np.sin(phi)
            civ.r[2] = z
        
        
    def generate_uniform_arrival_time(self,tmin,tmax):
        '''Generates a uniform distribution of civilisation arrival times'''
        
        for civ in self.civs:
            civ.tarise = tmin + np.random.random()*(tmax-tmin)                        
        
    def generate_gaussian_arrival_time(self,tmin,tmax, mu,sigma):
        '''
        Generates a gaussian distribution of civilisation arrival times
        Uses the accept-reject technique
        '''
        
        for civ in self.civs:
            accept = False
            while accept==False:
                civ.tarise = tmin + np.random.random()*(tmax-tmin)
                fmax = 1.0/(2.0*np.pi*sigma)
                
                f = fmax*np.exp(-(civ.tarise-mu)**2/(2.0*sigma)**2)
                
                randtest = fmax*np.random.random()
                                
                if(randtest < f):
                    accept=True                             
        
    def arrival_time_histogram(self):
        '''
        Plots a histogram based on civilisation arrival times
        '''
        
        time = []
        for civ in self.civs:
            time.append(civ.tarise)
        
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        ax.hist(time)
        plt.show()
        
    def sort_by_arrival_time(self):
        '''Sorts array of civilisations by their arrival time'''
        
        # Create array of arrival times
        
        times = []
        
        for civ in self.civs:
            times.append(civ.tarise)
                           
        # Now sort this (retrieving order of sort)
        
        print 'Sorting civilisations by arrival time'
        
        order = np.argsort(times)
        
        
        # Copy old array into new array
        newcivs = self.civs
        
        
        # Regenerate civs array in correct order using sort
        print 'New order found: shuffling civilisations'
        self.civs = []
        
        for i in range(self.N):
        # Use this to generate the sorted civilisations array
            self.civs.append(newcivs[order[i]])  
        print 'Civilisations shuffled'
            
    def check_for_groups(self):
        '''
        Loops over all civilisation pairs to generate group numbers
        Requires civilisations to be sorted in ascending arrival time order
        '''
        
        # Civilisation that arrives first starts its own group
        
        print 'Checking for groups'
        
        self.civs[0].groupleader = 1    
        
        # Loop over civilisation pairs
        counter = 0
        
        for i in range(self.N):
            
            percent = 100.0*float(i)/float(self.N)
            if(percent > counter):
                print counter, "% complete"
                counter +=10      
            
            for j in range(i+1,self.N):
                # Calculate magnitude of separation four vector 
                sep = self.civs[i].sep_4vector_magnitude(self.civs[j])
                
                # This civilisation pair is causally connected if sep >=0.0
                # j's group affiliation = i's group affiliation
                
                # If separation less than zero, j not affiliated
                # and therefore in its own group
                
                if(sep>=0.0):
                    self.civs[j].groupleader = self.civs[i].groupleader
                else:
                    # If this civilisation doesn't have a leader already, it becomes its own leader
                    if(self.civs[j].groupleader==0):self.civs[j].groupleader = j+1
                    
                    
                #print i, j, sep, self.civs[i].groupleader, self.civs[j].groupleader
                
        print 'Group checking complete'
                
    def count_groups(self):
        '''
        This method counts all the groups identified by check_for_groups
        Gives the total number of groups and tallies for each group
        '''
        
        self.groupmax = 0                            
        
        print 'Counting groups'
        # Firstly, find the maximum possible number of groups
        for civ in self.civs:
            if(civ.groupleader > self.groupmax): self.groupmax = civ.groupleader
            
        # Now find the population of each group sorted by leader
        
        self.groupcount = np.zeros(self.groupmax)
        
        for civ in self.civs:
            self.groupcount[civ.groupleader-1] +=1.0            
        
        # Now calculate the number of groups with at least one member from grouptally
        
        self.ngroups = 0
        for i in range(len(self.groupcount)):
            if self.groupcount[i]>0: 
                self.ngroups+=1
                self.groupID.append(i+1)
            
        self.groupID = np.asarray(self.groupID)
        
        # Finally, assign groupranks (first, second, third group in existence etc)
        
        for civ in self.civs:
            # Find leader's entry in groupID array
            civ.grouprank = np.nonzero(self.groupID==civ.groupleader)
            civ.grouprank = int(civ.grouprank[0])+1            
            
        # Remove all entries with zero counts
        self.groupcount = self.groupcount[np.nonzero(self.groupcount)]
        
    def plot_spatial2D(self):
        '''
        This creates an x-y plot of the galaxy
        TODO - collect x,y data by group 
        '''
                
        x = []
        y = []               
        pointcolor = []
        
        colorchoice = []         
          
        for i in range(self.ngroups):            
            colorchoice.append([np.random.random(), np.random.random(),np.random.random(),])            
                          
        
        # Select colours for each group
                        
        for civ in self.civs:
            x.append(civ.r[0])
            y.append(civ.r[1])
            pointcolor.append(colorchoice[civ.grouprank-1])
                
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        ax.scatter(x, y, c=pointcolor)
        #ax.scatter(x, y)
        plt.show()  
        
    def plot_spatial2D_voronoi(self):
        '''
        This creates an x-y plot of the galaxy
        And plots a voronoi tesselation
        TODO - needs scipy better than 0.10.1
        '''
                
        x = []
        y = []
        
        for civ in self.civs:
            x.append(civ.r[0])
            y.append(civ.r[1])
                
        points = [x,y]

        
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        ax.scatter(x, y)
        plt.show() 
        
    def output_group_statistics(self, outputfile):
        '''
        Outputs statistical data on all groups
        '''
        
        f_obj = open(outputfile,'w')
        
        print self.ngroups, len(self.groupID), len(self.groupcount)
        
        for i in range(self.ngroups):
            print i
            line = str(i)+'\t'+str(self.groupID[i]) + '\t'+str(self.civs[self.groupID[i]-1].tarise) + '\t' + str(self.groupcount[i]) + '\n'
            
            f_obj.write(line)
            
        f_obj.close()
            