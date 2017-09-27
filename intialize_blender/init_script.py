import sys
sys.path.append('/path/to/brender/') # <-- change this
import brender
import numpy as np
import bpy

##########################################################################
#   set camera
##########################################################################
brender.initiateCamera()

##########################################################################
#   set render
##########################################################################
render_directory = '/path/to/desired/folder/' # <-- change this
render_name = 'psr_'
render = brender.Render(render_directory, render_name)

brender.Render.set_resolution(1000, 1000)

##########################################################################
#   set lighting
##########################################################################
light = brender.Lighting('EMISSION')
if brender.objectsHaveLamp():
    brender.delete_object('Lamp')
