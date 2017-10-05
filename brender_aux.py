import bpy

def importFieldlines(out_path):
    import pickle
    pkl_file = open(out_pat + '.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pkl_file.close()
    return data1
    # import numpy as np
    # return np.load(out_path + '.npy')

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

def objectsHaveLamp():
    for obj in bpy.data.objects:
        if 'Lamp' in obj.name:
            return obj.name
    return False

def makeHaloMaterial(name, diffuse, specular = (1, 1, 1), alpha = 1, emiss = 1., mat_type = 'HALO', halo_size = None):
    mat = bpy.data.materials.new(name)
    print("Material was created.")
    print("\tname: " + name)
    mat.emit = emiss
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.use_transparency = True
    if mat_type is not None:
        mat.type = mat_type
    if halo_size is not None:
        mat.halo.size = halo_size
    return mat

# def make_volume_material(first_file, n_files, cmap, name):
#     mat = bpy.data.materials.new('vox_' + name)
#     print("Material was created.")
#     print("\tname: " + 'vox_' + name)
#     mat.type = 'VOLUME'
#     mat.volume.density = 0
#     mat.volume.density_scale = 2
#     mat.volume.emission = 0
#     mat.volume.scattering = 1.4
#
#     matSlot = mat.texture_slots.add()
#     matTex = bpy.data.textures.new('tex_' + name, 'VOXEL_DATA')
#     print("Texture was created.")
#     print("\tname: " + 'tex_' + name)
#     matSlot.texture = matTex
#
#     matTex.use_color_ramp = True
#     matTex.voxel_data.file_format = 'IMAGE_SEQUENCE'
#     texImg = bpy.data.images.load(first_file)
#     texImg.source = 'SEQUENCE'
#     matTex.image = texImg
#     matTex.voxel_data.filepath = first_file
#     matTex.image_user.frame_duration = n_files
#
#     matSlot.mapping = 'CUBE'
#     matSlot.texture_coords = 'ORCO'
#     matSlot.use_map_density = True
#     matSlot.use_map_emission = True
#     matSlot.use_map_color_emission = True
#     matSlot.density_factor = 1.
#     matSlot.emission_factor = 1.
#     matSlot.emission_color_factor = 1.
#
#     for i in range(len(cmap) - 2):
#         matTex.color_ramp.elements.new(position = 0.0)
#     for i in range(len(cmap)):
#         matTex.color_ramp.elements[i].position = cmap[i]['pos']
#         matTex.color_ramp.elements[i].color = cmap[i]['col']
#
#     return mat

def makeVolumeMaterial(voxfile, cmap, name, intens):
    mat = bpy.data.materials.new('vox_' + name)
    print("Material was created.")
    print("\tname: " + 'vox_' + name)
    mat.type = 'VOLUME'
    mat.volume.density = 0
    mat.volume.density_scale = 2
    mat.volume.emission = 0
    mat.volume.scattering = 1.4
    mat.volume.step_method = 'CONSTANT'
    mat.volume.step_size = 0.01

    matSlot = mat.texture_slots.add()
    matTex = bpy.data.textures.new('tex_' + name, 'VOXEL_DATA')
    print("Texture was created.")
    print("\tname: " + 'tex_' + name)
    matSlot.texture = matTex

    matTex.use_color_ramp = True
    matTex.voxel_data.file_format = 'BLENDER_VOXEL'
    matTex.voxel_data.filepath = voxfile
    matTex.voxel_data.intensity = intens

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

    return mat

def makeCube(name, size = (2,2,2), loc = (0,0,0)):
    import bmesh
    bpyscene = bpy.context.scene
    mesh = bpy.data.meshes.new(name)
    basic_cube = bpy.data.objects.new(name, mesh)
    bpyscene.objects.link(basic_cube)
    bpyscene.objects.active = basic_cube
    basic_cube.select = True
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    basic_cube.select = False
    basic_cube.dimensions = size
    basic_cube.location = loc
    basic_cube.scale = (1, 1, 1)
    return basic_cube

def makeSphere(name, size, loc, color):
    sphere_name = name
    sphere_color = color # (R,G,B)
    sph = Sphere(sphere_name, color = sphere_color)
    sph.location = loc
    sph.scale = (size, size, size)
    return sph

def getRightColor(color):
    if isinstance(color, str):
        if color[0] != '#':
            color = '#' + color
        if (len(color) != 4) and (len(color) != 7):
            print("Wrong color format. HEX or RGB supported only.")
            return
        color = hexToRgb(color)
    else:
        if len(color) != 3:
            print("Wrong color format. HEX or RGB supported only.")
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

########################################################################################
#
#   Working with objects and materials
#       code borrowed from AstroBlend `science.py` module
#
########################################################################################

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def deselect_all():
    scene = bpy.context.scene
    for ob in scene.objects:
        ob.select = False

# delete associated images from an object
def delete_unused_images(name):
    for img in bpy.data.images:
        if (img.name.find(name) != -1):
            img.user_clear()
            bpy.data.images.remove(img)
            del(img)

# delete object and data by name
def delete_object(name, scene_name = 'Scene'):
    unhide_object(name)
    deselect_all()
    bpy.data.objects[name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[name]
    if bpy.data.objects[name].type != 'LAMP' and bpy.data.objects[name].type != 'EMPTY' and bpy.data.objects[name].type != 'CAMERA':
        # delete assosiated materials first
        delete_unused_materials(name)
        # delete associated textures
        delete_unused_textures(name)
    # now, delete object
    # have to do it this way to actually remove it from memory
    me = bpy.data.objects[name].data
    if me:
        me.user_clear()
    if bpy.data.objects[name].type != 'LAMP' and bpy.data.objects[name].type != 'EMPTY' and bpy.data.objects[name].type != 'CAMERA':
        bpy.data.meshes.remove(me)
    else:
        bpy.data.objects.remove(bpy.data.objects[name])
    print('Deleted object.')
    print('\tname: ' + name)
    # also, delete empty, if there is one
    deselect_all()
    for obj in bpy.data.objects:
        if ((obj.name.find(name) != -1) and (obj.name.find('Empty') != -1)):
            bpy.data.objects['Empty'+name].select=True
            bpy.context.scene.objects.active=bpy.data.objects['Empty'+name]
            bpy.ops.object.delete()
    # also, delete empty of text center, if there is one
    deselect_all()
    for obj in bpy.data.objects:
        if ((obj.name.find(name) != -1) and (obj.name.find('CenterOf:') != -1)):
            bpy.data.objects['CenterOf:'+name].select=True
            bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+name]
            bpy.ops.object.delete()

# to delete unused materials from things when deleting the object
def delete_unused_materials(name):
    bpy.context.scene.objects.active=bpy.data.objects[name]
    obj = bpy.context.object
    while obj.data.materials:
        # note, in 2.69 .pop() on its own works
        obj.data.materials.pop(0, update_data=True)
        obj.data.materials.clear()
    for mat in bpy.data.materials:
        if (mat.name.find(name) != -1):
            mat.user_clear()
            bpy.data.materials.remove(mat)
            del(mat)
    # delete material slots too
    for i in range(0,len(bpy.data.objects[name].material_slots)):
        bpy.context.object.active_material_index = i
        bpy.ops.object.material_slot_remove()

# delete associated textures from an object
def delete_unused_textures(name):
    for tex in bpy.data.textures:
        if (tex.name.find(name) != -1):
            tex.user_clear()
            bpy.data.textures.remove(tex)
            del(tex)

def hide_object(name,hide_render=True):
# hide an object in both 3D viewer and render
    bpy.data.objects[name].hide = True
    bpy.data.objects[name].hide_render = hide_render

def unhide_object(name):
# hide an object in both 3D viewer and render
    bpy.data.objects[name].hide = False
    bpy.data.objects[name].hide_render = False


class Text(object):
    def __init__(self, name = "NoName", color=(1.,1,1), scale=(1.,1,1), shadeless=True):
        newtxt = name
        xyzloc = (0,0,0)
        self.__name = 'Text'
        emptyname = 'Empty' + self.__name # what to call empty for facing
        emptycenter = 'CenterOf:' + self.__name # where the actual tracking will be
        # add a new empty in the center of this text
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esphc = bpy.data.objects['Empty']
        esphc.name = emptycenter
        esphc.location = [xyzloc[0], xyzloc[1], xyzloc[2]] # give it an offset
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esph = bpy.data.objects['Empty']
        esph.name = emptyname
        esph.location = [xyzloc[0], xyzloc[1], xyzloc[2]+5] # give it an offset
        # now, fix this this empty to the middle of the text
        deselect_all()
        bpy.ops.object.text_add(location=xyzloc) # make text
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bpy.ops.font.delete() # delete what is there
        bpy.ops.font.text_insert(text=newtxt) # insert new text
        bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit object mode
        self.name = name
        emptyname = 'Empty' + self.name # what to call empty for facing
        emptycenter = 'CenterOf:' + self.name # where the actual tracking will be
        bpy.data.objects[self.name].scale = scale # scale new txt object
        txtsize = bpy.data.objects[self.name].dimensions # now, recenter this thing
        bpy.data.objects[self.name].location = (xyzloc[0] - txtsize[0]*0.5,
                                                xyzloc[0] - txtsize[1]*0.5,
                                                xyzloc[0] - txtsize[2]*0.5)
        tobj = bpy.data.objects[self.name]
        bpy.context.scene.objects.active = tobj # this is a key step to "highlight" esphc
        tobj.select = True
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.data.objects[self.name].constraints["Child Of"].target = esphc
        # now, link new text Center to an empty that we can move around
        esphc.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'
        deselect_all()
        bpy.context.scene.objects.active = esphc # this is a key step to "highlight" esphc
        # auto track to the new empty
        esphc.select = True
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.data.objects[emptycenter].constraints["Track To"].target = esph
        # now, set correct coords
        esphc.constraints["Track To"].track_axis = 'TRACK_Z'
        esphc.constraints["Track To"].up_axis = 'UP_Y'
        esphc.hide = True # hide this from the viewport
        self.color = color
        self.location = (0,0,0)
        self.pointing = (0,0,5)
        self.shadeless = shadeless
        self.scale = scale

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        deselect_all()
        location_old = [0,0,0]
        location_old[0] = bpy.data.objects['CenterOf:'+self.__name].location[0]
        location_old[1] = bpy.data.objects['CenterOf:'+self.__name].location[1]
        location_old[2] = bpy.data.objects['CenterOf:'+self.__name].location[2]
        pointing_old = [0,0,0]
        pointing_old[0] = self.pointing[0]
        pointing_old[1] = self.pointing[1]
        pointing_old[2] = self.pointing[2]
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bpy.ops.font.delete() # delete what is there
        bpy.ops.font.text_insert(text=name) # insert new text
        bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit object mode
        # now, recenter over center
        bpy.data.objects['CenterOf:'+self.__name].location = (0,0,0)
        bpy.data.objects['Empty'+self.__name].location = (0,0,5)
        txtsize = bpy.data.objects[self.__name].dimensions # now, recenter this thing
        bpy.data.objects[self.__name].location = (-0.5*txtsize[0], -0.5*txtsize[1],-0.5*txtsize[2])
        bpy.data.objects['CenterOf:'+self.__name].location = location_old
        bpy.data.objects['Empty'+self.__name].location = pointing_old
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects['Empty'+self.__name].name = 'Empty' + name
        bpy.data.objects['CenterOf:'+self.__name].name = 'CenterOf:' + name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.name].specular_color
        return self.__color

    @color.setter
    def color(self,color):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        delete_unused_materials(self.name)
        sphmat = makeMaterial(self.name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects['CenterOf:'+self.name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects['CenterOf:'+self.name]
        bpy.data.objects['CenterOf:'+self.name].location = location
        self.__location = location

    @property
    def pointing(self):
        self.__pointing = bpy.data.objects['Empty'+self.name].location
        return self.__pointing

    @pointing.setter
    def pointing(self,pointing):
        bpy.context.scene.objects.active = bpy.data.objects['Empty'+self.name]
        bpy.data.objects['Empty' + self.name].location = pointing
        self.__pointing = pointing

#    def delete(self):
#        # also, delete empty
#        deselect_all()
#        bpy.data.objects['Empty'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['Empty'+self.name]
#        bpy.ops.object.delete()
#        # also, delete empty center
#        deselect_all()
#        bpy.data.objects['CenterOf:'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+self.name]
#        bpy.ops.object.delete()
#        self.name = self.name
#        deselect_all()
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()


class Arrow(object):

    # add an arrow
    def __init__(self, name="NoNameArrow", color = (1,1,1), scale=(0.5,0.5,0.5),  shadeless = True,
                 tip_scale = 2.0, base_scale = 1.0):
        deselect_all()
        self.__name = 'Cylinder'
        # create arrow
        # now, make ability to point
        emptyname = 'Empty' + self.__name # what to call empty
        xyzloc = (0,0,0)
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esph = bpy.data.objects['Empty']
        esph.name = emptyname
        esph.location = [xyzloc[0], xyzloc[1], xyzloc[2]+5] # give it an offset
        bpy.ops.mesh.primitive_cone_add()
        bpy.ops.mesh.primitive_cylinder_add()
        cone = bpy.data.objects['Cone']
        arrow = bpy.data.objects['Cylinder']
        cone.location = (0,0,base_scale*scale[2]+scale[2]*tip_scale)
        arrow.location = (0,0,0)
        arrow.scale = (scale[0]*base_scale, scale[1]*base_scale, scale[2]*base_scale)
        cone.scale = (tip_scale*scale[0], tip_scale*scale[1], tip_scale*scale[2])
        join_surfaces(['Cylinder','Cone'])
        arrow.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'
        self.name = name
        # auto track to the new empty
        deselect_all()
        bpy.context.scene.objects.active = bpy.data.objects[self.name] # this is a key step to "highlight" the arrow
        # auto track to the new empty
        bpy.data.objects[self.name].select = True
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.data.objects[self.name].constraints["Track To"].target = esph
        # now, set correct coords
        ddir = 'TRACK_Z'
        updir = 'UP_X'
        bpy.data.objects[self.name].constraints["Track To"].track_axis = ddir
        bpy.data.objects[self.name].constraints["Track To"].up_axis = updir
        # now, set color
        self.color = color
        self.shadeless = shadeless
        self.scale = scale
        self.pointing = (0,0,5)
        self.location = (0,0,0)

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects['Empty'+self.__name].name = 'Empty' + name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.name].specular_color
        return self.__color

    @color.setter
    def color(self,color):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        delete_unused_materials(self.name)
        sphmat = makeMaterial(self.name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects[self.name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].location = location
        self.__location = location

    @property
    def pointing(self):
        self.__pointing = bpy.data.objects['Empty'+self.name].location
        return self.__pointing

    @pointing.setter
    def pointing(self,pointing):
        bpy.context.scene.objects.active = bpy.data.objects['Empty'+self.name]
        bpy.data.objects['Empty' + self.name].location = pointing
        self.__pointing = pointing

#   # delete arrow ... can probably put into delete_obj_mesh
#    def delete(self):
#        deselect_all()
#        # also, delete empty
#        deselect_all()
#        bpy.data.objects['Empty'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['Empty'+self.name]
#        bpy.ops.object.delete()
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()


class Sphere(object):

    # add a sphere
    def __init__(self, name="NoNameSphere", color = (1,1,1), scale=(1,1,1), segments = 32, shadeless = True):
        deselect_all()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, size=1.0)
        sph = bpy.data.objects['Sphere']
        self.__name = 'Sphere'
        self.name = name
        self.color = color
        self.shadeless = shadeless
        self.scale = scale
        self.location = (0,0,0)

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.__name].specular_color
        return self.__color

    @color.setter
    def color(self,color):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        delete_unused_materials(self.__name)
        sphmat = makeMaterial(self.__name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.__name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.__name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.__name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects[self.__name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location

#    # delete sphere ... can probably put into delete_obj_mesh
#    def delete(self):
#        deselect_all()
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()

# these are if you wanna change the colors or transparencies on the fly
def makeMaterial(name, diffuse, specular, alpha, emiss, mat_type=None, halo_size=None):
    mat = bpy.data.materials.new(name)
    mat.emit = emiss # emissivity is up to 2.0!
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha  # sets transparency (0.0 = invisable)
    mat.use_transparency = True # assumes Z-transparency
    # mat.ambient = 1use  # can't have for transparency
    if mat_type is not None:
        mat.type = mat_type
    if halo_size is not None:
        mat.halo.size = halo_size
    return mat
