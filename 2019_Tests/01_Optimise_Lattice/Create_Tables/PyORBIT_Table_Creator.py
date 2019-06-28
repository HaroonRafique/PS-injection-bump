# PyORBIT Table Creator
# Creates a .txt table that is read by PTC to set magnet strengths over time
# Currently works only for single multipoles (pure dipole, quad, sextupole ...)
# Haroon Rafique CERN BE-ABP-HSI 28.06.19
#
import numpy as np
import os

from math import log10, floor
def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

# For each element, create a PTC table (via function)
def Create_PTC_Table(name, multipole_order, time, normal, skew):
	
	filename = str(name) + str('.txt')
	f = open(filename, 'w')
	
	n_lines = len(time) + 2
	
	f.write('%i 1 %i \n' % (n_lines, multipole_order))
	f.write('%i\n' % (multipole_order))
	
	for i in xrange(len(time)):
		f.write('%1.11f %1.11f %1.11f\n' % (time[i], normal[i], skew[i]))	
	
	return

Create_PTC_Table('TEST', 2, [0,1,2], [11.32161, 12.1321564, 13.555555855555555], [0,0,0])

# Table time is in seconds
# 1 turn = 2.287E-6 seconds
# We want a full bump of 1E-3 seconds, or a half bump of 5E-4 seconds
# 2200 turns = 5.0314E-3 s
# Bump on for 5E-4 seconds
# zeroes from 5E-4 - 5.0314E-3 s

# Read TFS table

# Create some data structure
