# 29.08.19 Haroon Rafique CERN BE-ABP-HSI
------------------------------------------------------------------------

Proton Synchrotron Injection Bump Closure MAD-X and PTC Simulation:
Case: 00_SPLIT_KICKER_With_MULTIPOLE
- Using 8 x 10 cm HKICKERs for dipole component
- And 4 x zero-length MULTIPOLEs between each pair of HKICKERs for the sextupole component

Running Instructions:
------------------------------------------------------------------------

1. ./madx-linux64 < Flat_File.madx
2. ./move_files.sh
3. python Plot_PTC_cf_MADX_Closed_Orbit.py
4. python PyORBIT_Table_Creator.py
5. cd PyORBIT
6. Start pyorbit either a) locally or b) on HPC-Batch:

	6.a) ./START_local.sh pyOrbit.py $number_of_MPI_processes
	e.g. ./START_local.sh pyOrbit.py 4

	6.b)i) ./Make_SLURM_submission_script.py
	6.b.ii) sbatch SLURM_submission_script.sh

What's in the folder?
------------------------------------------------------------------------

Inputs:

> Lattice/ contains the MAD-X lattice sequence, strength, aperture, and element files.
> MADX_Input/ contains the MAD-X input table for the injecion bump variables, generated in PS-injection-bump/From_Scratch/01_Create_MADX_Input_Table
> PyORBIT/ contains the PyORBIT simulation files
> PyORBIT/lib/ contains PyORBIT libraries

> Flat_File.madx is the MAD-X input file and defines the simulation.
> clean_folder.sh removes junk after a simulation.
> move_files.sh moves files into relevent folders after a simulation.
> Plot_PTC_cf_MADX_Closed_Orbit.py plots the full closed orbit for each of the 50 steps in the MAD-X simulation, for MAD-X and PTC.
> PyORBIT_Table_Creator.py reads the contents of MADX_Tables/ and creates the corresponding PTC-PyORBIT readable tables in PyORBIT_Tables/.

> PyORBIT/Make_SLURM_submission_script.py is used to make the SLURM submission script for this simulation.
> PyORBIT/pyOrbit.py is the main PyORBIT simulation script.
> PyORBIT/simulation_parameters.py define simulation parameters for the pyOrbit.py simulation script, allowing the use of the same pyOrbit.py for multiple simulations.
> PyORBIT/clean_*.sh scripts are for cleaning the simulation folder after simulation completion.
> PyORBIT/Create_FF_and_Tables.sh contains running steps 1 - 5 in a script that can be called from within PyORBIT in pyOrbit.py.
> PyORBIT/PyORBIT_Tomo_file_MD4224_HB.mat is the tomoscope input file for PyORBIT to use when using a generate_initial_distribution_from_tomo distribution generator.

Outputs:

> MADX_Tables/ contains the MAD-X output tables required for a PTC-PyORBIT simulation. These still require one step of conversion.
> PTC_Twiss/ contains the (MAD-X) PTC twiss output files for each step in the injection bump.
> MAD_Twiss/ contians the MAD-X twiss output files for each step in the injection bump.
> PTC-PyORBIT_Tables/ contains the converted MAD-X output PTC tables, now in a PTC-PyORBIT readable format.

> madx.ps output from MAD-X shows plots from PTC and MAD-X.
> PTC-PyORBIT_flat_file.flt is the PTC-PyORBIT readable flat file that defines the PTC lattice.
> PS.seq is the final optimised Proton Synchrotron sequence.

> PyORBIT/All_Twiss/ contains the PTC Twiss generated in PTC-PyORBIT and saved for each turn.

