import bpy
from brender_aux import *

from lighting import Lighting
from camera import Camera
from render import Render

def initializeCamera():
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
    cam.type = 'PERSP' # 'ORTHO'
    cam.location = (4.5,-2,2)
    cam.pointing = (0,0,0)
    cam.lens = 50
    bpy.context.scene.camera = bpy.data.objects['Camera']
    # cam.ortho_scale = 2.0
    return cam

def getCamera():
    if objectsHaveCamera() is None:
        print('No camera found in the scene.')
        return None
    else:
        return objectsHaveCamera()

def createParticleMesh(coords, color, halo_size, name):
    color = getRightColor(color)

    me = bpy.data.meshes.new('prtl_' + name)
    print("Particle mesh was created.")
    print("\tname: " + 'prtl_' + name)
    ob = bpy.data.objects.new('prtl_' + name, me)
    print("Particle object was created.")
    print("\tname: " + 'prtl_' + name)

    ob.location = (0,0,0)

    bpy.context.scene.objects.link(ob)

    crds = [(0,0,0)]
    me.from_pydata(crds,[],[])
    ob.location = (0,0,0)
    ob = bpy.data.objects['prtl_' + name]

    deselect_all()
    ob.select = True

    bpy.context.scene.objects.active = ob
    mat = makeHaloMaterial(name = 'halo_' + name, diffuse = color, halo_size = halo_size)
    setMaterial(ob, mat)

    bpy.ops.object.mode_set(mode='EDIT')

    import bmesh
    bm = bmesh.from_edit_mesh(ob.data)
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    bm.verts[0].co = (coords[0][0], coords[0][1], coords[0][2])
    for i in range(0, len(coords)):
        bm.verts.new((coords[i][0], coords[i][1], coords[i][2]))

    bmesh.update_edit_mesh(ob.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    return ob

def createBoundingBox(name, col = (0., 0.7, 0.8), intens = 0.1, shape = (2,2,2)):
    b_cube = makeCube('bbox_' + name, size = shape)
    b_cube.dimensions = shape
    print("Cube was created.")
    print("\tname: " + 'bbox_' + name)
    b_mat = bpy.data.materials.new('bbox_' + name)
    b_mat.type = 'WIRE'
    b_mat.diffuse_intensity = 1.
    b_mat.specular_intensity = 1.
    b_mat.emit = intens
    b_mat.diffuse_color = col
    setMaterial(b_cube, b_mat)
    return b_cube

def createVolumePlot(voxfile, cmap, name, intens = 10, shape = (2,2,2)):
    my_cube = makeCube(name, size=shape)
    print("Cube was created.")
    print("\tname: " + name)
    # cmap is given in the form: [col1, col2, col3, ...], where
    # col* = [%position from 0 to 1%, %rgba data in the form of a tuple (x,x,x,x)%]
    # e.g. [[0.0, (0, 0, 1, 0), [0.2, (0, 0, 1, 0.5)], [1, (1, 0, 0, 1.)]]
    volume_mat = makeVolumeMaterial(voxfile, cmap, name, intens)
    setMaterial(my_cube, volume_mat)
    my_cube.dimensions = shape
    return my_cube

def createNetronStar(name, size, loc = (0, 0, 0), color = (0, 0.16, 0.7)):
    sphere = makeSphere(name, size, loc, color)
    print("Sphere was created.")
    print("\tname: " + name)
    mat = bpy.data.materials.new(name)
    print("Material was created.")
    print("\tname: " + name)
    mat.transparency_method = 'RAYTRACE'
    mat.use_shadeless = False
    mat.emit = 0.4
    mat.use_shadows = False
    mat.use_cast_shadows = False
    setMaterial(bpy.data.objects[name], mat)
    return sphere

def createFieldlines(name, trajectories, intens = 1., color = (1, 1, 1), scale = 1., shape = (2, 2, 2)):
    import numpy as np
    curveData = bpy.data.curves.new('crv_' + name, type='CURVE')
    print("Curve was created.")
    print("\tname: " + 'crv_' + name)
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    curveData.fill_mode = 'FULL'
    curveData.bevel_resolution = 10
    xc, yc, zc = np.array(shape) * 0.5
    for coords in trajectories:
        # map coords to spline
        polyline = curveData.splines.new('POLY')
        polyline.points.add(len(coords) - 1)
        for i, coord in enumerate(coords):
            x,y,z = (np.array(coord))
            polyline.points[i].co = (x * scale - xc, y * scale - yc, z * scale - zc, 1)
    # create Object
    curveOB = bpy.data.objects.new('crv_ob_' + name, curveData)
    print("Curve object was created.")
    print("\tname: " + 'crv_' + name)
    curveData.bevel_depth = 0.001
    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    mat = bpy.data.materials.new('crv_' + name)
    print("Material was created.")
    print("\tname: " + 'crv_' + name)
    mat.specular_intensity = 0
    mat.diffuse_intensity = 0
    mat.emit = intens
    mat.diffuse_color = color
    mat.use_shadows = False
    mat.use_cast_shadows = False
    setMaterial(curveOB, mat)
    return curveOB
