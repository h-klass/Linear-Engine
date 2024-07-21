import freetype
import numpy as np
import glfw
from OpenGL.GL import *

class TextRenderer:
    def __init__(self, font_path, font_size):
        self.face = freetype.Face(font_path)
        self.face.set_char_size(font_size * 64)
        self.font_size = font_size
        self.textures = {}

    def render_text(self, text):
        x, y = 0, 0
        vertices = []
        tex_coords = []
        for char in text:
            if char not in self.textures:
                self.textures[char] = self.load_char(char)
            texture, (w, h), (bearingX, bearingY), advance = self.textures[char]
            x0 = x + bearingX
            y0 = y - (h - bearingY)
            x1 = x0 + w
            y1 = y0 + h

            vertices.extend([x0, y0, x1, y0, x1, y1, x0, y1])
            tex_coords.extend([0, 1, 1, 1, 1, 0, 0, 0]) 
            x += advance

        vertices = np.array(vertices, dtype=np.float32)
        tex_coords = np.array(tex_coords, dtype=np.float32)

        return vertices, tex_coords

    def load_char(self, char):
        self.face.load_char(char)
        bitmap = self.face.glyph.bitmap
        w, h = bitmap.width, bitmap.rows
        data = np.array(bitmap.buffer, dtype=np.ubyte)
        
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, w, h, 0, GL_RED, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        advance = self.face.glyph.advance.x >> 6
        bearing = (self.face.glyph.bitmap_left, self.face.glyph.bitmap_top)

        return texture, (w, h), bearing, advance

def draw_text(renderer, text, x, y,color=(1, 1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, 0)
    vertices, tex_coords = renderer.render_text(text)
    glEnable(GL_TEXTURE_2D)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, vertices)
    glTexCoordPointer(2, GL_FLOAT, 0, tex_coords)

    glColor4f(*color) 

    for i, char in enumerate(text):
        texture, _, _, _ = renderer.textures[char]
        glBindTexture(GL_TEXTURE_2D, texture)
        glDrawArrays(GL_QUADS, i * 4, 4)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def main(font_size,text_string,xpos,ypos):
    renderer = TextRenderer("AppleGaramond.ttf", font_size)
    draw_text(renderer, text_string, xpos, ypos) 


