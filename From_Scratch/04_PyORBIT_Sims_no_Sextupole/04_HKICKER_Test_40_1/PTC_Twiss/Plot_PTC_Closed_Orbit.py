# Script to read multiple PTC twiss files and plot the closed orbit
# Expects a PTC twiss created with the following command:
# select, flag=ptc_twiss, column=name, s, betx, px, bety, py, disp3, disp3p, disp1, disp1p, x, y;
# 26.08.19 Haroon Rafique CERN BE-ABP-HSI 

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import numpy as np
import os
import scipy.io as sio

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5


extensions = ('.ptc')		# All outputs are .ptc files
iterators = []				# Integers (turn) used to iterate over files

# Search from current directory
print '\nFind PTC Twiss files\n'
for subdir, dirs, files in os.walk('.'):
	# Iterate over all files
    for file in files:
		# Find files with required extension
		ext = os.path.splitext(file)[-1].lower()
		if ext in extensions:
			# Print full file path
			# ~ print (os.path.join(subdir, file))		# full path to file
			fileno = int(file.split('.')[0])	# use turn number as a key
			iterators.append(fileno)

data = dict()


# iterate over files (turns)
print '\nRead s, x data from files\n'
last_s = 0

for turn in sorted(iterators):
	
	s = []
	x = []

	# Open file
	infile = str(turn) + '.ptc'
	fin=open(infile,'r').readlines()[90:]

	# Save s, x
	for l in fin:
		if last_s == float(l.split()[1]):
			pass
		else:
			last_s =float(l.split()[1])
			s.append(float(l.split()[1]))
			x.append(float(l.split()[-2]))

	# Add to dictionary as dict[turn] = (s, x)
	data[turn] = [s, x]
	last_s = 0
	

# Access turn 0, s column
# data[0][0]
# Access turn 25, x column, first value
# ~ print data[25][1][0]

print 'length of data = ', len(data[25][0])
print 'max x data = ', max(data[25][1])
print 'min x of data = ', min(data[25][1])


#-----------------------------------------------------------------------
#------------------------------PLOTTING---------------------------------
#-----------------------------------------------------------------------

case = '00_Split_HKICKER_with_MULTIPOLE'

print '\n\tStart Plotting\n'

fig, ax1 = plt.subplots();
plt.title("PTC Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(iterators)))
c_it = int(0)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

for turn in sorted(iterators):
	print 'Plotting turn ', turn
	plt.plot(data[turn][0], data[turn][1], color=colors[c_it])

	# For each turn plot s,x in a new colour
	c_it += 1

ax1.grid()

savename = 'PTC_Closed_Orbit' + case + '.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 1 done\n'


fig, ax1 = plt.subplots();
plt.title("PTC Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(iterators)))
c_it = int(0)

ax1.set_xlim(470.0, 510.0)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

test  = [1]

# ~ plt.plot(data[1][0], data[1][1], color=colors[c_it])

for turn in sorted(iterators):
	print 'Plotting turn ', turn
	plt.plot(data[turn][0], data[turn][1], color=colors[c_it])

	# For each turn plot s,x in a new colour
	c_it += 1

ax1.grid()

savename = 'PTC_Closed_Orbit' + case + '_zoom.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 2 done\n'

