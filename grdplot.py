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
		--hist_equalization='[True, color/shade, linear/normal]'

 Functionality to Impliment
 -C [contour_control] (doesn't work with surftype='i')

 -G color_mode ** (creates various color maps based on different variables)

 ?? -P pagesize

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
color_mode='1'
hist_equalization = [False, '', '']

# CREATE LIST OF VARIABLES
variables = [grid_input, output_file, perspective_input, color_style, intensity_file, color_mode, hist_equalization]

# CREATE LIST OF SYS VARIABLE TAGS
sysvariables = ['input', 'output', 'perspective', 'color_style', 'intensity_file', 'color_mode', 'hist_equalization']

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

'''
color_mode

1 - standard

2 - use shading method in .grdview and use grdgradient as .grd files (synthetic illumination)

3 - use drapegrid parameter in .grdview and reference the intensity_file (shaded by intensity file)

4 - use slope_file method of grdgradient (requires direction method to be specified), then pass the output
(outgrid?) as the .grd in .grdview (slope magnitude)

5 - same as above but shade by slope magnitude (shaded by slope magnitude) [shading = ]
'''

'''
hist_equalization

OPTION == [True, color, ]

- use histogram equalized grd in .grdview

OPTION == [True, shade, ]

- use histogram equalized grd into grdgradient, then pass gradient grid into [shading = ]

--------------------------------------------------------------------------------

## Linear Distribution ## OPTION = [True, , linear]

divisions = 16
linear = pygmt.grdhisteq.equalize_grid(grid=variables[0], divisions=divisions)
# linear_dist = pygmt.grd2xyz(grid=linear, output_type="pandas")["z"]
# pygmt.grdhisteq.compute_bins(grid=grid, divisions=divisions)

fig.grdview(grid=linear)

## Normal Distribution ## OPTION = [True, , normal]

normal = pygmt.grdhisteq.equalize_grid(grid=variables[0], gaussian=True)
#normal_dist = pygmt.grd2xyz(grid=normal, output_type="pandas")["z"]

fig.grdview(grid=normal)

'''

# COLOR_MODE 1 - STANDARD
if variables[5] == '1':
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
	    surftype="i",
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

# COLOR_MODE 2 - SYNTHETIC ILLUMINATION
# not working - not rendering grdview image
if variables[5] == '2':
	# Create new .grd for synthetic illumination
	dgrid = pygmt.grdgradient(grid=variables[0], radiance=[270, 30])

	print(
		pygmt.grdinfo(
			grid=dgrid,
		)
	)

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

	fig.grdview(
		# set grid
	    grid=dgrid,
		# set drapegrid
		#drapegrid=dgrid,
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

# COLOR_MODE 3 - SHADE BY INTENSITY FILE
if (variables[5] == '3' and intensity_file != ''):
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

	fig.grdview(
		# set grid
	    grid=variables[0],
		# set grid for shading
		shading=variables[4],
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

# COLOR_MODE 4 - FILL BY SLOPE MAGNITUDE
# failed 'grdgradient [ERROR]: No filename provided' - slope_file command not working
if variables[5] == '4':
	pygmt.makecpt(
		# REFERENCE TO cmap
		cmap=variables[3],
		#max, min, inc
		series=f'{minz}/{maxz}/5',
		# creates a uniform
		continuous=True
	)

	slope_mag_grd = ''

	pygmt.grdgradient(
		grid=variables[0],
		direction='a',
		slope_file=slope_mag_grd,
		outgrid=None
	)

	# GMT figure to handle all plotting
	fig = pygmt.Figure()

	fig.grdview(
		# set grid
	    grid=slope_mag_grd,
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

# COLOR_MODE 5 - SHADE BY SLOPE MAGNITUDE
if variables[5] == '5':
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

	fig.grdview(
		# set grid
	    grid=variables[0],
		# set shading grid
		shading = slope_mag_grd,
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

# HIST_EQUALIZATION = [TRUE, COLOR, LINEAR]


# HIST_EQUALIZATION = [TRUE, COLOR, NORMAL]


# HIST_EQUALIZATION = [TRUE, SHADE, LINEAR]


# HIST_EQUALIZATION = [TRUE, SHADE, NORMAL]
