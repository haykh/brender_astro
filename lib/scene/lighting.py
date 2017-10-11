import bpy
from lib.hlp_func import deselect_all
from math import sqrt

class Lighting(object):

    radius_lamp = 0.0 # radius to have lamp travel around, if following camera

    # how the motion of the lamp, if there is one, will be calculated
    #  options so far are 'TRACKING' to follow the camera or None, for fixed
    lamp_motion = None


    # what sort of lighting do we want to use?  Don't necessarily have to use this
    def __init__(self, lighting_type = 'SUN', lighting_motion=None,
                 xpos=-3.0, ypos=0.0, zpos=0.0, name = None):
        if lighting_type is 'EMISSION':
            name = 'Emission'
            self.__name = 'Emission'
        elif lighting_type is 'SUN':
            name = 'Sun'
            self.__name = name
        elif lighting_type is 'POINT':
            name = 'Point'
            self.__name = name
        if lighting_type is None or lighting_type is 'SUN' or lighting_type is 'POINT':
            # add in the sun
            bpy.ops.object.lamp_add(type=lighting_type)
            #self.name = name
            lamp = bpy.data.objects[self.__name]
            lamp.location.x = xpos
            lamp.location.y = ypos
            lamp.location.z = zpos
            radius_lamp = sqrt(xpos**2 + ypos**2 + zpos**2)
            lamp_motion = lighting_motion # for lamp tracking... check on implementation JPN 20150124
        if lighting_type == 'EMISSION': # or do emission lighting
            # turn up emissivity of all objects to look nice
            bpy.data.worlds['World'].light_settings.indirect_factor=20.
            # have to use approximate, not ray tracing for emitting objects ...
            #   ... for now...
            bpy.data.worlds['World'].light_settings.gather_method = 'APPROXIMATE'
            bpy.data.worlds['World'].horizon_color = [0.0, 0.0, 0.0] # horizon = black
            bpy.data.worlds['World'].light_settings.use_indirect_light = True  # emitting things
            lamp_motion = None # no tracking of lamp
            #self.name = 'Emission'
        self.lighting_type = lighting_type
        self.location = (xpos,ypos,zpos)

#    @property
#    def name(self):
#        if self.__name is not 'Emission':
#            self.__name = bpy.data.objects[self.__name].name
#        return self.__name

#    @name.setter
#    def name(self,name):
#        deselect_all()
#        if self.__name is not 'Emission':
#            bpy.context.scene.objects.active = bpy.data.objects[self.__name]
#            bpy.data.objects[self.__name].name = name # object name
#        self.__name = name

    @property
    def location(self):
        if self.__name is not 'Emission':
            self.__location = bpy.data.objects[self.__name].location
        else:
            print ('No location for Emission')
        return self.__location

    @location.setter
    def location(self,location):
        if self.__name is not 'Emission':
            bpy.context.scene.objects.active = bpy.data.objects[self.__name]
            bpy.data.objects[self.__name].location = location
        self.__location = location
