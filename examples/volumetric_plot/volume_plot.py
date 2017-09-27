##########################################################################
#
#   Before running make sure to fix all the path values below
#       see https://github.com/haykh/brender_astro/wiki/Volumetric-data-plot for details
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

#####################################
#   initialize
#####################################
import to_bvox
out_path = '/output/path/for/bvox/' # <-- make sure to have slash in the end
fname = '/path/to/flds.tot.001'
prefix = 'curr'
# function that takes as input data from flds.tot and outputs scalar field

# # def valueFunc(data):
# #    return data['dens'].value

def valueFunc(data):
    sx = len(data['jx'].value[0][0])
    sy = len(data['jx'].value[0])
    sz = len(data['jx'].value)
    halfx = np.floor(sx/2.)
    halfy = np.floor(sy/2.)
    halfz = np.floor(sz/2.)
    rsquared = np.array([[[((x - halfx)**2 + (y - halfy)**2 + (z - halfz)**2) for x in range(sx)] for y in range(sy)] for z in range(sz)])
    return np.sqrt(np.array(data['jx'].value)**2 + np.array(data['jy'].value)**2 + np.array(data['jz'].value)**2) * rsquared

def normalizeFunc(value): # accepts value and outputs 'density' coord
    return np.log(1. + value)

max_val = 0.1

# you only need to do this once
# if you already have the .bvox file, just give it's full path to `bvoxfile` variable
bvoxfile = to_bvox.makeBvox(out_path, fname, valueFunc, normalizeFunc, max_val, prefix)

#####################################
#   make
#####################################
# bvoxfile = out_path + prefix + '.bvox'
cmap = [[0.0, (0, 0, 1, 0)], [0.2, (0, 0, 1, 0.5)], [1, (1, 0, 0, 1.)]]
name = prefix
intens = 15.
volume_cube = brender.createVolumePlot(bvoxfile, cmap, name, intens)
