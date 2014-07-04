# Written 4/7/14 by dh4gan
# Reads in data from parameters file

def read_parameters_single(paramfile):
        
    rowdict = {'nCivilisations':0.0,'innerGHZ':0.0,'outerGHZ':0.0,'rScale':0.0,'zMin':0.0, 'Zmax':0.0,
            'meanLifetime':0.0,'sdLifetime':0.0,'meanArrival':0.0,'sdArrival':0.0}
        
    for line in open(paramfile,'r'):
        
        data = line.split()
        key = data[0]
        
        rowdict[key] = data[1]            
        
    nciv = int(rowdict['nCivilisations'])
    rinner = float(rowdict['innerGHZ'])
    router = float(rowdict['outerGHZ'])
    rscale = float(rowdict['rScale'])
    zmin = float(rowdict['zMin'])
    zmax = float(rowdict['zMax'])
    mu_life = float(rowdict['meanLifetime'])
    sigma_life = float(rowdict['sdLifetime'])
    mu_arrive = float(rowdict['meanArrival'])
    sigma_arrive = float(rowdict['sdArrival'])
    

    return nciv, rinner, router,rscale, zmin,zmax,mu_life,sigma_life, mu_arrive,sigma_arrive
    
    
def read_parameters_mcr(paramfile):
    # TODO
        
    rowdict = {'nRuns': 0.0,'nCivilisations':0.0,'innerGHZ':0.0,'outerGHZ':0.0,'rScale':0.0,'zMin':0.0, 'Zmax':0.0,
            'meanLifetime':0.0,'sdLifetime':0.0,'meanArrival':0.0,'sdArrival':0.0}
        
    for line in open(paramfile,'r'):
        
        data = line.split()
        key = data[0]
        
        rowdict[key] = data[1]            
        
        
    nruns = int(rowdict['nRuns'])
    nciv = int(rowdict['nCivilisations'])
    rinner = float(rowdict['innerGHZ'])
    router = float(rowdict['outerGHZ'])
    rscale = float(rowdict['rScale'])
    zmin = float(rowdict['zMin'])
    zmax = float(rowdict['zMax'])
    mu_life = float(rowdict['meanLifetime'])
    sigma_life = float(rowdict['sdLifetime'])
    mu_arrive = float(rowdict['meanArrival'])
    sigma_arrive = float(rowdict['sdArrival'])
    

    return nruns,nciv, rinner, router,rscale, zmin,zmax,mu_life,sigma_life, mu_arrive,sigma_arrive
