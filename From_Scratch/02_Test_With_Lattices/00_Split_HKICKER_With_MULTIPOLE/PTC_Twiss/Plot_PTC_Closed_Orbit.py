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

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
		ext = os.path.splitext(file)[-1].lower()
		if ext in extensions:
			print (os.path.join(subdir, file))		# full path to file
			filename = file.replace('_','.')		# replace _ with a .
			fileno = int(filename.split('.')[1])	# use turn number as a key
			iterators.append(fileno)
			if (fileno <= min_file_no):				# find min turn
				min_file_no = fileno
				min_file = file
			elif (fileno >= max_file_no):			# find max turn
				max_file_no = fileno
				max_file = file

# iterate over files (turns)
for turn in iterators:
	
	# Open file
	
	# Save s, x
	
	# Add to dictionary as dict[turn] = (s, x)
	

# Plot

	fig, ax1 = plt.subplots();
	plt.title("PTC Injection Closure Tune Swing");
# Loop over turns

	# colormap 
	colors = cm.rainbow(np.linspace(0, 1, len(iterators)))
	c_it = int(0)
	
	
# For each turn plot s,x in a new colour

	savename = 'PTC_Closed_Orbit.png'
	plt.savefig(savename, dpi = 800);


