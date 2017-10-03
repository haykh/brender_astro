import sys
sys.path.append('/path/to/brender/') # <-- change this
import brender
import numpy as np
import bpy

##########################################################################
#   set lighting
##########################################################################
light = brender.Lighting('EMISSION')
if brender.objectsHaveLamp():
    brender.delete_object('Lamp')
