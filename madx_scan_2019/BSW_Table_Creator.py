# BSW Table Creator
# Creates a .TFS table that is read by MAD-X to set magnet strengths over time
# Haroon Rafique CERN BE-ABP-HSI 07.06.19
#
import numpy as np
import os

from math import log10, floor
def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

# golden values for the bump
bsw40              =    0.003498034648
bsw42              =    -0.01422287844
bsw43              =    0.01290524313
bsw44              =    -0.006001526439
BSS_max = 2*1.11828e-01 #from twiss

# build the parameter sweep lists
# ~ nstep = 50.
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
# ~ header = "@ NAME             %08s \"BSWTABLE\"\n@ TYPE             %04s \"USER\"\n@ TITLE            %03s \"BSW\"\n@ ORIGIN           %16s \"5.04.02 Linux 64\"\n@ DATE             %08s \"07/06/19\"\n@ TIME             %08s \"12.09.14\"\n*             BSEXT_T\t\tBSEXT40_K2\t\tBSEXT42_K2\t\tBSEXT43_K2\t\tBSEXT44_K2\n$\t\t%le\t\t%le\t\t%le\t\t%le\t\t%le\n"
header = "@ NAME             %08s \"BSWTABLE\"\n@ TYPE             %04s \"USER\"\n@ TITLE            %03s \"BSW\"\n@ ORIGIN           %16s \"5.04.02 Linux 64\"\n@ DATE             %08s \"07/06/19\"\n@ TIME             %08s \"12.09.14\"\n*             BSEXT_T\tBSS\tBSW40\tBSW42\tBSW43\tBSW44\n$\t%le\t%le\t%le\t%le\t%le\t%le\n"


# MADX
#-BSStren*(BSW40/BSW42)
# Equivalent
#-BSS_val[t]*(bsw40*np.sin(t) / bsw42*np.sin(t))

f = open("BSEXT_Bump.tfs","w")

f.write(header)

for i in t:
	# Sextupole strengths
	# ~ s40 = -BSS_val[i]*(bsw40*np.sin(i) / bsw42*np.sin(i))
	# ~ s42 = -BSS_val[i]*(bsw42*np.sin(i) / bsw42*np.sin(i))
	# ~ s43 = -BSS_val[i]*(bsw43*np.sin(i) / bsw42*np.sin(i))
	# ~ s44 = -BSS_val[i]*(bsw44*np.sin(i) / bsw42*np.sin(i))	
	# ~ column = str('\t\t%2.5e\t\t%2.5e\t%2.5e\t%2.5e\t%2.5e\n' % (t[i], s40, s42, s43, s44))
	
	# Bumper strengths
	bss = BSS_max*np.cos(i)
	s40 = bsw40*np.sin(i)
	s42 = bsw42*np.sin(i)
	s43 = bsw43*np.sin(i)
	s44 = bsw44*np.sin(i)
	
	column = str('\t%2.5e\t%2.5e\t%2.5e\t%2.5e\t%2.5e\t%2.5e\n' % (i, bss, s40, s42, s43, s44))
 
	f.write(column)
	
