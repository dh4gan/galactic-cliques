# Galactic Cliques

This set of scripts seeds civilisations in a galaxy, and calculates how many civilisations can form causally connected groups.  Civilisations are placed in a spatial distribution corresponding to the canonical Galactic Habitable Zone, and their arrival time as a technological civilisation is sampled from a Gaussian distribution.

This population is then tested to determine which civilisations are aware of each other at arrival, which determines the size of a group.  The full details of this work were originally published as

*Forgan (2017): International Journal of Astrobiology, 16, 349-554*


## About the code

The code is written entirely in Python 2.7, and relies on numpy 1.8.0 and matplotlib 1.3.0.

### Objects and modules

`civilisation.py` - describes a Civilisation Object (a star system hosting a civilisation)

`galaxy.py` - describes a Galaxy object (a collection of Civilisations)

`params.py` - handles the reading in of data from parameter files (example given in `input_MCR.params`)

### Scripts to execute

`cliques_single.py` -  carries out a single realisation

`cliques_MCR.py` -  carries out a set of Monte Carlo Realisations (MCRs) for one set of parameters (to compute mean/standard deviations of key values)

the other files carry out many MCR sets to carry out a parameter sweep

`cliques_MCR_mu_vs_sigma_life.py`
`cliques_MCR_vs_mu_life.py`
`cliques_MCR_vs_nciv.py`
`cliques_MCR_vs_sdarrive.py`
`cliques_MCR_vs_sigma_life.py`

All of the above files end by plotting their output data.  If one wishes to plot and not re-run, then the `plot_` scripts allow this.
