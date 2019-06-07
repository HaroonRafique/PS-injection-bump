import os
import numpy as np
import matplotlib.pylab as plt
import datetime
import metaclass
from write_ptc_table import write_PTCtable
from mpi_helpers import mpi_mkdir_p

mpi_mkdir_p('Tables')

# Have to iterate through files and read each value
directory = '../Test'
for filename in os.listdir(directory):
	if filename.endswith(".twiss"): 
		print '\n\tReading File : ',directory,'/',filename
		twiss = metaclass.twiss(directory + '/' + filename)
		
		multipole_orders = [3]
		
		twiss.print_labels()
		twiss.print_names()
		twiss.find_name('BSEXT40')
		
		print twiss.BSEXT40_T
		
		t = twiss.BSEXT40_T		
		# ~ t = (1E-3 / 100) * int(filename.split('.')[0])
		print '\n\tTime = ', t
		
		# ~ print twiss.alllabels
		# ~ print twiss.keys()		
		
		write_PTCtable('Tables/BSEXT40.dat', multipole_orders, t, twiss.BSEXT40_K2, twiss.BSEXT40_K2*0)
		write_PTCtable('Tables/BSEXT42.dat', multipole_orders, t, twiss.BSEXT42_K2, twiss.BSEXT42_K2*0)
		write_PTCtable('Tables/BSEXT44.dat', multipole_orders, t, twiss.BSEXT43_K2, twiss.BSEXT43_K2*0)
		write_PTCtable('Tables/BSEXT44.dat', multipole_orders, t, twiss.BSEXT44_K2, twiss.BSEXT44_K2*0)
		
			
		
		
# ~ b = metaclass.twiss('PSB/output/BSW_betabeat_correction.tfs')

# ~ t = b.BSW_T
# ~ multipole_orders = [1,3]
# ~ write_PTCtable('Tables/BI1.BSW1L1.1.dat', multipole_orders, t, [b.BSW1_K0, b.BSW1_K2], [b.BSW1_K0*0, b.BSW1_K2*0])
# ~ write_PTCtable('Tables/BI1.BSW1L1.2.dat', multipole_orders, t, [b.BSW2_K0, b.BSW2_K2], [b.BSW2_K0*0, b.BSW2_K2*0])
# ~ write_PTCtable('Tables/BI1.BSW1L1.3.dat', multipole_orders, t, [b.BSW3_K0, b.BSW3_K2], [b.BSW3_K0*0, b.BSW3_K2*0])
# ~ write_PTCtable('Tables/BI1.BSW1L1.4.dat', multipole_orders, t, [b.BSW4_K0, b.BSW4_K2], [b.BSW4_K0*0, b.BSW4_K2*0])

# ~ multipole_orders = 2
# ~ write_PTCtable('Tables/QDE3_CompAll.dat',    multipole_orders, t, b.KD3, b.KD3*0)
# ~ write_PTCtable('Tables/QDE14_CompAll.dat',   multipole_orders, t, b.KD14, b.KD14*0)
# ~ write_PTCtable('Tables/QDEstd_CompAll.dat',  multipole_orders, t, b.KKD, b.KKD*0)
# ~ write_PTCtable('Tables/QFOstd_CompAll.dat',  multipole_orders, t, b.KKF, b.KKF*0)




