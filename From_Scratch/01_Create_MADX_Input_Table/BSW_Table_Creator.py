# BSW Table Creator
# Creates a .TFS table that is read by MAD-X to set magnet strengths over time
# Haroon Rafique CERN BE-ABP-HSI 07.06.19
#
# Expects 2 * 10 cm HKICKER with zero length MULTIPOLE (including only
# sextupole component) in sections 40, 42, 43, and 44 of the CERN
# Proton Synchrotron.

import numpy as np
import os

from math import log10, floor
def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

# golden values for the bump - from Eugenio Senes

# Values are for 2 * 10 cm HKICKERs per section (8 total)
# ~ bsw40              =    0.003498034648
# ~ bsw42              =    -0.01422287844
# ~ bsw43              =    0.01290524313
# ~ bsw44              =    -0.006001526439
# ~ BSS_max = 2*1.11828e-01 #from twiss
# ~ f = open("BSEXT_Bump_HKICKER.tfs","w")


# Values are for 1 * 20 cm SBEND/QUAD per section (4 total) with dipole and
# sextupole component added as an error
# ~ bsw40 = 2*0.003498034648
# ~ bsw42 = 2*-0.01422287844
# ~ bsw43 = 2*0.01290524313
# ~ bsw44 = 2*-0.006001526439
# ~ BSS_max = 2*1.11828e-01/0.2 #from twiss
# ~ f = open("BSEXT_Bump_QUAD.tfs","w")
# ~ f = open("BSEXT_Bump_SBEND.tfs","w")

# Values are for 1 * MULTIPOLE per section (4 total)
bsw40              =    0.003498034648/10
bsw42              =    -0.01422287844/10
bsw43              =    0.01290524313/10
bsw44              =    -0.006001526439/10
BSS_max = 2*1.11828e-01 #from twiss
f = open("BSEXT_Bump_MULTIPOLE.tfs","w")

# build the parameter sweep lists
nstep = 50.

t = np.arange(0,nstep+1,1)/nstep * np.pi/2
t = np.append(t, t+np.pi/2)

# strengths for the simulation
#sextupole strength
BSS_val = BSS_max*np.cos(t)

#quadrupole strength
bsw40_val = bsw40*np.sin(t)
bsw42_val = bsw42*np.sin(t)
bsw43_val = bsw43*np.sin(t)
bsw44_val = bsw44*np.sin(t)

# We want a table, with K2 columns, one for each sextupole (4)
# 9 spaces before and between each column
# with header something like:
header = "@ NAME             %08s \"BSWTABLE\"\n@ TYPE             %04s \"USER\"\n@ TITLE            %03s \"BSW\"\n@ ORIGIN           %16s \"5.04.02 Linux 64\"\n@ DATE             %08s \"07/06/19\"\n@ TIME             %08s \"12.09.14\"\n"

# MADX
#-BSStren*(BSW40/BSW42)
# Equivalent
#-BSS_val[t]*(bsw40*np.sin(t) / bsw42*np.sin(t))


f.write(header)

for i in t:
	
	# Bumper strengths
	bss = BSS_max*np.cos(i)
	s40 = bsw40*np.sin(i)
	s42 = bsw42*np.sin(i)
	s43 = bsw43*np.sin(i)
	s44 = bsw44*np.sin(i)
	
f.write('*'+' '.join(map(lambda i: i.rjust(18), ['BSEXT_T', 'BSS', 'BSW40_K0', 'BSW42_K0', 'BSW43_K0', 'BSW44_K0'])) + '\n')
f.write('$'+' '.join(map(lambda i: i.rjust(18), ['%le', '%le', '%le', '%le','%le', '%le'])) + '\n')

# ~ for i in xrange(0,len(t),100):
for i in xrange(0,len(t)):
		f.write(' '+' '.join(map(lambda i: ('%1.4e'%i).rjust(18), [t[i], BSS_max*np.cos(t[i]), bsw40*np.sin(t[i]), bsw42*np.sin(t[i]), bsw43*np.sin(t[i]), bsw44*np.sin(t[i])])) + '\n')



