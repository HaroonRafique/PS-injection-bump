# PS-injection-bump
Simulations for the PS injection bump studies (possible eddy currents effect)

The idea:
- Eddy currents are induced in the vacuum pipe by effect of the bump magnetic filed ramping
- These currents create additional sextupoles in correspondence of the bumps that perturb the tune via quadrupolar feed-down. This is modeled placing a thin sextupole in the middle of the bumps in madx and caluculating the twiss parameters while ramping the bump and the sextupoles accordingly. The bump discharges in the shape of a sine wave, while the eddy currents strength is proportional to the Bdot.

## MADx study
Bump ramp down in ~500 turns, MADx called in ~100 steps. Bump up and down was simulated in order to try to reproduce the Pano's measurement.
Two output files: 
*.out contains sextupole strength (then scaled in proportion to all the bumps), bumps strengths and calculated tunes
*.twiss is an ordinary twiss file in order to get the chroma and the beta beat w.r.t the normal cases (bump up and down)

**Open questions:**
- does it make sense the scaling of the bump by strength?
- chroma jump in the results ? --> what does madx do with a magnet at zero strength/very small strength ? is there any difference between 0 and somethinge-18?
- try to use the bump shape from OASIS signal

**TODO:**
- benchmark the full/simplified PS lattice in the MADx simulations
- check the higher multipole division factors when flattening the lattice for PTC (and so how the tables are calculated)

## pyORBIT study
in progress ....

## Folder structure:
```
.
├── MADx_scan					# bump ramped up and down, lattice including sextupoles
    ├── condor						# HTcondor stuff
    └── runMAD  						# the proper script folder
    	├── sweepBump_master.madx		# template code, modified via madx_caller.py
    	├── madx_caller.py    				# modifies the madx script and exectues it in a loop
	├── lattice						# lattice files folder from the optics repository
	└── result   						# this folder structure is important
		├── twiss
		└── out
├── MADx_scan_no_sextupoles        	# same but with no sextupoles
    └── ...  							# same folder structure
├── MADx_scan_parallel              		# fast code palallelised, lattice including sextupoles
    └── ...  							# same folder structure
├── MADx_scan_parallel_no_sextupoles	# fast code palallelised, lattice without sextupoles
    └── ...  							# same folder structure
├── MADx_reference           			# MADx runs with no sextupoles and bump up and down
├── Analysis                				# analysis scripts and results
└── pyOrbit_simulations      			# tracking simulations using the tables generated from the former two
    ├── ...            
    └── ...   

```
