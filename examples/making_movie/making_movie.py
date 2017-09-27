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
#   moving camera and rendering on the fly
#       this is just an example, in general any camera motion can be modeled
#
##########################################################################
x, y, z = cam.location # initial location
rxy = np.sqrt(x**2 + y**2)
phi_0 = np.arctan(x / y) # initial phase
steps_per_2pi = 30
for i in range(steps_per_2pi):
    phi = phi_0 - 2. * np.pi * i / steps_per_2pi
    loc = (rxy * np.cos(phi), np.sign(y) * rxy * np.sin(phi), z)
    cam.location = loc
    render.render()

# images can be later combined to make a movie
