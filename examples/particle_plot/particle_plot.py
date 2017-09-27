##########################################################################
#
#   Before running make sure to fix all the path values and the shape value below
#       see https://github.com/haykh/brender_astro/wiki/Particle-data-plot for details
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
#   Particles data plot
#
##########################################################################

#####################################
#   initialize
#####################################
import particle_output
out_path = '/output/path/for/particles/' # <-- make sure to have slash in the end
fname = '/path/to/prtl.tot.001'
n_particles = 20000 # number of particles per each sort
shape = (100, 100, 100) # <-- specify this accordingly
fpath = particle_output.makeParticles(out_path, fname, shape, n_particles)

# this only needs to be done once
# if you already have the raw particle data, simply read it to `coords` array
# and feed the `createParticleMesh` function with it

#####################################
#   make
#####################################
import numpy as np

halo_size = 0.005

xs, ys, zs, inds = np.loadtxt(fpath, unpack=True, usecols=(0,1,2,3))

xs_e = xs[inds == 0]
ys_e = ys[inds == 0]
zs_e = zs[inds == 0]
coords_e = list(zip(xs_e, ys_e, zs_e))
xs_i = xs[inds == 1]
ys_i = ys[inds == 1]
zs_i = zs[inds == 1]
coords_i = list(zip(xs_i, ys_i, zs_i))

part_lec = brender.createParticleMesh(coords_e, [1,0,0], halo_size, 'lecs')
part_ion = brender.createParticleMesh(coords_i, [0,0,1], halo_size, 'ions')
