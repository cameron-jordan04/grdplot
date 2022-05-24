## grdplot
# Cameron Jordan

# Command:
#	 python3 grdtest.py

# Purpose:
# 	 Create .eps or .png renderings of .grd files

# Basic Usage:
 	 -I 'filename.grd' to specify the input file
	 -O 'filename.png' to specify the name of the output file
	 -A '[azimuth, elevation]' to specify the perspective
 	 -W 'color style' (full list here: https://docs.generic-mapping-tools.org/6.2/cookbook/cpts.html)

# FIXME - Functionality to Impliment - in Man Pages
 -C[contour_control]
 -Gcolor_mode ** (creates various color maps based on different variables)
 -H
 -Kintensity_file
 -Oroot
 -Ppagesize
 -S[color/shade] (histogram equalization)
 -T (coastline plotting, controls in misc, -M)
 -Uorientation
 -V

# FIXME
 **render image using jupyter notebooks - render histogram and histogram equalization graph alongside final render in notebook
