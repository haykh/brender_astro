import sys
sys.path.append('/path/to/brender/') # <-- change this
import brender
import numpy as np
import bpy

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   set lighting
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
brender.Lighting('EMISSION')
brender.clearScene()
