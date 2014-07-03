# Written 2/7/14 by dh4gan
# Object that represents a star system hosting a galactic civilisation
# Used in simulations of social networks established by lightspeed communication

import numpy as np

c = 296.67 # lightspeed in kpc/Myr

class civilisation(object):        
    
    '''
    Object that represents a star system hosting a civilisation
    Used in simulations of social networks established by lightspeed communication
    '''


    def __init__(self, pos, arise,life, leader, rank):
        '''
        Constructor: cartesian position vector, arisal time, lifetime, group it is affiliated to
        '''
        self.r = pos # cartesian position vector
        self.tarise = arise # arisal time
        self.lifetime = life # lifetime
        self.groupleader = leader # leader of group it is affiliated with
        self.grouprank = rank # Order of group's appearance
        
    def separation_4vector(self,other):
        '''calculates the separation 4 vector between two civilisations
        d4x = (cdt, dx,dy,dz)'''
        
        d4x = np.zeros(4)
        
        d4x[0] = (self.tarise-other.tarise)*c
        
        for i in range(1,3):
            d4x[i] = self.r[i-1] - other.r[i-1]
        
        return d4x
    
    def sep_3vector_magnitude(self,other):
        '''calculates the magnitude of the separation 3 vector between two civilisations
        '''
        
        dr = 0.0                
        
        for i in range(1,3):
            dr = dr + (self.r[i-1] - other.r[i-1])**2
        
        dr = np.sqrt(dr)
        return dr
    
    def sep_4vector_magnitude(self,other):
        '''Calculates (cdt)^2 - (dr)^2 between two civilisations'''
        
        d4x = self.separation_4vector(other)
        
        mag = 0.0
        for i in range(1,3):
            mag = mag + d4x[i]*d4x[i]
            
        mag = d4x[0]*d4x[0] - mag
        
        return mag
            
        