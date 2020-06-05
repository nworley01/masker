import os
from sys import platform
if platform == 'darwin':
    os.environ["KIVY_WINDOW"]="sdl2"
    os.environ['KIVY_GL_BACKEND']='gl'
elif platform == "win32":
    pass


from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
#Config.set('graphics', 'width', '720')
#Config.set('graphics', 'height', '480')

from kivy.core.window import Window
Window.size = (900,600)

import kivy.graphics
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import (Line, Color, Mesh, Rectangle,
                           Canvas, Translate, Fbo,
                           ClearColor, ClearBuffers, Scale)

from kivy.graphics.tesselator import Tesselator
from os import listdir
from os.path import isfile, join

class MaskPoint(Widget):

    points = []
    dir = 'images/to_annotate'
    help = False
    img_name = None
    img_source = None
    img_files = [f for f in listdir(dir) if f[-3:] == 'jpg']
    current_index = -1
    total_images = len(img_files)

    def __init__(self):
        super(MaskPoint, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
            self, 'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.show_help()
        self.help = False

    def _keyboard_closed(self):
        print("my keyboard has been closed")
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #print('The key', keycode, "has been pressed")
        if keycode[1] == 'b': #backspace
            self.back_space()
        if keycode[1] == 'right': #next image
            self.image_next()
        if keycode[1] == 'left': #next image
            self.image_previous()
        if keycode[1] == 'm': #close mask and save
            self.make_mask()
        if keycode[1] == 'c':
            self.close_line_mesh()
        if keycode[1] == 'h':
            self.show_help()

    def make_mask(self):
        if self.help:
            print("Exit help menu before saving mask.")
        elif len(self.points)/2 > 3:
            self.canvas.clear()
            self.build_mesh()
            self.export_scaled_png()
        else:
            print('More points needed to build mask.')

    def image_next(self):
        self.points = []
        if self.current_index < self.total_images - 1:
            self.current_index +=1
            self.img_name = self.img_files[self.current_index]
            self.img_source = 'images/to_annotate/%s'%self.img_name
            print(self.img_source)
            self.draw_image()
            print("Annotating %s" % self.img_source)
            if self.help:
                self.help = False
        else:
            print('Out of images.')

    def image_previous(self):
        self.points = []
        if self.current_index > 0:
            self.current_index -=1
            self.img_name = self.img_files[self.current_index]
            self.img_source = 'images/to_annotate/%s'%self.img_name
            self.draw_image()
            print("Annotating %s" % self.img_source)
            if self.help:
                self.help = False
        else:
            print('You are already at the first image.')

    def draw_image(self):
        self.canvas.clear()
        with self.canvas:
            self.wimg = Image(source=self.img_source, size = Window.size, allow_stretch=True)

    def close_line_mesh(self):
        if len(self.points)/2 > 3:
            self.canvas.clear()
            self.draw_image()
            self.build_mesh()
        else:
            print('More points needed to build mask')

    def build_mesh(self):
        tess = Tesselator()
        tess.add_contour(self.points)
        tess.tesselate()
        with self.canvas:
            for vertices, indices in tess.meshes:
                self.canvas.add(Mesh(vertices=vertices,
                                     indices=indices,
                                     mode="triangle_fan"))

    def export_scaled_png(self):
        re_size = (720, 480)
        image_scale = 720/self.width

        fbo = Fbo(size=re_size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(image_scale, -image_scale, image_scale)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save('images/complete/%s_mask.jpg'%self.img_name[:-4], flipped=False)
        fbo.remove(self.canvas)

    def back_space(self):
        if len(self.points)/2 > 2:
            self.points = self.points[:-2]
            self.update()
        else:
            self.points = []

    def on_touch_down(self, touch):
        if touch.button == 'left':
            if self.help:
                pass
            else:
                self.points += (touch.x,touch.y)

    def on_touch_up(self,touch):
        if touch.button == 'left':
            if self.help:
                self.help = False
            self.update()

    def update(self):
        self.canvas.clear()
        self.draw_image()
        with self.canvas:
            Color(0, 0, 1.)
            Line(points=self.points, width=1)

    def show_help(self):
        if self.help:
            self.update()
            self.help = False
        else:
            with self.canvas:
                self.wimg = Image(source='help_menu.png', size = Window.size, allow_stretch=True)
            self.help = True

class masker_app(App):
    def build(self):
        self.title = 'Masker'
        return MaskPoint()

if __name__ == "__main__":
    masker_app().run()
