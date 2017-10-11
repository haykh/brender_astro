import bpy

def runScript(filename):
    exec(compile(open(filename).read(), filename, 'exec'))

# # # # # # # # # # # # # # # # # #
#   Working with Scene
def clearScene():
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink = True)
    for tex in bpy.data.textures:
        bpy.data.textures.remove(tex, do_unlink = True)
    for ob in bpy.data.objects:
        bpy.data.objects.remove(ob, do_unlink = True)
    for cur in bpy.data.curves:
        bpy.data.curves.remove(cur, do_unlink = True)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh, do_unlink = True)
    for img in bpy.data.images:
        bpy.data.images.remove(img, do_unlink = True)
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam, do_unlink = True)
    for lmp in bpy.data.lamps:
        bpy.data.lamps.remove(lmp, do_unlink = True)

def sceneHasCamera():
    for sc_obj in bpy.context.scene.objects:
        if 'Camera' in sc_obj.name:
            return True
    return False

def objectsHaveCamera():
    for obj in bpy.data.objects:
        if 'Camera' in obj.name:
            return obj
    return None

def initializeCamera():
    from lib.scene.camera import Camera
    if not sceneHasCamera(): # scene has no camera
        if objectsHaveCamera() is None:
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
    cam = Camera()
    cam.name = 'Camera'
    cam.type = 'PERSP' # 'ORTHO'
    cam.location = (4.5,-2,2)
    cam.pointing = (0,0,0)
    cam.lens = 50
    bpy.context.scene.camera = bpy.data.objects['Camera']
    # cam.ortho_scale = 2.0
    return cam
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#   Working with colors
def getRightColor(color):
    if isinstance(color, str):
        if color[0] != '#':
            color = '#' + color
        if (len(color) != 4) and (len(color) != 7):
            import sys
            if sys.version_info[0] < 3:
                print "Wrong color format. HEX or RGB supported only."
            else:
                print ("Wrong color format. HEX or RGB supported only.")
            return
        color = hexToRgb(color)
    else:
        if len(color) != 3:
            import sys
            if sys.version_info[0] < 3:
                print "Wrong color format. HEX or RGB supported only."
            else:
                print ("Wrong color format. HEX or RGB supported only.")
            return
        if color[0] > 1:
            color[0] = color[0] / 255.
            color[1] = color[1] / 255.
            color[2] = color[2] / 255.
    return color

def hexToRgb(hex):
    hex = hex.lstrip('#')
    if len(hex) == 3:
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]
    return [int(hex[i:i+2], 16) / 255. for i in (0, 2 ,4)]
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#   Working with objects
def hide_object(name, hide_render = True):
    bpy.data.objects[name].hide = True
    bpy.data.objects[name].hide_render = hide_render

def unhide_object(name):
    bpy.data.objects[name].hide = False
    bpy.data.objects[name].hide_render = False

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def deselect_all():
    scene = bpy.context.scene
    for ob in scene.objects:
        ob.select = False
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#   Working with data
def importFieldlines(out_file):
    import numpy as np
    lines = open(out_file).read().splitlines()
    fieldlines = []
    fieldline = None
    for line in lines:
        tup = tuple(map(float, line.split(' ')))
        if len(tup) == 1:
            if fieldline is not None:
                fieldlines.append(fieldline)
            fieldline = []
        elif len(tup) == 3:
            x,y,z = tup
            fieldline.append([x,y,z])
        else:
            raise 'Reading error'
    fieldlines.append(fieldline)
    return fieldlines
# # # # # # # # # # # # # # # # # #
