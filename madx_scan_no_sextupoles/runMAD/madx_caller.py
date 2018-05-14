# MADx caller --> no sextupoles
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

# build the parameter sweep lists
nstep = 50. #will give twice the steps than this

t = np.arange(0,nstep+1,1)/nstep * np.pi/2
t = np.append(t, t+np.pi/2)
# strengths for the simulation
#quadrupole strength
bsw40_val = bsw40*np.sin(t)
bsw42_val = bsw42*np.sin(t)
bsw43_val = bsw43*np.sin(t)
bsw44_val = bsw44*np.sin(t)


# read the master madx script
with open('/afs/cern.ch/work/e/esenes/madx_scan_condor_noSextupoles/runMAD/sweepBump_master.madx','r+') as f:
    message = f.read()
    head = message[:1364]
    body1 = message[1364:1685] #up to just before the ptc_twiss
    body2 = message[1760:1854] # skip the ptc_twiss
    tail = message[1890:]
    f.close()


# now run madx iteratively
for k in range(len(bsw40_val)):
    firstAdd = '\n\nbsw40 := ' + str(bsw40_val[k]) + ';\n' + 'bsw42 := ' + str(bsw42_val[k]) + ';\n' + 'bsw43 := ' + str(bsw43_val[k]) + ';\n'  + 'bsw44 := ' + str(bsw44_val[k]) + ';\n'

    customTwiss = '\nptc_twiss,closed_orbit,icase=56,no=4,summary_table=ptc_twiss_summary,file='+str(k)+'.twiss;\n'

    assignRow = 'Assign, echo='+str(k)+'.out;\n'
    # recompose the script adding the desired lines
    newMessage = head+firstAdd+body1+customTwiss+body2+assignRow+tail
    with open('/afs/cern.ch/work/e/esenes/madx_scan_condor_noSextupoles/runMAD/sweepBump.madx','w') as f:
        f.write(newMessage)
        f.close()


    print('Iter '+str(k)+' : RUNNING MADx ...')
    os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64</afs/cern.ch/work/e/esenes/madx_scan_condor_noSextupoles/runMAD/sweepBump.madx")
