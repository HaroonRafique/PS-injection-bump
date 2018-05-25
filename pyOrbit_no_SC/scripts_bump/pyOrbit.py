# Merged with Alex's

import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import pickle
import os.path
import imp

# utils
from orbit.utils.orbit_mpi_utils import bunch_orbit_to_pyorbit, bunch_pyorbit_to_orbit
from orbit.utils.consts import mass_proton, speed_of_light, pi

# bunch
from bunch import Bunch
from bunch import BunchTwissAnalysis, BunchTuneAnalysis
from orbit.bunch_utils import ParticleIdNumber

# diagnostics
from orbit.diagnostics import TeapotStatLatsNode, TeapotMomentsNode, TeapotTuneAnalysisNode
from orbit.diagnostics import addTeapotDiagnosticsNodeAsChild, addTeapotMomentsNodeSet, addTeapotStatLatsNodeSet
'''
# teapot lattice
from orbit.teapot import teapot
from orbit.teapot import TEAPOT_Lattice
from orbit.teapot import DriftTEAPOT
from orbit.lattice import AccLattice, AccNode, AccActionsContainer
from orbit.collimation import TeapotCollimatorNode, addTeapotCollimatorNode
from orbit.rf_cavities import RFNode, RFLatticeModifications
'''
'''
#Aperture
from orbit.aperture import TeapotApertureNode
'''
# PTC lattice
from libptc_orbit import *
from ext.ptc_orbit import PTC_Lattice
from ext.ptc_orbit import PTC_Node
from ext.ptc_orbit.ptc_orbit import setBunchParamsPTC, readAccelTablePTC,\
     readScriptPTC, updateParamsPTC, synchronousSetPTC, synchronousAfterPTC,\
     trackBunchThroughLatticePTC, trackBunchInRangePTC
'''
# longitudinal space charge
from orbit.space_charge.sc1d import addLongitudinalSpaceChargeNode, addLongitudinalSpaceChargeNodeAsChild, SC1D_AccNode
from spacecharge import LSpaceChargeCalc
'''
# transverse space charge
from orbit.space_charge.analytical import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalcAnalyticGaussian
from spacecharge import GaussianLineDensityProfile
from spacecharge import InterpolatedLineDensityProfile

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
from lib.save_bunch_as_matfile import *


print "Start ..."
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)

#----------------------------------------------
# Create folder sctructure
#----------------------------------------------
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('output')

#----------------------------------------------
# Generate Lattice (MADX + PTC)
#----------------------------------------------
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < flat_file_generator.madx")
orbit_mpi.MPI_Barrier(comm)

#----------------------------------------------
# Simulation Parameters
#----------------------------------------------

turn = 0
turns_max = 5000
turns_print = xrange(-1, turns_max, 100)

#----------------------------------------------
# Initialize a Teapot-Style PTC lattice
#----------------------------------------------

PTC_File = "BUMP_STUDIES.flt"
length_of_name = len(PTC_File)
ptc_init_(PTC_File, length_of_name - 1)
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

# readScriptPTC('Input/fringe.txt')
# readScriptPTC('Input/time.txt')
# readScriptPTC('Input/chrom.ptc')
#~ readScriptPTC('madx/ptc/chrom.txt')
readScriptPTC('Input/PS-TIME-TABLES.PTC')


print '\nLattice parameters ...'
print '  circumference: \t', Lattice.getLength(), 'm'
print '  alphax0: \t\t', Lattice.alphax0
print '  betax0: \t\t', Lattice.betax0, 'm'
print '  alphay0: \t\t', Lattice.alphay0
print '  betay0: \t\t', Lattice.betay0, 'm'
print '  Dx0: \t\t\t', Lattice.etax0, 'm'
print '  Dpx0: \t\t', Lattice.etapx0
print '  harm. number: \t', Lattice.nHarm
print '  nodes: \t\t', Lattice.nNodes

paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm
'''
#----------------------------------------------

# Add apertures

#----------------------------------------------

position = 0
# declaration of the variable position
for node in Lattice.getNodes():
# loop over the list of the nodes of (our) lattice
# for each node in the list:
  myaperturenode = TeapotApertureNode(1, 10, 10, position)

  # create an aperture at position = position
  node.addChildNode(myaperturenode, node.ENTRANCE)
  node.addChildNode(myaperturenode, node.BODY)
  node.addChildNode(myaperturenode, node.EXIT)

  # attach the <child node> to current <node>
  position += node.getLength()
  # increment the variable position
'''
#----------------------------------------------
# Simulation Parameters and bunch distribution
#----------------------------------------------

print '\nAdding main bunch ...'

Particle_distribution_file = 'Input/PS_matched_transvers.dist'  # generate_initial_distribution(parameters_dict, lattice_parameters_file='Input/optics_ptc.txt')
#mm, mrad, long. rad (-pi bis +pi), dE (GeV)

Intensity = 80e10
m0 = mass_proton 	# protons ...

#definition of number of macro particles based on number of lines in file
N_mp = sum(1 for line in open(Particle_distribution_file))
macrosize = Intensity/N_mp
bunch = Bunch()
setBunchParamsPTC(bunch)
kin_Energy = bunch.getSyncParticle().kinEnergy()
print '  Momentum: ', bunch.getSyncParticle().momentum(), 'GeV'
print '  Ekin:     ', bunch.getSyncParticle().kinEnergy(), 'GeV'
print '  Gamma:    ', bunch.getSyncParticle().gamma()
print '  Beta:     ', bunch.getSyncParticle().beta()
print '  Charge:   ', bunch.charge(), 'e'
print '  Mass:     ', bunch.mass(), 'GeV'


#
# tmax = 500
# input_params = {}
# input_params['mainbunch_file'] = 'output/mainbunch.dat'
# input_params['intensity'] = 4*78e+10
# input_params['n_macroparticles'] = 5000
# input_params['macrosize'] = input_params['intensity']/input_params['n_macroparticles']
# input_params['epsn_x'] = 1.4e-6 #m
# input_params['epsn_y'] = 1.2e-6 #m
# input_params['dpp_rms'] = 0.87e-3
# input_params['blength_rms'] = 5.96 #m
# input_params['LongitudinalCut'] = 2.4
# input_params['LongitudinalJohoParameter'] = 1.2
# input_params['turns_max'] = tmax
# input_params['turns_print'] = range(-1, tmax, 10) + range(100000) + range(tmax-1000, tmax)
# input_params['turns_emittance_update'] = [] #range(-1, input_params['turns_max'], 20)
# input_params['turn'] = 0
# input_params['emittance_memory_x'] = np.zeros(20)
# input_params['emittance_memory_y'] = np.zeros(20)
#
# parameters = {}
# parameters['TransverseCut'] = 5
#
# parameters['length'] = Lattice.getLength()/Lattice.nHarm
# parameters['harmonic_number'] = Lattice.nHarm
# parameters['rf_voltage'] = 0.025e6
# parameters['circumference'] =Lattice.getLength()
# parameters['gamma_transition'] = Lattice.gammaT
# parameters['phi_s'] = 0
# parameters['gamma'] = bunch.getSyncParticle().gamma()
# parameters['beta'] = bunch.getSyncParticle().beta()
# parameters['energy'] = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
# parameters['bunch_length'] = input_params['blength_rms']/(parameters['beta']*speed_of_light)*4
#
# parameters['alphax0'] = Lattice.alphax0
# parameters['betax0'] = Lattice.betax0
# parameters['alphay0'] = Lattice.alphay0
# parameters['betay0'] = Lattice.betay0
# parameters['etax0'] = Lattice.etax0
# parameters['etapx0'] = Lattice.etapx0
# parameters['etay0'] = Lattice.etay0
# parameters['etapy0'] = Lattice.etapy0
# parameters['x0']      = Lattice.orbitx0
# parameters['xp0']     = Lattice.orbitpx0
# parameters['y0']      = Lattice.orbity0
# parameters['yp0']     = Lattice.orbitpy0
#
# parameters.update(input_params)
# Particle_distribution_file =  generate_initial_distribution_FMA (parameters)
# #	Particle_distribution_file =  generate_initial_distribution_y0 (parameters,orientation='y')

bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, N_mp + 1) #read in only first n_macroparticles particles.
if bunch.getSizeGlobal() < N_mp:
	print '\nError: The provided particle distribution has less macroparticles than requested ... Exiting!'
	raise SystemExit

  # set macrosize
bunch.addPartAttr("macrosize")
for i in range(bunch.getSize()):
  bunch.partAttrValue("macrosize", i, 0, macrosize)

# ID the particles
particleidnumber = ParticleIdNumber()
particleidnumber.addParticleIdNumbers(bunch) # Give them uniquely number ids



paramsDict["bunch"]= bunch
lostbunch = Bunch()
paramsDict["lostbunch"]=lostbunch
lostbunch.addPartAttr("LostParticleAttributes")

#----------------------------------------------
# Start simulation
#----------------------------------------------

#Prepare the analysis class that will look at emittances, etc.
bunchtwissanalysis = BunchTwissAnalysis()


# #----------------------------------------------------
# # Add space charge nodes
# #----------------------------------------------------
# ''
# # Make a SC solver using frozen potential
# print '\nSetting up the space charge calculations ...'
# sc_path_length_min = 0.00000001
# bunchtwissanalysis.analyzeBunch(bunch)
#
# # consider line density based on measurement provided in file
# density=np.loadtxt('density_2.dat', dtype=float)
# LineDensity = InterpolatedLineDensityProfile(-12.5,12.5,density.tolist())
#
# # simple Gaussian line density - sufficient to create a certain tune spread - density defined above not required
# LineDensity = GaussianLineDensityProfile(input_params['blength_rms'])
#
# space_charge_solver = SpaceChargeCalcAnalyticGaussian( input_params['intensity'], input_params['epsn_x'] ,
# 						input_params['epsn_y'],  input_params['dpp_rms'], LineDensity)
# sc_nodes = scLatticeModifications.setSCanalyticalAccNodes(Lattice, sc_path_length_min, space_charge_solver)
#
# print '  Installed', len(sc_nodes), 'space charge nodes'
# ''
#
# #-----------------------------------------------------
# # Add tune analysis child node
# #-----------------------------------------------------
#
# parentnode_number = 97
# parentnode = Lattice.getNodes()[parentnode_number]
# Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
# tunes = TeapotTuneAnalysisNode("tune_analysis")
# tunes.assignTwiss(Twiss_at_parentnode_entrance['betax'], Twiss_at_parentnode_entrance['alphax'], Twiss_at_parentnode_entrance['etax'], Twiss_at_parentnode_entrance['etapx'], Twiss_at_parentnode_entrance['betay'], Twiss_at_parentnode_entrance['alphay'])
# addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)
#

#----------------------------------------------------
# Define output dictionary
#----------------------------------------------------

output_dictionary = Output_dictionary()
output_dictionary.addParameter('turn', lambda: turn)
output_dictionary.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
output_dictionary.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
output_dictionary.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
output_dictionary.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
output_dictionary.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
output_dictionary.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
output_dictionary.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
output_dictionary.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
output_dictionary.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
output_dictionary.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output_dictionary.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output_dictionary.addParameter('eps_z', lambda: bunchtwissanalysis.getEmittance(2) / (speed_of_light*bunch.getSyncParticle().beta()) * 1e9 * 4 * pi)
output_dictionary.addParameter('bunchlength', lambda: np.sqrt(bunchtwissanalysis.getCorrelation(4,4)) / (speed_of_light * bunch.getSyncParticle().beta()) * 4)
output_dictionary.addParameter('dpp_rms', lambda: np.sqrt(bunchtwissanalysis.getCorrelation(5,5)) / (bunch.getSyncParticle().gamma() * bunch.mass() * bunch.getSyncParticle().beta() ** 2))


# save initial distribution
mainbunch_file = 'output/mainbunch_start.dat'
bunch.dumpBunch(mainbunch_file)


#----------------------------------------------------
# Do some turns and dump particle information
#----------------------------------------------------

bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
if orbit_mpi.MPI_Comm_rank(bunch.getMPIComm()) == 0:
	output_parameters = ['turn', 'intensity', 'x', 'y', 'eps_x', 'eps_y']
	# output_parameters = ['turn', 'intensity', 'N_mp', 'gamma']
	output_dict = {}
	for entry in output_parameters: output_dict[entry] = np.zeros(turns_max)

print '\nnow start tracking...'

for turn in range(turns_max):#range(turn, turns_max):
    Lattice.trackBunch(bunch, paramsDict)
    bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance
    output_dictionary.update()
    bunch.dumpBunch("Turn_" + str(turn).zfill(5) + ".dat")
