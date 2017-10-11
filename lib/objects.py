import bpy
from lib.hlp_func import *

class BoundingBox(object):
    def __init__(self,
                 name="NoNameBbox",
                 color = (1, 1, 1),
                 size = (2, 2, 2),
                 location = (0,0,0),
                 intensity = 1.):
        deselect_all()
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0), radius=1)
        cube = bpy.data.objects['Cube']
        cube.name = name
        cube.scale = (1,1,1)
        cube.dimensions = size
        cube.location = location
        b_mat = bpy.data.materials.new(name)
        b_mat.type = 'WIRE'
        b_mat.diffuse_intensity = 1.
        b_mat.specular_intensity = 1.
        b_mat.emit = intensity
        b_mat.diffuse_color = getRightColor(color)
        setMaterial(cube, b_mat)
        self.__name = name
        self.__intensity = intensity
        self.__color = getRightColor(color)
        self.__size = size
        self.__location = location
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, color):
        b_mat = bpy.data.materials[self.__name]
        b_mat.diffuse_color = getRightColor(color)
        self.__color = getRightColor(color)
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self, size):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].dimensions = size
        self.__size = size
    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location
    @property
    def intensity(self):
        return self.__color
    @intensity.setter
    def intensity(self, intensity):
        b_mat = bpy.data.materials[self.__name]
        b_mat.emit = intensity
        self.__intensity = intensity

class Sphere(object):
    def __init__(self,
                 name="NoNameSphere",
                 color = (0, 0.16, 0.7),
                 size = (2, 2, 2),
                 location = (0, 0, 0),
                 intensity = 0.4):
        deselect_all()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, size=1.)
        sphere = bpy.data.objects['Sphere']
        sphere.name = name
        sphere.scale = (1, 1, 1)
        sphere.dimensions = size
        sphere.location = location
        sph_mat = bpy.data.materials.new(name)
        sph_mat.diffuse_color = getRightColor(color)
        sph_mat.transparency_method = 'RAYTRACE'
        sph_mat.use_shadeless = False
        sph_mat.emit = intensity
        sph_mat.use_shadows = False
        sph_mat.use_cast_shadows = False
        setMaterial(sphere, sph_mat)
        self.__name = name
        self.__intensity = intensity
        self.__color = getRightColor(color)
        self.__size = size
        self.__location = location
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, color):
        sph_mat = bpy.data.materials[self.__name]
        sph_mat.diffuse_color = getRightColor(color)
        self.__color = getRightColor(color)
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self, size):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].dimensions = size
        self.__size = size
    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location
    @property
    def intensity(self):
        return self.__color
    @intensity.setter
    def intensity(self, intensity):
        b_mat = bpy.data.materials[self.__name]
        b_mat.emit = intensity
        self.__intensity = intensity

class VolumePlot(object):
    def __init__(self,
                 voxfilepath,
                 name="NoNameBVOX",
                 size = (2, 2, 2),
                 location = (0, 0, 0),
                 intensity = 10.,
                 cmap = [[0.0, (0, 0, 1, 0)], [0.2, (0, 0, 1, 0.5)], [1, (1, 0, 0, 1.)]]
                         ):
        deselect_all()
        # creating object
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0), radius=1)
        box = bpy.data.objects['Cube']
        box.name = name
        box.scale = (1,1,1)
        box.dimensions = size
        box.location = location

        # creating material
        mat = bpy.data.materials.new(name)
        mat.type = 'VOLUME'
        mat.volume.density = 0.
        mat.volume.density_scale = 2.
        mat.volume.emission = 0.
        mat.volume.scattering = 1.4
        mat.volume.step_method = 'CONSTANT'
        mat.volume.step_size = 0.01

        matSlot = mat.texture_slots.add()
        matTex = bpy.data.textures.new(name, 'VOXEL_DATA')
        matSlot.texture = matTex

        matTex.use_color_ramp = True
        matTex.voxel_data.file_format = 'BLENDER_VOXEL'
        matTex.voxel_data.filepath = voxfilepath
        matTex.voxel_data.intensity = intensity
        matTex.intensity = 1.
        matTex.contrast = 1.

        matSlot.mapping = 'CUBE'
        matSlot.texture_coords = 'ORCO'
        matSlot.use_map_density = True
        matSlot.use_map_emission = True
        matSlot.use_map_color_emission = True
        matSlot.density_factor = 1.
        matSlot.emission_factor = 1.
        matSlot.emission_color_factor = 1.

        for i in range(len(cmap) - 2):
            matTex.color_ramp.elements.new(position = 0.0)
        for i in range(len(cmap)):
            matTex.color_ramp.elements[i].position = cmap[i][0]
            matTex.color_ramp.elements[i].color = cmap[i][1]

        setMaterial(box, mat)
        self.__name = name
        self.__intensity = intensity
        self.__cmap = cmap
        self.__size = size
        self.__location = location
        self.__voxdata = voxfilepath
        self.__density = 2.
        self.__brightness = 1.
        self.__contrast = 1.
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        for tex in bpy.data.textures:
            if tex.name == self.__name:
                tex.name = name # change textures name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name
    @property
    def cmap(self):
        return self.__cmap
    @cmap.setter
    def cmap(self, cmap):
        matTex = bpy.data.textures[self.__name]
        ramp_elems = matTex.color_ramp.elements
        for i in range(1, len(ramp_elems) - 1):
            ramp_elems.remove(ramp_elems[i])
        for i in range(len(cmap) - 2):
            ramp_elems.new(position = 0.0)
        for i in range(len(cmap)):
            ramp_elems[i].position = cmap[i][0]
            ramp_elems[i].color = cmap[i][1]
        self.__cmap = cmap
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self, size):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].dimensions = size
        self.__size = size
    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location
    @property
    def intensity(self):
        return self.__intensity
    @intensity.setter
    def intensity(self, intensity):
        matTex = bpy.data.textures[self.__name]
        matTex.voxel_data.intensity = intensity
        self.__intensity = intensity
    @property
    def voxdata(self):
        return self.__voxdata
    @voxdata.setter
    def voxdata(self, voxdata):
        matTex = bpy.data.textures[self.__name]
        matTex.voxel_data.filepath = voxdata
        self.__voxdata = voxdata
    @property
    def density(self):
        return self.__density
    @density.setter
    def density(self, density):
        mat = bpy.data.materials[self.__name]
        mat.volume.density_scale = density
        self.__density = density
    @property
    def brightness(self):
        return self.__brightness
    @brightness.setter
    def brightness(self, brightness):
        matTex = bpy.data.textures[self.__name]
        matTex.intensity = brightness
        self.__brightness = brightness
    @property
    def contrast(self):
        return self.__contrast
    @contrast.setter
    def contrast(self, contrast):
        matTex = bpy.data.textures[self.__name]
        matTex.contrast = contrast
        self.__contrast = contrast

class ParticlePlot(object):
    def __init__(self,
                 coords,
                 name="NoNamePPlot",
                 halo_size = 0.005,
                 location = (0, 0, 0),
                 color = (0, 0, 1)
                         ):
        deselect_all()
        # creating object
        me = bpy.data.meshes.new(name)
        ob = bpy.data.objects.new(name, me)
        ob.location = location
        bpy.context.scene.objects.link(ob)
        crds = [(0,0,0)]
        me.from_pydata(crds,[],[])
        deselect_all()
        ob.select = True
        bpy.context.scene.objects.active = ob
        # creating material
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = getRightColor(color)
        mat.alpha = 1.
        mat.type = 'HALO'
        mat.halo.size = halo_size
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
        self.__name = name
        self.__color = getRightColor(color)
        self.__halo_size = halo_size
        self.__location = location
        self.__coords = coords
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        for me in bpy.data.meshes:
            if me.name == self.__name:
                me.name = name # change textures name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, color):
        mat = bpy.data.materials[self.__name]
        mat.diffuse_color = getRightColor(color)
        self.__color = getRightColor(color)
    @property
    def halo_size(self):
        return self.__halo_size
    @halo_size.setter
    def halo_size(self, halo_size):
        mat = bpy.data.materials[self.__name]
        mat.halo.size = halo_size
        self.__halo_size = halo_size
    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location
    @property
    def coords(self):
        return self.__coords
    @coords.setter
    def coords(self, coords):
        ob = bpy.data.objects[self.__name]
        deselect_all()
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        import bmesh
        bm = bmesh.from_edit_mesh(ob.data)
        for i in range(len(self.__coords)):
            if hasattr(bm.verts, "ensure_lookup_table"):
                bm.verts.ensure_lookup_table()
            bm.verts.remove(bm.verts[0])
        if hasattr(bm.verts, "ensure_lookup_table"):
            bm.verts.ensure_lookup_table()
        bm.verts[0].co = (coords[0][0], coords[0][1], coords[0][2])
        for i in range(0, len(coords)):
            bm.verts.new((coords[i][0], coords[i][1], coords[i][2]))
        bmesh.update_edit_mesh(ob.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        self.__coords = coords

class FieldLines(object):
    def __init__(self,
                 fieldlines,
                 name="NoNameFieldlines",
                 color = (1, 1, 1),
                 scale = 1.,
                 location = (0, 0, 0),
                 size = (2, 2, 2),
                 intensity = 1.):
        deselect_all()
        curveData = bpy.data.curves.new(name, type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2
        curveData.fill_mode = 'FULL'
        curveData.bevel_resolution = 10
        xc, yc, zc = np.array(shape) * 0.5 + location
        for coords in fieldlines:
            # map coords to spline
            polyline = curveData.splines.new('POLY')
            polyline.points.add(len(coords) - 1)
            for i, coord in enumerate(coords):
                x,y,z = (np.array(coord))
                polyline.points[i].co = (x * scale - xc, y * scale - yc, z * scale - zc, 1)
        # create Object
        curveOB = bpy.data.objects.new(name, curveData)
        curveData.bevel_depth = 0.001
        scn = bpy.context.scene
        scn.objects.link(curveOB)
        scn.objects.active = curveOB
        mat = bpy.data.materials.new(name)
        mat.specular_intensity = 0
        mat.diffuse_intensity = 0
        mat.emit = intensity
        mat.diffuse_color = color
        mat.use_shadows = False
        mat.use_cast_shadows = False
        setMaterial(curveOB, mat)
        self.__name = name
        self.__intensity = intensity
        self.__color = getRightColor(color)
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, color):
        b_mat = bpy.data.materials[self.__name]
        b_mat.diffuse_color = getRightColor(color)
        self.__color = getRightColor(color)
    @property
    def intensity(self):
        return self.__color
    @intensity.setter
    def intensity(self, intensity):
        mat = bpy.data.materials[self.__name]
        mat.emit = intensity
        self.__intensity = intensity
