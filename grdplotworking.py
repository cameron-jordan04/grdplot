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
# Basic Usage:
# 	 -I 'filename.grd' to specify the input file
# 	 -O 'filename.png' to specify the name of the output file
#	 -A '[azimuth, elevation]' to specify the perspective
# 	 -W 'color style' (full list here: https://docs.generic-mapping-tools.org/6.2/cookbook/cpts.html)
#
# FIXME - Functionality to Impliment - in Man Pages
# -C[contour_control]
# -Gcolor_mode ** (creates various color maps based on different variables)
# -H 
# -Kintensity_file 
# -Oroot 
# -Ppagesize
# -S[color/shade] (histogram equalization)
# -T (coastline plotting, controls in misc, -M)
# -Uorientation 
# -V
#
# FIXME
# **render image using jupyter notebooks - render histogram and histogram equalization graph alongside final render in notebook
#
# ---------------------------------------------------------
import pygmt
import sys
import re

# DECLARE OPTIONAL VARIABLES
grid_input = 0
output_file = 0
color_style = 0
perspective_input = 0

# CHECK INPUTS
if sys.argv[1] == "--help" or sys.argv[1] == "--h":
	print('''
		USAGE INFORMATION:
			REQUIRED:
		-I 'filename.grd' to specify the input file
		
			OPTIONAL:
  	 	-O 'filename.png' to specify the name of the output file
	 	-A '[azimuth, elevation]' to specify the perspective
 	 	-W 'color style'
	''');
	
	exit() # Exits program after calling --help command
else:
	# CHECK REQUIRED COMPONENTS
	if sys.argv[1] == "-I":
		grid_input = sys.argv[2] #'ZTopo.grd'
		
	# CHECK OPTIONAL COMPONENTS
	if len(sys.argv) > 3:
		if sys.argv[3] == "-O":
			output_file = sys.argv[4] # assign name of output file
		if sys.argv[3] == "-A":
			perspective_input_long = sys.argv[4]
		if sys.argv[3] == "-G":
			color_style = sys.argv[4]
	if len(sys.argv) > 5:
		if sys.argv[5] == "-A":
			perspective_input_long = sys.argv[6]
		if sys.argv[5] == "-G":
			color_style = sys.argv[6]
	
	
# SET UNSPECIFIED DEFAULT VARIABLES
if output_file == 0:
	output_file = 'results/grid_image.png'
	
if color_style == 0:
	color_style = 'jet'
	
if perspective_input == 0:
	perspective_input = [-130, 30]
else:
	perspective_input = perspective_input_long[1:len(perspective_input_long) - 1]

frame =  ["xa1f0.25","ya1f0.25", "z2000+lmeters", "wSEnZ"]

### EXTRACT LOAD DATA FROM ...

# ASSIGN OUTPUT OF grdinfo TO grd_info
grd_info = pygmt.grdinfo(grid=grid_input)

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

### EXTRACT LOAD DATA FROM ...

# CREATE COLOR PALETTE
pygmt.makecpt(

        # REFERENCE TO cmap
        cmap=color_style,
        
        #max, min, inc
        series=f'{minz}/{maxz}/5',
        
        continuous=True
    )

# GMT figure to handle all plotting
fig = pygmt.Figure()

fig.grdview(
    
    # filename as entered above
    grid=grid_input,
    
    # minlon, maxlon, minlat, and maxlat set above, variable 5 and 6 indicate elevation range
    region=[minlon, maxlon, minlat, maxlat, minz, maxz],
    
    # first variable = degrees azimuth (-180 to 180), second variable = degrees elevation (0 - 90) - both of perspective
    perspective=perspective_input,
    
    # set labels to axis, and name the directional axis
    frame=["xa", "ya", "WSNE"],
    
    # M15c = 15 cm Mercator projection (map scale)
    projection="M15c",
    
    # sets relative z topo size to be 1.5 cm
    zsize="1.5c",
    
    # defines topological surface type; i = image
    surftype="i",
    
    # draws a plane at this specified z-level +g(color)
    plane=f'{minz}+ggrey',
    
    # adds uniform shading (-1, 1)
    shading=0,

    # Set the contour pen thickness to "1p"
    contourpen="1p",
)

fig.colorbar(

	perspective=True, 
	
	frame=["a2000", "x+l'Elevation in (m)'", "y+lm"]
)

fig.savefig(

	#accepts .eps file type (rotation is incorrect)
	output_file, 
	
	crop=True, 
	
	dpi=300
) 

