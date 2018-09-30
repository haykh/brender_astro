import sys
sys.path.append('/home/hakobyan/Downloads/brender_astro') # <-- change this
import brender
import numpy as np
import bpy

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   set lighting
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
brender.Lighting('EMISSION')
brender.clearScene()
