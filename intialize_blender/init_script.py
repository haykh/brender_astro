import sys
sys.path.append('/path/to/brender/') # <-- change this
import brender
import numpy as np

##########################################################################
#   set camera
##########################################################################
if not brender.sceneHasCamera(): # scene has no camera
    if brender.objectsHaveCamera() is None:
        if len(bpy.data.cameras) > 0:
            cam = bpy.data.cameras[0]
        else:
            cam = bpy.data.cameras.new("Camera")
        cam_ob = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.objects.link(cam_ob)
    else:
        cam_ob = objectsHaveCamera()
        if len(bpy.data.cameras) > 0:
            cam = bpy.data.cameras[0]
        else:
            cam = bpy.data.cameras.new("Camera")
        bpy.context.scene.objects.link(cam_ob)

cam = brender.Camera()
cam.type = 'PERSP' # 'ORTHO'
cam.location = (4.5,-2,2)
cam.pointing = (0,0,0)
cam.lens = 50
# cam.ortho_scale = 2.0

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
