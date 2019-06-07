# MADx caller
#
#   --> New version that rewrites the madx file instead of calling strength files
#
#   Eugenio Senes
#   Created 14.02.2018
import numpy as np
import os

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

# this peice for with-sextupoles
with open('./sweepBump_master.madx','r') as f:
    message = f.read()
    
    # using optimised seq
    # ~ head = message[:1310]
    # ~ body1 = message[1310:1631] #up to just before the ptc_twiss
    # ~ body2 = message[1708:1801] # skip the ptc_twiss
    # ~ tail = message[1801:]
    
    # using new sequence (older than optimised)
    head = message[:1301]
    body1 = message[1301:1625] #up to just before the ptc_twiss
    body2 = message[1702:1795] # skip the ptc_twiss
    tail = message[1795:]
    f.close()

verbose = False

if verbose:
	print '\n\nHEAD\n ------------------------------------------ \n'
	print head
	print '\n\nBODY1\n ------------------------------------------ \n'
	print body1
	print '\n\nBODY2\n ------------------------------------------ \n'
	print body2
	print '\n\nTAIL\n ------------------------------------------ \n'
	print tail

	os.exit(1)

for k in range(len(bsw40_val)):
    # define the rows to add
    firstAdd = '\n\nBSStren := ' + str(BSS_val[k]) + ';\n' + 'bsw40 := ' + str(bsw40_val[k]) + ';\n' + 'bsw42 := ' + str(bsw42_val[k]) + ';\n' + 'bsw43 := ' + str(bsw43_val[k]) + ';\n'  + 'bsw44 := ' + str(bsw44_val[k]) + ';\n'

    customTwiss = '\nptc_twiss, closed_orbit, icase=56, no=4, summary_table=ptc_twiss_summary, file='+str(k)+'.twiss;\n'
    assignRow = '\nAssign, echo='+str(k)+'.out;\n'
    
    # recompose the script adding the desired lines
    newMessage = head + firstAdd + body1 + customTwiss + body2 + assignRow + tail
    
    # create the madx file and run it
    with open('sweepBump.madx','w') as f:
        f.write(newMessage)
        f.close()
   # # ~ os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < sweepBump.madx") # AFS version
	os.system("/home/HR/Documents/madx-linux64-gnu < sweepBump.madx") # local version
