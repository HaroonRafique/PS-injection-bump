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

# Read TFS table
# We ignore the time column
def Read_TFS_Return_Data(file_in):
	fi = open(file_in, 'r')
	contents = fi.readlines()

	data = []
	for l in contents:
		if ('@' in l) or ('$' in l) or ('*' in l):
			pass
		else:
			data.append(float(l.split()[1]))

	return data
	

# Function takes the data, creates the correct timing for each value in
# seconds, then appends the required number of intervals with zeroes
def Create_Timing(ramp_stop_time, simulation_stop_time, data):
	data_2 = data
	
	# create sequence for time
	d_len = len(data)
	time = np.linspace(0, ramp_stop_time, d_len)
	
	# Calculate interval to complete data until the end of the simulation
	interval = ramp_stop_time / (d_len-1)
	
	# Append zeroes (bump is closed)
	steps = int((simulation_stop_time - ramp_stop_time)	/ interval) + 5
	
	for i in xrange(steps):
		if i is 0:
			pass
		else:
			time = np.append(time, (ramp_stop_time + (i*interval)))
			data_2.append(0.0)
				
	return time, data_2


Create_PTC_Table('TEST', 2, [0,1,2], [11.32161, 12.1321564, 13.555555855555555], [0,0,0])

# Table time is in seconds
# 1 turn = 2.287E-6 seconds
# We want a full bump of 1E-3 seconds, or a half bump of 5E-4 seconds
# 2200 turns = 5.0314E-3 s
# Bump on for 5E-4 seconds
# zeroes from 5E-4 - 5.0314E-3 s

B_40 = Read_TFS_Return_Data('BSEXT40.tfs')
B_40_final = Create_Timing(5E-4, 5.0314E-3, B_40)
Create_PTC_Table('BSEXT40', 3, B_40_final[0], B_40_final[1], np.zeros(len(B_40_final[0])))

B_42 = Read_TFS_Return_Data('BSEXT42.tfs')
B_42_final = Create_Timing(5E-4, 5.0314E-3, B_42)
Create_PTC_Table('BSEXT42', 3, B_42_final[0], B_42_final[1], np.zeros(len(B_42_final[0])))

B_43 = Read_TFS_Return_Data('BSEXT43.tfs')
B_43_final = Create_Timing(5E-4, 5.0314E-3, B_43)
Create_PTC_Table('BSEXT43', 3, B_43_final[0], B_43_final[1], np.zeros(len(B_43_final[0])))

B_44 = Read_TFS_Return_Data('BSEXT44.tfs')
B_44_final = Create_Timing(5E-4, 5.0314E-3, B_44)
Create_PTC_Table('BSEXT44', 3, B_44_final[0], B_44_final[1], np.zeros(len(B_44_final[0])))

BSM40 = Read_TFS_Return_Data('PI.BSM40.1.tfs')
BSM40_final = Create_Timing(5E-4, 5.0314E-3, BSM40)
Create_PTC_Table('BSM40', 2, BSM40_final[0], BSM40_final[1], np.zeros(len(BSM40_final[0])))
