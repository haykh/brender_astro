import bpy
from math import pi
from lib.hlp_func import deselect_all

class Camera(object):
    # initialize the camera with an empty for pointing
    def __init__(self,cam_name = 'Camera', clip_end = None, clip_begin = None,
                 horizon_color=[0.0, 0.0, 0.0]):
        # (I) set initial camera location, and an empty object to track
        #     the camera with, using Blender's internal tracker
        camera_x = 5.
        camera_y = 0.0
        camera_z = 0.0
        if clip_end is None: # clip rendering, usually for galaxy stuff want big
            clip_end = 100.0
        if clip_begin is None:
            clip_begin = 0.01
        bpy.data.cameras[cam_name].clip_end = clip_end
        bpy.data.cameras[cam_name].clip_start = clip_begin
        camobj = bpy.data.objects[cam_name] # get cam as an object to track
        camobj.location = [camera_x, camera_y, camera_z]
        camobj.rotation_mode = 'QUATERNION' # supposedly, mo betta then 'XYZ'
        camobj.rotation_euler = [90.0*(pi/180.0), 0.0, -90.0*(pi/180.0)]
        # (II) now, set up camera tracking on an empty
        # add empty for tracking
        bpy.ops.object.empty_add(type='SPHERE')
        # set location to 0,0,0 for starts
        esph = bpy.data.objects['Empty']
        # change name for cam empty incase we want to parent other things
        esph.name = 'Empty'+cam_name
        esph.location = [0, 0, 0]
        esph.select = False
        # add an autotrack to this empty
        camobj.select=False
        # select objects in correct series to have camera track object
        camobj.select = True
        esph.select = True
        bpy.ops.object.track_set(type='TRACKTO')
        bpy.data.worlds['World'].horizon_color = horizon_color # horizon = black, default
        self.__name = cam_name
        self.name = cam_name
        self.clip_end = clip_end
        self.clip_begin = clip_begin
        self.horizon_color = self.horizon_color
        self.location = (5,0,0)
        self.pointing = (0,0,0)
        self.bviz = 0

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects['Empty'+self.__name].name = 'Empty' + name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def type(self):
        self.__type = bpy.data.cameras[self.name].type
        return self.__type

    @type.setter
    def type(self,type):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.cameras[self.name].type = type
        self.__type = type

    @property
    def ortho_scale(self):
        self.__ortho_scale = bpy.data.cameras[self.name].ortho_scale
        return self.__ortho_scale

    @ortho_scale.setter
    def ortho_scale(self,ortho_scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.cameras[self.name].ortho_scale = ortho_scale
        self.__ortho_scale = ortho_scale

    @property
    def lens(self):
        self.__lens = bpy.data.cameras[self.name].lens
        return self.__lens

    @lens.setter
    def lens(self,lens):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.cameras[self.name].lens = lens
        self.__lens = lens

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

    @property
    def clip_end(self):
        self.__clip_end = bpy.data.cameras[self.name].clip_end
        return self.__clip_end

    @clip_end.setter
    def clip_end(self,clip_end):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.cameras[self.name].clip_end = clip_end
        self.__clip_end = clip_end

    @property
    def clip_begin(self):
        self.__clip_begin = bpy.data.cameras[self.name].clip_start
        return self.__clip_begin

    @clip_begin.setter
    def clip_begin(self,clip_begin):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.cameras[self.name].clip_start = clip_begin
        self.__clip_begin = clip_begin

    @property
    def horizon_color(self):
        self.__horizon_color = bpy.data.worlds['World'].horizon_color
        return self.__horizon_color

    @horizon_color.setter
    def horizon_color(self, horizon_color):
        bpy.data.worlds['World'].horizon_color = horizon_color # horizon = black, default
        self.__horizon_color = horizon_color
