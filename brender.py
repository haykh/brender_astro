import bpy
from brender_aux import *

from lighting import Lighting
from camera import Camera
from render import Render

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

def createBoundingBox(name, col = (0., 0.7, 0.8), intens = 0.1):
    b_cube = makeCube('bbox_' + name)
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

def createVolumePlot(voxfile, cmap, name, intens = 10):
    my_cube = makeCube(name)
    print("Cube was created.")
    print("\tname: " + name)
    # cmap is given in the form: [col1, col2, col3, ...], where
    # col* = [%position from 0 to 1%, %rgba data in the form of a tuple (x,x,x,x)%]
    # e.g. [[0.0, (0, 0, 1, 0), [0.2, (0, 0, 1, 0.5)], [1, (1, 0, 0, 1.)]]
    volume_mat = makeVolumeMaterial(voxfile, cmap, name, intens)
    setMaterial(my_cube, volume_mat)
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
    setMaterial(sphere, mat)
    return sphere

def generateFieldlines(fpath, density = 1., keys = ('bx', 'by', 'bz'), n_traj = 100, max_dist = 120, min_seglen = 100., seg_step = 0.2):
    import h5py
    import numpy as np
    key_1, key_2, key_3 = keys

    data = h5py.File(fpath, 'r')
    u = np.array(data[key_1].value)
    v = np.array(data[key_2].value)
    w = np.array(data[key_3].value)

    maxUVW = np.sqrt(u**2 + v**2 + w**2).max()
    u /= maxUVW
    v /= maxUVW
    w /= maxUVW

    size_x = len(u[0][0])
    size_y = len(u[0])
    size_z = len(u)
    x = range(size_x)
    y = range(size_y)
    z = range(size_z)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    from find_flow import _gen_starting_points_3d, next_greater_power_of_2, grid2map_3d, map2grid_3d, integrate_3d

    n_cells_x = int(30 * density)
    n_cells_y = int(30 * density)
    n_cells_z = int(30 * density)
    nx_2 = next_greater_power_of_2(n_cells_x)
    ny_2 = next_greater_power_of_2(n_cells_y)
    nz_2 = next_greater_power_of_2(n_cells_z)
    n_cells_x = 2**nx_2
    n_cells_y = 2**ny_2
    n_cells_z = 2**nz_2
    gmap = np.zeros((n_cells_z, n_cells_y, n_cells_x))
    # print n_cells_x, n_cells_y, n_cells_z

    trajectories = []
    for xm, ym, zm in _gen_starting_points_3d((nx_2, ny_2, nz_2)):
        if gmap[zm][ym][xm] == 0:
            t = integrate_3d(xm, ym, zm, x, y, z, u, v, w, gmap, seg_step, max_dist)
            if (t is not None) and (len(t) > min_seglen / seg_step):
                for i in range(len(t)):
                    t[i] /= np.array([size_x, size_y, size_z])
                    t[i] -= np.array(0.5)
                    t[i] *= np.array(2)
                trajectories.append(t)
    import random as rnd
    if len(trajectories) > n_traj:
        trajectories = np.random.choice(trajectories, n_traj)
    return trajectories

def createFieldlines(name, trajectories):
    import numpy as np
    curveData = bpy.data.curves.new('crv_' + name, type='CURVE')
    print("Curve was created.")
    print("\tname: " + 'crv_' + name)
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    curveData.fill_mode = 'FULL'
    curveData.bevel_resolution = 10
    for coords in trajectories:
        # map coords to spline
        polyline = curveData.splines.new('POLY')
        polyline.points.add(len(coords) - 1)
        for i, coord in enumerate(coords):
            x,y,z = (np.array(coord))
            polyline.points[i].co = (x, y, z, 1)

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
    mat.emit = 1
    mat.specular_intensity = 0
    mat.diffuse_intensity = 0
    mat.emit = 10
    mat.use_shadows = False
    mat.use_cast_shadows = False
    setMaterial(curveOB, mat)

    return curveOB
