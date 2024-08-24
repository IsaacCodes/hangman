#Imports + setup
import pygame as pg

import settings

pg.init()


#List of all game objects
objects = pg.sprite.LayeredUpdates()

#Game font
def font(size: int):
  return pg.font.Font("freesansbold.ttf", size)

#Basic object class
class Object(pg.sprite.Sprite):
  def __init__(self, pos: "tuple[int, int]", group: bool, layer: int):
    #Sprite class parent
    super().__init__()
    #Converts image type + alpha
    self.image = self.image.convert_alpha()
    #Creates a rect from the surface
    self.rect = self.image.get_rect(center=pos)

    #Assigns layer and adds player to objects list
    self._layer = layer
    if group:
      objects.add(self)

#Text class
class Text(Object):
  def __init__(self, pos: "tuple[int, int]", text: str, text_size=24, text_color="black", group=True, layer=0):

    #Stores vars
    self.text = text
    self.text_color = text_color
    self.font = font(text_size)
    
    #Creates font image
    self.image = self.font.render(text, True, text_color)

    #Object parent
    super().__init__(pos, group, layer)

  def update(self, new_text):
    #If text is changing
    if new_text != self.text:
      #Store and updates the text
      self.text = new_text
      self.image = self.font.render(new_text, True, self.text_color)

class MultiText(list):
  def __init__(self, pos: "tuple[int, int]", text: str, text_size=24, text_color="black", line_buffer=0, group=True, layer=0):
    #Stores lines of text
    lines = []
    text_lines = text.split("\n")
    for i, line in enumerate(text_lines):
      #Creates + stores text object
      text_height = font(text_size).size(text)[1]
      line_pos = pos[0], pos[1] + (text_height+line_buffer) * (i-len(text_lines)/2+0.5)
      line = Text(line_pos, line, text_size, text_color, group, layer)
      lines.append(line)
      
    super().__init__(lines)


#Rectangle class
class Rectangle(Object):
  def __init__(self, pos: "tuple[int, int]", size: "tuple[int, int]", color="black", border_size=0, border_color="black", corner_rounding=0, text="", text_size=24, text_color="black", line_buffer=0, group=True, layer=0):
    #Creates the base rectangle
    self.image = pg.Surface(size, pg.SRCALPHA)
    pg.draw.rect(self.image, color, pg.Rect((0, 0), size), 0, corner_rounding)
    #If there is a border
    if border_size != 0:
      #Draw a border onto the rectangle
      pg.draw.rect(self.image, border_color, pg.Rect((0, 0), size), border_size, corner_rounding)

    #Creates text and adds its image
    if text != "":
      lines = MultiText(pos, text, text_size, text_color, line_buffer, False)
      for element in lines:
        blit_x = (size[0] - element.rect.width)/2 - (pos[0] - element.rect.centerx)
        blit_y = (size[1] - element.rect.height)/2 - (pos[1] - element.rect.centery)
        self.image.blit(element.image, (blit_x, blit_y))

    #Object parent
    super().__init__(pos, group, layer)
      
  def remove(self):
    super().remove(self)
    for line in self.lines:
      super().remove(line)
      

#Circle class
class Circle(Object):
  def __init__(self, pos: "tuple[int, int]", diameter: int, color="black", border_size=0, border_color="black", group=True, layer=0):    
    #Alpha compatible image + draw interior circle on it
    self.image = pg.Surface((diameter, diameter), pg.SRCALPHA)
    pg.draw.circle(self.image, color, (diameter//2, diameter//2), diameter//2)
    #Draw circle border
    if border_size != 0:
      pg.draw.circle(self.image, border_color, (diameter//2, diameter//2), diameter//2, border_size)

    #Object parent
    super().__init__(pos, group, layer)

#Custom image class
class Image(Object):
  def __init__(self, pos: "tuple[int, int]", file: str, size=(0, 0), smooth=True, group=True, layer=0):
    #Loads image
    self.image = pg.image.load(f"{settings.dir}//images//{file}")

    #Changes the size
    if size != (0, 0):
      if smooth:
        self.image = pg.transform.smoothscale(self.image, size)
      else:
        self.image = pg.transform.scale(self.image, size)

    #Object parent
    super().__init__(pos, group, layer)