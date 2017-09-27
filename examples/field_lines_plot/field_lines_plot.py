##########################################################################
#
#   Before running make sure to fix all the path values below
#       see details: https://github.com/haykh/brender_astro/wiki/Field-line-plot
#
##########################################################################

import sys
sys.path.append('/path/to/BRender')
import brender
import numpy as np

##########################################################################
#   set camera
##########################################################################
cam = brender.initilizeCamera()

##########################################################################
#   set render
##########################################################################
render_directory = '/path/to/output/render/'
render_name = 'psr_'
render = brender.Render(render_directory, render_name)

brender.Render.set_resolution(1000, 1000)

##########################################################################
#   bounding box
##########################################################################
name = 'psr'
b_box = brender.createBoundingBox(name, intens=0.5)

##########################################################################
#
#   3D density plot
#
##########################################################################

##########################################################################
#
# assuming the .bvox file already exists
#   see details: https://github.com/haykh/brender_astro/wiki/Volumetric-data-plot
#
##########################################################################
out_path = '/output/path/for/bvox/' # <-- make sure to have slash in the end
prefix = 'curr'
bvoxfile = out_path + prefix + '.bvox'
cmap = [[0.0, (0, 0, 1, 0)], [0.2, (0, 0, 1, 0.5)], [1, (1, 0, 0, 1.)]]
name = prefix
intens = 15.
volume_cube = brender.createVolumePlot(bvoxfile, cmap, name, intens)

##########################################################################
#
#   Field flow plot
#
##########################################################################

#####################################
#   initialize
#####################################
fname = '/path/to/flds.tot.001'

# those are all optional parameters
density = 1. # provide density of field lines
n_traj = 100
max_dist_from_center = 120 # max length of trajectory point from the center of the cube
seg_step = 0.2
min_fldline_length = 100
keys = ('bx', 'by', 'bz') # plotting b-field

trajectories = brender.generateFieldlines(fname, density, keys, n_traj, max_dist_from_center, min_fldline_length, seg_step)

#####################################
#   make
#####################################
name = 'b-field'
curve_obj = brender.createFieldlines(name, trajectories)


#####################################
#   making neutron star
#       see details: https://github.com/haykh/brender_astro/wiki/Basics-of-BRender#creating-a-neutron-star
#####################################
name = 'neutronstar'
size = 0.06
ns_obj = brender.createNetronStar(name, size)
