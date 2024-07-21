import numpy as np
import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import glfw
from matrixinputmodule import *
from mathmodule import *
import textrendermodule


def main():
    #simulation declarations
    glfw.init()
    WIN_SIZE = [int(640*2), int(360*2), 0]
    WIN_SIZE[2] = int(max(WIN_SIZE))
    global screen
    screen = glfw.create_window(WIN_SIZE[0], WIN_SIZE[1], "linearengine", None, None)
    global xz_angle, yz_angle, zoom, mouse_pos_key, mouse_pos, mouse_pos_init, show_menu, matrix_scale
    xz_angle = 0
    yz_angle = 0
    zoom = 1
    mouse_pos_key = False
    mouse_pos = [0,0]
    mouse_pos_init = [0,0]
    dt = 1/20000
    show_menu = False
    matrix_scale = 0
    matrix_history = [[[1,0,0],[0,1,0],[0,0,1]]]

    #colors
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    GRID_COLOR = (110,110,110,100)
        
    #controlvariables
    global show_grid,scale,show_volume_grid
    scale = 50
    show_grid = True
    show_volume_grid = False
    HEADS_NUM = 3
    GRID_OPACITY = 0.1
    custom_vectors = [[1,1,1]]
    
    #initalize opengl
    glfw.make_context_current(screen)
    ogl.glViewport(0, 0, WIN_SIZE[0], WIN_SIZE[1])
    oglu.gluOrtho2D(0, WIN_SIZE[0], 0, WIN_SIZE[1])
    ogl.glMatrixMode(ogl.GL_MODELVIEW)
    # Enable settings
    ogl.glEnable(ogl.GL_BLEND)
    glfw.window_hint(glfw.SAMPLES, 4)
    ogl.glEnable(ogl.GL_MULTISAMPLE)
    ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)


    def draw_axis():
        if show_grid == True:

            # draws axes
            render((-WIN_SIZE[0]/2, 0, 0), (WIN_SIZE[0]/2, 0, 0), RED, 1, 3)
            render((0, -WIN_SIZE[1]/2, 0),(0, WIN_SIZE[1]/2, 0), GREEN, 1, 3)
            render((0, 0, -WIN_SIZE[0]/2),(0, 0, WIN_SIZE[0]/2), BLUE, 1, 3)

            # draws x-axis grid lines over (x,y,z)
            i = 0
            while(i<=WIN_SIZE[1]/scale*0.5):
                j=0
                while(j<=WIN_SIZE[2]/scale*0.5):
                    render((-WIN_SIZE[0]/2,i*scale,j*scale),(WIN_SIZE[0]/2,i*scale,j*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((-WIN_SIZE[0]/2,-i*scale,j*scale),(WIN_SIZE[0]/2,-i*scale,j*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((-WIN_SIZE[0]/2,i*scale,-j*scale),(WIN_SIZE[0]/2,i*scale,-j*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((-WIN_SIZE[0]/2,-i*scale,-j*scale),(WIN_SIZE[0]/2,-i*scale,-j*scale),GRID_COLOR,GRID_OPACITY,1)
                    j+=1
                if show_volume_grid:
                    i+=1
                else:
                    while(i<=WIN_SIZE[1]/scale*0.5):
                        render((-WIN_SIZE[0]/2,i*scale,0),(WIN_SIZE[0]/2,i*scale,0),GRID_COLOR,GRID_OPACITY,1)
                        render((-WIN_SIZE[0]/2,-i*scale,0),(WIN_SIZE[0]/2,-i*scale,0),GRID_COLOR,GRID_OPACITY,1)
                        i+=1
                    break
#
            # draws y-axis grid lines over (x,y,z)
            i = 0
            while(i<=WIN_SIZE[2]/scale*0.5):
                j=0
                while(j<=WIN_SIZE[0]/scale*0.5):
                    render((j*scale,-WIN_SIZE[1]/2,i*scale),(j*scale,WIN_SIZE[1]/2,i*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((-j*scale,-WIN_SIZE[1]/2,i*scale),(-j*scale,WIN_SIZE[1]/2,i*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((j*scale,-WIN_SIZE[1]/2,-i*scale),(j*scale,WIN_SIZE[1]/2,-i*scale),GRID_COLOR,GRID_OPACITY,1)
                    render((-j*scale,-WIN_SIZE[1]/2,-i*scale),(-j*scale,WIN_SIZE[1]/2,-i*scale),GRID_COLOR,GRID_OPACITY,1)
                    j+=1
                if show_volume_grid:
                    i+=1
                else:
                    break
#
            # draws z-axis grid lines over (x,y,z)
            i = 0
            while(i<=WIN_SIZE[1]/scale*0.5):
                j=0
                while(j<=WIN_SIZE[0]/scale*0.5):
                    render((j*scale,i*scale,-WIN_SIZE[2]/2),(j*scale,i*scale,WIN_SIZE[2]/2),GRID_COLOR,GRID_OPACITY,1)
                    render((-j*scale,i*scale,-WIN_SIZE[2]/2),(-j*scale,i*scale,WIN_SIZE[2]/2),GRID_COLOR,GRID_OPACITY,1)
                    render((j*scale,-i*scale,-WIN_SIZE[2]/2),(j*scale,-i*scale,WIN_SIZE[2]/2),GRID_COLOR,GRID_OPACITY,1)
                    render((-j*scale,-i*scale,-WIN_SIZE[2]/2),(-j*scale,-i*scale,WIN_SIZE[2]/2),GRID_COLOR,GRID_OPACITY,1)
                    j+=1
                if show_volume_grid:
                    i+=1
                else:
                    break
        
    # transforms vector (start:p1 and end:p2) by custom matrix
    def custom_transform(p1,p2):
        global matrix_scale
        matrix_scale += dt
        # animates interpolated transformations between old transform/matrix and new transform/matrix
        if matrix_scale < 1:
            p1 = transform_vect(matrix_add(scale_matrix(1-matrix_scale,matrix_history[len(matrix_history)-2]),scale_matrix(matrix_scale,matrix_history[len(matrix_history)-1])),p1)
            p2 = transform_vect(matrix_add(scale_matrix(1-matrix_scale,matrix_history[len(matrix_history)-2]),scale_matrix(matrix_scale,matrix_history[len(matrix_history)-1])),p2)
        # skip interpolation step if already animated
        else:
            p1 = transform_vect(matrix_history[len(matrix_history)-1],p1)
            p2 = transform_vect(matrix_history[len(matrix_history)-1],p2)
        return p1,p2

    # fundamental line rendering function
    def render(p1,p2,color,opacity,thickness):
        # transform by custom matrix
        p1,p2 = custom_transform(p1,p2)

        # rotation transform by viewing angle
        xz_rot_matrix = [[np.cos(xz_angle),0,-np.sin(xz_angle)],[0,1,0],[np.sin(xz_angle),0,np.cos(xz_angle)]]
        yz_rot_matrix = [[1,0,0],[0,np.cos(yz_angle),np.sin(yz_angle)],[0,-np.sin(yz_angle),np.cos(yz_angle)]]
        p1_rot = transform_vect(yz_rot_matrix,transform_vect(xz_rot_matrix,p1))
        p2_rot = transform_vect(yz_rot_matrix,transform_vect(xz_rot_matrix,p2))

        # scale transform by zoom
        p1_rot_scale = scale_vect(zoom,p1_rot)
        p2_rot_scale = scale_vect(zoom,p2_rot)

        # denormalize and translate for actual window size and space
        p1_norm = [p1_rot_scale[0]+WIN_SIZE[0]/2,p1_rot_scale[1]+WIN_SIZE[1]/2]
        p2_norm = [p2_rot_scale[0]+WIN_SIZE[0]/2,p2_rot_scale[1]+WIN_SIZE[1]/2]

        # OPENGL render transformed vector
        ogl.glLineWidth(thickness)
        ogl.glColor4f(color[0], color[1], color[2], opacity)  
        ogl.glBegin(ogl.GL_LINES)
        ogl.glVertex2f(p1_norm[0], p1_norm[1]) 
        ogl.glVertex2f(p2_norm[0], p2_norm[1]) 
        ogl.glEnd()

    # class for rendering all visual vectors
    class VisVector:
        def __init__(self, pos):
            self.pos = pos

        def show(self):
            # render body
            render([0,0,0],scale_vect(scale,self.pos),WHITE,1,4)

            # render head/tops
            head_0 = []
            # render HEADS_NUM # of arrowheads
            for i in range(HEADS_NUM):
                if i == 0:
                    # initialize rotation axis and angle for first arrowhead: rotated from body towards x-axis
                    norm_ortho_vect = scale_vect(1/np.sqrt(np.power(self.pos[2],2)+np.power(self.pos[1],2)),[0,self.pos[2],-self.pos[1]])
                    head_angle = 5*np.pi/6
                else:
                    # initialize rotation axis and angle for other arrowheads: initial arrowhead rotated around body 
                    norm_ortho_vect = scale_vect(1/vect_length(self.pos),self.pos)
                    head_angle = 2*np.pi/HEADS_NUM*i
                # initialize generalized rotation matrix (rotates vector around custom axis)
                head_rot_matrix = [[np.cos(head_angle)+np.power(norm_ortho_vect[0],2)*(1-np.cos(head_angle)),norm_ortho_vect[0]*norm_ortho_vect[1]*(1-np.cos(head_angle))-norm_ortho_vect[2]*np.sin(head_angle),norm_ortho_vect[0]*norm_ortho_vect[2]*(1-np.cos(head_angle))+norm_ortho_vect[1]*np.sin(head_angle)],
                     [norm_ortho_vect[0]*norm_ortho_vect[1]*(1-np.cos(head_angle))+norm_ortho_vect[2]*np.sin(head_angle),np.cos(head_angle)+np.power(norm_ortho_vect[1],2)*(1-np.cos(head_angle)),norm_ortho_vect[1]*norm_ortho_vect[2]*(1-np.cos(head_angle))-norm_ortho_vect[0]*np.sin(head_angle)],
                     [norm_ortho_vect[0]*norm_ortho_vect[2]*(1-np.cos(head_angle))-norm_ortho_vect[1]*np.sin(head_angle),norm_ortho_vect[1]*norm_ortho_vect[2]*(1-np.cos(head_angle))+norm_ortho_vect[0]*np.sin(head_angle),np.cos(head_angle)+np.power(norm_ortho_vect[2],2)*(1-np.cos(head_angle))]]
                if i == 0:
                    # rotate body to first arrowhead location
                    head_0 = scale_vect(0.3*scale/vect_length(transform_vect(head_rot_matrix,self.pos)),transform_vect(head_rot_matrix,self.pos))
                    head_i = head_0
                else:
                    # rotate first arrowhead around body
                    head_i = scale_vect(0.3*scale/vect_length(transform_vect(head_rot_matrix,head_0)),transform_vect(head_rot_matrix,head_0))
                # draw arrowhead(s)
                render(scale_vect(scale,self.pos),[head_i[0]+scale*self.pos[0],head_i[1]+scale*self.pos[1],head_i[2]+scale*self.pos[2]],WHITE,1,2)

    # callback function handling key presses
    def key_callback(window, key, scancode, action, mods):
        global show_grid,scale,show_volume_grid,show_menu
        if key == glfw.KEY_ESCAPE and action == glfw.RELEASE:
            glfw.terminate()
        if key == glfw.KEY_G and action == glfw.RELEASE:
            show_grid = not show_grid
        if key == glfw.KEY_S and action == glfw.RELEASE:
            if scale <= 175:
                scale += 25
            else:
                scale = 25
        if key ==  glfw.KEY_V and action == glfw.RELEASE:
            show_volume_grid = not show_volume_grid
        if key == glfw.KEY_M and action == glfw.RELEASE:
            show_menu = not show_menu

    # callback function handling cursor position
    def cursor_position_callback(screen, xpos, ypos):
        global mouse_pos
        mouse_pos = [xpos,ypos]

    # callback function handling mouse button presses
    def mouse_button_callback(screen, button, action, mods):
        global mouse_pos_key,mouse_pos,mouse_pos_init,xz_angle,yz_angle,zoom
        # determine if button held
        if (button == glfw.MOUSE_BUTTON_1) and (action == glfw.PRESS):
            mouse_pos_init = mouse_pos
            mouse_pos_key = True
        if (button == glfw.MOUSE_BUTTON_1) and (action == glfw.RELEASE):
            mouse_pos_key = False
        if button == glfw.MOUSE_BUTTON_2 and action == glfw.RELEASE:
            xz_angle = 0
            yz_angle = 0
            zoom = 1

    # callback function handling scroll wheel movement
    def scroll_callback(screen, xoffset, yoffset):
        global zoom
        if yoffset > 0:
            zoom += 0.1
        elif yoffset < 0:
            zoom += -0.1
        if zoom < 0.1:
            zoom = 0.1


    # main simulation run loop
    while not glfw.window_should_close(screen):
        
        # event handler
        glfw.poll_events()
        glfw.set_key_callback(screen,key_callback)
        glfw.set_cursor_pos_callback(screen,cursor_position_callback)
        glfw.set_mouse_button_callback(screen,mouse_button_callback)
        glfw.set_scroll_callback(screen,scroll_callback)

        # viewing rotation responder
        if mouse_pos_key:
            mouse_poscurrent = mouse_pos
            deltapos = [mouse_poscurrent[0]-mouse_pos_init[0],mouse_poscurrent[1]-mouse_pos_init[1]]
            xz_angle += deltapos[0]/WIN_SIZE[0]*np.pi
            yz_angle += deltapos[1]/WIN_SIZE[1]*np.pi
            mouse_pos_init = mouse_poscurrent

        # menu initializer
        if show_menu:
            matrix_scale = 0
            try:
                custom_vectorstemp,custommatrixtemp,whatchange = menuHandler()
                if whatchange[0]:
                    custom_vectors = custom_vectorstemp
                if whatchange[1]:
                    matrix_history.append( matrix_prod(custommatrixtemp,matrix_history[len(matrix_history)-1]) )
                show_menu = False
            except:
                show_menu = False

        # info text rendering
        info_text_array = [
            "windowsize: " + str(WIN_SIZE[0 : 2]),
            "zoom: x" + str(round(zoom,1)),
            "x,z rotation: " + str(round(xz_angle*180/np.pi)),
            "y,z rotation: " + str(round(yz_angle*180/np.pi)),
            "(S) scale: " + str(scale),
            "(V) volumetric grid: " + str(show_volume_grid),
            "(G) show grid/axis: " + str(show_volume_grid),
            "(M) open vector and matrix menu",
        ]
        for i in range(len(info_text_array)):
            textrendermodule.main(18,info_text_array[i],10,WIN_SIZE[1]-15*(i+1))



        # render vectors and axis (draw in ascending priority)
        if len(custom_vectors) != 0:
            for i in range(len(custom_vectors)):
                VisVector(custom_vectors[i]).show()
        draw_axis()
         

        # update screen
        glfw.swap_buffers(screen)
        ogl.glClear(ogl.GL_COLOR_BUFFER_BIT)
        
    
main()

glfw.terminate()