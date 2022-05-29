'''
---------------------------------------------------------

Cameron Jordan

Command:
	 python3 grdtest.py

Purpose:
 	 Create .eps or .png renderings of .grd files

USAGE INFORMATION:
 	REQUIRED:
		--input='filename.grd' to specify the input file
OPTIONAL:
 	 	--output='filename.png' to specify the name of the output file
	 	--perspective='[azimuth, elevation]' to specify the perspective
		--color_style='color style'
		--intensity_file='intensity_file.grd'
		--color_mode='#' (enter a number 1-7)

 Functionality to Impliment
 -C [contour_control] (doesn't work with surftype='i')

 -G color_mode ** (creates various color maps based on different variables)

 -P pagesize

 -S [color/shade] (histogram equalization)

 -U orientation

---------------------------------------------------------
'''

import pygmt
import sys
import re

# SET DEFAULT VARIABLES
grid_input = 0
output_file = 'results/output.png'
perspective_input = [-130, 30] #[azimuth, elevation]
color_style = 'jet'
intensity_file = ''
color_mode=1

# CREATE LIST OF VARIABLES
variables = [grid_input, output_file, perspective_input, color_style, intensity_file, color_mode]

# CREATE LIST OF SYS VARIABLE TAGS
sysvariables = ['input', 'output', 'perspective', 'color_style', 'intensity_file', 'color_mode']

# CHECK INPUTS
if sys.argv[1] == "--help" or sys.argv[1] == "--h":
	print('''
		USAGE INFORMATION:
			REQUIRED:
		--input='filename.grd' to specify the input file
			OPTIONAL:
  	 	--output='filename.png' to specify the name of the output file
	 	-perspective='[azimuth, elevation]' to specify the perspective
 	 	-color_style='color style'
	''');
	exit() # Exits program after calling --help command
else:
	for index in sys.argv:
		# EXTRACT THE SYS VARIABLE TAG, i.e. WHICH VARIABLE THE VALUE IS ASSIGNED TO
		arg = index[index.find('--')+2:index.rfind('=')]
		# EXTRACT THE VALUE OF THE VARIABLE
		value = index[index.find('=')+1:]
		for var in sysvariables:
			if arg == var:
				# GET INDEX OF var IN sysvariables
				currindex = sysvariables.index(var )
				# ASSIGN VALUE TO CORRECT VARIABLE
				variables[currindex] = value

### -------------------- START - EXTRACT LOAD DATA --------------------

# ASSIGN OUTPUT OF grdinfo TO grd_info
grd_info = pygmt.grdinfo(grid=variables[0])

# DECLARE SEARCH TERMS
to_find = ["x_min", "x_max", "y_min", "y_max", "v_min", "v_max"]

# CREATE EMPTY LIST TO STORE POSITION DATA
load_data_scrape = []

# SEARCH FOR x_min, x_max, y_min, y_max, v_min & x_max IN grd_info
for pos in to_find:
	new_string = grd_info[grd_info.find(pos):]
	data = re.search('\-?\d*\.?\d+', new_string)
	if data:
		# floatData = list(map(float, data))
		load_data_scrape.append(data.group())

# ASSIGN LIST RESULTS TO VARIABLES
r = load_data_scrape
minlon, maxlon, minlat, maxlat, minz, maxz = r[0], r[1], r[2], r[3], r[4], r[5]

### -------------------- END - EXTRACT LOAD DATA --------------------

pygmt.makecpt(
	# REFERENCE TO cmap
	cmap=variables[3],
	#max, min, inc
	series=f'{minz}/{maxz}/5',
	# creates a uniform
	continuous=True
)

# GMT figure to handle all plotting
fig = pygmt.Figure()

'''
def set_grid():
	if(color_mode == 1):
		return variables[0]
	elif(color_mode == 2): # not rendering differently than color_mode 1
		illumination_grid = pygmt.grdgradient(grid=variables[0], radience=[270,30])
		return illumination_grid
	#elif(color_mode == 3):

color_mode

1 - standard

2 - use shading method in .grdview and use grdgradient as .grd files

3 - use drapegrid parameter in .grdview and reference the intensity_file

4 - use slope_file method of grdgradient (requires direction method to be specified), then pass the output
(outgrid?) as the .grd in .grdview

5 - same as above but shade by slope magnitude
'''

fig.grdview(
	# set grid
    grid=variables[0],
    # minlon, maxlon, minlat, and maxlat set above, variable 5 and 6 indicate elevation range
    region=[minlon, maxlon, minlat, maxlat, minz, maxz],
    # first variable = degrees azimuth (-180 to 180), second variable = degrees elevation (0 - 90) - both of perspective
    perspective=variables[2],
    # set labels to axis, and name the directional axis
    frame=["xa", "ya", "WSNE"],
    # M15c = 15 cm Mercator projection (map scale)
    projection="M15c",
    # sets relative z topo size to be 1.5 cm
    zsize="1.5c",
    # defines topological surface type; i = image, sm = surface + m (for mesh) -- does not complete
    surftype="s",
    # Set the contour pen thickness to "1p" (only for surface (s) or mesh (default), surface types)
    # contourpen="1p"
)

fig.colorbar(
	# inherits the perspective of the render
	perspective=True,
	# sets frame for color bar
	frame=["a100", "x+l'Elevation in (m)'", "y+lm"],
	# sets color of color bar
	cmap=variables[3]
)

fig.savefig(
	#accepts .eps file type (rotation is incorrect)
	variables[1],
	# If True, will crop the figure canvas (page) to the plot area.
	crop=True,
	# If True, will open the figure in an external viewer.
	show=True,
	# Set raster resolution in dpi.
	dpi=300
)
