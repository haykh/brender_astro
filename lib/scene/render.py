import bpy

class Render:

    # initialize rendering
    def __init__(self, render_directory, render_name, scene_name = 'Scene', file_format = 'PNG'):
        bpy.data.scenes[scene_name].render.image_settings.file_format = file_format
        self.__scene_name = scene_name
        self.scene_name = scene_name
        self.__nframe = 0
        self.nframe = 0
        # where things are stored
        self.render_directory = render_directory
        self.render_name = render_name
        self.file_format = file_format

    @property
    def file_format(self):
        self.__file_format = bpy.data.scenes[self.scene_name].render.image_settings.file_format
        return self.__file_format

    @file_format.setter
    def file_format(self,file_format):
        bpy.data.scenes[self.scene_name].render.image_settings.file_format = file_format
        self.__file_format = file_format

    @property
    def nframe(self):
        return self.__nframe

    @nframe.setter
    def nframe(self,nframe):
        self.__nframe = nframe

    @property
    def scene_name(self):
        return self.__scene_name

    @scene_name.setter
    def scene_name(self,scene_name):
        self.__scene_name = scene_name

    @property
    def render_directory(self):
        return self.__render_directory

    @render_directory.setter
    def render_directory(self,render_directory):
        self.__render_directory = render_directory

    @property
    def render_name(self):
        return self.__render_name

    @render_name.setter
    def render_name(self,render_name):
        self.__render_name = render_name

    def set_resolution(res_x, res_y):
        scene = bpy.data.scenes["Scene"]
        scene.render.resolution_x = res_x
        scene.render.resolution_y = res_y
        scene.render.resolution_percentage = 100

    def render(self):
        # render for each rotation
        num = "%04d" % (self.nframe)
        r_name = self.render_name + num
        bpy.data.scenes[self.scene_name].render.filepath = self.render_directory + r_name
        # don't render if you're not above crash_frame
        bpy.ops.render.render(write_still=True)
        self.nframe = self.nframe+1
