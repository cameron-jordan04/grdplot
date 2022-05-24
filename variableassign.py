import sys
import re

# format of input --input='ZTopo.grd'

# set defaults of variables
grid_input = 'none'
output_file = 'output.png'
perspective_input = '[-130, 30]'
color_style = 'jet'

# vector of variables to assign to
variables = [grid_input, output_file, perspective_input, color_style]

sysvariables = ['input', 'output', 'perspective', 'color_style']

for index in sys.argv:
	# extract which variable is being assigned
	arg = index[index.find('--')+2:index.rfind('=')]
	
	# extract the value of the variable to be assigned
	value = index[index.find('=')+1:]
	
	for var in sysvariables:
		if arg == var:
			# get index of var in sysvariables
			currindex = sysvariables.index(var )
			# assign value to appropriate variable
			variables[currindex] = value
			
print(*variables)


