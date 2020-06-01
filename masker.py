from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Line, Color, Mesh
from kivy.config import Config

from kivy.graphics.tesselator import Tesselator

Window.size = (720, 480)

class MaskPoint(Widget):
    points = []
    folder = ''
    img_source = 'img1_34.jpg'
    img_iter = iter(['img1_34.jpg','img1_34.jpg'])

    def __init__(self):
        super(MaskPoint, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
            self, 'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print("my keyboard has been closed")
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, "has been pressed")
        if keycode[1] == 'b': #backspace
            self.back_space()
        if keycode[1] == 'c': #close shape
            self.close_line_mesh()
        if keycode[1] == 's': #save mask
            self.save()
        if keycode[1] == 'n': #next image
            self.next_image(self.img_iter)
        if keycode[1] == 'm': #close mask and save
            self.make_mask()
        if keycode[1] == 'x':
            self.clear_canvas()

    def clear_canvas(self):
        self.canvas.clear()

    def make_mask(self):
        if len(self.points)/2 > 3:
            print('a')
            self.canvas.clear()
            self.build_mesh()
            self.save()
        else:
            print('More points needed to build mask')

    def next_image(self, img_iter):
        try:
            img_source = next(img_iter)
            self.draw_image()
            self.parent.title = "Masker: %s" % img_source
        except StopIteration:
            print('Out of images.')

    def draw_image(self):
        with self.canvas:
            self.wimg = Image(source='img1_34.jpg', size=(720,480))

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

    def save(self):
        self.export_to_png('file.jpg')

    def back_space(self):
        if len(self.points)/2 > 2:
            self.points = self.points[:-2]
            self.update()
        else:
            self.points = []

    def on_touch_down(self, touch):
        self.points += (touch.x,touch.y)

    def on_touch_move(self, touch):
        x=1
    def on_touch_up(self,touch):
        self.update()

    def update(self):
        self.canvas.clear()
        self.draw_image()
        with self.canvas:
            Color(0, 0, 1.)
            Line(points=self.points, width=1)

class masker_app(App):
    def build(self):
        self.title = 'Masker'
        return MaskPoint()

if __name__ == "__main__":
    masker_app().run()
