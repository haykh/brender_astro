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
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[brender.objectsHaveLamp()].select = True
    bpy.ops.object.delete()
