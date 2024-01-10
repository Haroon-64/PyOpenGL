import pygame as pg 
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram,compileShader


class APP:
    
    def __init__(self):
        
        pg.init()                                                          # return no. of modules initlized
        pg.display.set_mode((640,480),pg.OPENGL|pg.DOUBLEBUF)              # DOUBLEBUFFER -> 2 frames 1. visible, o2, drawn
        self.clock =pg.time.Clock()                                        # fro framerate
        
        glClearColor(.1, .2, .3, 1)                                        # colors to be displayed      Normalized (RGBA)
        self.shader = self.CreateShader('shaders/vertex.txt', 'shaders/fragment.txt')
        glUseProgram(self.shader)                                          # use shaders before creating object
        self.Triangle = TRIANGLE()
        self.MainLoop()
        
    def CreateShader(self, VertexFile, FragmentFile):
        
        with open(VertexFile, 'r') as f:
            vertexSrc = f.readlines()
        with open(FragmentFile, 'r') as f:
            FragmentSrc = f.readlines()
        
        shader = compileProgram(
            compileShader(vertexSrc, GL_VERTEX_SHADER),
            compileShader(FragmentSrc, GL_FRAGMENT_SHADER),
        )
        return shader
            
    def MainLoop(self):
        
        R = True
        while R:
            for Event in pg.event.get():
                if Event.type == pg.QUIT:
                    R = False
                    
            # Refresh
            glClear(GL_COLOR_BUFFER_BIT)                                   # clear color values of current frame
            glUseProgram(self.shader)
            glBindVertexArray(self.Triangle.VAO)
            glDrawArrays(GL_TRIANGLES, 0,self.Triangle.VertexC)
            pg.display.flip()
            
            self.clock.tick(60)
            
        self.quit()
        
    def quit(self):
        
        self.Triangle.Destroy()
        glDeleteProgram(self.shader)
        pg.quit()
        

class TRIANGLE:
    
    def __init__(self) -> None:
        
        self.Vertices =(
            -.5, -.5, 0, 1, 0, 0, 0,                                       # position, Color, Textures, Lighting etc  # normalized
            .5,  -.5, 0, 1, 0, 0, 0,
             0, .5, 0, 1, 0, 0, 0,

        )
        self.Vertices = np.array(self.Vertices, dtype=np.float32)        # C style data for gpu
        self.VertexC = 3
        self.VAO = glGenVertexArrays(1)                                  # vertex array associated with vbo to store as va
        glBindVertexArray(self.VAO)
        self.VBO = glGenBuffers(1)                                       # vertex buffer container object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)                          
        glBufferData(GL_ARRAY_BUFFER, self.Vertices.nbytes, self.Vertices, GL_STATIC_DRAW)             # send to gpu as set once-read multi
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))                       # describe VBO 0-> pos,3 -> points, dtype, normalize, bytes for next pos(6*4),offset 
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))                      # 1-> color...    , offset fot color 3*4 
         
    def Destroy(self):
        
        glDeleteVertexArrays(1, (self.VAO, ))          # 1, list of objects
        glDeleteBuffers(1, (self.VBO, ))
        
if __name__ == "__main__":                                                    # identify entry point
    app = APP()
        
            