# ---------------------------------------------------------
#
# Cameron Jordan
#
# Command:
#	 python3 grdtest.py
#
# Purpose:
# 	 Create .eps or .png renderings of .grd files
#
# USAGE INFORMATION:
#	REQUIRED:
#		--input='filename.grd' to specify the input file
#	OPTIONAL:
# 	 	--output='filename.png' to specify the name of the output file
#	 	-perspective='[azimuth, elevation]' to specify the perspective
#	 	-color_style='color style'
#
# FIXME - Functionality to Impliment - in Man Pages
# -C [contour_control] (doesn't work with surftype='i')
#
# -G color_mode ** (creates various color maps based on different variables)
#
# -K intensity_file
#
# -P pagesize
#
# -S[color/shade] (histogram equalization)
#
# -T (coastline plotting, controls in misc, -M)
#
# -U orientation
#
# FIXME
# **render image using jupyter notebooks - render histogram and histogram equalization graph alongside final render in notebook
#
# ---------------------------------------------------------

import pygmt
import sys
import re

# SET DEFAULT VARIABLES
grid_input = 0
output_file = 'results/output.png'
perspective_input = [-130, 30]
color_style = 'jet'

# CREATE LIST OF VARIABLES
variables = [grid_input, output_file, perspective_input, color_style]

# CREATE LIST OF SYS VARIABLE TAGS
sysvariables = ['input', 'output', 'perspective', 'color_style']

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

# TEST PRINT FOR ASSIGNMENT OF VARIABLES -- UNIT TEST
print(*variables)

### EXTRACT LOAD DATA

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

### END - EXTRACT LOAD DATA

# CREATE COLOR PALETTE
pygmt.makecpt(

        # REFERENCE TO cmap
        cmap=variables[3],

        #max, min, inc
        series=f'{minz}/{maxz}/5',

        continuous=True
    )

# GMT figure to handle all plotting
fig = pygmt.Figure()

fig.grdview(

    # filename as entered above
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
    surftype="i",

    # draws a plane at this specified z-level +g(color)
    plane=f'{minz}+ggrey',

    # adds uniform shading (-1, 1)
    shading=0,

    # Set the contour pen thickness to "1p" (only for surface (s) or mesh (default), surface types)
    # contourpen="1p"
)

fig.colorbar(

	perspective=True,

	frame=["a2000", "x+l'Elevation in (m)'", "y+lm"],

	cmap='jet'
)

fig.savefig(

	#accepts .eps file type (rotation is incorrect)
	variables[1],

	crop=True,

	show=True,

	dpi=300
)
