# Sorry about the length; Once i started, i had trouble stopping (~3500 lines)

# There is also a new version of Tetris at https://drive.usercontent.google.com/u/0/uc?id=13-xb9KquyZOFVU7Ka3X_63KxtaeJmk_1&export=download

###############################################
# Important information:                      #
#   This project uses reference duplication.  #
#   Every time you see something like         #
#             a=[b][0]                        #
#   you are seeing an example of reference    #
#   duplication. By editing part of one       #
#   variable (not the whole thing), the other #
#   will always match.                        #
#   Good: a.append(5)    Bad: a+=[5]          #
#                                             #
# If you want an updated version, go to       #
# https://github.com/1101-Grills-Oren/leavethe#
#lightson/blob/6d29680a1e3c60e3d232143f53a1369#
#4943c5401/versions/current.py                #
#                                             #
# This is going to be a continued project.    #
#                                             #
#                                             #
# Startup splash: tkinter on secondary thread #
# Recursion: see command ?while for usage.    #
# Classes: There are many of these.           #
# Functions: Much functions very yes.         #
#                                             #
#  Controls: WASD for movement.               #
#            t for command chat.              #
#    Left click to attack towards the cursor. #
#      esc to leave chat or end game          #
# the command ./terminateProgram does the same#
#                                             #
###############################################

#Commands:
#    declare msg:str                                                                   this does basically nothing
#    tp x:float y:float                                                                teleports the player to x,y
#    setGrav x:float y:float                                                           changes player gravity
#    setVel x:float y:float                                                            changes player velocity
#    player.pos                                                                        command to get player position
#    placeRoom rid:any x:int y:int                                                     Places room with id rid at x,y
#    \summon id:str x:int_opt y:int_opt                                                Summons something with id id at x,y. If x is not supplied, spawns at player position.
#    variable id:var_id(str) attr attribute(str)                                       Returns attribute attribute of variable id. Example: (var 'ex'=[0,4,2,9]) variable ex attr __len__     Example returns: Length of array ex
#    variable id:var_id(str) command cmd:command(str)                                  Sets variable id to return value of command cmd.
#    variable id:var_id(str) value v:str                                               Sets variable id to v (type:string)
#    variable id:var_id(str) value_int v:int                                           Sets variable id to v (type:int)
#    variable id:var_id(str) value_float v:float                                       Sets variable id to v (type:float)
#    variable id:var_id(str) var x:var_id(str)                                         sets variable id to be equal to variable x
#    variable id:var_id(str) append value:str                                          For arrays, appends a new value (type str) to variable id   For other types, crashes
#    variable id:var_id(str) append_var var:var_id(str)                                For arrays, appends the value contained in variable var to variable id   For other types, crashes
#    variable id:var_id(str) pop i:int                                                 returns index of array variable id, removing it at the same time
#    variable id:var_id(str) type newtype[str|int|float]:str                           Changes variable type. new type is determined by newtype
#    variable id:var_id(str) sum var:var_id(str) var:var_id(str)...                    sets variable id to the sum of variables var
#    variable id:var_id(str) subtract var1:var_id(str) var2:var_id(str)                sets variable id to var1-var2
#    variable id:var_id(str) min var1:var_id(str) var2:var_id(str)                     sets variable id to min(var1,var2)
#    variable id:var_id(str) max var1:var_id(str) var2:var_id(str)                     sets variable id to max(var1,var2)
#    variable id:var_id(str) divide var1:var_id(str) var2:var_id(str)                  sets variable id to var1/var2
#    variable id:var_id(str) multiply var1:var_id(str) var2:var_id(str)...             Sets variable id to var1*var2*...
#    variable id:var_id(str) arrayize id2:var_id_opt(str)                              If variable id2 exists, sets variable id to [id2]. Else, sets variable id to []. Useful for making arguments for file commands.
#    variable_get id:var_id(str)                                                       returns the value of variable id
#    get_enemy args                                                                    returns a list of enemies with data args. Options: x,y: center of command execution     d_min,d_max: Min and max distance for the top-right corner of the enemy in tiles.     c_max: maximum number of return values    type: Limit return objects to type type. Can be repeated for multiple types.
#    get_object args                                                                   returns a list of objects with data args. Options match those in get_enemy.
#    get_player                                                                        Returns the current player. Redundant.
#    executeFile fname:str args                                                        executes the command file fname after setting variable args to be args.split(' ')
#    executeFile_argless fname:str                                                     executes the command file fname without setting arguments.
#    a==b,a>b,a>=b,a<b,a<=b,a!=b var:var_id(str) value:int|float                       Similar to if you ran the names as code with "a" being the variable var and "b" being a constant to compare to.
#    a==v,a>v,a>=v,a!=v var1:var_id(str) var2:var_id(str)                              same as above, but with a=var1 and v=var2
#    !v var:var_id(str)                                                                returns inverted value of var var_id. If var is false, returns true, if true, returns false.
#    !execute cmd:command(str)                                                         Executes command cmd and inverts the return value.
#    ?execute condition:var_id(str) cmd:command(str)                                   executes command cmd, but only if variable "condition" is not false.
#    ./programTerminate                                                                Ends the program. Non-recoverable (nothing can stop it)
#    ./protectVariable var:var_id(str)                                                 takes the variable var and makes its main object nonreplaceable (subvalues can change, but not the main object). Non-recoverable.
#    ./lockVariable var:var_id(str)                                                    Makes the variable var (under that alias) read-only. Non-recoverable.
#    
#
#    
#    
#    Symbolic variables:
#       player                                The player. Read Only
#       player.attr                           player attributes such as health, max health, shots left. Modifiable.
#       player.pos                            player position. Modifiable
#       player.vel                            player velocity. Modifiable
#       player.onGround                       whether the player is on the ground or not. Read Only.
#       player.fireCooldown                   how long until the player will be able to fire again. Read only.
#       player.ducking                        Is the player crouching? Read only.
#       player.shotsLeft                      how many shots the player has left before a reload? Read only.
#       player.reloadTime                     how long does the player need to be on the ground to reload one projectile? Read only.
#       fps[0]                                Framerate.
#    



#example comands:
# \summon meh    - summon experimental enemeh





























import threading
import sys
import subprocess
l=sys.argv.__len__()
shouldpass=0
if(l>1):
    if(sys.argv[1]=='splash'):
        shouldpass=1


#start splash
global splashtext
splashtext='testing'
if shouldpass:
    pass
    
















































#end splash
else:
    def splashfunction():
        import tkinter as tk
        import msvcrt
        window=tk.Tk(screenName='splash',baseName='splash')
        textDisplay=tk.Label(window,text='test',width=100)
        textDisplay.grid(row=0,column=0)
    
        def splashUpdate(*args):
            global splashtext
            x=splashtext
            if(x!=""):
                textDisplay['text']=x
                print(x)
                splashtext=""
            window.after(1,splashUpdate)
        window.after(1,splashUpdate)
        tk.mainloop()

    #splashthread=threading.Thread(target=splashfunction)
    #splashthread.start()
    #splash=subprocess.Popen("py -m gamev1 splash")
    
    
    #IMAGE FOLDER
    imagefolder="M:\\images"
    
    import os
    import random
    from typing import List
    
    # import basic pygame modules
    global pg
    global key
    global mouse
    import pygame as pg
    key=pg.key
    mouse=pg.mouse
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from PIL import Image
    from numpy import array
    #import glfwApi
    import glfw_postproc as glfwApi
    # see if we can load more than standard BMP
    if not pg.image.get_extended():
        raise SystemExit("Sorry, extended image module required")
    
    
    # game constants
    MAX_SHOTS = 2  # most player bullets onscreen
    ALIEN_ODDS = 22  # chances a new alien appears
    BOMB_ODDS = 60  # chances a new bomb will drop
    ALIEN_RELOAD = 12  # frames between new aliens
    SCREENRECT = pg.Rect(0, 0, 940, 480)
    SCORE = 0
    
    
    global FRAMERATE,FRAMERATE2
    FRAMERATE=20
    FRAMERATE2=20
    
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    global CAMERA_POS
    CAMERA_POS=[-400,-300]
    CAMERA_SCALE=2
    CAMERA_BOUNDARIES=(0,0,0,0)
    rooms={}
    
    global OPENGL_CAMERA_SHIFT
    OPENGL_CAMERA_SHIFT=[0,0]
    
    def toBinary(value:int,length=0):
        return ''.join([str(int(value/(2**x))%2) for x in range(length)])
    
    def fromBinary(value):
        retval=0
        for i in value:
            retval*=2
            retval+=int(i)
        return retval
    
    def load_image(file):
        """loads an image, prepares it for play"""
        file = os.path.join(main_dir, "data", file)
        try:
            surface = pg.image.load(file)
        except pg.error:
            raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
        return surface.convert()
    
    
    def load_sound(file):
        """because pygame can be compiled without mixer."""
        if not pg.mixer:
            return None
        file = os.path.join(main_dir, "data", file)
        try:
            sound = pg.mixer.Sound(file)
            return sound
        except pg.error:
            print(f"Warning, unable to load, {file}")
        return None
    global winfo
    winfo=0
    global texturesToLoad
    texturesToLoad=[]
    global renderCommands
    renderCommands=[]
    def surface_array(surfaceobj):
        x=[]
        w=surfaceobj.get_width()
        h=surfaceobj.get_height()
        a=surfaceobj.get_alpha()
        if(a==None):
            a=255
        for j in range(h):
            for i in range(w):
                b=surfaceobj.get_at((i,j))
                for c in range(3):
                    x.append(b[c])
                x.append([a if b!=(0,0,0,255) else 0][0])
        #for i in range(w):
        #    for j in range(h):
        #        x.append(1)
        return {'data':x,'size':[w,h]}
    
    
    def loadTexture(texture2):
        global texturesToLoad
        texturesToLoad.append(texture2)
        return (texturesToLoad.__len__()-1)
    def drawQuad(centerX, centerY,width,height, textureID, shouldCenter=0,altThings=None):
        global currentdepth
        global OPENGL_CAMERA_SHIFT
        width=width/20
        height=height/20
        #print(textureID,centerX,centerY,width,height)
        centerX=(centerX/20-15+width+OPENGL_CAMERA_SHIFT[0])/currentdepth
        centerY=(-centerY/20+8-height+OPENGL_CAMERA_SHIFT[1])/currentdepth
        width=width/currentdepth
        height=height/currentdepth
        if shouldCenter:
            OPENGL_CAMERA_SHIFT=[OPENGL_CAMERA_SHIFT[0]-(centerX+width/2)/5,OPENGL_CAMERA_SHIFT[1]-centerY/5]
        #print(centerX,centerY)
        if shouldCenter!=-1:
            verts = [(width, height), (width,-height), (-width,-height), (-width,height)]
            texts = ((1, 0), (1, 1), (0, 1), (0, 0))
            surf = (0, 1, 2, 3)
            global currentRenderOptions
            if altThings==None:
                altThings=[0,currentRenderOptions['shadow'],0]
            for i in surf:
                verts[i]=(verts[i][0]+centerX,verts[i][1]+centerY)
            global renderCommands
            renderCommands.append(['quad_textured',*verts,*texts,textureID,altThings])
        
    def drawQuadScaled(centerX, centerY,width,height, textureID, scalew=1,scaleh=1):
        global currentdepth
        global OPENGL_CAMERA_SHIFT
        width=width/20
        height=height/20
        #print(textureID,centerX,centerY,width,height)
        centerX=(centerX/20-15+width+OPENGL_CAMERA_SHIFT[0])/currentdepth
        centerY=(-centerY/20+8-height+OPENGL_CAMERA_SHIFT[1])/currentdepth
        width=width/currentdepth
        height=height/currentdepth
        #print(centerX,centerY)
        verts = [(width, height), (width,-height), (-width,-height), (-width,height)]
        texts = ((scalew/10, 0), (scalew/10, scaleh/10), (0, scaleh/10), (0, 0))
        surf = (0, 1, 2, 3)
        for i in surf:
            verts[i]=(verts[i][0]+centerX,verts[i][1]+centerY)
        global renderCommands
        global skipRenderTextures
        if textureID not in skipRenderTextures:
            renderCommands.append(['quad_textured',*verts,*texts,textureID,[0,currentRenderOptions['shadow']]])
    import math
    def drawQuadRoated(centerX, centerY,width,height, textureID,rotation=0, shouldCenter=0):
        global currentdepth
        global OPENGL_CAMERA_SHIFT
        width=width/20
        height=height/20
        #print(textureID,centerX,centerY,width,height)
        centerX=(centerX/20-15+width+OPENGL_CAMERA_SHIFT[0])/currentdepth-width
        centerY=(-centerY/20+8-height+OPENGL_CAMERA_SHIFT[1])/currentdepth-height

        width=width/currentdepth
        height=height/currentdepth
        if shouldCenter:
            OPENGL_CAMERA_SHIFT=[OPENGL_CAMERA_SHIFT[0]-centerX/5,OPENGL_CAMERA_SHIFT[1]-centerY/5]
        #print(centerX,centerY)
        x=(width*math.cos(rotation)+height*math.sin(-rotation), -width*math.sin(-rotation)+height*math.cos(rotation),
          -height*math.sin(-rotation)+width*math.cos(rotation), -height*math.cos(rotation)-width*math.sin(-rotation))
        verts = [(x[0],x[1]),
                 (x[2],x[3]),
                 (-x[0],-x[1]),
                 (-x[2],-x[3])
                ]
        texts = ((1, 0), (1, 1), (0, 1), (0, 0))
        surf = (0, 1, 2, 3)
        for i in surf:
            verts[i]=(verts[i][0]+centerX,verts[i][1]+centerY)
        global renderCommands
        renderCommands.append(['quad_textured',*verts,*texts,textureID,[0,currentRenderOptions['shadow']]])

    global currentRenderOptions
    currentRenderOptions={'shadow':0,'lastShadow':0,'nextShadow':0}
    
    
    def drawQuadStatic(centerX, centerY,width,height, textureID):
        maetriks=glfwApi.getMatrix()
        width=width
        height=height
        #print(textureID,centerX,centerY,width,height)
        centerX=centerX/2
        centerX-=maetriks[0]
        centerX/=maetriks[2]
        width/=maetriks[2]
        centerX+=15
        centerY=centerY
        centerY-=maetriks[1]
        centerY/=maetriks[3]
        height/=maetriks[3]
        centerY-=8
        verts = [(width, height*2), (width,0), (-0,-0), (-0,height*2)]
        texts = ((1, 0), (1, 1), (0, 1), (0, 0))
        surf = (0, 1, 2, 3)
        for i in surf:
            verts[i]=(verts[i][0]+centerX,verts[i][1]+centerY)
        global renderCommands
        global currentRenderOptions
        renderCommands.append(['quad_textured',*verts,*texts,textureID,[1,currentRenderOptions['shadow']]])
    #16 render width
    renderscale=40
    global currentdepth
    currentdepth=1
    global baseDepth
    baseDepth=30
    currentdepth=1
    def setup():
        global texturesToLoad
        glfwApi._start({i:texturesToLoad[i] for i in range(texturesToLoad.__len__())},940,480,"Mewo?")
    global lastCameraPos
    lastCameraPos=[0,0]
    def drawAll(all):
        global currentRenderOptions
        currentRenderOptions['shadow']=800
        global currentdepth
        global baseDepth
        global CAMERA_POS
        global player
        global lastFrameClock
        global FRAMERATE2
        t=time.time()-lastFrameClock
        lerpAmount=(t/(1/FRAMERATE2))%1
        global lastCameraPos
        lastCameraPos=[lastCameraPos[0]/5*4+CAMERA_POS[0]/5,lastCameraPos[1]/5*4+CAMERA_POS[1]/5]
        CAMERA_POSX=(-lastCameraPos[0],-lastCameraPos[1])
        
        players=[[[i.safeRect.left*lerpAmount+i.prevRect.left*(1-lerpAmount),i.safeRect.top*lerpAmount+i.prevRect.top*(1-lerpAmount),i.safeRect.size[0],i.safeRect.size[1]],i.imgid] for i in all if type(i)==Player]#+[[[i.rect.left,i.rect.top,i.rect.size[0],i.rect.size[1]],i.imgid] for i in [player]]
        for i in players:
            if i[1]!=None:
                drawQuad(i[0][0]-CAMERA_POSX[0]*CAMERA_SCALE, i[0][1]-CAMERA_POSX[1]*CAMERA_SCALE,i[0][2],i[0][3], i[1],-1)
        #glClear(GL_DEPTH_BUFFER_BIT| GL_COLOR_BUFFER_BIT)
        depth=0
        newdepth=0
        for i in all:
            #print(i)
            if('depth' in i.__dict__):
                newdepth=i.depth
            else:
                newdepth=0
            if(newdepth!=depth):
                #glTranslatef(0.0, 0.0, depth/4*3)
                depth=newdepth
                currentdepth=(depth+baseDepth)/baseDepth
                #glTranslatef(0.0, 0.0, -depth/4*3)

            
            
            if((type(i)!=Player)):
                if 'imgid' in i.__dict__:
                    if i.imgid!=None:
                        if 'rect' in i.__dict__:
                            if i.rect!=None:
                                #print('tsetuptemprect')
                                if ([i.prevRect.top,i.prevRect.left]==[0,0])|(i.prevRect.size==[0,0]):
                                    i.prevRect=i.rect
                                tempRect=[i.rect.left*lerpAmount+i.prevRect.left*(1-lerpAmount),i.rect.top*lerpAmount+i.prevRect.top*(1-lerpAmount),i.rect.size[0]*lerpAmount+i.prevRect.size[0]*(1-lerpAmount),i.rect.size[1]*lerpAmount+i.prevRect.size[1]*(1-lerpAmount)]
                                #print('ssetuptemprect')
                                shouldRender=True
                                if 'shouldRender' in i.__dict__:
                                    shouldRender=i.shouldRender
                                if shouldRender:
                                    if((tempRect[0]*((depth/4*3+renderscale)/renderscale)+CAMERA_POSX[0]*CAMERA_SCALE)<(940*0+pg.display.get_window_size()[0]*CAMERA_SCALE+depth*0)):
                                        if((tempRect[1]*((depth/4*3+renderscale)/renderscale)+CAMERA_POSX[1]*CAMERA_SCALE)<(480*0+pg.display.get_window_size()[1]*CAMERA_SCALE+depth*0)):
                                            if(tempRect[0]*((depth/4*3+renderscale)/renderscale)+tempRect[2]*CAMERA_SCALE*((depth/4*3+renderscale)/renderscale)+CAMERA_POSX[0]*CAMERA_SCALE)>(0-depth*0):
                                                if(tempRect[1]*((depth/4*3+renderscale)/renderscale)+tempRect[3]*CAMERA_SCALE*((depth/4*3+renderscale)/renderscale)+CAMERA_POSX[1]*CAMERA_SCALE)>(0-depth*0):
                                                    if 'rotation' in i.__dict__:
                                                        drawQuadRoated(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid,i.rotation)
                                                        if type(i) in [LaPew]:
                                                            renderCommands[-1][-1]=[False,currentRenderOptions['shadow'],2]
                                                    elif type(i) in [Wall]:
                                                        drawQuadScaled(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid,tempRect[2]/20,tempRect[3]/20)
                                                        #else:
                                                        #    drawQuad(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid)
                                                    #elif type(i)==Background:
                                                    #    drawQuad(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid,[0,0])
                                                    elif type(i) in [SaveMarker,LaPew]:
                                                        try:
                                                            drawQuad(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid,0,[False,currentRenderOptions['shadow'],1.5])
                                                        except Exception as err:
                                                            print('saveMarker prerender error ',err)
                                                    elif type(i) in [Hazard]:
                                                        try:
                                                            drawQuad(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid,0,[False,currentRenderOptions['shadow'],0])
                                                        except Exception as err:
                                                            print('prerender error ',err)
                                                    else:
                                                        drawQuad(tempRect[0]-CAMERA_POSX[0]*CAMERA_SCALE, tempRect[1]-CAMERA_POSX[1]*CAMERA_SCALE,tempRect[2],tempRect[3], i.imgid)
                                                    if 'lightLevel' in i.__dict__:
                                                        if i.lightLevel!=0:
                                                            renderCommands[-1][-1].append(0)
                                                            renderCommands[-1][-1][2]=i.lightLevel
                                                    elif 'lightLevel' in type(i).__dict__:
                                                        if i.lightLevel!=0:
                                                            renderCommands[-1][-1].append(0)
                                                            renderCommands[-1][-1][2]=i.lightLevel
        #glTranslatef(0.0, 0.0, depth/4*3)
        currentdepth=1
        for i in players:
            if i[1]!=None:
                drawQuad(i[0][0]-CAMERA_POSX[0]*CAMERA_SCALE, i[0][1]-CAMERA_POSX[1]*CAMERA_SCALE,i[0][2],i[0][3], i[1],1)

    def drawGUI(elements):
        #glTranslatef(0.0, 0.0, 0)
        for i in elements:
            if 'imgid' in i.__dict__:
                if i.imgid!=None:
                    #drawQuadStatic(i.rect.left/20-8*3, i.rect.top/20-4.08510638*3,i.rect.size[0]/20,i.rect.size[1]/20, i.imgid)
                    drawQuadStatic(i.rect.left, i.rect.top,i.rect.size[0],i.rect.size[1], i.imgid)
        #glTranslatef(0.0, 0.0, 0)
    
        #for c in text:
        #    glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    
    
    
    
    
    # Each type of game object gets an init and an update function.
    # The update function is called once per frame, and it is when each object should
    # change its current position and state.
    #
    # The Player object actually gets a "move" function instead of update,
    # since it is passed extra information about the keyboard.
    global totalCollisionChecks
    totalCollisionChecks=0
    def isColliding(a,b):
        global totalCollisionChecks
        totalCollisionChecks+=1
        return (a[0]<b[2])&(a[2]>b[0])&(a[1]<b[3])&(a[3]>b[1])
    def collisionUnion(a,b):
        return (min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
    global newParticles
    import time

    pygamesprite=pg.sprite.Sprite
    class newpgsprite(pygamesprite):
        def __init__(self,*groups):
            pygamesprite.__init__(self, *groups)
            self.prevRect=pg.rect.Rect((0,0,0,0))
    pg.sprite.Sprite=newpgsprite




















    class genericElement(pg.sprite.Sprite):
        textureIds: List[int] = []
        def __init__(self,pos,width,height,parent,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.rect=pg.rect.Rect((pos[0],pos[1],width,height))
            self.state={'hovered':False,'elementData':{}}
            self.elementId=[int(random.random()*65536),int(random.random()*65536),int(random.random()*65536),int(random.random()*65536)]
            self.parent=[parent][0]
            self.imgId=0
            self.imgid=self.textureIds[self.getImgId()]
        #@property
        #def imgid(self):
        #    return self.textureIds[self.getImgId()]
        def getImgId(self):
            return self.imgId
        def onClick(self,location:tuple,mouseButton:int,modifiers,guiVariables:dict):
            print('click type',mouseButton,'at',location,'with',modifiers)
            return -1
        def onMouseOver(self,guiVariables:dict):
            self.state['hovered']=True
            return {}
        def onMouseElsewhere(self,guiVariables:dict):
            self.state['hovered']=False
            return {}
        def onDrag(self,amount:tuple,mouseButton:int,modifiers:list,guiVariables:dict):
            return {}
        def onKpress(self,keyId:int,modifiers:list,guiVariables:dict):
            return {}
        def onTick(self,guiVariables:dict):
            return {}

    class GenericGui:
        def __init__(self,parent):
            self.parent=[parent][0]
            self.elements=[]
            self.guiVars={}
            self.isOpen=False
        def onOpen(self):
            global GUIelements
            for element in self.elements:
                GUIelements.add(element)
            self.isOpen=True
        def onClose(self):
            global GUIelements
            for element in self.elements:
                element.kill()
            self.isOpen=False
        def _onClick(self,location,button,mod):
            self.onClick(location,button,mod)
            for element in self.elements:
                
                if isColliding((element.rect.left,element.rect.top,element.rect.left+element.rect.size[0],element.rect.top+element.rect.size[1]*2),
                              (location[0],location[1],location[0]+1,location[1]+1)):
                    temp=element.onClick(((location[0]-element.rect.left)/(element.rect.size[0]),(location[1]-element.rect.top)/(element.rect.size[1]*2)),button,mod,self.guiVars)
                    if(temp!=-1):
                        self._mergeVars(self,temp)
                        return
            
                        
        def onClick(self,loc,but,mod):
            print('click type',but,'at',loc,'with',mod)
            return None
        def _onTick(self):
            for element in self.elements:
                
                self._mergeVars(element.onTick(self.guiVars))
            self.onTick()
        def onTick(self):
            return None
        def createElement(self,location,type):
            if type==0:
                self.elements.append(genericElement([location[0],location[1]],location[2],location[3],[self][0],))
        def createElements(self):
            self.createElement((0,0,50,50),0)
        def openGui(self):
            if self.elements==[]:
                self.createElements()
            self.onOpen()

        def _mergeVars(self,vars):
            for var in vars:
                self.guiVars[var]=vars[var]

    global testGuiA
    testGuiA=GenericGui(None)
    global allGuis
    allGuis=[]
    allGuis.append(testGuiA)



    #executeCode global testGuiA;testGuiA.openGui()



    class TriggerSystem:
        triggerList={}
        def trigger(triggerId):
            print(TriggerSystem,'now triggering',triggerId)
            if triggerId in TriggerSystem.triggerList:
                for trigger in TriggerSystem.triggerList[triggerId]:
                    try:
                        trigger[1]()
                        if trigger[0]==True:
                            TriggerSystem.triggerList[triggerId].pop(TriggerSystem.triggerList[triggerId].index(trigger))
                    except:
                        print('\t\t\tInvalid Trigger!')
                        TriggerSystem.triggerList[triggerId].pop(TriggerSystem.triggerList[triggerId].index(trigger))
        def addTrigger(triggerId,onlyonce, function):
            if triggerId not in TriggerSystem.triggerList:
                TriggerSystem.triggerList[triggerId]=[]
            TriggerSystem.triggerList[triggerId].append((onlyonce,function))

    
    
    class TriggerBrush(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        climbable=False
        shouldRender=False
        def __init__(self,pos,size,triggerId, *groups):
            self.width=size[0]
            self.height=size[1]
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width,self.height))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=pos
            self.imgid=None
            #self.imgid=self.textureIds[0]
            self.isSolid=False
            self.updateFrame()
            self.updateFrame()
            self.triggerId=triggerId
        def updateb(self,collideobjs):
            global player
            playerpos=(player.pos[0],player.pos[1],player.pos[0]+player.width,player.pos[1]+player.height)
            brushArea=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            if isColliding(playerpos,brushArea):
                TriggerSystem.trigger(self.ttriggerId)
                print('\t\t\t\t\t\t\tTriggering Id',self.triggerId)
        def updateb_2(self,collideobjs):
            pass
        def updateb_3(self,collideobjs):
            pass





    
    class Entity(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        climbable=False
        shouldRender=True
        def __init__(self, *groups):
            self.width=20
            self.height=20
            self.gravity=[0,0.2]
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width,self.height))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[0]
            self.wasOnGround=0
            self.lastShots=[time.time(),time.time()-1]
            self.isSolid=False
            self.updateFrame()
            self.updateFrame()
            self.extraUpdateFunct=lambda self:0

        def setPos(self,pos):
            self.pos=pos
        def setPosX(self,x):
            self.pos[0]=x
        def setPosY(self,y):
            self.pos[1]=y
        def accelerateHoriz(self,amount):
            self.animationFrame+=0.1
            if(self.animationFrame>=4):
                self.animationFrame=0
            self.velocity[0]+=(self.friction*2)*amount/self.mass
            #if self.onGround:
            #    if amount < 0:
            #        self.image = self.images[int(self.animationFrame)]
            #        self.imgid = self.textureIds[int(self.animationFrame)]
            #    elif amount > 0:
            #        self.image = self.images[5+int(self.animationFrame)]
            #        self.imgid = self.textureIds[5+int(self.animationFrame)]
            #else:
            #    if amount < 0:
            #        self.image = self.images[4+int(self.animationFrame/4)]
            #        self.imgid = self.textureIds[4+int(self.animationFrame/4)]
            #    elif amount > 0:
            #        self.image = self.images[9+int(self.animationFrame/4)]
            #        self.imgid = self.textureIds[9+int(self.animationFrame/4)]
            #if amount<0:
            #    self.facing=-1
            #elif amount>0:
            #    self.facing=1
            #self.rect = self.image.get_rect()
        def applyFriction(self,amount):
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*(1)**0.5
            self.velocity[1]+=self.gravity[1]*(1)**0.5
        def applyVelocity(self):
            self.pos[0]+=self.velocity[0]
            self.pos[1]+=self.velocity[1]
        def collideAndMove(self,objs,platformobjs=[],horiz=True):
            objs2=[]
            self.rect.left-=self.rect.size[0]*9
            self.rect.top-=self.rect.size[1]*9
            size1=self.rect.size
            self.rect.size=(self.rect.size[0]*19,self.rect.size[1]*19)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
            resetVelocity=[0,0]
            newVelocity=0
            hazardCollision=0
            sendBack=0
            farthestDownRoofPosition=-10000000000000000000000000000000000
            if horiz==True:
                self.pos[0]+=self.velocity[0]*1.5*60**2/FRAMERATE**2
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                
                
                
                for obj in objs:
                    isSolid=True
                    if 'isSolid' in obj.__dict__:
                        isSolid=obj.isSolid
                    if (obj!=self)&isSolid:
                        objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                        if(isColliding(objpos,playerpos)):
                            velshift=obj.velocity[0],obj.velocity[1]
                            obj.velocity[0]=obj.velocity[1]=0
                            self.velocity[0]-=velshift[0]
                            self.velocity[1]-=velshift[1]
                            newVelocity-=velshift[0]
                            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                            if(self.velocity[0]<0):
                                self.pos[0]=max(objpos[2],self.pos[0])
                                resetVelocity[0]=1
                                newVelocity=max(newVelocity,obj.velocity[0])
                            elif(self.velocity[0]>0):
                                self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                                resetVelocity[0]=1
                                newVelocity=min(newVelocity,obj.velocity[0])
                            
                            obj.velocity[0]+=velshift[0]
                            obj.velocity[1]+=velshift[1]
                            self.velocity[0]+=velshift[0]
                            self.velocity[1]+=velshift[1]
                            newVelocity+=velshift[0]
                if(resetVelocity[0]):
                    self.velocity[0]=newVelocity
                
            else:
                
                canStandOnObjs=[]
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in platformobjs:
                    objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
                    if(isColliding(objpos,playerpos)):
                        canStandOnObjs.append(obj)
                
                wasOnGround=self.onGround
                self.onGround=0
                leftStairsPos=-100
                self.pos[1]+=self.velocity[1]*1.5*60**2/FRAMERATE**2
                newVelocity=0
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in objs:
                    isSolid=True
                    if 'isSolid' in obj.__dict__:
                        isSolid=obj.isSolid
                    if (obj!=self)&isSolid:
                        objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                        objposb=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                        if(isColliding(objpos,playerpos)):
                            velshift=obj.velocity[0],obj.velocity[1]
                            obj.velocity[0]=obj.velocity[1]=0
                            self.velocity[0]-=velshift[0]
                            self.velocity[1]-=velshift[1]
                            newVelocity-=velshift[1]
                            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                            if(self.velocity[1]<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                                farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
                                self.pos[1]=farthestDownRoofPosition+1
                                newVelocity=max(newVelocity,obj.velocity[1])
                                resetVelocity[1]=1
                            elif(self.velocity[1]>0)|((self.velocity[1]==0)&(self.onGround)):
                                self.onGround=1
                                self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                                
                                newVelocity=min(newVelocity,obj.velocity[1])
                                resetVelocity[1]=1
                            obj.velocity[0]+=velshift[0]
                            obj.velocity[1]+=velshift[1]
                            self.velocity[0]+=velshift[0]
                            self.velocity[1]+=velshift[1]
                            newVelocity+=velshift[1]
                if(resetVelocity[1]):
                    self.velocity[1]=newVelocity
            
            #    if pg.mixer and boom_sound is not None
        
        def updateFrame(self):
            self.prevRect=self.rect
            b=pg.display.get_window_size()
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            #print(self.pos)
        #def gunpos(self):
        #    pos = self.facing * self.gun_offset + self.rect.centerx
        #    return pos, self.rect.top

        def updateb(self,collideobjs):
            self.extraUpdateFunct(self)
        def updateb_2(self,collideobjs):
            
            self.collideAndMove(collideobjs[0],collideobjs[1],True)
            self.updateFrame()
        def updateb_3(self,collideobjs):
            self.collideAndMove(collideobjs[0],collideobjs[1],False)
            self.applyGravity()
            self.friction=0.5*self.onGround+0.1
            self.applyFriction(self.friction)
            self.takeDamages(collideobjs[6])
            #if self.isSolid:
            #    collideobjs[0].add(self)
            
            self.updateFrame()
        
        
                
        
        def takeDamages(self,bullets):    
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in bullets:
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(playerpos,objpos)):
                    shouldInvert=False
                    if 'pull' in obj.__dict__:
                        if obj.pull==True:
                            shouldInvert=True
                    if shouldInvert:
                        self.velocity[0]-=obj.velocity[0]/5
                        self.velocity[1]-=obj.velocity[1]/5
                    else:
                        self.velocity[0]+=obj.velocity[0]/5
                        self.velocity[1]+=obj.velocity[1]/5
                    obj.kill()

    defaultSpriteCollide=pg.sprite.spritecollide
    def newSpriteCollide(object,group,shouldKill=False):
        if type(group)==type([]):
            return group
        else:
            value=[i for i in group if type(i)!=CollisionGroup]
            for i in group:
                if type(i)==CollisionGroup:
                    #print(i.pos)
                    if isColliding((object.pos[0],object.pos[1],object.pos[0]+object.width,object.pos[1]+object.height),(i.pos[0],i.pos[1],i.pos[0]+i.width,i.pos[1]+i.height)):
                        for j in i.objects:
                            value.append(j)
            return value
    pg.sprite.spritecollide=newSpriteCollide
    class CollisionGroup(pg.sprite.Sprite):
        def __init__(self, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.rect = pg.rect.Rect((0,0,0,0))
            self.velocity=[0,0]
            self.pos=[0,0]
            self.width=0
            self.height=0
            self.objects=pg.sprite.Group()
            self.updates=[]
            self.roomid=0

        def addObject(self,object):
            self.objects.add(object)
        def updateArea(self):
            if self.objects.sprites()!=[]:
                mins=[1000000000,1000000000]
                maxes=[-1000000000,-1000000000]
                for i in self.objects:
                    a=i.pos[0]
                    b=i.pos[1]
                    c=i.pos[0]+i.width
                    d=i.pos[1]+i.height
                    mins=[min(mins[0],a),min(mins[1],b)]
                    maxes=[max(maxes[0],c),max(maxes[1],d)]
                    if 'velocity' in i.__dict__:
                        a=i.pos[0]+i.velocity[0]*1.5*60**2/FRAMERATE**2
                        b=i.pos[1]+i.velocity[1]*1.5*60**2/FRAMERATE**2
                        c=i.pos[0]+i.width+i.velocity[0]*1.5*60**2/FRAMERATE**2
                        d=i.pos[1]+i.height+i.velocity[1]*1.5*60**2/FRAMERATE**2
                        mins=[min(mins[0],a),min(mins[1],b)]
                        maxes=[max(maxes[0],c),max(maxes[1],d)]
                mins=[mins[0]-20,mins[1]-20]
                maxes=[maxes[0]+20,maxes[1]+20]
                self.pos=mins
                self.rect.left=self.pos[0]
                self.rect.top=self.pos[1]
                self.width=maxes[0]-mins[0]
                self.height=maxes[1]-mins[1]
                self.rect.size=(self.width,self.height)

        def findIsCollidingWith(self,collideobjgroup):
            isCollidingWith=[]
            loc=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in collideobjgroup:
                if 'pos' in obj.__dict__:
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(objpos,loc)):
                        if(type(obj)==CollisionGroup):
                            for i in self.findIsCollidingWith(obj.objects):
                                isCollidingWith.append(i)
                        else:
                            isCollidingWith.append(obj)
                else:
                    pass
                    #print('\t\t\t\t\t\t\t\t\t\t\t\t\t\tinvalid collision object')
            return isCollidingWith
                        
        

        def removeIfDead(self):
            if self.objects.sprites().__len__()==0:
                self.kill()

        def kill(self):
            pg.sprite.Sprite.kill(self)
            for obj in self.objects:
                obj.kill()
        
        def updateb(self,collideobjs):
            #print('\t\t\t\t\t\t\t\t\t\tgroup updateb',self.objects.sprites().__len__(),self.pos,self.width,self.height)
            self.updateArea()
            inRangeObjects=[self.findIsCollidingWith(i) for i in collideobjs[0:2]]+[[]]+[self.findIsCollidingWith(i) for i in collideobjs[3:]]
            for i in self.objects:
                try:
                    i.updateb(inRangeObjects)
                finally:
                    pass
            self.updateArea()
            self.removeIfDead()
        def updateb_2(self,collideobjs):
            #print('\t\t\t\t\t\t\t\t\t\tgroup updateb_2',self.objects.sprites().__len__(),self.pos,self.width,self.height)
            self.updateArea()
            inRangeObjects=[self.findIsCollidingWith(i) for i in collideobjs]
            for i in self.objects:
                try:
                    i.updateb_2(inRangeObjects)
                finally:
                    pass
            self.updateArea()
            self.removeIfDead()
            
        def updateb_3(self,collideobjs):
            #print('\t\t\t\t\t\t\t\t\t\tgroup updateb_3',self.objects.sprites().__len__(),self.pos,self.width,self.height)
            self.updateArea()
            inRangeObjects=[self.findIsCollidingWith(i) for i in collideobjs]
            for i in self.objects:
                try:
                    i.updateb_3(inRangeObjects)
                finally:
                    pass
            self.updateArea()
            self.removeIfDead()
            
    class ChainedEntity(Entity):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        width=5
        height=5
        gravity=[0,0.2]
        def __init__(self, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width,self.height))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[0]
            self.wasOnGround=0
            self.lastShots=[time.time(),time.time()-1]
            self.isSolid=False
            self.chainedTo=[]
            self.chainedTob=[]
            self.stretchiness=0.75
            self.chainLen=5*(1-self.stretchiness)
            self.tempvel=[0,0]
            self.rotation=0
            self.shouldRotate=True
        def accelerateHoriz(self,amount):
            self.animationFrame+=0.1
            if(self.animationFrame>=4):
                self.animationFrame=0
            self.velocity[0]+=(self.friction*2)*amount/self.mass
            #if self.onGround:
            #    if amount < 0:
            #        self.image = self.images[int(self.animationFrame)]
            #        self.imgid = self.textureIds[int(self.animationFrame)]
            #    elif amount > 0:
            #        self.image = self.images[5+int(self.animationFrame)]
            #        self.imgid = self.textureIds[5+int(self.animationFrame)]
            #else:
            #    if amount < 0:
            #        self.image = self.images[4+int(self.animationFrame/4)]
            #        self.imgid = self.textureIds[4+int(self.animationFrame/4)]
            #    elif amount > 0:
            #        self.image = self.images[9+int(self.animationFrame/4)]
            #        self.imgid = self.textureIds[9+int(self.animationFrame/4)]
            #if amount<0:
            #    self.facing=-1
            #elif amount>0:
            #    self.facing=1
            #self.rect = self.image.get_rect()
        def applyFriction(self,amount):
            if (self.velocity[0]**2+self.velocity[1]**2)>1600:
                self.velocity[0]-=self.velocity[0]/self.mass*60/FRAMERATE/2
                self.velocity[1]-=self.velocity[1]/self.mass*60/FRAMERATE/2
            elif (self.velocity[0]**2+self.velocity[1]**2)>900:
                self.velocity[0]-=self.velocity[0]/self.mass*60/FRAMERATE/10
                self.velocity[1]-=self.velocity[1]/self.mass*60/FRAMERATE/10
            elif (self.velocity[0]**2+self.velocity[1]**2)>400:
                self.velocity[0]-=self.velocity[0]/self.mass*60/FRAMERATE/20
                self.velocity[1]-=self.velocity[1]/self.mass*60/FRAMERATE/20
            else:
                self.velocity[0]-=self.velocity[0]/self.mass*60/FRAMERATE/50
                self.velocity[1]-=self.velocity[1]/self.mass*60/FRAMERATE/50
            if(self.velocity[0]**2<0.00001):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.00001):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*(1)**0.5
            self.velocity[1]+=self.gravity[1]*(1)**0.5
        def applyVelocity(self):
            self.pos[0]+=self.velocity[0]
            self.pos[1]+=self.velocity[1]
        def chainUpdate(self):
            
            v1=self.velocity[0]*1.5*60**2/FRAMERATE**2
            v2=self.velocity[1]*1.5*60**2/FRAMERATE**2
            xb=self.pos[0]+v1
            yb=self.pos[1]+v2

            nvelx=[]
            nvely=[]
            closepos=[[self.pos,[self.width,self.height]]]
            for obj in self.chainedTo:
                len2=0
                if type(obj)==tuple:
                    len2=obj[0]
                    try:
                        if obj.__len__()>=3:
                            if(obj[2]):
                                closepos.append([obj[1].pos,[obj[1].width,obj[1].height]])
                    finally:
                        pass
                    obj=obj[1]
                    
                else:
                    if 'chainLen' in obj.__dict__:
                        len2=obj.chainLen
                    else:
                        len2=(obj.width+obj.height)/3

                ov0=obj.velocity[0]*1.5*60**2/FRAMERATE**2
                ov1=obj.velocity[1]*1.5*60**2/FRAMERATE**2

                if(((xb+self.width/2-(obj.pos[0]+ov0+obj.width/2))**2+(yb+self.height/2-(obj.pos[1]+ov1+obj.height/2))**2)**0.5)>((self.chainLen+len2)/2):
                    distMult=((self.chainLen+len2)/2)/(((xb+self.width/2-(obj.pos[0]+ov0+obj.width/2))**2+(yb+self.height/2-(obj.pos[1]+ov1+obj.height/2))**2)**0.5)
                    xdist=(xb+self.width/2-(obj.pos[0]+ov0+obj.width/2))*distMult
                    ydist=(yb+self.height/2-(obj.pos[1]+ov1+obj.height/2))*distMult
                    nvelx.append((xdist+(obj.pos[0]+ov0+obj.width/2)-(self.pos[0]+self.width/2))/1.5/60/60*FRAMERATE*FRAMERATE)
                    nvely.append((ydist+(obj.pos[1]+ov1+obj.height/2)-(self.pos[1]+self.height/2))/1.5/60/60*FRAMERATE*FRAMERATE)
            nvel0,nvel1=self.velocity[0],self.velocity[1]
            if nvelx!=[]:
                nvel0=sum(nvelx)/(nvelx.__len__())
            if nvely!=[]:
                nvel1=sum(nvely)/(nvely.__len__())
            dvel0=nvel0-self.velocity[0]
            dvel1=nvel1-self.velocity[1]
            
            mvchange=10
            if(dvel0**2+dvel1**2)**0.5>mvchange:
                dvel=(dvel0**2+dvel1**2)**0.5
                dvel0*=mvchange/dvel
                dvel1*=mvchange/dvel
            try:
                posd=[sum([i[0][0]+i[1][0]/2 for i in closepos])/closepos.__len__()-self.pos[0]-self.width/2,sum([i[0][1]+i[1][1]/2 for i in closepos])/closepos.__len__()-self.pos[1]-self.height/2]
                self.tempvel[0]=self.velocity[0]
                self.tempvel[1]=self.velocity[1]
                self.tempvel[0]+=dvel0*(1-self.stretchiness)
                self.tempvel[1]+=dvel1*(1-self.stretchiness)
                self.tempvel[0]+=posd[0]/10*FRAMERATE/60
                self.tempvel[1]+=posd[1]/10*FRAMERATE/60
            finally:
                pass
            m=40
            if self.tempvel[0]>m:
                self.tempvel[0]=(self.tempvel[0]-m)**0.5+m
            if self.tempvel[1]>m:
                self.tempvel[1]=(self.tempvel[1]-m)**0.5+m
            if self.tempvel[0]<-m:
                self.tempvel[0]=-(-self.tempvel[0]-m)**0.5-m
            if self.tempvel[1]<-m:
                self.tempvel[1]=-(-self.tempvel[1]-m)**0.5-m
            """
            for obj in self.chainedTo:
                len2=0
                if 'chainLen' in obj.__dict__:
                    len2=obj.chainLen
                else:
                    len2=(obj.width+obj.height)/3
                if(((self.pos[0]+self.width/2-(obj.pos[0]+obj.width/2))**2+(self.pos[1]+self.height/2-(obj.pos[1]+obj.height/2))**2)**0.5)>((self.chainLen+len2)/2):
                    xdist=(self.pos[0]+self.width/2-(obj.pos[0]+obj.width/2))
                    ydist=(self.pos[1]+self.height/2-(obj.pos[1]+obj.height/2))
                    dist=(xdist**2+ydist**2)**0.5+0.001
                    dist2=dist
                    dist=dist+(self.chainLen+len2)/2
                    self.velocity[0]-=xdist*dist2/dist/dist
                    self.velocity[1]-=ydist*dist2/dist/dist"""
        def collideAndMove(self,objs,platformobjs=[],horiz=True):
            objs2=[]
            self.rect.left-=200
            self.rect.top-=200
            size1=self.rect.size
            self.rect.size=(self.rect.size[0]+400,self.rect.size[1]+400)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
            resetVelocity=[0,0]
            newVelocity=0
            hazardCollision=0
            sendBack=0
            farthestDownRoofPosition=-10000000000000000000000000000000000
            if horiz==True:
                self.pos[0]+=self.velocity[0]*1.5*60**2/FRAMERATE**2
                playerpos=(0,0,0,0)
                if self.velocity[0]>0:
                    playerpos=(self.pos[0]-self.velocity[0]*1.5*60**2/FRAMERATE**2,self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                else:
                    playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width-self.velocity[0]*1.5*60**2/FRAMERATE**2,self.pos[1]+self.height)
                
                
                
                for obj in objs:
                    v=[obj.velocity[0],obj.velocity[1]]
                    obj.velocity[0]-=v[0]
                    obj.velocity[1]-=v[1]
                    self.velocity[0]-=v[0]
                    self.velocity[1]-=v[1]
                    newVelocity-=v[0]
                    ov1=v[0]*1.5*60**2/FRAMERATE**2
                    ov2=v[1]*1.5*60**2/FRAMERATE**2
                    if (obj not in [self,*[i[0] for i in self.chainedTo],*self.chainedTob]):
                        objpos=(obj.pos[0]+ov1,obj.pos[1]+ov2,obj.pos[0]+obj.width+ov1,obj.pos[1]+obj.height+ov2)
                        if(isColliding(objpos,playerpos)):
                            objpos=(obj.pos[0]+ov1,obj.pos[1]+ov2,obj.pos[0]+obj.width+ov1,obj.pos[1]+obj.height+ov2)
                            if(self.velocity[0]<0):
                                self.pos[0]=max(objpos[2],self.pos[0])
                                resetVelocity[0]=1
                                newVelocity=max(newVelocity,obj.velocity[0])
                            elif(self.velocity[0]>0):
                                self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                                resetVelocity[0]=1
                                newVelocity=min(newVelocity,obj.velocity[0])
                    obj.velocity[0]+=v[0]
                    obj.velocity[1]+=v[1]
                    self.velocity[0]+=v[0]
                    self.velocity[1]+=v[1]
                    newVelocity+=v[0]
                if(resetVelocity[0]):
                    self.velocity[0]=newVelocity
                
            else:
                
                canStandOnObjs=[]
                self.pos[1]+=self.velocity[1]*1.5*60**2/FRAMERATE**2
                
                if self.velocity[1]>0:
                    playerpos=(self.pos[0],self.pos[1]-self.velocity[1]*1.5*60**2/FRAMERATE**2,self.pos[0]+self.width,self.pos[1]+self.height)
                else:
                    playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]-self.velocity[1]*1.5*60**2/FRAMERATE**2+self.height)
                for obj in platformobjs:
                    objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
                    if(isColliding(objpos,playerpos)):
                        canStandOnObjs.append(obj)
                
                wasOnGround=self.onGround
                self.onGround=0
                leftStairsPos=-100
                self.pos[1]+=self.velocity[1]*1.5*60**2/FRAMERATE**2
                newVelocity=0
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in objs:
                    v=[obj.velocity[0],obj.velocity[1]]
                    obj.velocity[0]-=v[0]
                    obj.velocity[1]-=v[1]
                    self.velocity[0]-=v[0]
                    self.velocity[1]-=v[1]
                    newVelocity-=v[0]
                    ov1=v[0]*1.5*60**2/FRAMERATE**2
                    ov2=v[1]*1.5*60**2/FRAMERATE**2
                    if (obj not in [self,*[i[0] for i in self.chainedTo],*self.chainedTob]):
                        objpos=(obj.pos[0]+ov1,obj.pos[1]+ov2,obj.pos[0]+obj.width+ov1,obj.pos[1]+obj.height+ov2)
                        objposb=(obj.pos[0]+ov1,obj.pos[1]+ov2,obj.pos[0]+obj.width+ov1,obj.pos[1]+obj.height+ov2)
                        if(isColliding(objpos,playerpos)):
                            objpos=(obj.pos[0]+ov1,obj.pos[1]+ov2,obj.pos[0]+obj.width+ov1,obj.pos[1]+obj.height+ov2)
                            if(self.velocity[1]<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                                farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
                                self.pos[1]=farthestDownRoofPosition+1
                                newVelocity=max(newVelocity,obj.velocity[1])
                                resetVelocity[1]=1
                            elif(self.velocity[1]>0)|((self.velocity[1]==0)&(self.onGround)):
                                self.onGround=1
                                self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                                
                                newVelocity=min(newVelocity,obj.velocity[1])
                                resetVelocity[1]=1
                    obj.velocity[0]+=v[0]
                    obj.velocity[1]+=v[1]
                    self.velocity[0]+=v[0]
                    self.velocity[1]+=v[1]
                    newVelocity+=v[1]
                if(resetVelocity[1]):
                    self.velocity[1]=newVelocity
            
            #    if pg.mixer and boom_sound is not None
        
        def updateFrame(self):
            self.prevRect=self.rect
            #try:
            if self.shouldRotate:
                b=pg.display.get_window_size()
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE-2
                self.rect.size=(self.width,self.height+2)
                c=[i for i in self.chainedTo if i.__len__()>=3]
                
                c=[i[1].pos for i in c if i[2]]
                
                d=sum([i[0] for i in c])/c.__len__()-self.pos[0]
                e=sum([i[1] for i in c])/c.__len__()-self.pos[1]
                
                if c.__len__()>=2:
                    self.rect.left=(d+self.pos[0]*CAMERA_SCALE)
                    self.rect.top=(e+self.pos[1]*CAMERA_SCALE)-2
                    self.rect.size=(self.width,self.height+2)
            
                
                self.rotation=self.rotation/2+math.atan2(c[0][0]-self.pos[0],c[0][1]-self.pos[1])/2
            else:
                self.rect.left=(self.pos[0]+self.width/2)*CAMERA_SCALE
                self.rect.top=(self.pos[1]-self.height/2)*CAMERA_SCALE
                self.rect.size=(self.width,self.height)
            #finally:
            #    pass
            #print(self.pos)
        #def gunpos(self):
        #    pos = self.facing * self.gun_offset + self.rect.centerx
        #    return pos, self.rect.top

        def updateb(self,collideobjs):
            self.chainUpdate()
        def updateb_2(self,collideobjs):
            self.velocity=self.tempvel
            self.collideAndMove(collideobjs[0],collideobjs[1],True)
            self.updateFrame()
        def updateb_3(self,collideobjs):
            self.collideAndMove(collideobjs[0],collideobjs[1],False)
            self.applyGravity()
            #self.friction=0.3
            self.applyFriction(self.friction)
            self.takeDamages(collideobjs[6])
            if self.isSolid:
                collideobjs[0].add(self)
        
            
            self.updateFrame()
        
        
                
        
        def takeDamages(self,bullets):    
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in bullets:
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(playerpos,objpos)):
                    shouldInvert=False
                    if 'pull' in obj.__dict__:
                        if obj.pull==True:
                            shouldInvert=True
                    if shouldInvert:
                        self.velocity[0]-=obj.velocity[0]/5
                        self.velocity[1]-=obj.velocity[1]/5
                    else:
                        self.velocity[0]+=obj.velocity[0]/5
                        self.velocity[1]+=obj.velocity[1]/5
                    obj.kill()
    class movableTile(Entity):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        width=20
        height=20
        gravity=[0,0.2]
        def __init__(self,pos, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width*2,self.height*2))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[0]
            self.wasOnGround=0
            self.lastShots=[time.time(),time.time()-1]
            self.isSolid=False
            self.isSolid=True
            self.pos=pos
            self.extraUpdateFunct=lambda self:0
            
    class movableTile2(ChainedEntity):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        def __init__(self,pos,size, *groups):
            
            self.width=size[0]
            self.height=size[1]
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width*2,self.height*2))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.friction=0.0
            self.imgid=self.textureIds[0]
            self.wasOnGround=0
            self.lastShots=[time.time(),time.time()-1]
            self.isSolid=False
            self.isSolid=False
            self.pos=pos
            self.chainedTo=[]
            self.chainedTob=[]
            self.stretchiness=0.00
            self.chainLen=4*(1-self.stretchiness)
            self.gravity=[0,0.1]
            self.climbable=True
            self.tempvel=[0,0]
            self.rotation=0
            self.shouldRotate=True

    def mergeRect(*rects):
        mins=[999999999999999,999999999999999]
        maxes=[-999999999999999,-999999999999999]
        for rect in rects:
            a=rect[0]
            b=rect[1]
            c=rect[2]
            d=rect[3]
            mins=[min(mins[0],a),min(mins[1],b)]
            maxes=[max(maxes[0],c),max(maxes[1],d)]
        return (*mins,*maxes)
    
    class Player(pg.sprite.Sprite):
        speed = 10
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        width=20
        height=35
        gravity=[0,0.6]
        climbspeed=3
        def __init__(self, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.facing = -1
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.attributes={'barrels':2,'health':10,'maxhealth':10,'stepsize':10}
            self.animationFrame=0
            self.savePos=self.pos
            self.anticorruptroomandpos=(0,[0,-50])
            self.immunityFrames=0
            self.friction=0.1
            self.imgid=self.textureIds[0]
            self.imgidy=None
            self.firecooldown=0
            self.ducking=0
            self.shotsleft=0
            self.wasOnGround=0
            self.canClimb=0
            self.reloadTime=0
            self.wasDucking=0
            self.safeRect=pg.rect.Rect((self.pos[0],self.pos[1],self.width,self.height))
            self.lastShots=[time.time(),time.time()-1]
            self.frictionObjs=[[0,0]]
            self.climbingOn=[]
            self.canClimbOn=[]
            self.isClimbing=False
        def move(self, direction):
            if direction:
                self.facing = direction
            #self.rect.move_ip(direction * self.speed, 0)
            if direction < 0:
                self.image = self.images[0]
            elif direction > 0:
                self.image = self.images[1]
            self.rect = self.image.get_rect()
            #self.rect.top = self.origtop# - (self.rect.left // self.bounce % 2)
        def accelerateHoriz(self,amount,origin):
            self.velocity[0]-=origin[0]
            self.velocity[1]-=origin[1]
            self.animationFrame+=0.1
            if(self.animationFrame>=4):
                self.animationFrame=0
            if self.canClimb!=0:
                self.velocity[0]/=2
                if amount<0:
                    self.velocity[0]-=self.climbspeed/2*FRAMERATE**2/60**2
                    self.climbingOn=[i for i in self.canClimbOn]
                elif amount>0:
                    self.velocity[0]+=self.climbspeed/2*FRAMERATE**2/60**2
                    self.climbingOn=[i for i in self.canClimbOn]
                else:
                    self.velocity[0]=0
                
            else:
                self.velocity[0]+=(0.1+self.friction)*amount/self.mass
            self.velocity[0]+=origin[0]
            self.velocity[1]+=origin[1]
            if self.onGround:
                if amount < 0:
                    self.image = self.images[int(self.animationFrame)]
                    self.imgid = self.textureIds[int(self.animationFrame)]
                elif amount > 0:
                    self.image = self.images[5+int(self.animationFrame)]
                    self.imgid = self.textureIds[5+int(self.animationFrame)]
            else:
                if amount < 0:
                    self.image = self.images[4+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[4+int(self.animationFrame/4)]
                elif amount > 0:
                    self.image = self.images[9+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[9+int(self.animationFrame/4)]
            if amount<0:
                self.facing=-1
            elif amount>0:
                self.facing=1
            #self.rect = self.image.get_rect()
        def applyFriction(self,amount,zero=[0,0]):
            self.velocity[0]-=zero[0]
            self.velocity[1]-=zero[1]
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
            self.velocity[0]+=zero[0]
            self.velocity[1]+=zero[1]
        def applyGravity(self,down,origin):
            self.velocity[0]-=origin[0]
            self.velocity[1]-=origin[1]
            if (self.canClimb not in [0])&(self.isClimbing!=0):
                climbvectors=[[math.sin(i),math.cos(i)]for i in self.canClimb]
                climbvector=[(sum([i[0] for i in climbvectors]))/climbvectors.__len__(),(sum([i[1] for i in climbvectors]))/climbvectors.__len__()]
                self.velocity[0]/=3/2
                self.velocity[1]/=3/2
                if down:
                    self.velocity[0]+=self.climbspeed/3*2*climbvector[0]*FRAMERATE/60
                    self.velocity[1]+=self.climbspeed/3*2*climbvector[1]*FRAMERATE/60
                    self.climbingOn=[i for i in self.canClimbOn]
                poses=[(*i.pos,i.width,i.height) for i in self.climbingOn]
                avgpos=[(sum([i[0]+i[2]/2 for i in poses]))/poses.__len__(),(sum([i[1]+i[3]/2 for i in poses]))/poses.__len__()]
                cpos=(self.pos[0]+self.width/2,self.pos[1]+self.height/2)
                #print('\t\t\t\t\t\t\t\t\t\t\t',cpos,'\t',avgpos)
                if avgpos[0]>cpos[0]+2:
                    self.velocity[0]+=(avgpos[0]-cpos[0])
                elif avgpos[0]<cpos[0]-2:
                    self.velocity[0]+=(avgpos[0]-cpos[0])
                if avgpos[1]>cpos[1]+2:
                    self.velocity[1]+=(avgpos[1]-cpos[1])
                elif avgpos[1]<cpos[1]-2:
                    self.velocity[1]+=(avgpos[1]-cpos[1])
            else:
                self.velocity[1]+=self.gravity[1]*(1)**0.5*60/FRAMERATE
                self.velocity[0]+=self.gravity[0]*(1)**0.5*60/FRAMERATE
            self.velocity[0]+=origin[0]
            self.velocity[1]+=origin[1]

        def applyVelocity(self):
            self.pos[0]+=self.velocity[0]
            self.pos[1]+=self.velocity[1]
        def jump(self):
            if (self.canClimb not in [0])&(self.isClimbing!=0):
                climbvectors=[[math.sin(i),math.cos(i)]for i in self.canClimb]
                climbvector=[(sum([i[0] for i in climbvectors]))/climbvectors.__len__(),(sum([i[1] for i in climbvectors]))/climbvectors.__len__()]

                self.velocity[0]/=2
                self.velocity[1]/=2
                self.velocity[0]+=-self.climbspeed/2*climbvector[0]*60/FRAMERATE
                self.velocity[1]+=-self.climbspeed/2*climbvector[1]*60/FRAMERATE
                self.climbingOn=[i for i in self.canClimbOn]
            else:
                if(self.onGround):
                    self.velocity[1]=-10*FRAMERATE/60
        def collideAndMove(self,objs,platformobjs=[],horiz=True):
            objs2=[]
            if(self.ducking):
                self.pos[1]+=15
                self.height-=15
            self.rect.left-=self.rect.size[0]*9
            self.rect.top-=self.rect.size[1]*9
            size1=self.rect.size
            self.rect.size=(self.rect.size[0]*19,self.rect.size[1]*19)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
            resetVelocity=[0,0]
            hazardCollision=0
            sendBack=0
            farthestDownRoofPosition=-10000000000000000000000000000000000
            frictionList=[]
            if horiz:
                opp=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                if(self.velocity[1]<0):
                    playerpos=(self.pos[0],self.pos[1]+self.attributes['stepsize'],self.pos[0]+self.width,self.pos[1]+self.height)
                if(self.onGround):
                    playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height-self.attributes['stepsize'])
                
                playerposb=mergeRect(playerpos,opp)
                playerpos=(playerposb[0],playerpos[1],playerposb[2],playerpos[3])
                
                newVelocity=self.velocity[0]
                
                
                for obj in objs:    
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(objpos,playerpos)):
                        frictionList.append(obj.velocity)
                        a=1
                        if('isSolid' in obj.__dict__):
                            if obj.isSolid==0:
                                a=0
                        if a:
                            velshift=obj.velocity[0]
                            obj.velocity[0]-=velshift
                            newVelocity-=velshift
                            self.velocity[0]-=velshift
                            obj.pos[1]-=velshift*1.5*60**2/FRAMERATE**2
                            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                            if((self.velocity[0]-obj.velocity[0])<0):
                                self.pos[0]=max(objpos[2],self.pos[0])
                                if obj.velocity[0]>newVelocity:
                                    newVelocity=max(newVelocity,obj.velocity[0])
                                if obj.velocity[0]<newVelocity:
                                    newVelocity=min(newVelocity,obj.velocity[0])
                                resetVelocity[0]=1
                            elif((self.velocity[0]-obj.velocity[0])>0):
                                self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                                if obj.velocity[0]>newVelocity:
                                    newVelocity=max(newVelocity,obj.velocity[0])
                                if obj.velocity[0]<newVelocity:
                                    newVelocity=min(newVelocity,obj.velocity[0])
                                resetVelocity[0]=1
                            if(type(obj)==Hazard):
                                hazardCollision=obj.damage
                                sendBack=obj.sendBack
                            
                            obj.velocity[0]+=velshift
                            newVelocity+=velshift
                            self.velocity[0]+=velshift
                            obj.pos[1]+=velshift*1.5*60/FRAMERATE
                if(resetVelocity[0]):
                    self.velocity[0]=newVelocity
            else:
                self.canClimbOn=[]
                self.canClimb=0
                farthestDownRoofPosition=-10000000000000000000000000000000000
                canStandOnObjs=[]
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in platformobjs:
                    objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
                    if(isColliding(objpos,playerpos)):
                        canStandOnObjs.append(obj)
                
                wasOnGround=self.onGround
                self.onGround=0
                leftStairsPos=-100
                
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
                newVelocity=self.velocity[1]
                playerpos=mergeRect(playerpos,(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height))
                
                for obj in objs:
                    velshift=obj.velocity[1]
                    obj.velocity[1]-=velshift
                    newVelocity-=velshift
                    self.velocity[1]-=velshift
                    obj.pos[1]+=velshift*1.5*60/FRAMERATE
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    objposb=(obj.pos[0],obj.pos[1]-self.attributes['stepsize'],obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.attributes['stepsize'])
                    if(isColliding(objpos,playerpos)):
                        frictionList.append(obj.velocity)
                        a=1
                        if('isSolid' in obj.__dict__):
                            if obj.isSolid==0:
                                a=0
                                if obj.climbable:
                                    if self.isClimbing:
                                        frictionList.append(obj.velocity)
                            else:
                                frictionList.append(obj.velocity)
                        else:
                            frictionList.append(obj.velocity)
                        if a:
                            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                            if((self.velocity[1]-obj.velocity[1])<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                                farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
    
                                if obj.velocity[1]>newVelocity:
                                    newVelocity=max(newVelocity,obj.velocity[1])
                                if obj.velocity[1]<newVelocity:
                                    newVelocity=min(newVelocity,obj.velocity[1])
                                
                                self.pos[1]=farthestDownRoofPosition+1
                                resetVelocity[1]=1
                            elif((self.velocity[1]-obj.velocity[1])>0)|((self.velocity[1]==0)&(self.onGround)):
                                self.onGround=1
                                self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                                if obj.velocity[1]>newVelocity:
                                    newVelocity=max(newVelocity,obj.velocity[1])
                                if obj.velocity[1]<newVelocity:
                                    newVelocity=min(newVelocity,obj.velocity[1])
                                
                                resetVelocity[1]=1
                            if(type(obj)==Hazard):
                                hazardCollision=obj.damage
                                sendBack=obj.sendBack
                        if('climbable' in obj.__dict__):
                            if obj.climbable:
                                if self.canClimb==0:
                                    self.canClimb=[]
                                    #print('\t\t\t\t\t\t\t\t\t\t\tappendCl1mbFAIL')
                                if 1:
                                    self.canClimb.append(obj.rotation);
                                    self.canClimbOn.append(obj);
                                    #print('\t\t\t\t\t\t\t\t\t\t\tappendCl1mb')
                                else:
                                    self.canClimb=1
                    if(wasOnGround):
                        if not self.onGround:
                            if obj.width==2:
                                if(isColliding(objposb,playerpos)):
                                    if self.velocity[0]>0:
                                        self.onGround=1
                                        self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                        self.velocity[1]=0
                                    elif self.velocity[0]<0:
                                        self.onGround=1
                                        self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                        self.velocity[1]=0
                    
                    obj.velocity[1]+=velshift
                    newVelocity+=velshift
                    self.velocity[1]+=velshift
                    obj.pos[1]-=velshift*1.5*60/FRAMERATE
                if(resetVelocity[1]):
                    self.velocity[1]=newVelocity
                for obj in canStandOnObjs:
                    
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(objpos,playerpos)):
                        
                        if(self.velocity[1]<0):
                            self.pos[1]=objpos[3]
                            resetVelocity[1]=1
                        else:
                            self.onGround=1
                            self.pos[1]=objpos[1]-self.height
                            resetVelocity[1]=1
                        if(type(obj)==Hazard):
                            hazardCollision=obj.damage
                            sendBack=obj.sendBack
            if self.immunityFrames==-1:
                if(hazardCollision!=0):
                    self.immunityFrames=90
                    self.attributes['health']-=hazardCollision
                    for i in range(42):
                        newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2,1,120])
                    if(sendBack):
                        self.velocity=[0,0]
                        self.pos=self.savePos
                    
            if(resetVelocity[1]):
                self.velocity[1]=newVelocity
            #    if pg.mixer and boom_sound is not None:
            #        boom_sound.play()
            #    Explosion(alien, all)
            #    Explosion(player, all)
            #    SCORE = SCORE + 1
            #    player.kill()
        
            if(self.ducking):
                self.pos[1]-=15
                self.height+=15
            return frictionList

        def getRoomShadows(self,rooms):
            global currentRenderOptions
            pos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            shadowValues=[]
            for obj in rooms:
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                #print(obj.id, 'shad', str(obj.shadowLevel),objpos,pos)
                if (isColliding(objpos,pos)):
                    if obj.shadowLevel!=None:
                        shadowValues.append(obj.shadowLevel)
            if shadowValues==[]:
                shadowValues=currentRenderOptions['shadow']
            else:
                shadowValues=sum(shadowValues)/shadowValues.__len__()
            #print(shadowValues,currentRenderOptions['shadow'])
            if shadowValues>currentRenderOptions['shadow']+1:
                currentRenderOptions['shadow']+=int((shadowValues-currentRenderOptions['shadow'])/10)-1
            elif shadowValues<currentRenderOptions['shadow']-1:
                currentRenderOptions['shadow']+=int((shadowValues-currentRenderOptions['shadow'])/10)+1


        
        
        def duckingChecks(self,objs):
            objs2=[]
            if(self.ducking==0)&(self.wasDucking==1):
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            
                self.rect.left-=self.rect.size[0]*2
                self.rect.top-=self.rect.size[1]*2
                size1=self.rect.size
                self.rect.size=(self.rect.size[0]*5,self.rect.size[1]*5)
                for i in pg.sprite.spritecollide(self,objs,0):
                    objs2.append(i)
                objs=objs2
                self.rect.size=size1
                self.rect.left+=self.rect.size[0]*2
                self.rect.top+=self.rect.size[1]*2
                for obj in objs:    
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(objpos,playerpos)):
                        self.ducking=1
                
        
        
        
        
        
        
        
        
        
        
        def updateRooms(self,groups):
            allobjs=groups[5]
            roomslist=groups[3]
            allrooms=groups[4]
            pos=(self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height)
            for obj in roomslist:
                if obj.disabled==0:
                    pos2=(obj.pos[0]-glfwApi.getWindowSize()[0]*0.75,obj.pos[1]-glfwApi.getWindowSize()[1]*0.75,obj.pos[0]+obj.width+glfwApi.getWindowSize()[0]*0.75,obj.pos[1]+obj.height+glfwApi.getWindowSize()[1]*0.75)
                    if(isColliding(pos,pos2)):
                        #print('att build room')
                        obj.triggerBuildRoom(groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
                        #print('succeed build room')
            for obj in allrooms:
                pos2=(obj.pos[0]-glfwApi.getWindowSize()[0]*0.75,obj.pos[1]-glfwApi.getWindowSize()[1]*0.75,obj.pos[0]+obj.width+glfwApi.getWindowSize()[0]*0.75,obj.pos[1]+obj.height+glfwApi.getWindowSize()[1]*0.75)
                if not (isColliding(pos,pos2)):
                    #print('att unbuild room')
                    obj.unbuildRoom(groups[5],roomslist)
                    #print('succeed unbuild room')
                    #obj.unbuildRoom(allobjs,roomslist)
        def updateCamPos(self):
            #lastCameraPos=CAMERA_POS
            b=pg.display.get_window_size()
            CAMERA_POS[0]=(CAMERA_POS[0]*1+(self.pos[0]+self.width/2-b[0]/2)*9)/10+b[0]*(1-1/CAMERA_SCALE)/2
            CAMERA_POS[1]=(CAMERA_POS[1]*1+(self.pos[1]+self.height/2-b[1]/2)*9)/10+b[1]*(1-1/CAMERA_SCALE)/2
        def updateFrame(self):
            b=pg.display.get_window_size()
            self.updateCamPos()
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            self.safeRect.left=(self.pos[0])*CAMERA_SCALE
            self.safeRect.top=(self.pos[1])*CAMERA_SCALE
            #print(self.pos)
        #def gunpos(self):
        #    pos = self.facing * self.gun_offset + self.rect.centerx
        #    return pos, self.rect.top
        def fixNoRooms(self,objs):
            if objs[4].__len__()==0:
                self.attributes['health']-=0
                self.velocity=[0,0]
                self.pos=self.savePos
                rooms[self.anticorruptroomandpos[0]].buildRoom(self.anticorruptroomandpos[1],*objs)
        def immunityFramesVisuals(self):
            if(self.immunityFrames>-1):
                if(self.immunityFrames%30>=15):
                    if(self.imgid!=None):
                        self.imgidy=self.imgid+1-1
                        self.imgid=None
                    
                elif(self.immunityFrames%30>=0):
                    if(self.imgid==None):
                        self.imgid=self.imgidy+1-1
                        self.imgidy=None
                self.immunityFrames-=1
            if(self.immunityFrames==0):
                for i in self.images:
                    i.set_alpha(255)
        def updateb(self,collideobjs,horiz,vert,fire,down=0):
            self.prevRect.left=self.rect.left
            self.prevRect.top=self.rect.top
            #print(f'\t\t\t\t\t\t\t\t\t\t{self.canClimbOn.__len__()}\t\t{self.climbingOn.__len__()}')
            self.accelerateHoriz(horiz*8/self.mass/(1+self.ducking),[sum([i[0] for i in self.frictionObjs])/self.frictionObjs.__len__(),sum([i[1] for i in self.frictionObjs])/self.frictionObjs.__len__()])
            self.frictionObjs=[]
            if(vert):
                self.jump()
            self.wasDucking=self.ducking
            if(collideobjs[1]==[]):
                if(self.onGround):
                    self.ducking=1
                else:
                    self.ducking=0
            else:
                self.ducking=0
            self.duckingChecks(collideobjs[0])
            #self.applyVelocity()
            if(self.onGround):
                if self.reloadTime<=0:
                    self.shotsleft=min(self.shotsleft+1,self.attributes['barrels'])
                    self.reloadTime=0
                self.reloadTime-=1
            elif(self.canClimb not in [0,[]])&(self.isClimbing):
                if self.reloadTime<=0:
                    self.shotsleft=min(self.shotsleft+1,self.attributes['barrels'])
                    self.reloadTime=0
                self.reloadTime-=0.5
            if(fire[0])&(self.firecooldown<=0):
                self.fire()
            if(fire[1])&(self.firecooldown<=0):
                self.fireb(0)
            if(fire[2])&(self.firecooldown<=0):
                self.fireb(1)
                        
            self.frictionObjs+=self.collideAndMove(collideobjs[0],collideobjs[1],True)
            self.updateFrame()
        def updateb_2(self,collideobjs,horiz,vert,fire,down=0,climbtoggle=0):
            self.frictionObjs+=self.collideAndMove(collideobjs[0],collideobjs[1],False)
            if self.frictionObjs==[]:
                self.frictionObjs=[[0,0]]
            self.applyGravity(down,[sum([i[0] for i in self.frictionObjs])/self.frictionObjs.__len__(),sum([i[1] for i in self.frictionObjs])/self.frictionObjs.__len__()])
            self.friction=0.59*self.onGround+0.01
            if self.isClimbing!=0:
                self.friction=0.6
            self.applyFriction(self.friction,[sum([i[0] for i in self.frictionObjs])/self.frictionObjs.__len__(),sum([i[1] for i in self.frictionObjs])/self.frictionObjs.__len__()])

            self.getRoomShadows(collideobjs[4])
            
            self.firecooldown-=1
            self.updateRooms(collideobjs)
            self.takeDamages(collideobjs[6])
            self.updateFrame()
            self.updateSafePoint(collideobjs[5],collideobjs[4])
            self.fixNoRooms(collideobjs)
            self.immunityFramesVisuals()
            if(type(self.isClimbing)==type([1,2])):
                self.isClimbing=self.isClimbing.__len__()
            if climbtoggle:
                #print('\t\t\t\t\t'+['unclimb' if self.isClimbing else 'climb'][0])
                if self.isClimbing==0:
                    self.isClimbing=60*self.canClimb
                    self.climbingOn=[i for i in self.canClimbOn]
                else:
                    self.isClimbing=0
            if self.canClimb==0:
                if self.isClimbing>0:
                    self.isClimbing-=1
                    #print('\t\t\t\t\t fail climb',self.isClimbing)
            else:
                if(type(self.isClimbing)==type([1,2])):
                    self.isClimbing=self.isClimbing.__len__()
                if self.isClimbing>0:
                    self.isClimbing=60
                    #print('\t\t\t\ttryb')
                    if self.climbingOn.__len__()<=2:
                        self.climbingOn=[i for i in self.canClimbOn]
            if self.isClimbing<=0:
                self.climbingOn=[]
            else:
                self.climbingOn=[i for i in self.climbingOn if i in self.canClimbOn]
                if self.climbingOn==[]:
                    self.isClimbing=0
            global FRAMERATE
            if self.isClimbing==60:
                if (self.velocity[0]**2+self.velocity[1]**2)>200:
                    FRAMERATE=FRAMERATE2*16
                    #print('time 16')
                elif (self.velocity[0]**2+self.velocity[1]**2)>100:
                    FRAMERATE=FRAMERATE2*9
                    #print('time 9')
                elif (self.velocity[0]**2+self.velocity[1]**2)>50:
                    FRAMERATE=FRAMERATE2*4
                    #print('time 4')
                else:
                    FRAMERATE=FRAMERATE2
                    #print('time 1')
            else:
                
                if (self.velocity[0]**2+self.velocity[1]**2)>1600:
                    FRAMERATE=FRAMERATE2*9
                    #print('time 9')
                elif (self.velocity[0]**2+self.velocity[1]**2)>900:
                    FRAMERATE=FRAMERATE2*4
                    #print('time 4')
                elif (self.velocity[0]**2+self.velocity[1]**2)>400:
                    FRAMERATE=FRAMERATE2*2
                    #print('time 2')
                else:
                    FRAMERATE=FRAMERATE2
                    #print('time 1')
            FRAMERATE=FRAMERATE2*1.5
            
        def fire(self):
            global newObjects
            atktype=0
            atkspd=1
            if(self.shotsleft!=0):
                pos1=pg.mouse.get_pos()
                pos1=[pos1[0]-glfwApi.getWindowSize()[0]/2,pos1[1]-glfwApi.getWindowSize()[1]/2]
                x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)#+random.random()/10-1/20
                y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)#+random.random()/10-1/20
                #newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
                if atktype==0:
                    newObjects.append([0,[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*20,y*20],0,[5,5],1000,0.1,0,False])
                else:
                    for i in range(-2,3):
                        spd=random.random()*3+7
                        theta=i*3.14159*2/50+0.1*(random.random()-0.5)
                        xb=x*math.cos(theta)+y*math.sin(-theta)
                        yb=-x*math.sin(-theta)+y*math.cos(theta)
                        newObjects.append([0,[self.pos[0]+self.width/2+xb*spd,self.pos[1]+self.height/2+yb*spd],[xb*spd,yb*spd],0,[5,5],1000,0.1,0,False])
                self.firecooldown=10*FRAMERATE/60*1/atkspd#(min((self.lastShots[1]-self.lastShots[0])*60/FRAMERATE*53,20))*FRAMERATE/60#10 when not lazer
                self.lastShots=[self.lastShots[1],time.time()]
                #self.velocity[0]*=(1-(x**2)**0.5*(self.firecooldown/FRAMERATE*60)/20)
                #self.velocity[1]*=(1-(y**2)**0.5*(self.firecooldown/FRAMERATE*60)/20)
                self.velocity[0]-=x*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*60/FRAMERATE
                self.velocity[1]-=y*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*60/FRAMERATE
                self.shotsleft-=1
                for i in self.climbingOn:
                    i.velocity[0]-=x*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*1.1
                    i.velocity[1]-=y*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*1.1
        def fireb(self,pull):
            global newObjects
            if(self.shotsleft!=0):
                pos1=pg.mouse.get_pos()
                pos1=[pos1[0]-glfwApi.getWindowSize()[0]/2,pos1[1]-glfwApi.getWindowSize()[1]/2]
                x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)#+random.random()/10-1/20
                y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)#+random.random()/10-1/20
                #newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
                newObjects.append([0,[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*20,y*20],0,[5,5],1000,0.1,0,pull])
                self.firecooldown=1*FRAMERATE/60#(min((self.lastShots[1]-self.lastShots[0])*60/FRAMERATE*53,20))*FRAMERATE/60#10 when not lazer
                self.lastShots=[self.lastShots[1],time.time()]
                self.velocity[0]-=x*self.firecooldown/2/(self.climbingOn.__len__()/20+1)
                self.velocity[1]-=y*self.firecooldown/2/(self.climbingOn.__len__()/20+1)
                self.shotsleft-=0.1
                for i in self.climbingOn:
                    i.velocity[0]-=x*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*1.1
                    i.velocity[1]-=y*self.firecooldown/2/(self.climbingOn.__len__()/20+1)*1.1

                
        def updateSafePoint(self,objs,rooms):
            for obj in objs:
                if type(obj)==SaveMarker:
                    if(isColliding((self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height),(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height))):
                        self.savePos=[obj.pos[0]+30-self.width/2,obj.pos[1]+40-self.height]
                        for i in rooms:
                            if i.id==obj.roomid:
                                self.anticorruptroomandpos=(i.type,i.pos)
        def takeDamages(self,bullets):
            if(self.ducking):
                self.pos[1]+=15
                self.height-=15
            if(self.immunityFrames<=0):
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in bullets:
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(playerpos,objpos)):
                        self.attributes['health']-=1
                        self.velocity[0]=-self.facing*5
                        self.velocity[1]=-10
                        obj.kill()
                        self.immunityFrames=10
            if(self.ducking):
                self.pos[1]-=15
                self.height+=15
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    class Enemeh(pg.sprite.Sprite):
        speed = 10
        textureIdsAll: List[List[int]] = []
        mass=2
        width=20
        height=35
        gravity=[0,1]
        def __init__(self,x,y, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.facing = -1
            self.velocity=[0,0]
            self.pos=[x,y]
            self.onGround=0
            self.attributes={'barrels':2,'health':2,'maxhealth':2,'stepsize':10}
            self.animationFrame=0
            self.savePos=self.pos
            self.anticorruptroomandpos=(0,[0,-50])
            self.immunityFrames=0
            self.friction=0.1
            self.textureIds: List[int] = self.textureIdsAll[0]
            self.imgid=self.textureIds[0]
            self.imgidy=None
            self.firecooldown=0
            self.shotsleft=0
            self.wasOnGround=0
            self.aggro=0
            self.aiData=[0,0]
            self.attackFrame=0
            self.isAttacking=0
        def move(self, direction):
            if direction:
                self.facing = direction
            #self.rect.move_ip(direction * self.speed, 0)
            if direction < 0:
                self.image = self.images[0]
            elif direction > 0:
                self.image = self.images[1]
            self.rect = self.image.get_rect()
        def updatec(self,collideobjs,player):
            move=0
            jump=0
            if(self.isAttacking==0):
                if self.aggro:
                    if(player.pos[0]<self.pos[0]-50*(self.facing==-1)):
                        move=-.5
                    elif(player.pos[0]>self.pos[0]+50*(self.facing==1)):
                        move=0.5
                    else:
                        self.isAttacking=1
                        self.attackFrame=0
                    if(self.velocity[0]==0):
                        jump=1-(not not move)
                    if(self.isAttacking):
                        jump=0
                else:
                    if(self.aiData[0]<0):
                        self.aiData[0]+=1
                        move=0.25
                    elif(self.aiData[0]>0):
                        self.aiData[0]-=1
                        if(self.aiData[1]==0):
                            move=-0.25
                    else:
                        if(self.aiData[1]==1):
                            self.aiData[0]=90
                            self.aiData[1]=0
                        elif(self.aiData[1]==0):
                            self.aiData[0]=-90
                            self.aiData[1]=1
                    if((player.pos[0]-self.pos[0])**2+(player.pos[1]-self.pos[1])**2)<120**2:
                        self.aggro=1
            self.updateb(collideobjs,move,jump,0)
            if(self.isAttacking):
                #newParticles.append([[self.pos[0]+self.width/2+math.cos(2-(self.attackFrame/30)**2/2)*self.facing*10-10,self.pos[1]+self.height/2-10-math.sin(2-(self.attackFrame/30)**2/2)*10],[0,0],[0,0],0,[20,20],2,0,0])
                for i in range(6):
                    newParticles.append([[self.pos[0]+self.width/2+math.cos(2-(self.attackFrame/20)**2/2)*self.facing*(10-i)*4-i*1,self.pos[1]+self.height/2-i*1-math.sin(2-(self.attackFrame/20)**2/2)*(10-i)*4],[0,0],[0,0],0,[i*2,i*2],2,0,0])
                self.attackFrame+=1
                if(self.attackFrame>40):
                    self.isAttacking=0
                    newObjects.append([1,self.pos[0]+self.width/2+self.facing*25-10,self.pos[1]+self.height/2,20,1,0])
        #self.rect.top = self.origtop# - (self.rect.left // self.bounce % 2)
        def accelerateHoriz(self,amount):
            self.animationFrame+=0.1
            if(self.animationFrame>=4):
                self.animationFrame=0
            self.velocity[0]+=(self.friction*2)*amount/self.mass
            if self.onGround:
                if self.velocity[0] < 0:
                    self.image = self.images[int(self.animationFrame)]
                    self.imgid = self.textureIds[int(self.animationFrame)]
                    self.facing=-1
                elif self.velocity[0] > 0:
                    self.image = self.images[5+int(self.animationFrame)]
                    self.imgid = self.textureIds[5+int(self.animationFrame)]
                    self.facing=1
            else:
                if self.velocity[0] < 0:
                    self.image = self.images[4+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[4+int(self.animationFrame/4)]
                    self.facing=-1
                elif self.velocity[0] > 0:
                    self.image = self.images[9+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[9+int(self.animationFrame/4)]
                    self.facing=1
            #self.rect = self.image.get_rect()
        def applyFriction(self,amount):
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*(60/FRAMERATE)**0.5
            self.velocity[1]+=self.gravity[1]*(60/FRAMERATE)**0.5
        def applyVelocity(self):
            self.pos[0]+=self.velocity[0]
            self.pos[1]+=self.velocity[1]
        def jump(self):
            if(self.onGround):
                self.velocity[1]=-13
        def collideAndMove(self,objs,platformobjs=[]):
            objs2=[]
            self.rect.left-=self.rect.size[0]*10
            self.rect.top-=self.rect.size[1]*10
            size1=self.rect.size
            self.rect.size=(self.rect.size[0]*19,self.rect.size[1]*19)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
            resetVelocity=[0,0]
            hazardCollision=0
            sendBack=0
            self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            if(self.velocity[1]<0):
                playerpos=(self.pos[0],self.pos[1]+self.attributes['stepsize'],self.pos[0]+self.width,self.pos[1]+self.height)
            if(self.onGround):
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height-self.attributes['stepsize'])
            
            
            farthestDownRoofPosition=-10000000000000000000000000000000000
            for obj in objs:    
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(objpos,playerpos)):
            
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                    if(self.velocity[0]<0):
                        self.pos[0]=max(objpos[2],self.pos[0])
                        resetVelocity[0]=1
                    elif(self.velocity[0]>0):
                        self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                        resetVelocity[0]=1
                    if(type(obj)==Hazard):
                        hazardCollision=obj.damage
                        sendBack=obj.sendBack
            if(resetVelocity[0]):
                self.velocity[0]=0
            canStandOnObjs=[]
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in platformobjs:
                objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
                if(isColliding(objpos,playerpos)):
                    canStandOnObjs.append(obj)
            
            wasOnGround=self.onGround
            self.onGround=0
            leftStairsPos=-100
            self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in objs:
                
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                objposb=(obj.pos[0],obj.pos[1]-self.attributes['stepsize'],obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.attributes['stepsize'])
                if(isColliding(objpos,playerpos)):
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                    if(self.velocity[1]<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                        farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
                        self.pos[1]=farthestDownRoofPosition+1
                        resetVelocity[1]=1
                    elif(self.velocity[1]>0)|((self.velocity[1]==0)&(self.onGround)):
                        self.onGround=1
                        self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                        resetVelocity[1]=1
                    if(type(obj)==Hazard):
                        hazardCollision=obj.damage
                        sendBack=obj.sendBack
                if(wasOnGround):
                    if not self.onGround:
                        if obj.width==2:
                            if(isColliding(objposb,playerpos)):
                                if self.velocity[0]>0:
                                    self.onGround=1
                                    self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                    self.velocity[1]=0
                                elif self.velocity[0]<0:
                                    self.onGround=1
                                    self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                    self.velocity[1]=0
            if(resetVelocity[1]):
                self.velocity[1]=0
            for obj in canStandOnObjs:
                
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(objpos,playerpos)):
                    
                    if(self.velocity[1]<0):
                        self.pos[1]=objpos[3]
                        resetVelocity[1]=1
                    else:
                        self.onGround=1
                        self.pos[1]=objpos[1]-self.height
                        resetVelocity[1]=1
                    if(type(obj)==Hazard):
                        hazardCollision=obj.damage
                        sendBack=obj.sendBack
            if self.immunityFrames==-1:
                if(hazardCollision!=0):
                    self.immunityFrames=90
                    self.attributes['health']-=hazardCollision
                    for i in range(42):
                        newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2,1,120])
                    if(sendBack):
                        self.velocity=[0,0]
                        self.pos=self.savePos
                    
            if(resetVelocity[1]):
                self.velocity[1]=0
            #    if pg.mixer and boom_sound is not None:
            #        boom_sound.play()
            #    Explosion(alien, all)
            #    Explosion(player, all)
            #    SCORE = SCORE + 1
            #    player.kill()
        def updateFrame(self):
            self.prevRect=self.rect
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            if(self.attributes['health']<=0):
                self.kill()
        #def gunpos(self):
        #    pos = self.facing * self.gun_offset + self.rect.centerx
        #    return pos, self.rect.top
        def immunityFramesVisuals(self):
            if(self.immunityFrames>-1):
                if(self.immunityFrames%30>=15):
                    if(self.imgid!=None):
                        self.imgidy=self.imgid+1-1
                        self.imgid=None
                    
                elif(self.immunityFrames%30>=0):
                    if(self.imgid==None):
                        self.imgid=self.imgidy+1-1
                        self.imgidy=None
                self.immunityFrames-=1
            if(self.immunityFrames==0):
                for i in self.images:
                    i.set_alpha(255)
        def updateb(self,collideobjs,horiz,vert,fire):
            self.accelerateHoriz(horiz*5/self.mass)
            if(vert):
                self.jump()
            #self.applyVelocity()
            if(self.onGround):
                self.shotsleft=self.attributes['barrels']
                self.firecooldown-=1
            if(fire)&(self.firecooldown<=0):
                self.fire()
            
            self.collideAndMove(collideobjs[0],collideobjs[1])
            self.applyGravity()
            self.friction=0.5*self.onGround+0.1
            self.applyFriction(self.friction)
            self.takeDamages(collideobjs[6])
            self.firecooldown-=1
            self.updateFrame()
            self.immunityFramesVisuals()
        def takeDamages(self,bullets):
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in bullets:
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(playerpos,objpos)):
                    self.aggro=1
                    self.attributes['health']-=obj.damage
                    self.velocity[0]+=obj.velocity[0]*obj.damage
                    self.velocity[1]+=obj.velocity[1]*obj.damage
                    obj.kill()
                    for i in range(int(40*obj.damage)):
                        b=5-random.random()*20+15
                        newParticles.append([[self.pos[0]+self.width/2-obj.velocity[0],self.pos[1]+self.height/2-obj.velocity[1]],[-obj.velocity[0]/(3+random.random())+4*random.random()-2,-obj.velocity[1]/(3+random.random())+4*random.random()-2],[0,1],0,[b,b],500+100*random.random(),0.1+0.1*random.random(),2,1,120])
                
        def fire(self):
            if(self.shotsleft!=0):
                pos1=pg.mouse.get_pos()
                pos1=[pos1[0]-glfwApi.getWindowSize()[0]/2,pos1[1]-glfwApi.getWindowSize()[1]/2]
                x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)
                y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)
                newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
                self.firecooldown=10*FRAMERATE/60
                self.velocity[0]/=(1+(x**2)**0.5)
                self.velocity[1]/=5
                self.velocity[0]-=x*20
                self.velocity[1]-=y*20
                self.shotsleft-=1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    class PhysicsParticle(pg.sprite.Sprite):
        speed = 10
        images: List[List[pg.Surface]] = []
        textureIds: List[List[int]] = []
        mass=2
        def __init__(self,pos,velocity,gravity,particle,size,life,spin,shouldBounce,shouldStick,fadeType=1,fadeDuration=120, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            #for i in range(self.images.__len__()):
            #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[particle][0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.rect.size=size
            self.velocity=velocity
            self.gravity=gravity
            self.width=size[0]
            self.height=size[1]
            self.spin=spin
            self.shouldBounce=shouldBounce
            self.shouldStick=shouldStick
            self.pos=pos
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[particle][0]
            self.particle=particle
            self.imgidy=None
            self.life=life
            self.stuck=0
            self.rotation=0
            self.fadeFrame=0
            self.fadeType=fadeType
            self.fadeDuration=fadeDuration
        def applyFriction(self,amount):
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*60/FRAMERATE
            self.velocity[1]+=self.gravity[1]*60/FRAMERATE
        def collideAndMove(self,objs):
            resetVelocity=[0,0]
            hazardCollision=0
            sendBack=0
            self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            self.rect.size=[self.rect.size[0]+((self.velocity[0]*1.5*60/FRAMERATE)**2)**0.5,self.rect.size[1]]
            for obj in pg.sprite.spritecollide(self,objs,0):
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(self.velocity[0]<0):
                        self.pos[0]=max(objpos[2],self.pos[0])
                        resetVelocity[0]=1
                    elif(self.velocity[0]>0):
                        self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                        resetVelocity[0]=1
            if(resetVelocity[0]):
                if(self.shouldStick):
                    self.stuck=1
                    if(self.velocity[0]>0):
                        self.pos[0]+=self.width
                    else:
                        self.pos[0]-=self.width
                self.velocity[0]=0
            self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            self.onGround=0
            self.updateFrame()
            self.rect.size=[self.width,self.rect.size[1]+((self.velocity[1]*1.5*60/FRAMERATE)**2)**0.5]
            for obj in pg.sprite.spritecollide(self,objs,0):
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(self.velocity[1]<0):
                        self.pos[1]=max(objpos[3],self.pos[1])
                        resetVelocity[1]=1
                    elif(self.velocity[1]>0):
                        self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                        resetVelocity[1]=1
                        self.onGround=1
            if(resetVelocity[1]):
                if(self.shouldStick):
                    
                    if(self.velocity[1]>0):
                        self.pos[1]+=self.height
                    else:
                        self.pos[1]-=self.height
                    self.stuck=1
                
                if(self.shouldBounce):
                    self.velocity[1]=-self.velocity[1]/2
                else:
                    self.velocity[1]=0
            self.rect.size=[self.width,self.height]
            if(type(self.spin) in [float,int]):
                self.rotation+=self.spin*(60/FRAMERATE)
            #    if pg.mixer and boom_sound is not None:
            #        boom_sound.play()
            #    Explosion(alien, all)
            #    Explosion(player, all)
            #    SCORE = SCORE + 1
            #    player.kill()
        def updateFrame(self):
            self.prevRect=self.rect
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
        def updateb(self,collideobjs):
            self.life-=(3-self.stuck*2)/3
            if(self.life<=0):
                self.kill()
            else:
                if(self.stuck==0):
                    self.collideAndMove(collideobjs[0])
                    self.applyGravity()
                    self.friction=0.5*self.onGround+0.1
                    self.applyFriction(self.friction)
                self.updateFrame()
                if(self.stuck):
                    self.velocity=[0,0]
                    if(self.fadeType==1):
                        self.fadeFrame+=self.fadeDuration*60/FRAMERATE/(self.textureIds[self.particle].__len__())
                        if(self.fadeFrame>self.textureIds[self.particle].__len__()):
                            self.kill()
                        else:
                            self.imgid=self.textureIds[self.particle][int(self.fadeFrame)]





















    class Particle(pg.sprite.Sprite):
        speed = 10
        images: List[List[pg.Surface]] = []
        textureIds: List[List[int]] = []
        mass=2
        def __init__(self,pos,velocity,gravity,particle,size,life,spin,shouldBounce,shouldStick,fadeType=1,fadeDuration=120, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            #for i in range(self.images.__len__()):
            #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[particle][0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.rect.size=size
            self.velocity=velocity
            self.gravity=gravity
            self.width=size[0]
            self.height=size[1]
            self.spin=spin
            self.shouldBounce=shouldBounce
            self.shouldStick=shouldStick
            self.pos=pos
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[particle][0]
            self.particle=particle
            self.imgidy=None
            self.life=life
            self.stuck=0
            self.rotation=0
            self.fadeFrame=0
            self.fadeType=fadeType
            self.fadeDuration=fadeDuration
        def applyFriction(self,amount):
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*60/FRAMERATE
            self.velocity[1]+=self.gravity[1]*60/FRAMERATE
        
        def updateFrame(self):
            self.prevRect=self.rect
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
        def updateb(self,collideobjs):
            self.life-=1
            if(self.life<=0):
                self.kill()
            else:
                #if(self.motionType==0):
                self.updateFrame()
                #self.imgid=self.textureIds[self.particle][int(self.fadeFrame)]
































    class ChainObject(pg.sprite.Sprite):
        len=10
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        #lightLevel=30
        def __init__(self,pos,velocity,particle,size,life,spin,rotation, *groups):
            pg.sprite.Sprite.__init__(self, *groups)









    
    
    
    
    class LaPew(pg.sprite.Sprite):
        speed = 10
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        #lightLevel=30
        def __init__(self,pos,velocity,particle,size,life,spin,rotation,pull, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            #for i in range(self.images.__len__()):
            #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[particle],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.rect.size=size
            self.velocity=velocity
            self.gravity=[0,0]
            self.width=size[0]
            self.height=size[1]
            self.spin=spin
            self.pos=pos
            self.onGround=0
            self.friction=0
            self.imgid=self.textureIds[particle]
            self.imgidy=None
            self.life=life
            self.stuck=0
            self.rotation=rotation
            self.type=2
            self.damage=2
            self.lightLevel=3;
            self.pull=pull;
            self.updateFrame()
            self.prevRect.left=self.rect.left
            self.prevRect.top=self.rect.top
            self.prevRect.size=self.rect.size
        def applyFriction(self,amount):
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*60/FRAMERATE
            self.velocity[1]+=self.gravity[1]*60/FRAMERATE
        def collideAndMove(self,objs):
            objs2=[]
            self.rect.left-=5*20
            self.rect.top-=5*20
            size1=self.rect.size
            self.rect.size=(10*20,10*20)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
            self.rect.left+=5*20
            self.rect.top+=5*20
            resetVelocity=[0,0]
            hazardCollision=0
            sendBack=0
            self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
            playerpos=collisionUnion(
                (self.pos[0]-self.velocity[0]*1.5*60/FRAMERATE,self.pos[1],self.pos[0]+self.width-self.velocity[0]*1.5*60/FRAMERATE,self.pos[1]+self.height),
                (self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            )
            self.rect.size=[self.rect.size[0]+((self.velocity[0]*1.5*60/FRAMERATE)**2)**0.5,self.rect.size[1]]
            for obj in pg.sprite.spritecollide(self,objs,0):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(objpos,playerpos)):
                    if(self.velocity[0]<0):
                        if self.type not in [2]:
                            self.pos[0]=max(objpos[2],self.pos[0])
                        resetVelocity[0]=1
                    elif(self.velocity[0]>0):
                        if self.type not in [2]:
                            self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                        resetVelocity[0]=1
            if(resetVelocity[0]):
                if self.type in [0,1]:
                    if self.damage>1:
                        if self.type==0:
                            self.damage-=1
                            self.height-=1
                        self.velocity[0]*=-1
                        #self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
                    else:
                        self.kill()
                        return
                else:
                    if self.type in [2]:
                        self.stuck=1
                    else:
                        self.kill()
                        return
            self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
            playerpos=collisionUnion(
                (self.pos[0],self.pos[1]-self.velocity[1]*1.5*60/FRAMERATE,self.pos[0]+self.width,self.pos[1]+self.height-self.velocity[1]*1.5*60/FRAMERATE),
                (self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            )
            self.onGround=0
            self.updateFrame()
            self.rect.size=[self.width,self.rect.size[1]+((self.velocity[1]*1.5*60/FRAMERATE)**2)**0.5]
            for obj in pg.sprite.spritecollide(self,objs,0):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(objpos,playerpos)):
                    if(self.velocity[1]<0):
                        if self.type not in [2]:
                            self.pos[1]=max(objpos[3],self.pos[1])
                        resetVelocity[1]=1
                    elif(self.velocity[1]>0):
                        if self.type not in [2]:
                            self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                        resetVelocity[1]=1
                        self.onGround=1
            if(resetVelocity[1]):
                if self.type in [0,1]:
                    if self.damage>1:
                        if self.type==0:
                            self.damage-=1
                            self.height-=1
                        self.velocity[1]*=-1
                        #self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
                    else:
                        self.kill()
                else:
                    if self.type in [2]:
                        self.stuck=1
                    else:
                        self.kill()
            self.rect.size=[self.width,self.height]
            if(type(self.spin) in [float,int]):
                self.rotation+=self.spin*(60/FRAMERATE)
            #    if pg.mixer and boom_sound is not None:
            #        boom_sound.play()
            #    Explosion(alien, all)
            #    Explosion(player, all)
            #    SCORE = SCORE + 1
            #    player.kill()
        def updateFrame(self):
            global player
            self.rotation=math.atan2(self.velocity[0],self.velocity[1])+math.pi/2
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            self.rect.size=[self.width*(math.sqrt(self.velocity[1]**2+self.velocity[0]**2+1))*0.5,self.height]
            if((self.rect.left-player.rect.left)<-2000)|((self.rect.left-player.rect.left)>3000)|((self.rect.top-player.rect.top)<-2000)|((self.rect.top-player.rect.top)>3000):
                self.kill()
        def updateb(self,collideobjs):
            self.prevRect.left=self.rect.left
            self.prevRect.top=self.rect.top
            self.prevRect.size=self.rect.size
            self.life-=(3-self.stuck*2)/3
            if(self.life<=0):
                self.kill()
            else:
                if self.stuck==1:
                    if self.type in [2]:
                        self.kill()
                if(self.stuck==0):
                    self.collideAndMove(collideobjs[0])
                    self.applyGravity()
                    self.friction=0.5*self.onGround+0.1
                    self.applyFriction(self.friction)
                self.updateFrame()
                if(self.stuck):
                    
                    self.velocity=[0,0]
        
    class GenericSingleFrameAttack(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,w,h,v,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.image = pg.transform.scale(self.images[v], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=[x,y]
            self.width=w
            self.height=h
            self.imgid=self.textureIds[v]
            self.rect.size=[w,h]
            self.life=3
        def update(self):
            self.rect = self.rect.clamp(SCREENRECT)
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            self.life-=1
            if(self.life<=0):
                self.kill()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    class Wall(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        velocity=[0,0]
        def __init__(self,x,y,w,h,v,rid,*groups):
            
            pg.sprite.Sprite.__init__(self, *groups)
            self.image = pg.transform.scale(self.images[v], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=[x,y]
            self.width=w
            self.height=h
            self.roomid=rid
            self.imgid=self.textureIds[v]
            self.rect.size=[[w,h] if v in [0,6] else [20,20]][0]
            self.depth=0
            self.shouldRender=True
            self.lightLevel=[-7 if v in [0,2,3,4,5] else 0][0]
            self.prevRect=self.rect
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
                self.prevRect=self.rect
    
    class CursorVisual(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,w,h,v,*groups):
            
            pg.sprite.Sprite.__init__(self, *groups)
            self.image = self.images[v]
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=[x,y]
            self.width=w
            self.height=h
            self.imgid=self.textureIds[v]
            self.rect.size=[w,h]
            self.depth=0
        def update(self):
            if 'rect' in self.__dict__:
                global scrwidth,scrheight
                left=(pg.mouse.get_pos()[0])*640/scrwidth*2-self.width/3*2#+16+8
                top=(pg.mouse.get_pos()[1])*640/scrheight-self.height/3*2#-8
                matrix=glfwApi.getMatrix()
                #left=left/20-8*3/2
                #top=top/20-4.08510638*3
                #left-=15/2/2
                #left*=matrix[2]
                #left*=2
                #left+=matrix[0]
                #top*=-1
                #top+=8
                #top*=matrix[3]
                #top+=matrix[1]
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=left
                self.rect.top=top
                
    
    class Hazard(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        velocity=[0,0]
        def __init__(self,x,y,w,h,rid,imgid,*groups):
            
            pg.sprite.Sprite.__init__(self, *groups)
            self.image = pg.transform.scale(self.images[imgid], (w,h))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=[x,y]
            self.width=w
            self.height=h
            self.roomid=rid
            self.damage=1
            self.sendBack=1
            self.depth=0
            self.imgid=self.textureIds[imgid]
            self.rect.size=[self.width,self.height]
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    
    class RoomBoundary(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,id,rid,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.pos=[x,y]
            self.image = pg.transform.scale(self.images[0], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.width=20
            self.height=20
            self.renderOff=[20,20]
            self.boundaryId=id
            self.disabled=0
            self.roomid=rid
            #self.imgid=self.textureIds[0]
            self.rect.size=[self.width,self.height]
            self.depth=0
        def triggerBuildRoom(self,*groups):
            if(self.disabled==0):
                x=getRoomToBuildFromBoundaryId(self.boundaryId,self.pos)
                print(self.boundaryId)
                if(x!=None):
                    if not (x[0].isalpha()):
                        rooms[int(x[0])].buildRoom([x[1],x[2]],groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
                    else:
                        rooms[(x[0])].buildRoom([x[1],x[2]],groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
                    pos=(self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height)
                    for i in groups[3]:
                        pos2=(i.pos[0],i.pos[1],i.pos[0]+i.height,i.pos[1]+i.height)
                        if(isColliding(pos,pos2)):
                            i.disabled=1
                    self.disabled=1
                else:
                    print('Missing Link!')
                    self.kill()
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    
    class SaveMarker(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        lightLevel=1
        def __init__(self,x,y,rid,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.pos=[x-20,y-20] 
            self.depth=0
            self.image = pg.transform.scale(self.images[0], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.width=60
            self.height=60
            self.roomid=rid
            self.imgid=self.textureIds[0]
            self.rect.size=[20,20]
            
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0]+20)*CAMERA_SCALE
                self.rect.top=(self.pos[1]+20)*CAMERA_SCALE
    
    
    class barPart(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,imageids,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.image=pg.transform.scale(self.images[imageids[0]],(10,10))
            self.rect=self.image.get_rect()
            self.pos=[x,y]
            self.state=0
            self.stateVals=imageids
            self.rect.left=self.pos[0]
            self.rect.top=self.pos[1]
            self.imgid=self.textureIds[self.stateVals[0]]
        def setstate(self,state):
            self.rect.left=self.pos[0]
            self.rect.top=self.pos[1]
            self.state=state
            self.imgid=self.textureIds[self.stateVals[state]]
        def update(self):
            if 'rect' in self.__dict__:
                self.rect.left=(self.pos[0]-0*CAMERA_POS[0])
                self.rect.top=(self.pos[1]-0*CAMERA_POS[1])
    
    class Bar(pg.sprite.Sprite):
        def __init__(self,x,y,imgs,imgsalterego,w,v,m,sproff,renderGroup,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.pos=[x,y]
            self.images: List[pg.Surface] = imgs
            self.imagesalterego: List[int] = imgsalterego
            self.width=w
            self.value=-100
            self.maxValue=m
            self.bgObjects=[]
            self.fgObjects=[]
            self.spriteOffset=sproff
            self.scale=CAMERA_SCALE
            if(barPart.images.__len__()<sproff+1):
                for i in imgs:
                    barPart.images.append(i)
                for i in imgsalterego:
                    barPart.textureIds.append(i)
            for i in range(self.width):
                if(i==0):
                    self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff],renderGroup))
                    renderGroup.change_layer(self.bgObjects[-1],30)
                elif(i<(self.width-1)):
                    self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+1],renderGroup))
                    renderGroup.change_layer(self.bgObjects[-1],30)
                else:
                    self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+2],renderGroup))
                    renderGroup.change_layer(self.bgObjects[-1],30)
            
            for i in range(self.width):
                if(i==0):
                    self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+3,sproff+4,sproff+5],renderGroup))
                    renderGroup.change_layer(self.fgObjects[-1],31)
                elif(i<(self.width-1)):
                    self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+6,sproff+7,sproff+8],renderGroup))
                    renderGroup.change_layer(self.fgObjects[-1],31)
                else:
                    self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+9,sproff+10,sproff+11],renderGroup))
                    renderGroup.change_layer(self.fgObjects[-1],31)
            self.updateV(v)
        def updateV(self,value):
            numObjsOld=self.value/self.maxValue*self.width
            numObjsNew=value/self.maxValue*self.width
            if(numObjsOld!=numObjsNew):
                if(int(numObjsNew)==1):
                    self.fgObjects[0].setstate(2)
                    for i in range(1,self.width):
                        self.fgObjects[i].setstate(0)
                else:
                    for i in range(-int(-numObjsNew),self.width):
                        self.fgObjects[i].setstate(0)
                    for i in range(0,-int(-numObjsNew)):
                        self.fgObjects[i].setstate(1)
                    if(i!=0):
                        self.fgObjects[-int(-numObjsNew)-1].setstate(2)
    class Background(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.image=pg.transform.scale(self.images[0],(3000,2000))
            self.rect=self.image.get_rect()
            self.imgid=self.textureIds[0]
        def update(self):
            global player
            self.rect.left=player.rect.left-1500
            self.rect.top=player.rect.top-1000
    
    def getRoomToBuildFromBoundaryId(boundary,roomOffset):
        if(boundary[1])==None:
            return None
        else:
            value0=boundary[0].split('_')
            value0=(int(value0[0]),int(value0[1]))
            value1=boundary[1]
            value2=[]
            value2.append(value1[0:value1.index('_')])
            value1=value1[value1.index('_')+1:]
            value2.append(value1[0:value1.index('_')])
            value1=value1[value1.index('_')+1:]
            value2.append(value1)
            value3=(value2[0],int(value2[1]),int(value2[2]))
            return (value3[0],roomOffset[0]-20*value3[1],roomOffset[1]-20*value3[2])
    roomsBuilt=0
    class BuiltRoom(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,w,h,id,type,sources,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.width=w
            self.height=h
            self.pos=[x,y]
            self.id=id
            self.type=type
            self.image=pg.transform.scale(self.images[0],(w*CAMERA_SCALE,h*CAMERA_SCALE))
            self.shadowLevel=None
            self.rect=self.image.get_rect()
            self.setImages(sources)
            self.rect.size=[self.width,self.height]
            #self.imgid=loadTexture(surface_array(self.image))
        def unbuildRoom(self,allgroup,boundaryGroup):
            for i in allgroup:
                if type(i) in [Wall,Hazard,RoomBoundary,SaveMarker,CollisionGroup]:
                    if i.roomid==self.id:
                        i.kill()
            for i in boundaryGroup:
                if (type(i)==RoomBoundary):
                    if i.roomid==self.id:
                        i.kill()
            for i in boundaryGroup:
                if(type(i)==RoomBoundary):
                    if i.disabled==1:
                        shouldKeepDisabled=0
                        for j in allgroup:
                            if(type(j)==RoomBoundary):
                                if(i!=j):
                                    if(isColliding((i.pos[0],i.pos[1],i.pos[0]+i.height,i.pos[1]+i.height),(j.pos[0],j.pos[1],j.pos[0]+j.height,j.pos[1]+j.height))):
                                        shouldKeepDisabled=1
                        if shouldKeepDisabled==0:
                            i.disabled=shouldKeepDisabled
            self.kill()
        def setShadows(self,amount):
            self.shadowLevel=amount
        def setImages(self,allgroup):
            newimage=pg.surface.Surface((self.width,self.height))
            for obj in allgroup.sprites():
                if('roomid' in obj.__dict__):
                    if obj.roomid==self.id:
                        newimage.blit(obj.image,(obj.pos[0]-self.pos[0],obj.pos[1]-self.pos[1]))
            self.image=pg.transform.scale(newimage,(self.width*CAMERA_SCALE,self.height*CAMERA_SCALE))
            self.image.set_colorkey((0,0,0))
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    newParticles=[]
    def isValid_old(data,group,x=0,y=0,w=1,h=1,max=1000):
        if (w>max)|(h>max)|((x+w)>data.__len__())|((y+h)>data[0].__len__()):
            return 0
        totalWidth=data.__len__()
        totalHeight=data[0].__len__()
        l=x
        t=y
        r=min(totalWidth,x+w)
        bot=min(totalHeight,y+h)
        for a in range(l,r):
            for b in range(t,bot):
                if data[a][b]!=group:
                    return 0
                    
        return 1
    def isValid(data,group,x=0,y=0,w=1,h=1,max=1000):
        if (w>max)|(h>max)|((x+w)>data.__len__())|((y+h)>data[0].__len__()):
            return 0
        
        totalWidth=data.__len__()
        totalHeight=data[0].__len__()
        l=x
        t=y
        r=min(totalWidth,x+w)
        bot=min(totalHeight,y+h)
        groupsWith={1:[1,-1],-1:[-1]}
        if group in [i for i in groupsWith]:
            groupsWith=groupsWith[group]
        else:
            groupsWith=[group]
    
    
        d2=[]
        for i in data[l:r]:
            d2.append([])
            for j in i[t:bot]:
                d2[-1].append(j)
        #print(d2)
    
        
        for a in range(r-l):
            for b in range(bot-t):
                v=d2[a][b]
                if v not in groupsWith:
                    #print("No")
                    return 0
                #else:
                #    print(v,groupsWith[groupsWith.index(v)],groupsWith)
        #print("Yes",group,groupsWith)
        return 1
    class Room():
        def __init__(self,data,w,h,id,shadowLevel=None):
            #pg.sprite.Sprite.__init__(self, *groups)
            self.width=w
            self.height=h
            self.id=id
            self.shadowLevel=shadowLevel
            self.data=data
            self.boundaryList=[]
            self.compressedTiles=[]
        def decompressData(self):
            data=self.data
            data2=[]
            if(type(data)==dict):
                palette=data['palette']
                palettelen=palette.__len__()
                palettelen2=1
                while(2**(palettelen2))<palettelen:
                    palettelen2+=1
                data=data['data']
                for i in data:
                    data2.append([])
                    for j in range(self.width):
                        data2[-1].append(palette[fromBinary(i[j*palettelen2:(j+1)*palettelen2])])
            self.data=data2
            for j in range(self.height):
                for i in range(self.width):
                    if(self.data[j][i]==5):
                        self.boundaryList.append([str(i)+"_"+str(j),None])
            #print(self.boundaryList)
            self.compressTiles()
            #print(self.id,self.data)


            dispChars={0:"  ",1:"[]",-1:'()',-2:"##",2:"==",3:"\\_",4:"_/", 7:"/ ",6:" \\",8:"^^",9:"* ",5:"  ",10:' |'}
            dispCharsbg={i:[dispChars[i][0] if dispChars[i][0]!=" " else dispChars[-2][0]][0]+[dispChars[i][1] if dispChars[i][1]!=" " else dispChars[-2][1]][0] for i in dispChars}

            print("Room ",self.id)
            print("Number of objects:",self.compressedTiles.__len__())
            z=[]
            for i in self.data:
                z.append([])
                for j in i:
                    z[-1].append((0,0))
            #for index in range(y2.__len__()-1,-1,-1):
            for index in range(self.compressedTiles.__len__()):
                #print(y2)
                i=self.compressedTiles[index]
                x,y,w,h=i[0],i[1],i[2],i[3]
                t=i[4]
                b=i[5]
                for a in range(w):
                    for b in range(h):
                        z[y+b][x+a]=(t,b)
            print("/-"+"--"*(z[0].__len__()-1)+"-\\")
            for i in z:
                print('|',end="")
                for j in i:
                    if j[1]==False:
                        print(dispChars[j[0]],end="")
                    else:
                        print(dispCharsbg[j[0]],end="")
                print('|')
            print("\\-"+"--"*(z[0].__len__()-1)+"-/")














        def setShadows(self,amount):
            self.shadowLevel=amount







        
        def compressTiles(self,max=10):
            width=self.width
            height=self.height
            decompressedTiles=[[{'width':1,'height':1,'tile':self.data[i][j],'nope':[1 if self.data[i][j] in [0] else 0][0]} for i in range(self.height)] for j in range(self.width)]
            for i in decompressedTiles:
                for j in i:
                    j['group']=j['tile']
                    if j['group']==0:
                        j['nope']=1
            mainmode='TOGGLE'
            currentAction='HORIZ'
            currentSkip='NONE'
            ungroupable=[3,4,5,6,7]
            ungroupable=[0,2,3,4,5,6,7,8,9,10]
            for x523 in range(width):
                for y523 in range(height):
                    if decompressedTiles[x523][y523]['tile'] not in ungroupable:
                        if decompressedTiles[x523][y523]['nope']==0:
                            if decompressedTiles[x523][y523]['width']!=0:
                                #print(decompressedTiles[x523][y523])
                                currentSkip="None"
                                while isValid([[j['group'] for j in i] for i in decompressedTiles],decompressedTiles[x523][y523]['group'],x523,y523,decompressedTiles[x523][y523]['width'],decompressedTiles[x523][y523]['height'],max=max):
                                    currentAction=['VERT','HORIZ'][currentAction=='VERT']
                                    if currentSkip==currentAction:
                                        pass
                                    elif currentAction=='HORIZ':
                                        decompressedTiles[x523][y523]['width']+=1
                                    elif currentAction=='VERT':
                                        decompressedTiles[x523][y523]['height']+=1
                                currentSkip=currentAction
                                if currentAction=='HORIZ':
                                    decompressedTiles[x523][y523]['width']-=1
                                elif currentAction=='VERT':
                                    decompressedTiles[x523][y523]['height']-=1
                                while isValid([[j['group'] for j in i] for i in decompressedTiles],decompressedTiles[x523][y523]['group'],x523,y523,decompressedTiles[x523][y523]['width'],decompressedTiles[x523][y523]['height'],max=max):
                                    currentAction=['VERT','HORIZ'][currentAction=='VERT']
                                    if currentSkip==currentAction:
                                        currentAction=['VERT','HORIZ'][currentAction=='VERT']
                                    if currentAction=='HORIZ':
                                        decompressedTiles[x523][y523]['width']+=1
                                    elif currentAction=='VERT':
                                        decompressedTiles[x523][y523]['height']+=1
                                if currentAction=='HORIZ':
                                    decompressedTiles[x523][y523]['width']-=1
                                elif currentAction=='VERT':
                                    decompressedTiles[x523][y523]['height']-=1
                                for i in range(x523,x523+decompressedTiles[x523][y523]['width']):
                                    for j in range(y523,y523+decompressedTiles[x523][y523]['height']):
                                        if (i!=x523)|(j!=y523):
    
                                            decompressedTiles[i][j]['nope']=1
            for x523 in range(width):
                for y523 in range(height):
                    i=x523
                    j=y523
                    dataval=decompressedTiles[x523][y523]['tile']
                    decompressedTiles[x523][y523]['backgroundYes']=False
                    if dataval in [8,9,5,3,4,6,7]:
                        touchCount=0
                        if(i>0):
                            if self.data[j][i-1]==-2:
                                touchCount+=1
                        if(j>0):
                            if self.data[j-1][i]==-2:
                                touchCount+=1
                        if(i<self.width-1):
                            if self.data[j][i+1]==-2:
                                touchCount+=1
                        if(j<self.height-1):
                            if self.data[j+1][i]==-2:
                                touchCount+=1
                        if touchCount>=2:
                            decompressedTiles[x523][y523]['backgroundYes']=True
                    if dataval in [-1]:
                        touchCount=0
                        n=[-1,6,7]
                        if(i>0):
                            if self.data[j][i-1] in n:
                                touchCount+=1
                        if(j>0):
                            if self.data[j-1][i] in n:
                                touchCount+=1
                        if(i<self.width-1):
                            if self.data[j][i+1] in n:
                                touchCount+=1
                        if(j<self.height-1):
                            if self.data[j+1][i] in n:
                                touchCount+=1
                        if(touchCount!=0):
                            decompressedTiles[x523][y523]['backgroundYes']=True
                
            self.compressedTiles=[]
            for x523 in range(width):
                for y523 in range(height):
                    if (decompressedTiles[x523][y523]['nope']==0)|(decompressedTiles[x523][y523]['tile'] in ungroupable):
                        if decompressedTiles[x523][y523]['tile']!=0:
                            j=decompressedTiles[x523][y523]
                            self.compressedTiles.append([x523,y523,j['width'],j['height'],j['tile'],j['backgroundYes']])
                    #*[[j['width'],j['height'],j['tile']] for j in i if j['nope']==0] for i in decompressedTiles
        def buildRoom(self,offset,*groups):
            global entities
            global roomsBuilt
            wallgroup=groups[0]
            platformgroup=groups[1]
            allgroup=groups[5]#[2]
            allgroupt=groups[2]
            boundaryGroup=groups[3]
            builtRoomsGroup=groups[4]
            returns=[]
            boundaryListId=0
            b=BuiltRoom(offset[0],offset[1],self.width*20,self.height*20,roomsBuilt,self.id,allgroup,builtRoomsGroup,allgroupt)
            b.setShadows(self.shadowLevel)
            
            for obj in self.compressedTiles:
                
                i=obj[0]
                j=obj[1]
                dataval=obj[4]
                w=obj[2]
                h=obj[3]
                backgroundYes=obj[5]
                if 1:
                    if dataval in [-1,-2]:
                        pass
                    if dataval==1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,20*h,0,roomsBuilt,wallgroup,allgroup))
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,20*h,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
                    elif dataval==-1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,20*h,0,roomsBuilt,allgroup))
                        #returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        #allgroup.change_layer(returns[-1],-5)
                    elif dataval==-2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,20*h,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
                    elif dataval==2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,1,0,roomsBuilt,platformgroup,allgroup))
                    elif dataval==3:
                        tempObj=CollisionGroup(wallgroup,allgroup)
                        tempObj.roomid=roomsBuilt
                        for k in range(10):
                            returns.append(Wall(i*20+k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,[2 if k==0 else 1][0],roomsBuilt,tempObj.objects,allgroup))
                            if(k==0):
                                allgroup.change_layer(returns[-1],-4)
                        tempObj.updateArea()
                    elif dataval==4:
                        tempObj=CollisionGroup(wallgroup,allgroup)
                        tempObj.roomid=roomsBuilt
                        for k in range(10):
                            returns.append(Wall(i*20+18-k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,1,roomsBuilt,tempObj.objects,allgroup))
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],0,0,3,roomsBuilt,allgroup))
                        allgroup.change_layer(returns[-1],-4)
                        tempObj.updateArea()
                    elif dataval==5:
                        returns.append(RoomBoundary(offset[0]+i*20,offset[1]+j*20,self.boundaryList[boundaryListId],roomsBuilt,boundaryGroup,allgroup))
                        allgroup.change_layer(returns[-1],-1)
                        boundaryListId+=1
                    elif dataval==6:
                        tempObj=CollisionGroup(wallgroup,allgroup)
                        tempObj.roomid=roomsBuilt
                        for k in range(10):
                            returns.append(Wall(i*20+k*2+offset[0],j*20+18-k*2+offset[1],2,20-k*2,0,roomsBuilt,tempObj.objects,allgroup))
                        pass
                        tempObj.updateArea()
                    elif dataval==7:
                        tempObj=CollisionGroup(wallgroup,allgroup)
                        tempObj.roomid=roomsBuilt
                        for k in range(10):
                            returns.append(Wall(i*20+19-k*2+offset[0],j*20+offset[1],1,(k+1)*2,1,roomsBuilt,tempObj.objects,allgroup))
                        returns.append(Wall(i*20+18-9*2+offset[0],j*20+offset[1],1,(9+1)*2,5,roomsBuilt,tempObj.objects,allgroup))
                        allgroup.change_layer(returns[-1],-4)
                        tempObj.updateArea()
                    elif dataval==8:
                        returns.append(Hazard(i*20+offset[0],j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                        returns.append(Hazard(i*20+offset[0]+10,j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                    elif dataval==9:
                        returns.append(SaveMarker(i*20+offset[0],j*20+offset[1],roomsBuilt,allgroup))
                    elif dataval==10:#closableDoor
                        tempObj=CollisionGroup(wallgroup,allgroup,entities)
                        
                        tempObj.roomid=roomsBuilt
                        #returns.append(Wall(i*20+18-9+offset[0],j*20+offset[1]-10,2,10,1,roomsBuilt,tempObj.objects,allgroup))
                        #returns.append(Wall(i*20+18-9+offset[0],j*20+offset[1]+20,2,10,1,roomsBuilt,tempObj.objects,allgroup))
                        returns.append(movableTile([i*20+9+offset[0],j*20+offset[1]-51],entities,tempObj.objects,allgroup))
                        
                        returns[-1].width=2
                        returns[-1].height=41
                        returns[-1].pos=[i*20+9+offset[0],j*20+offset[1]-51]
                        #returns[-1].gravity=[0,0]
                        returns[-1].imgid=Wall.textureIds[0]
                        returns[-1].updateFrame()
                        returns[-1].rect.size=(2,41)
                        returns.append(movableTile([i*20+9+offset[0],j*20+offset[1]+20],entities,tempObj.objects,allgroup))
                        returns[-1].width=2
                        returns[-1].height=41
                        returns[-1].pos=[i*20+9+offset[0],j*20+offset[1]+20]
                        returns[-1].gravity[1]*=-1
                        returns[-1].imgid=Wall.textureIds[0]
                        returns[-1].updateFrame()
                        returns[-1].rect.size=(2,41)
                        returns[-1].extraUpdateFunct=lambda self:[self.setPosX(i*20+9+offset[0])]

                        tempObjb=CollisionGroup(wallgroup,allgroup)
                        tempObjb.roomid=roomsBuilt
                        returns.append(Wall(i*20+offset[0],j*20+offset[1]-61,8,42,0,roomsBuilt,wallgroup,allgroup))
                        returns.append(Wall(i*20+offset[0]+12,j*20+offset[1]-61,8,42,0,roomsBuilt,wallgroup,allgroup))
                        returns.append(Wall(i*20+offset[0],j*20+offset[1]-63,20,1,0,roomsBuilt,wallgroup,allgroup))
                        
                        returns.append(Wall(i*20+offset[0],j*20+offset[1]+20,8,42,0,roomsBuilt,wallgroup,allgroup))
                        returns.append(Wall(i*20+offset[0]+12,j*20+offset[1]+20,8,42,0,roomsBuilt,wallgroup,allgroup))
                        #returns.append(Wall(i*20+offset[0],j*20+offset[1]+62,20,1,0,roomsBuilt,wallgroup,allgroup))
                        
                        
                        tempObj.updateArea()
                        tempObjb.updateArea()
                        """self.width=20
            self.height=20
            self.gravity=[0,0.2]
            pg.sprite.Sprite.__init__(self, *groups)
            for i in range(self.images.__len__()):
                self.images[i]=pg.transform.scale(self.images[i],(self.width,self.height))
            self.image = pg.transform.scale(self.images[0],(self.width,self.height))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.velocity=[0,0]
            self.pos=[200,100]
            self.onGround=0
            self.friction=0.1
            self.imgid=self.textureIds[0]
            self.wasOnGround=0
            self.lastShots=[time.time(),time.time()-1]
            self.isSolid=False
            self.updateFrame()
            self.updateFrame()"""
                    if backgroundYes==1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20*w,20*h,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
            allgroupt.change_layer(b,-10)
            roomsBuilt+=1
            #print(allgroupt.sprites().__len__())
        def buildRoom_old(self,offset,*groups):
            global roomsBuilt
            wallgroup=groups[0]
            platformgroup=groups[1]
            allgroup=groups[5]#[2]
            allgroupt=groups[2]
            boundaryGroup=groups[3]
            builtRoomsGroup=groups[4]
            returns=[]
            boundaryListId=0
            b=BuiltRoom(offset[0],offset[1],self.width*20,self.height*20,roomsBuilt,self.id,allgroup,builtRoomsGroup,allgroupt)
            
            for i in range(self.width):
                for j in range(self.height):
                    dataval=self.data[j][i]
                    if dataval==1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,0,roomsBuilt,wallgroup,allgroup))
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
                    elif dataval==-1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,0,roomsBuilt,allgroup))
                        #returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        #allgroup.change_layer(returns[-1],-5)
                    elif dataval==-2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
                    elif dataval==2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,1,0,roomsBuilt,platformgroup,allgroup))
                    elif dataval==3:
                        for k in range(10):
                            returns.append(Wall(i*20+k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,[2 if k==0 else 1][0],roomsBuilt,wallgroup,allgroup))
                            if(k==0):
                                allgroup.change_layer(returns[-1],-4)
                            else:
                                returns[-1].shouldRender=False
                    elif dataval==4:
                        for k in range(10):
                            returns.append(Wall(i*20+18-k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,1,roomsBuilt,wallgroup,allgroup))
                            returns[-1].shouldRender=False
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],0,0,3,roomsBuilt,allgroup))
                        allgroup.change_layer(returns[-1],-4)
                    elif dataval==5:
                        returns.append(RoomBoundary(offset[0]+i*20,offset[1]+j*20,self.boundaryList[boundaryListId],roomsBuilt,boundaryGroup,allgroup))
                        allgroup.change_layer(returns[-1],-1)
                        boundaryListId+=1
                    elif dataval==6:
                        for k in range(10):
                            returns.append(Wall(i*20+k*2+offset[0],j*20+18-k*2+offset[1],2,20-k*2,0,roomsBuilt,wallgroup,allgroup))
                            
                    elif dataval==7:
                        for k in range(10):
                            returns.append(Wall(i*20+19-k*2+offset[0],j*20+offset[1],1,(k+1)*2,1,roomsBuilt,wallgroup,allgroup))
                            returns[-1].shouldRender=False
                        returns.append(Wall(i*20+18-9*2+offset[0],j*20+offset[1],1,(9+1)*2,5,roomsBuilt,wallgroup,allgroup))
                        allgroup.change_layer(returns[-1],-4)
                    elif dataval==8:
                        returns.append(Hazard(i*20+offset[0],j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                        returns.append(Hazard(i*20+offset[0]+10,j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                    elif dataval==9:
                        returns.append(SaveMarker(i*20+offset[0],j*20+offset[1],roomsBuilt,allgroup))
                    if dataval in [8,9,5,3,4,6,7]:
                        touchCount=0
                        if(i>0):
                            if self.data[j][i-1]==-2:
                                touchCount+=1
                        if(j>0):
                            if self.data[j-1][i]==-2:
                                touchCount+=1
                        if(i<self.width-1):
                            if self.data[j][i+1]==-2:
                                touchCount+=1
                        if(j<self.height-1):
                            if self.data[j+1][i]==-2:
                                touchCount+=1
                        if touchCount>=2:
                            returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                            allgroup.change_layer(returns[-1],-5)
                            returns[-1].depth=5
                    if dataval in [-1]:
                        touchCount=0
                        n=[-1,6,7]
                        if(i>0):
                            if self.data[j][i-1] in n:
                                touchCount+=1
                        if(j>0):
                            if self.data[j-1][i] in n:
                                touchCount+=1
                        if(i<self.width-1):
                            if self.data[j][i+1] in n:
                                touchCount+=1
                        if(j<self.height-1):
                            if self.data[j+1][i] in n:
                                touchCount+=1
                        if(touchCount!=0):
                            returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                            returns[-1].depth=5
                            allgroup.change_layer(returns[-1],-5)
            allgroupt.change_layer(b,-10)
            roomsBuilt+=1
            #print(allgroupt.sprites().__len__())
        def link(self,other,boundaryId0,boundaryId1):
            self.boundaryList[boundaryId0][1]=str(other.id)+"_"+other.boundaryList[boundaryId1][0]
            #print(self.boundaryList)
            
            
    #class Alien(pg.sprite.Sprite):
    #    """An alien space ship. That slowly moves down the screen."""
    #
    #    speed = 13
    #    animcycle = 12
    #    images: List[pg.Surface] = []
    #
    #    def __init__(self, *groups):
    #        pg.sprite.Sprite.__init__(self, *groups)
    #        self.image = self.images[0]
    #        self.rect = self.image.get_rect()
    #        self.facing = random.choice((-1, 1)) * Alien.speed
    #        self.frame = 0
    #        if self.facing < 0:
    #            self.rect.right = SCREENRECT.right
    #
    #    def update(self, *args, **kwargs):
    #        self.rect.move_ip(self.facing, 0)
    #        if not SCREENRECT.contains(self.rect):
    #            self.facing = -self.facing
    #            self.rect.top = self.rect.bottom + 1
    #            self.rect = self.rect.clamp(SCREENRECT)
    #        self.frame = self.frame + 1
    #        self.image = self.images[self.frame // self.animcycle % 3]
    
    backgroundstrength=(0.3,0.3,0.3,0,0,0)
    global newObjects
    newObjects=[]
    global newEattacks
    newEattacks=[]


    COMMAND_ARGUMENT_INT=21833
    COMMAND_ARGUMENT_FLOAT=21834
    COMMAND_ARGUMENT_STRING=21835
    COMMAND_ARGUMENT_STRING_GREEDY=21839

    COMMAND_ARGUMENT_INT_OPTIONAL=21836
    COMMAND_ARGUMENT_FLOAT_OPTIONAL=21837
    COMMAND_ARGUMENT_STRING_OPTIONAL=21838
    
    COMMAND_ARGUMENT_SPECIAL_VARIABLE=21701
    
    COMMAND_ARGUMENT_INVALID=21900
    COMMAND_ARGUMENT_MISSING=21901
    COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE=21901
    COMMAND_NONEXISTENT=21902
    COMMAND_ALREADY_EXISTS=21903


    global commandStorages
    commandStorages={}
    
    
    class invalidCommandError(Exception):
        pass
    class commandArgument:
        def __init__(self,type:int,name:str):
            self.type=type
            self.name=name
        def get_value(self,command,index):
            c=command.split(' ')
            if(c.__len__()<=index):
                if self.type in [COMMAND_ARGUMENT_INT_OPTIONAL,COMMAND_ARGUMENT_FLOAT_OPTIONAL,COMMAND_ARGUMENT_STRING_OPTIONAL]:
                    return None
                return COMMAND_ARGUMENT_MISSING
            b=c[index]
            if(self.type==COMMAND_ARGUMENT_INT)|(self.type==COMMAND_ARGUMENT_INT_OPTIONAL):
                if b.isdecimal():
                    return int(b)
                elif (b.count('-')==1)&(b[0]=='-')&b[1:].isdecimal()&(b.count('.')<=1):
                    return int(b)
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif(self.type==COMMAND_ARGUMENT_FLOAT)|(self.type==COMMAND_ARGUMENT_FLOAT_OPTIONAL):
                if "".join(b.split('.')).isdecimal()&(b.count('.')<=1):
                    return float(b)
                elif (b.count('-')==1)&(b[0]=='-')&"".join(b[1:].split('.')).isdecimal()&(b.count('.')<=1):
                    return float(b)
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif(self.type==COMMAND_ARGUMENT_STRING)|(self.type==COMMAND_ARGUMENT_STRING_OPTIONAL):
                return b
            elif self.type==COMMAND_ARGUMENT_SPECIAL_VARIABLE:
                if b.__len__()>3:
                    if [b[0]=='v',b[1]=='a',b[2]=='r',b[3]=='_']:
                        try: 
                            return getVariableValue(b[4:])
                        except:
                            return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
                    else:
                        return COMMAND_ARGUMENT_INVALID
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif self.type==COMMAND_ARGUMENT_STRING_GREEDY:
                return " ".join(c[index:])

    class command:
        def __init__(self,**kwargs):
            self.name=kwargs['name']
            self.arguments=[]
            self.trigger=kwargs['triggerCommand']
            for i in kwargs['args'].split(" "):
                j=i.split(':')
                n=j[0]
                if j.__len__()>1:
                    ts=j[1]
                    if '|' not in ts:
                        if ts=='int':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_INT,n))
                        elif ts=='float':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_FLOAT,n))
                        elif ts=='str':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING,n))
                        elif ts=='str_greedy':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING_GREEDY,n))
                        elif ts=='int_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_INT_OPTIONAL,n))
                        elif ts=='float_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_FLOAT_OPTIONAL,n))
                        elif ts=='str_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING_OPTIONAL,n))
                        elif ts=='var':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_SPECIAL_VARIABLE,n))
                        else:
                            raise invalidCommandError
                    else:
                        self.arguments.append([])
                        for ts2 in ts.split('|'):
                            if ts2=='int':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_INT,n))
                            elif ts2=='float':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_FLOAT,n))
                            elif ts2=='str':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING,n))
                            elif ts2=='str_greedy':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING_GREEDY,n))
                            elif ts2=='int_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_INT_OPTIONAL,n))
                            elif ts2=='float_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_FLOAT_OPTIONAL,n))
                            elif ts2=='str_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING_OPTIONAL,n))
                            elif ts2=='var':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_SPECIAL_VARIABLE,n))
                            else:
                                raise invalidCommandError
        def execute(self,input):
            arg2=[(self.arguments[i].get_value(input,i+1) if type(self.arguments[i])==commandArgument else [self.arguments[i][j].get_value(input,i+1) for j in range(self.arguments[i].__len__())]) for i in range(self.arguments.__len__())]
            for i in range(arg2.__len__()):
                if type(self.arguments[i])!=commandArgument:
                    b=arg2[i]
                    for j in b:
                        if j not in [COMMAND_ARGUMENT_INVALID,COMMAND_ARGUMENT_MISSING,COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE,None]:
                            arg2[i]=j
                            break
                    if arg2[i]==b:
                        arg2[i]=COMMAND_ARGUMENT_INVALID
            if sum([i in [COMMAND_ARGUMENT_INVALID,COMMAND_ARGUMENT_MISSING,COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE] for i in arg2])!=0:
                return COMMAND_ARGUMENT_INVALID
            return self.trigger(arg2)

    class commandSystem:
        def __init__(self):
            self.commands={}
        def executeBase(self,commandI):
            
            cname=commandI.split(" ")[0]
            if cname not in self.commands:
                return COMMAND_NONEXISTENT
            else:
                return self.commands[cname].execute(commandI)
        def addCommand(self,commandD,toRun):
            
            cname=commandD.split(" ")[0]
            if cname in self.commands:
                return COMMAND_ALREADY_EXISTS
            cargs=' '.join(commandD.split(" ")[1:])
            self.commands[cname]=command(name=cname,args=cargs,triggerCommand=toRun)

    class renderObject(pg.sprite.Sprite):
        def __init__(self,pos,size,id,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.imgid=id
            self.rect=pg.Rect(*pos,*size)
            self.rect.size=self.rect.size[0],-self.rect.size[1]
            self.rect.left-=self.rect.size[0]
    class textRenderer:
        textureIds:List[int]=[]
        charSizes:List[int]=[]
        chars:List[str]=[]
        def __init__(self,pos,size,renderGroup):
            self.pos=pos
            self.size=size
            self.rect=pg.Rect(*pos,*size)
            self.objects=[]
            self.rGroup=renderGroup
        def setText(self,text,cursorPos=None):
            global scrwidth,scrheight
            for i in self.objects:
                i.kill()
            self.objects=[]
            pos=[0,0]
            if cursorPos==None:
                for char in text:
                    if char not in ['\n','\n!']:
                        self.objects.append(renderObject((self.pos[0]*scrwidth/scrwidth+pos[0]*scrwidth/scrwidth+self.charSizes[self.chars.index(char)]*scrwidth/scrwidth,self.pos[1]*scrwidth/scrwidth+pos[1]*scrwidth/scrwidth),(self.charSizes[self.chars.index(char)]*scrwidth/scrwidth,10*scrwidth/scrwidth),self.textureIds[self.chars.index(char)],self.rGroup))
                        pos[0]+=self.charSizes[self.chars.index(char)]*2
                    else:
                        pos[0]=0
                        pos[1]+=21*scrwidth/scrwidth
                    if pos[0]+self.pos[0]>scrwidth:
                        pos[0]=0
                        pos[1]+=21*scrwidth/scrwidth
            else:
                numObjs=0
                #print(cursorPos)
                for char in text:
                    if char not in ['\n','\n!']:
                        self.objects.append(renderObject((self.pos[0]*scrwidth/scrwidth+pos[0]*scrwidth/scrwidth+self.charSizes[self.chars.index(char)]*scrwidth/scrwidth,self.pos[1]+pos[1]),(self.charSizes[self.chars.index(char)]*scrwidth/scrwidth,10*scrwidth/scrwidth),self.textureIds[self.chars.index(char)],self.rGroup))
                        if numObjs==cursorPos:
                            self.objects.append(renderObject((self.pos[0]*scrwidth/scrwidth+pos[0]*scrwidth/scrwidth+self.charSizes[self.chars.index("|")]/2*scrwidth/scrwidth,self.pos[1]+pos[1]),(self.charSizes[self.chars.index('|')]*scrwidth/scrwidth,10*scrwidth/scrwidth),self.textureIds[self.chars.index('|')],self.rGroup))
                        pos[0]+=self.charSizes[self.chars.index(char)]*2
                        numObjs+=1
                    else:
                        pos[0]=0
                        pos[1]+=21
                        numObjs+=1
                    if pos[0]+self.pos[0]>scrwidth:
                        pos[0]=0
                        pos[1]+=21
                if numObjs==cursorPos:
                    self.objects.append(renderObject((self.pos[0]*scrwidth/scrwidth+pos[0]*scrwidth/scrwidth+self.charSizes[self.chars.index("|")]/2*scrwidth/scrwidth,self.pos[1]*scrwidth/scrwidth+pos[1]*scrwidth/scrwidth),(self.charSizes[self.chars.index('|')]*scrwidth/scrwidth,10*scrwidth/scrwidth),self.textureIds[self.chars.index('|')],self.rGroup))
                    






    def getVariableValue(source):
            global commandStorages

            a=None
            b=[]
            c=None
            d=None
            if('[' in source):
                a=source.split('[')[0]
                for x in source.split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=source
            return c[d]





    global skipRenderTextures
    skipRenderTextures=[]
    global lastFrameClock
    lastFrameClock=time.time()
    def main(winstyle=0):
        global skipRenderTextures
        #global all
        global GUIelements
        #global winfo
        #global newParticles
        #global newObjects
        global splashtext
        global winfo,player,enemies,walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks,healthBarRender,newParticles,newObjects,phyicsparticles,playerPewGroup,enemyAttacks
        animationsList={'player':{'walk':4,'fall':1}}
        # Initialize pygame
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None
    
        fullscreen = False
        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pg.display.mode_ok(SCREENRECT.size, 0, 32)
        screen = pg.display.set_mode(SCREENRECT.size, 0, bestdepth,vsync=0)
        #pg.display.set_mode(SCREENRECT.size,winstyle|pg.RESIZABLE,vsync=1)
        #pg.display.set_mode(SCREENRECT.size,pg.OPENGL|pg.RESIZABLE|pg.DOUBLEBUF)
        #pg.key.set_repeat(500,75)
        1+winfo
        #winfo=pg.display.Info()
        # Load images, assign to sprite classes
        # (do this before the classes are used, after screen setup)
        img = load_image(imagefolder+r"\tictactoe\blank2.png")
        img2 = load_image(imagefolder+r"\tictactoe\blank1.png")
        img3 = load_image(imagefolder+r"\tictactoe\o.png")
        img4 = load_image(imagefolder+r"\specialgamev1\builtRoom.png")
        img4.set_colorkey([0,0,0])
        img3.set_colorkey([0,0,0])
        images={'hazard1':"hazard.png","save_marker":"devtextures\\savemarker.png","particle_blood":"devtextures\\savemarker.png",'tile1':"tiles\\bricksFull.png",'tile2':"tiles\\intentionallyempty.png",'tile3':"tiles\\brickStairsLeft.png",'tile4':"tiles\\brickStairsRight.png",'tile5':"tiles\\brickStairsInvertedright.png",'tile6':"tiles\\brickStairsInvertedLeft.png",'movabletile':"entity\\tile.png"}
        crops={'tile1':(0,0,20,16)}
        retextures={'tile3':'tile1','tile4':'tile1','tile5':'tile1','tile6':'tile1'}
        backgrounds={'tile-2':'tile1'}
        tints={'particle_blood':[255/255,50/255,50/255]}
        retransparency={'particle_blood':64}
        scaled={'tile1':10,'tile2':10,'tile-2':10,'tile3':10,'tile4':10,'tile5':10,'tile6':10}
    
        bitmaps={'cursor':({'o':(0,255,0),'X':(255,0,0),'.':(255,0,0),' ':(0,0,0,0)},(               #sized 16x16
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "ooooooo.""Xooooooo",
        "oooooooX"".ooooooo",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ",
        "       o""o       ")),
                'lapew1':({'o':(0,0,255),'.':(0,127,255,0.5),' ':(0,0,0,0)},(               #sized 16x16
        "                ",
        " ...            ",
        ".oo...          ",
        "o.o.o...        ",
        ".o.o.oo...      ",
        "o.o.oo.oo...    ",
        ".o.o.ooo.oo...  ",
        "o.o.oo.o.oooo...",
        ".o.o.ooo.oo...  ",
        "o.o.oo.oo...    ",
        ".o.o.oo...      ",
        "o.o.o...        ",
        ".oo...          ",
        " ...            ",
        "                ")),
                'faintCloud':({'.':(0,127,255,0),' ':(0,0,0,0)},(               #sized 16x16
        "."))}
    
    
    
        
    
    
    
        
        for i in images:
            images[i]=load_image(imagefolder+"\\specialgamev1\\"+images[i])
            images[i].set_colorkey([0,0,0])
        for i in crops:
            image=images[i]
            newrect=crops[i]
            x=pg.surface.Surface((newrect[2]-newrect[0],newrect[3]-newrect[1]))
            x.blit(image,(-newrect[0],-newrect[1]))
            images[i]=x
        for i in retextures:
            image=images[i]
            imagebase=images[retextures[i]]
            w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
            for x in range(w1):
                for y in range(h1):
                    r=image.get_at((x,y))
                    if(r[0]+r[1]+r[2])!=0:
                        image.set_at((x,y),imagebase.get_at((int(x/w1*w2),int(y/h1*h2))))
            images[i]=image
        
        for i in backgrounds:
            if i in images:
                image=images[i]
                imagebase=images[backgrounds[i]]
                w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
                for x in range(w1):
                    for y in range(h1):
                        r=image.get_at((x,y))
                        if(r[0]+r[1]+r[2])==0:
                            b=imagebase.get_at((int(x/w1*w2),int(y/h1*h2)))
                            image.set_at((x,y),(b[0]*backgroundstrength[0]+backgroundstrength[3],b[1]*backgroundstrength[1]+backgroundstrength[4],b[2]*backgroundstrength[2]+backgroundstrength[5]))
                images[i]=image
            else:
                imagebase=images[backgrounds[i]]
                image=pg.surface.Surface((imagebase.get_width(),imagebase.get_height()))
                w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
                for x in range(w1):
                    for y in range(h1):
                        r=image.get_at((x,y))
                        b=imagebase.get_at((int(x/w1*w2),int(y/h1*h2)))
                        image.set_at((x,y),(b[0]*backgroundstrength[0]+backgroundstrength[3],b[1]*backgroundstrength[1]+backgroundstrength[4],b[2]*backgroundstrength[2]+backgroundstrength[5]))
                images[i]=image
        for i in tints:
            image=images[i]
            tint=tints[i]
            w1,h1=image.get_width(),image.get_height()
            for x in range(w1):
                for y in range(h1):
                    r=image.get_at((x,y))
                    if(r[0]+r[1]+r[2])!=0:
                        p=image.get_at((x,y))
                        image.set_at((x,y),(p[0]*tint[0],p[1]*tint[1],p[2]*tint[2],p[3]))
            images[i]=image
        for i in retransparency:
            baseimage=images[i]
            for j in range(retransparency[i]):
                z=baseimage.copy()
                z.set_alpha(255*(retransparency[i]-j)/retransparency[i])
                images[i+"_trans_"+str(j)]=z
        for i in scaled:
            image=images[i]
            scale=scaled[i]
            imagerect=image.get_rect()
            w=imagerect.size[0]
            h=imagerect.size[1]
            x=pg.surface.Surface((w*scale,h*scale))
            for u in range(scale):
                for j in range(scale):
                    x.blit(image,(u*w,j*h))
            images[i]=x

        for i in bitmaps:
            data,map=bitmaps[i]
            height,width=(map.__len__(),map[0].__len__())
            x=pg.surface.Surface((width,height))#, flags=pg.SRCALPHA)
            pixelalpha=0
            for u in range(width):
                for j in range(height):
                    x.set_at((u,j),(data[map[j][u]]))
                    if data[map[j][u]].__len__()==4:
                        if(data[map[j][u]][3]!=0):
                            #x.set_alpha((u,j),data[map[j][u]][3])
                            pixelalpha=True
            x.set_colorkey(data[' '])
            images[i]=x
        
        imagesb={}

        img2.fill((1,1,1))
        img2.set_alpha(128)
        images['a']=img2
        
        #images['bgkgrnand'].set_alpha(254)
        
        
        for i in images:
            print("LOADING TEXTURE \""+i+"\"")
            splashtext=("LOADING TEXTURE \""+i+"\"")
            imagesb[i]=loadTexture(surface_array(images[i]))
            pg.time.wait(1)
        font=pg.font.Font(None,60)
        for i in "asdfghjklqwertyuiopzxcvbnm 1234567890-=`~!@#$%^&*()_+QWERTYUIOP{}[]ASDFGHJKL:ZXCVBNM<>?,./\\|;'\"":
            print("LOADING FONT CHAR "+i+"")
            splashtext=("LOADING FONT CHAR "+i+"")
            z=font.render(i,True,(0,255,0),(0,1,0))
            
            textRenderer.textureIds.append(loadTexture(surface_array(z)))
            textRenderer.chars.append(i)
            textRenderer.charSizes.append(z.get_rect().size[0]/3)
            pg.time.wait(1)
        for i in [["\t","\\t"]]:
            print("LOADING FONT CHAR "+i[1]+"")
            splashtext=("LOADING FONT CHAR "+i[1]+"")
            z=font.render(i[1],True,(0,255,255),(0,1,0))
            
            textRenderer.textureIds.append(loadTexture(surface_array(z)))
            textRenderer.chars.append(i[0])
            textRenderer.charSizes.append(z.get_rect().size[0]/3)
            pg.time.wait(1)
        for i in "asdfghjklqwertyuiopzxcvbnm 1234567890-=`~!@#$%^&*()_+QWERTYUIOP{}[]ASDFGHJKL:ZXCVBNM<>?,./\\|;'\"":
            print("LOADING FONT CHAR "+i+"")
            splashtext=("LOADING FONT CHAR "+i+"")
            z=font.render(i,True,(0,255,0),(0,1,127))
            
            textRenderer.textureIds.append(loadTexture(surface_array(z)))
            textRenderer.chars.append(i+"!")
            textRenderer.charSizes.append(z.get_rect().size[0]/3)
            pg.time.wait(1)
        for i in [["\t","\\t"]]:
            print("LOADING FONT CHAR "+i[1]+"")
            splashtext=("LOADING FONT CHAR "+i[1]+"")
            z=font.render(i[1],True,(0,255,255),(0,1,127))
            
            textRenderer.textureIds.append(loadTexture(surface_array(z)))
            textRenderer.chars.append(i[0]+"!")
            textRenderer.charSizes.append(z.get_rect().size[0]/3)
            pg.time.wait(1)
        Background.images.append(img2)
        barTextures=["leftb.png","midb.png","rightb.png","leftf0.png","leftf1.png","leftf2.png","midf0.png","midf1.png","midf2.png","rightf0.png","rightf1.png","rightf1.png"]
        barTextures=[load_image(imagefolder+"\\specialgamev1\\healthbar\\"+i) for i in barTextures]
        barTexturesb=[loadTexture(surface_array(i)) for i in barTextures]
        for i in barTextures:
            i.set_colorkey([0,0,0])
        animations={}
        for i in animationsList:
            for j in animationsList[i]:
                for k in range(animationsList[i][j]):
                    k=k+1
                    animations['anim_'+str(i)+"_"+str(j)+"_"+str(k)]=load_image(imagefolder+"\\specialgamev1\\"+'anim_'+str(i)+"_"+str(j)+"_"+str(k)+".png")
                    print('anim_'+str(i)+"_"+str(j)+"_"+str(k))
                    splashtext="Loading Image "+('anim_'+str(i)+"_"+str(j)+"_"+str(k))            
                    pg.time.wait(1)
        n=[i for i in animations]
        for i in n:
            animations[i+'_flip']=pg.transform.flip(animations[i],1,0)
        Player.images = [animations[i] for i in animations if ('player' in i)]
        print([i for i in animations if ('player' in i)]+["flip_"+i for i in animations if ('player' in i)])
        #[pg.transform.scale(img,(Player.width,Player.height)), pg.transform.flip(pg.transform.scale(img,(Player.width,Player.height)), 1, 0)]
        Wall.images = [images[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2','faintCloud']]
        Entity.images = [images[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2']]
        Hazard.images = [images['hazard1']]
        SaveMarker.images = [images['save_marker']]
        RoomBoundary.images.append(img3)
        BuiltRoom.images.append(img4)
        PhysicsParticle.images.append([images[i] for i in images if 'particle_blood' in i])
        Particle.images.append([images[i] for i in images if 'particle_blood' in i])
        LaPew.images.append(images['lapew1'])
        GenericSingleFrameAttack.images.append(images['particle_blood'])
        CursorVisual.images.append(images['cursor'])
        movableTile.images.append(images['movabletile'])
        movableTile2.images.append(images['movabletile'])
        animationsb={}
        for i in animations:
            print("LOADING TEXTURE ANIMATION \""+i+"\"")
            animationsb[i]=loadTexture(surface_array(animations[i]))
            splashtext="Finalizing Texture"+(i)
            pg.time.wait(1)
    
        setup()
    
    
    
    
    
        Player.textureIds = [animationsb[i] for i in animationsb if ('player' in i)]
        Wall.textureIds = [imagesb[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2','faintCloud']]
        Entity.textureIds = [imagesb[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2']]
        genericElement.textureIds = [imagesb[i] for i in ["tile1"]]
        Hazard.textureIds = [imagesb['hazard1']]
        SaveMarker.textureIds = [imagesb['save_marker']]
        RoomBoundary.textureIds.append(loadTexture(surface_array(img3)))
        BuiltRoom.textureIds.append(loadTexture(surface_array(img4)))
        PhysicsParticle.textureIds.append([imagesb[i] for i in imagesb if 'particle_blood' in i])
        Particle.textureIds.append([imagesb[i] for i in imagesb if 'particle_blood' in i])
        LaPew.textureIds.append(imagesb['lapew1'])
        GenericSingleFrameAttack.textureIds.append(imagesb['particle_blood'])
        CursorVisual.textureIds.append(imagesb['cursor'])
        Background.textureIds.append(imagesb['a'])
        movableTile.textureIds.append(imagesb['movabletile'])
        movableTile2.textureIds.append(imagesb['movabletile'])
        # decorate the game window
        #icon = pg.transform.scale(Alien.images[0], (32, 32))
        #pg.display.set_icon(icon)
        #pg.display.set_caption("Pygame Aliens")
        #pg.mouse.set_visible(0)
        skipRenderTextures.append(imagesb['tile2'])
        Enemeh.images=Player.images
        Enemeh.textureIdsAll=[Player.textureIds]
    
        
        # create the background, tile the bgd image
        bgdtile = load_image(imagefolder+r"\backgroundm.png")
        background = pg.Surface(SCREENRECT.size)
        for x in range(0, SCREENRECT.width, bgdtile.get_width()):
            background.blit(bgdtile, (x, 0))
        #screen.blit(background, (0, 0))
        pg.display.flip()
    
        # load the sound effects
        #sound_id=load_sound(filename)
        #if pg.mixer:
        #    music = os.path.join(main_dir, "data", "house_lo.wav")
        #    pg.mixer.music.load(music)
        #    pg.mixer.music.play(-1)
    
        # Initialize Game Groups
        walls = pg.sprite.Group()
        platforms = pg.sprite.Group()
        all = pg.sprite.LayeredUpdates()
        allb = all#pg.sprite.LayeredUpdates()
        GUIelements = pg.sprite.LayeredUpdates()
        phyicsparticles=pg.sprite.Group()
        playerPewGroup=pg.sprite.Group()
        enemyAttacks=pg.sprite.Group()
        boundaries = pg.sprite.Group()
        builtRooms = pg.sprite.Group()
        global entities
        entities = pg.sprite.Group()
        healthBarRender=Bar(10,10,barTextures,barTexturesb,10,10,10,0,GUIelements)
        # Create Some Starting Values
        clock = pg.time.Clock()
    
        

        backgroundObg=Background(all)
        all.change_layer(backgroundObg,-1000000)














        global codesnippets
        codesnippets={}



        global fps
        fps=[0]
        commandStorages['fps']=[fps][0]

        global tickingFiles
        tickingFiles=[]

        global hooks
        hooks=[{}]#hooks[0]: varchange, index is var
        #{'type':"varchange",'name':"",'trigger':{'type':"cmd",'cmd':"executeFile_argless terminateIfPlayerDead"}}
        global initFiles
        initFiles=[]
        global protectedVariables
        protectedVariables=[]
        global rOnlyVariables
        rOnlyVariables=['fps']
        global files
        files={}

        files['tpRelative']='\n'.join(["variable playerpos_old command player.pos",
        "variable playerpos_new arrayize ???",
        "variable playerpos_new append_var playerpos_old[0]",
        "variable playerpos_new append_var playerpos_old[1]",
        "variable xoffset arrayize args[0]",
        "variable xoffset append 0",
        "variable xoffset var xoffset[0]",
        "variable xoffset type float",
        "variable yoffset arrayize args[1]",
        "variable yoffset append 0",
        "variable yoffset var yoffset[0]",
        "variable yoffset type float",
        "variable playerpos_new[0] sum playerpos_new[0] xoffset",
        "variable playerpos_new[1] sum playerpos_new[1] yoffset",
        "tp var_playerpos_new[0] var_playerpos_new[1]"
        ])

        files['setPlayerHealth']='\n'.join(["variable player command get_player",
        'variable playerAttr command variable player attr attributes',
        "variable args[0] type int",
        "variable playerAttr['health'] var args[0]"
        ])

        files['healPlayer']='\n'.join(["variable player command get_player",
        'variable playerAttr command variable player attr attributes',
        "variable args[0] type int",
        "variable playerAttr['health'] sum playerAttr['health'] args[0]",
        "variable playerAttr['health'] min playerAttr['health'] playerAttr['maxhealth']"
        ])


        
        files['loadPlayerVariables']='\n'.join(["variable player command get_player",
        'variable player.attr command variable player attr attributes',
        'variable player.pos command variable player attr pos',
        'variable player.vel command variable player attr velocity',
        'variable player.onGround command variable player attr onGround',
        'variable player.fireCooldown command variable player attr firecooldown',
        'variable player.ducking command variable player attr ducking',
        'variable player.shotsLeft command variable player attr shotsleft',
        'variable player.reloadTime command variable player attr reloadTime',
        './lockVariable player',
        './protectVariable player.attr',
        './protectVariable player.pos',
        './protectVariable player.vel',
        './lockVariable player.onGround',
        './lockVariable player.fireCooldown',
        './lockVariable player.ducking',
        './lockVariable player.shotsLeft',
        './lockVariable player.reloadTime'
        ])

        initFiles.append('loadPlayerVariables')
        
        files['terminateIfPlayerDead']='\n'.join([
        'variable isDead command a<=b player.attr[\'health\'] 0',
        "?execute isDead ./programTerminate"
        ])

        tickingFiles.append('terminateIfPlayerDead')
        
        def executeFile(fname):
            n=files[fname]
            n=n.split('\n')
            for m in n:
                #print(m)
                #print(cmdsys.executeBase(m))
                cmdsys.executeBase(m)
                
        global cmdsys
        cmdsys=commandSystem()
        cmdsys.addCommand("declare x:str",lambda x:print(x))
        def tpCommand(args):
            global player
            player.pos[0]=args[0]*20
            player.pos[1]=args[1]*20
            player.velocity=[0,0]
            return (int(player.pos[0])/20,int(player.pos[1])/20)
        def playerPos(args):
            global player
            return (int(player.pos[0])/20,int(player.pos[1])/20)
        def setGravCommand(args):
            global player
            player.gravity[0]=args[0]
            player.gravity[1]=args[1]
        def setVelocityCommand(args):
            global player
            player.velocity[0]=args[0]
            player.velocity[1]=args[1]
        def summonCommand(args):
            global player
            p=playerPos([])
            if(args[1]==None):
                args[1]=p[0]
                args[2]=p[1]
            if args[0]=="meh":
                x=Enemeh(args[1]*20,args[2]*20,enemies,all)
            if args[0]=="tile":
                newObjects.append([3,args[1]*20,args[2]*20])
                #newobjects 3 pos
            else:
                return "Eh, the enemy "+str(args[0])+" doesnt exist yet."
        def placeRoomCommand(args):
            global player
            global rooms
            if args[0] in rooms:
                rooms[args[0]].buildRoom([int(args[1])*20,int(args[2])*20],walls,platforms,all,boundaries,builtRooms,allb)
            elif int(args[0]) in rooms:
                rooms[int(args[0])].buildRoom([int(args[1])*20,int(args[2])*20],walls,platforms,all,boundaries,builtRooms,allb)
            else:
                return "Error! Room "+args[0]+" nonexistent!"


        """def getVariableValue(source):
            global commandStorages

            a=None 
            b=[]
            c=None
            d=None
            if('[' in source):
                a=source.split('[')[0]
                for x in source.split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=source
            return c[d]"""
        
        def variableCommand(args):
            global commandStorages
            global cmdsys
            global protectedVariables
            global rOnlyVariables
            
            a=None
            b=[]
            c=None
            d=None
            if('[' in args[0]):
                a=args[0].split('[')[0]
                for x in args[0].split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=args[0]

            if args[1]=='attr':
                a=c[d].__getattribute__(args[2])
                if(type(a) in [str,list,dict,tuple,int,float]):
                    return a
                else:
                    return a()

            if args[0].split('[')[0] in rOnlyVariables:
                return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
            if args[0] in protectedVariables:
                return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
            
            if(args[1]=='var'):
                c[d]=getVariableValue(args[2])
            elif(args[1]=='command'):
                c[d]=cmdsys.executeBase(args[2])
            elif(args[1]=='value'):
                c[d]=args[2]
            elif(args[1]=='value_int'):
                c[d]=int(args[2])
            elif(args[1]=='value_float'):
                c[d]=float(args[2])
            elif(args[1]=='append'):
                c[d].append(args[2])
            elif(args[1]=='append_var'):
                c[d].append(getVariableValue(args[2]))
            elif(args[1]=='pop'):
                return c[d].pop(int(args[2]))
            elif(args[1]=='type'):
                if args[2]=='str':
                    c[d]=str(c[d])
                elif args[2]=='int':
                    c[d]=int(c[d])
                elif args[2]=='float':
                    c[d]=float(c[d])
            elif args[1]=='sum':
                m=args[2].split(' ')
                c[d]=sum([getVariableValue(i) for i in m[1:]],m[0])
            elif args[1]=='subtract':
                m=args[2].split(' ')
                c[d]=getVariableValue(m[0])-getVariableValue(m[1])
            elif args[1]=='min':
                m=args[2].split(' ')
                c[d]=min(getVariableValue(m[0]),getVariableValue(m[1]))
            elif args[1]=='max':
                m=args[2].split(' ')
                c[d]=max(getVariableValue(m[0]),getVariableValue(m[1]))
            elif args[1]=='divide':
                m=args[2].split(' ')
                c[d]=getVariableValue(m[0])/getVariableValue(m[1])
            elif args[1]=='multiply':
                m=args[2].split(' ')
                y=1
                for i in m:
                    y*=getVariableValue(i)
                c[d]=y
            elif args[1]=='arrayize':
                try:
                    c[d]=[getVariableValue(args[2])]
                except:
                    c[d]=[]
            if args[1] in ['var','command','value','value_int','value_float','append','append_var','pop','type','sum','subtract','min','max','divide','multiply','arrayize']:
                if a in hooks:
                    cmdsys.executeBase(hooks[a]['cmd'])
        def getVariableCommand(args):
            return getVariableValue(args[0])
        def runFileCommand(args):
            global commandStorages
            commandStorages['args']=args[1].split(' ')
            return executeFile(args[0])
        def runFileCommand_argless(args):
            return executeFile(args[0])

        def getEnemyCommand(args):
            global enemies
            retval=[]

            capAmount=99999999
            startpos=[0,0]
            distanceMin=0
            distanceMax=99999999
            typeRequirements=[]
            l=args[0].split(' ')
            for i in l:
                if(i.split('=')[0]=='x'):
                    startpos[0]=float(i.split('=')[1])
                elif(i.split('=')[0]=='y'):
                    startpos[1]=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_min'):
                    distanceMin=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_max'):
                    distanceMax=float(i.split('=')[1])
                elif(i.split('=')[0]=='c_max'):
                    capAmount=int(i.split('=')[1])
                elif(i.split('=')[0]=='type'):
                    typeRequirements.append(i.split('=')[1])
            for i in enemies:
                dist=((startpos[0]-i.pos[0])**2+(startpos[1]-i.pos[1])**2)**0.5
                if dist/20>=distanceMin:
                    if dist/20<=distanceMax:
                        if typeRequirements!=[]:
                            if type(i).__name__ in typeRequirements:
                                retval.append([i][0])
                                if retval.__len__()>=capAmount:
                                    break
                            
            return retval
        def getPlayerCommand(args):
            global player
            return [player][0]
        def getRenderableObjectCommand(args):
            global all
            retval=[]

            capAmount=99999999
            startpos=[0,0]
            distanceMin=0
            distanceMax=99999999
            typeRequirements=[]
            l=args[0].split(' ')
            for i in l:
                if(i.split('=')[0]=='x'):
                    startpos[0]=float(i.split('=')[1])
                elif(i.split('=')[0]=='y'):
                    startpos[1]=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_min'):
                    distanceMin=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_max'):
                    distanceMax=float(i.split('=')[1])
                elif(i.split('=')[0]=='c_max'):
                    capAmount=int(i.split('=')[1])
                elif(i.split('=')[0]=='type'):
                    typeRequirements.append(i.split('=')[1])
            #print(typeRequirements)
            for i in all:
                dist=((startpos[0]-i.pos[0])**2+(startpos[1]-i.pos[1])**2)**0.5
                if dist/20>=distanceMin:
                    if dist/20<=distanceMax:
                        if typeRequirements!=[]:
                            if type(i).__name__ in typeRequirements:
                                retval.append([i][0])
                                if retval.__len__()>=capAmount:
                                    break
                            else:
                                pass#print(type(i).__name__)

        def checkMatchesVariableValueCommand(args):
            if getVariableValue(args[0])==args[1]:
                return True
            return False
        def checkMatchesVariableVarCommand(args):
            if getVariableValue(args[0])==getVariableValue(args[1]):
                return True
                
            return False
        def checkComparegVariableVarCommand(args):
            if getVariableValue(args[0])>getVariableValue(args[1]):
                return True
            return False
        def checkComparegeqVariableVarCommand(args):
            if getVariableValue(args[0])>=getVariableValue(args[1]):
                return True
            return False
        def checkCompareneqVariableVarCommand(args):
            if getVariableValue(args[0])!=getVariableValue(args[1]):
                return True
            return False
        def checkComparegVariableValueCommand(args):
            if getVariableValue(args[0])>(args[1]):
                return True
            return False
        def checkComparegeqVariableValueCommand(args):
            if getVariableValue(args[0])>=(args[1]):
                return True
            return False
        def checkComparelVariableValueCommand(args):
            if getVariableValue(args[0])<(args[1]):
                return True
            return False
        def checkCompareleqVariableValueCommand(args):
            if getVariableValue(args[0])<=(args[1]):
                return True
            return False
        def checkCompareneqVariableValueCommand(args):
            if getVariableValue(args[0])!=(args[1]):
                return True
            return False
        def invertValue(args):
            return not getVariableValue(args[0])
        def invertCommandResult(args):
            global cmdsys
            return not cmdsys.executeBase(args[0])
        def terminateCommand(args):
            global player,inCmdConsole
            inCmdConsole=-1
            player.kill()

        def conditionalRunCommand(args):
            if(getVariableValue(args[0])):
                cmdsys.executeBase(args[1])

        def conditionalRunCommandWhileLoop(args):
            if(getVariableValue(args[0])):
                cmdsys.executeBase(args[1])
                conditionalRunCommandWhileLoop(args)
        def addProtectedVariableCommand(args):
            global protectedVariables
            protectedVariables.append(args[0])
        def addReadOnlyVariableCommand(args):
            global rOnlyVariables
            rOnlyVariables.append(args[0])
        def getVariables_Object(args):
            return vars(getVariableValue(args[0]))
        def getVariables(args):
            global allVariables
            m=[[allVariables[0][i]] for i in allVariables[0] if i==args[0]]
            if m==[]:
                return None
            return m[0]
        def executeFunction(args):
            global allVariables
            m=[[allVariables[0][i]] for i in allVariables[0] if i==args[0]]
            if m==[]:
                return None
            return m[0]()
        
        def executeCodeSnipCommand(args):
            global allVariables
            for i in codesnippets[args[0]][0]:
                if i in allVariables:
                    vars()[i]=[allVariables[i]][0]
            exec(codesnippets[args[0]][1])
        def executeCodeCommand(args):
            #exec("args[0]=\""+args[0]+"\"")
            global allVariables
            try:
                exec(args[0])
            except Exception as err:
                return err
            
        global allVariables
        allVariables=vars()
        print(allVariables)
        cmdsys.addCommand("tp target:var x:float|var y:float|var",tpCommand)
        cmdsys.addCommand("setGrav x:float|var y:float|var",setGravCommand)
        cmdsys.addCommand("setVel x:float|var y:float|var",setVelocityCommand)
        
        cmdsys.addCommand("player.pos",playerPos)
        cmdsys.addCommand("placeRoom id:str x:int y:int",placeRoomCommand)
        cmdsys.addCommand("\summon id:str x:int_opt y:int_opt",summonCommand)

        
        cmdsys.addCommand("variable varname:str operation:str with:str_greedy",variableCommand)
        cmdsys.addCommand("variable_get varname:str",getVariableCommand)
        cmdsys.addCommand("get_enemy args:str_greedy",getEnemyCommand)
        cmdsys.addCommand("get_object args:str_greedy",getRenderableObjectCommand)
        cmdsys.addCommand("get_player",getPlayerCommand)
        
        cmdsys.addCommand("executeFile filename:str args:str_greedy",runFileCommand)
        cmdsys.addCommand("executeFile_argless filename:str",runFileCommand_argless)

        cmdsys.addCommand("executeCodeSnippet snippetname:str_greedy",executeCodeSnipCommand)
        cmdsys.addCommand("executeCode code:str_greedy",executeCodeCommand)
        
        cmdsys.addCommand("a==b variable:str value:int|float|str",checkMatchesVariableValueCommand)
        cmdsys.addCommand("a==v variable:str var:str",checkMatchesVariableVarCommand)
        cmdsys.addCommand("a>b a:str b:int|float|str",checkComparegVariableValueCommand)
        cmdsys.addCommand("a>=b a:str b:int|float|str",checkComparegeqVariableValueCommand)
        cmdsys.addCommand("a<b a:str b:int|float|str",checkComparelVariableValueCommand)
        cmdsys.addCommand("a<=b a:str b:int|float",checkCompareleqVariableValueCommand)
        cmdsys.addCommand("a!=b a:str b:int|float|str",checkCompareneqVariableValueCommand)

        cmdsys.addCommand("a>v a:str b:str",checkComparegVariableVarCommand)
        cmdsys.addCommand("a>=v a:str b:str",checkComparegeqVariableVarCommand)
        cmdsys.addCommand("a!=v a:str b:str",checkCompareneqVariableVarCommand)

        cmdsys.addCommand("!v v:str",invertValue)
        cmdsys.addCommand("!execute v:str_greedy",invertCommandResult)
        cmdsys.addCommand("?execute c:str v:str_greedy",conditionalRunCommand)
        cmdsys.addCommand("?while c:str v:str_greedy",conditionalRunCommandWhileLoop)
        cmdsys.addCommand("./programTerminate",terminateCommand)
        cmdsys.addCommand("./protectVariable variable:str",addProtectedVariableCommand)
        cmdsys.addCommand("./lockVariable variable:str",addReadOnlyVariableCommand)
        cmdsys.addCommand("getVars variable:str",getVariables_Object)
        cmdsys.addCommand("getVar variable:str",getVariables)
        cmdsys.addCommand("executeVariableFunction variable:str",executeFunction)
        
        












        global cmdconsoletext,cmdconsole,inCmdConsole,cmdconsoledata,chatOldDisplay,chatStorage
        global chatsize
        chatsize=10
        chatOldDisplay=[textRenderer([100,100+20*_],[500,100],GUIelements) for _ in range(chatsize)]
        cmdconsole=textRenderer([100,100+20*chatsize],[500,100],GUIelements)
        cmdconsoletext=""
        cmdconsoledata=[[""],[0,0]]
        chatStorage=[""]*chatsize+["Welcome to the chat!"]
        cmdconsole.setText(cmdconsoletext)
        inCmdConsole=False









        
        enemies = pg.sprite.Group()
    
        # initialize our starting sprites
        #backgroundObject=Background(all)
        #all.change_layer(backgroundObject,-1000)
        global player
        player = Player(all)
        player.pos=[0,-50]
        rooms[0]=Room({'data':["000 000 000 000 000 000 000".replace(' ',''),
                               "000 000 000 000 000 000 000".replace(' ',''),
                               "000 000 000 000 000 000 000".replace(' ',''),
                               "000 000 000 000 000 000 101".replace(' ',''),
                               "000 110 000 000 100 010 010".replace(' ',''),
                               "011 000 000 100 001 000 000".replace(' ',''),
                               "001 001 001 111 001 001 001".replace(' ','')],'palette':[0,1,2,3,4,5,9,-1]},w=7,h=7,id=0,shadowLevel=895)
        rooms[0].setShadows(0)
        rooms[1]=Room({'data':["0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ',''),
                              "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ',''),
                              "0000 0000 0000 0000 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001 0001".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 1000 1000 0001 0001 0001 0001 1000 1000 1000 0001".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 1000 1000 0001 0001 0001 0001 1000 1000 1000 0001".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 1000 0000 0001 0001 0001 0001 0001 0001 0001 0001".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 0000 0111 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 1000 0000 0111 1001 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 1000 0000 0111 1001 1001 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 1000 0000 0111 1001 1001 1001 1001 0011 0000 0000 0000 0000 0000 0101".replace(' ',''),
                              "0000 0000 0000 0000 0001 1000 0000 0111 1001 1001 1001 0100 0001 0001 0001 0000 0000 0000 0001 0001".replace(' ',''),
                              "0000 0000 0000 0000 0001 0000 0111 1001 1001 1001 0100 1000 1000 1000 1000 0000 0000 0000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 0001 0111 1001 1001 1001 0100 1000 1000 1000 1000 1000 0110 0110 0110 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 0111 1001 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 1001 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0101 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                              "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ','')],'palette':[0,1,2,9,4,5,8,7,-1,-2]},w=20,h=20,id=1)
        rooms[1].setShadows(600)
        rooms["tallhallway"]=Room({'data':["0001"*100]+["0001"+"1010"*98+"0001"]*3+["0001"*100]+["1011"*100]*19+["0101"+"1011"*98+"0101"]+["0001"*100]+["0001"+"1010"*98+"0001"]*3+["0001"*100],'palette':[0,1,2,3,4,5,6,7,8,9,-1,-2]},w=100,h=30,id="tallhallway")
        rooms['tallhallway'].setShadows(400)
        rooms[2]=Room({'data':["000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 001 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 001 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 011 000".replace(' ',''),
                              "000 000 001 001 001 000 001 001 001 001 000 000 000 000 000 000 000 001 001 001".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ','')],'palette':[0,1,2,9,4,5,8,10]},w=20,h=20,id=2)
        rooms[2].setShadows(800)
        rooms["spikepit"]=Room({'data':["000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110".replace(' ','')],'palette':[0,1,2,9,4,5,8,7]},w=20,h=20,id="spikepit")
        rooms[0].decompressData()
        rooms[1].decompressData()
        rooms[2].decompressData()
        rooms['spikepit'].decompressData()
        rooms['tallhallway'].decompressData()
        rooms['tallhallway'].link(rooms[0],0,0)
        rooms['tallhallway'].link(rooms[1],1,1)
        rooms[0].link(rooms['tallhallway'],0,0)
        
        rooms[1].link(rooms['tallhallway'],1,1)
        rooms[1].link(rooms[2],1,0)
        rooms[2].link(rooms[1],0,0)
        #rooms[2].link(rooms['spikepit'],1,0)
        splashtext="Loading Complete!"
        pg.time.wait(100)
        import pyautogui
        #i=pyautogui.getWindowsWithTitle('tk')
        #i[0].close()
        
        #splashthread._stop()
        global events
        events=[]
        global scrwidth,scrheight

        cursor=CursorVisual(0,0,16,16,0,GUIelements)
        GUIelements.change_layer(cursor,100000)
        #gamename='???'
        #captionsplashes=['Wait, is that safe?','May the cats win!','Mewo?','Paw. Paw Paw Paw Paw Paw. Meow?']
        #caption=gamename+': '+captionsplashes[random.randrange(captionsplashes.__len__())]
        #pg.display.set_caption(caption)
        #windowsPotential=pyautogui.getWindowsWithTitle(caption)
        #caption=gamename+': '+captionsplashes[random.randrange(captionsplashes.__len__())]
        #pg.display.set_caption(caption)
        global window
        #window=[i for i in windowsPotential if i.title==caption][0]



        for i in range(0):
            for j in range(5):
                newObjects.append([3,160+20*i,0-20*j])
        """
        aChain=CollisionGroup(walls,entities)
        
        
        mtiles=[]
        a=None#movableTile2([200,-150],[80,10],walls,entities,all)
        #a.isSolid=True
        #a.shouldRotate=False
        #a.climbable=False
        #mtiles.append(a)
        for i in range(40,0,-1):
            b=movableTile2([-232.5-0*(i+1),-155+5*(i+3)],[5,5],aChain.objects,all)
            mtiles.append(b)
            b.chainedTo.append(a)
            b.chainedTo.append(a)
            if a!=None:
                if 'chainedTo' in a.__dict__:
                    a.chainedTo.append((b))
            a=b
#            b.gravity[1]=0.01
            b.isSolid=False
            b.climbable=True
            b.shouldRotate=True
        b=Wall(1270-1200-210-100,-150,20,10,0,-1,walls,all)
        #b.isSolid=True
        #b.shouldRotate=False
        #b.climbable=False
        mtiles.append(b)
        #b.gravity[1]*=1.5
        #b.chainLen*=5
        #b.width=20
        #b.height=20
        #b.isSolid=True
        #b.climbable=False
        for ind in range(mtiles.__len__()-1):
            p=[]
            q=[]
            for i in range(mtiles.__len__()):
                if ind!=i:
                    p.append((10*(((ind-i))**2)**0.5,mtiles[i]))
                    if (ind-i) in (1,-1):
                        p[-1]=(*p[-1],True)
                        print(p[-1])
                    elif (ind-i) not in [i for i in range(-50,50) if ((i>-5)&(i<5))]:
                        q.append(mtiles[i])
                    #if ind>i:
                    #    p.append(p[-1])
            mtiles[ind].chainedTo=p
            mtiles[ind].chainedTob=mtiles
        
        a=Wall(-500,140,1000,10,0,-1,walls,all)"""
        Wall(0,-100,50,50,7,-1,all).lightLevel=1
        def updateLoop():
            global pg
            #pg.time.wait(1000)
            
            global key
            global mouse
            global events
            global inCmdConsole
            global winfo,player,enemies,walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks,healthBarRender,newParticles,newObjects,phyicsparticles,playerPewGroup,enemyAttacks
            
            lastFrameStart=time.time()
            frameStart=time.time()+1
            lastFpses=[50,50,50]
            tickCount=0
            #try:
            if 1:
                velocity=textRenderer([100,100],[500,100],GUIelements)
                wasGrabbing=0
                global lastFrameClock
                global allGuis
                while glfwApi.shouldWindowClose()==0:
                    
                    lastFrameClock=time.time()
                    lastFrameStart=frameStart
                    frameStart=time.time()
                    #print('tick is alive')
                    #print('physics')
                    player.add(all)
                    tickCount+=1
                    if tickCount%20==0:
                        velocity.setText(str(int((player.velocity[0]**2+player.velocity[1]**2)**0.5)/20))
                    
                    if builtRooms.__len__()==0:
                        rooms[0].buildRoom([0,0],walls,platforms,all,boundaries,builtRooms,allb)
                        floors=[]
                        #print(all.sprites().__len__())
                    # get input
                    clicks=[]
                    for event in events:
                        #if event.type == pg.QUIT:
                        #    return
                        #if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        #    return
                        #if event.type == pg.KEYDOWN:
                        #    if event.key == pg.K_f:
                        #        if not fullscreen:
                        #            print("Changing to FULLSCREEN")
                        #            screen_backup = screen.copy()
                        #            screen = pg.display.set_mode(
                        #                SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth,vsync=1
                        #            )
                        #            screen.blit(screen_backup, (0, 0))
                        #        else:
                        #            print("Changing to windowed mode")
                        #            screen_backup = screen.copy()
                        #            screen = pg.display.set_mode(
                        #                SCREENRECT.size, winstyle|pg.RESIZABLE, bestdepth,vsync=1
                        #            )
                        #            screen.blit(screen_backup, (0, 0))
                        #        pg.display.flip()
                        #        fullscreen = not fullscreen
                        #print(event)
                        if event[0]=='kpress':
                            if event[3]==0:
                                if(event[1]==glfwApi.glfw.KEY_T):
                                    inCmdConsole=1
                                    cmdsys.executeBase("declare mewo")
                        if event[0]=='mouse':
                            if event[2]==0:
                                clicks.append((event[1],event[3]))
                                print(clicks)
                    #<Event(769-KeyUp {'unicode': 'a', 'key': 97, 'mod': 36864, 'scancode': 4, 'window': None})>,
                    events=[]
                    keystate = pg.key.get_pressed()+[0]*500
                    #print([i for i in range(keystate.__len__()) if keystate[i]==1])
                    #print(keystate)
                    cursorstate = pg.mouse.get_pressed()+[0]*500
                    if inCmdConsole:
                        keystate=[0 for i in keystate]
                        cursorstate=[0 for i in cursorstate]
                    
                    for click in clicks:
                        print(pg.mouse.get_pos(), click[0],click[1])
                    mousePos=(*pg.mouse.get_pos(),1,1)
                    centerX=mousePos[0]
                    centerY=mousePos[1]
                    width=mousePos[2]
                    height=mousePos[3]
                    maetriks=glfwApi.getMatrix()
                    size=glfwApi.getWindowSize()
                    centerX*=640/size[0]
                    centerY*=640/size[1]
                    mousePos=(centerX,centerY,width,height)
                    
                    for gui in allGuis:
                        if gui.isOpen:
                            gui._onTick()
                            for click in clicks:
                                #print(mousePos, click[0],click[1])
                                gui._onClick(mousePos, click[0],click[1])
                    #pg.mouse.get_pos
                    
                    #print(5,[i for i in range(keystate.__len__()) if keystate[i]==1])
                    #x=[i for i in range(keystate.__len__()) if keystate[i]!=0]
                    #if x!=[]:
                    #    print(x)
                    # clear/erase the last drawn sprites
                    #all.clear(screen, background)
            
                    # update all the sprites
                    # handle player input
                    if inCmdConsole==0:
                        horizmove = keystate[68] - keystate[65]
                        #if keystate[68]|keystate[65]:
                        #    print('horizmove',horizmove)
                        jump = keystate[87]
                        down=keystate[83]
                        grab=False
                        if not wasGrabbing:
                            grab=keystate[67]
                        wasGrabbing=keystate[67]
                        #if jump!=0:
                        #    print('jump')
                        #if down!=0:
                        #    print('down')
                        #try:
                        if 1:
                            if down==0:
                                player.updateb([walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,(cursorstate[0],cursorstate[1],keystate[80]),0)
                            else:
                                player.updateb([walls,[],all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,(cursorstate[0],cursorstate[1],keystate[80]),1)
                        #except BaseException as x:
                        #    print('DIE,',x,'- Gleeson Hedge')

                        for i in entities:
                            i.updateb([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup])
                        for i in entities:
                            i.updateb_2([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup])
                        #try:
                        if 1:
                            if down==0:
                                player.updateb_2([walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,(cursorstate[0],cursorstate[1],keystate[80]),0,grab)
                            else:
                                player.updateb_2([walls,[],all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,(cursorstate[0],cursorstate[1],keystate[80]),1,grab)
                                
                        #except BaseException as x:
                        #    print('DIE2,',x,'- Gleeson Hedge')
                        for i in entities:
                            i.updateb_3([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup])
                        #player.jump(jump)
                        healthBarRender.updateV(player.attributes['health'])
                        for i in newParticles:
                            try:
                                if i[2]==[0,0]:
                                    Particle(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]==1,i[7]==2,[0 if i.__len__()<9 else i[8]][0],[0 if i.__len__()<10 else i[9]][0],all,phyicsparticles)
                                else:
                                    PhysicsParticle(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]==1,i[7]==2,[0 if i.__len__()<9 else i[8]][0],[0 if i.__len__()<10 else i[9]][0],all,phyicsparticles)
                            except BaseException as x:
                                print('pspawnerr',x)
                        for i in newObjects:
                            try:
                                if i[0]==0:
                                    all.change_layer(LaPew(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8], all,playerPewGroup),-5)
                                if i[0]==1:
                                    GenericSingleFrameAttack(i[1],i[2],i[3],i[4],i[5], all,enemyAttacks)
                                if i[0]==2:
                                    x=Enemeh(i[1],i[2],enemies,all)
                                    x.textureIds= x.textureIdsAll[i[3]]
                                if i[0]==3:
                                    x=movableTile([i[1],i[2]],walls,entities,all)
                            except BaseException as err:
                                print('new object invalid:',err)
                            newObjects=[]
                        newParticles=[]
                        if(phyicsparticles.sprites().__len__()>1000):
                            phyicsparticles.sprites()[0].kill()
                        for i in phyicsparticles:
                            i.updateb([walls])
                        for i in playerPewGroup:
                            i.updateb([walls])
                            #print('playerpewupdate')
                        
                        for i in enemies:
                            i.updatec([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup],player)
                        all.update()
                        GUIelements.update()
            
                    
                    #collisions?
                    #for alien in pg.sprite.spritecollide(player, aliens, 1):
                    #    if pg.mixer and boom_sound is not None:
                    #        boom_sound.play()
                    #    Explosion(alien, all)
                    #    Explosion(player, all)
                    #    SCORE = SCORE + 1
                    #    player.kill()
            
                    # See if shots hit the aliens.
                    #for alien in pg.sprite.groupcollide(aliens, shots, 1, 1).keys():
                    #    if pg.mixer and boom_sound is not None:
                    #        boom_sound.play()
                    #    Explosion(alien, all)
                    #    SCORE = SCORE + 1
            
                    # draw the scene
                    #dirty = all.draw(screen)
                    #drawAll(all)
                    #drawGUI(GUIelements)
                    #pg.display.flip()#update()#dirty)
            
                    # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
                    
                    global totalCollisionChecks
                    print('\t\t\t\tCollision Checks in Frame:',totalCollisionChecks) #reenable
                    totalCollisionChecks=0
                    clock.tick(FRAMERATE2+5)
                    spf=frameStart-lastFrameStart
                    if spf!=0:
                        fps[0]=1/spf
                    else:
                        fps[0]=100000
                    lastFpses=[fps[0]]+lastFpses
                    lastFpses=lastFpses[:(100)]
                    #print('update',sum(lastFpses)/lastFpses.__len__())
            #except Exception as x:
            #    print(x)
            #finally:
            #    print('untarcabel eror')
        global events2
        events2=[]
        def executeCmdConsoleupdate():
            #pg.time.wait(1000)
            import time
            import pyperclip
            global events2
            global inCmdConsole,cmdconsole,cmdconsoletext,cmdconsoledata,chatOldDisplay,chatStorage
            global chatsize
            global tickingFiles
            horizPos=0
            horizPosCopyDrag=0
            global scrwidth,scrheight
            try:
                while (inCmdConsole!=-1) & 0==glfwApi.shouldWindowClose():
                    #print('Console is alive')
                    #winfo=pg.display.Info()
                    #scrwidth,scrheight=glfwApi.getWindowSize()[0],glfwApi.getWindowSize()[1]
                    #print('console')
                    for event in events2:
                        #if event.type == pg.QUIT:
                        if event[0]=='char':
                            if chr(event[1])=='\r':
                                if horizPos!=horizPosCopyDrag:
                                    horizPosCopyDrag,horizPos=min(horizPosCopyDrag,horizPos),max(horizPosCopyDrag,horizPos)
                                    cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPosCopyDrag]+[i for i in cmdconsoletext][horizPos:])
                                    horizPosCopyDrag=horizPos=horizPosCopyDrag
                                cmdconsoletext=cmdconsoletext[:horizPos]+"\n"+cmdconsoletext[horizPos:]
                                horizPosCopyDrag=horizPos=horizPos+1
                            else:
                                cmdconsoletext=cmdconsoletext[:horizPos]+chr(event[1])+cmdconsoletext[horizPos:]
                                horizPosCopyDrag=horizPos=horizPos+1
                        elif (event[3] == 2)|(event[3] == 1):
                            if event[1] == glfwApi.glfw.KEY_BACKSPACE:
                                if horizPos!=horizPosCopyDrag:
                                    horizPosCopyDrag,horizPos=min(horizPosCopyDrag,horizPos),max(horizPosCopyDrag,horizPos)
                                    cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPosCopyDrag]+[i for i in cmdconsoletext][horizPos:])
                                    horizPosCopyDrag=horizPos=horizPosCopyDrag
                                elif horizPos>0:
                                    cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPos-1]+[i for i in cmdconsoletext][horizPos:])
                                    horizPosCopyDrag=horizPos=horizPos-1
                            elif event[1]==glfwApi.glfw.KEY_ENTER:
                                if event[4]%2==1:
                                    if horizPos!=horizPosCopyDrag:
                                        horizPosCopyDrag,horizPos=min(horizPosCopyDrag,horizPos),max(horizPosCopyDrag,horizPos)
                                        cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPosCopyDrag]+[i for i in cmdconsoletext][horizPos:])
                                        horizPosCopyDrag=horizPos=horizPosCopyDrag
                                    cmdconsoletext=cmdconsoletext[:horizPos]+"\n"+cmdconsoletext[horizPos:]
                                    horizPosCopyDrag=horizPos=horizPos+1
                                else:
                                    x=cmdsys.executeBase(cmdconsoletext)
                                    cmdconsoledata[0].append(cmdconsoletext)
                                    cmdconsoledata[1][1]=cmdconsoledata[0].__len__()
                                    for i in cmdconsoletext.split('\n'):
                                        chatStorage.append(i)
                                    if x!=None:
                                        chatStorage.append(str(x))
                                    cmdconsoletext=""
                                    horizPosCopyDrag=horizPos=0
                                    
                                
    
    
    
    
    
    
                            elif event[1] == glfwApi.glfw.KEY_ESCAPE:
                                cmdconsoletext=""
                                inCmdConsole=False
                                [chatOldDisplay[i].setText("#") for i in range(chatsize)]
                            elif event[1] == glfwApi.glfw.KEY_UP:
                                cmdconsoledata[1][1]=max(0,cmdconsoledata[1][1]-1)
                                cmdconsoletext=cmdconsoledata[0][cmdconsoledata[1][1]]
                            elif event[1] == glfwApi.glfw.KEY_DOWN:
                                cmdconsoledata[1][1]=min(cmdconsoledata[0].__len__(),cmdconsoledata[1][1]+1)
                                if(cmdconsoledata[1][1]!=cmdconsoledata[0].__len__()):
                                    cmdconsoletext=cmdconsoledata[0][cmdconsoledata[1][1]]
                                else:
                                    cmdconsoletext=""
                            elif event[1] == glfwApi.glfw.KEY_LEFT:
                                if event[4]%2==1:
                                    horizPos=max(0,min(cmdconsoletext.__len__(),horizPos-1))
                                else:
                                    horizPos=horizPosCopyDrag=max(0,min(cmdconsoletext.__len__(),horizPos-1))
                            elif event[1] == glfwApi.glfw.KEY_RIGHT:
                                if event[4]%2==1:
                                    horizPos=max(0,min(cmdconsoletext.__len__(),horizPos+1))
                                else:
                                    horizPosCopyDrag=horizPos=max(0,min(cmdconsoletext.__len__(),horizPos+1))
                            elif event[1] in [pg.K_F1  #                F1
    ,pg.K_F2              #    F2
    ,pg.K_F3              #    F3
    ,pg.K_F4              #    F4
    ,pg.K_F5              #    F5
    ,pg.K_F6              #    F6
    ,pg.K_F7              #    F7
    ,pg.K_F8              #    F8
    ,pg.K_F9              #    F9
    ,pg.K_F10             #    F10
    ,pg.K_F11             #    F11
    ,pg.K_F12             #    F12
    ,pg.K_F13             #    F13
    ,pg.K_F14             #    F14
    ,pg.K_F15             #    F15
    ,pg.K_NUMLOCK         #    numlock
    ,pg.K_CAPSLOCK        #    capslock
    ,pg.K_SCROLLOCK       #    scrollock
    ,glfwApi.glfw.KEY_LEFT_SHIFT
    ,glfwApi.glfw.KEY_LEFT_CONTROL
    ,glfwApi.glfw.KEY_LEFT_ALT
    ,glfwApi.glfw.KEY_RIGHT_SHIFT
    ,glfwApi.glfw.KEY_RIGHT_CONTROL
    ,glfwApi.glfw.KEY_RIGHT_ALT
    #,pg.K_RSHIFT          #    right shift
    #,pg.K_LSHIFT          #    left shift
    #,pg.K_RCTRL           #    right control
    #,pg.K_LCTRL           #    left control
    #,pg.K_RALT            #    right alt
    #,pg.K_LALT            #    left alt
    #,pg.K_RMETA           #    right meta
    #,pg.K_LMETA           #    left meta
    #,pg.K_LSUPER          #    left Windows key
    #,pg.K_RSUPER          #    right Windows key
    #,pg.K_MODE            #    mode shift
    #,pg.K_HELP            #    help
    #,pg.K_PRINT           #    print screen
    #,pg.K_SYSREQ          #    sysrq
    #,pg.K_BREAK           #    break
    #,pg.K_MENU            #    menu
    #,pg.K_POWER           #    power
    #,pg.K_EURO            #    Euro
    #,pg.K_AC_BACK
                                              ]:
                                pass
                            else:
                                
                                skip=0
                                if (event[1]==glfwApi.glfw.KEY_C):
                                    if (event[4]%4-event[4]%2)==2:
                                        pyperclip.copy(cmdconsoletext[min(horizPosCopyDrag,horizPos):max(horizPosCopyDrag,horizPos)])
                                        skip=1
                                    elif horizPos!=horizPosCopyDrag:
                                        horizPosCopyDrag,horizPos=min(horizPosCopyDrag,horizPos),max(horizPosCopyDrag,horizPos)
                                        cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPosCopyDrag]+[i for i in cmdconsoletext][horizPos:])
                                        horizPosCopyDrag=horizPos=horizPosCopyDrag
                                elif horizPos!=horizPosCopyDrag:
                                    horizPosCopyDrag,horizPos=min(horizPosCopyDrag,horizPos),max(horizPosCopyDrag,horizPos)
                                    cmdconsoletext=''.join([i for i in cmdconsoletext][:horizPosCopyDrag]+[i for i in cmdconsoletext][horizPos:])
                                    horizPosCopyDrag=horizPos=horizPosCopyDrag
                                if event[1]==glfwApi.glfw.KEY_V:
                                    if (event[4]%4-event[4]%2)==2:
                                        horizPosCopyDrag=horizPos=horizPos+pyperclip.paste().__len__()
                                        cmdconsoletext=cmdconsoletext[:horizPos]+pyperclip.paste().replace('\r','')+cmdconsoletext[horizPos:]
                                        skip=1
                                if skip==0:
                                    pass
                                    #cmdconsoletext=cmdconsoletext[:horizPos]+chr(event[1])+cmdconsoletext[horizPos:]
                                    #horizPosCopyDrag=horizPos=horizPos+1
                            #cmdconsole.setText(cmdconsoletext,[horizPos if (time.time()%1>0.5) else None][0])
                            
                    if(inCmdConsole):
                        if horizPos>horizPosCopyDrag:
                            cmdconsole.setText([cmdconsoletext[i]+'!' if (i>=horizPosCopyDrag)&(i<horizPos) else cmdconsoletext[i] for i in range(cmdconsoletext.__len__())],[horizPos if (time.time()%1>0.5) else None][0])
                        elif horizPos<horizPosCopyDrag:
                            cmdconsole.setText([cmdconsoletext[i]+'!' if (i<horizPosCopyDrag)&(i>=horizPos) else cmdconsoletext[i] for i in range(cmdconsoletext.__len__())],[horizPos if (time.time()%1>0.5) else None][0])
                        else:
                            cmdconsole.setText(cmdconsoletext,[horizPos if (time.time()%1>0.5) else None][0])
                        pass
                        [chatOldDisplay[i].setText(chatStorage[i-chatsize][:100]) for i in range(chatsize)]
                        
                    #<Event(769-KeyUp {'unicode': 'a', 'key': 97, 'mod': 36864, 'scancode': 4, 'window': None})>,
                    events2=[]
                    clock.tick(FRAMERATE2)
                    for f in tickingFiles:
                        executeFile(f)
            except Exception as err:
                print(err,'Console ded')
        global key
        global mouse
        pg.key.get_pressed=glfwApi.getKeys
        pg.mouse.get_pressed=glfwApi.getMouseButtons
        pg.mouse.get_pos=glfwApi.getCursorPos
        pg.display.get_window_size=glfwApi.getWindowSize
        #key=pg.key
        #mouse=pg.mouse
        #cursor = pg.cursors.compile((               #sized 16x16
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"ooooooo.""Xooooooo",
        #"oooooooX"".ooooooo",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       ",
        #"       o""o       "))
        global cursorPos
        cursorPos=pg.mouse.get_pos()
        pg.K_F1=glfwApi.glfw.KEY_F1
        pg.K_F2=glfwApi.glfw.KEY_F2
        pg.K_F3=glfwApi.glfw.KEY_F3
        pg.K_F4=glfwApi.glfw.KEY_F4
        pg.K_F5=glfwApi.glfw.KEY_F5
        pg.K_F6=glfwApi.glfw.KEY_F6
        pg.K_F7=glfwApi.glfw.KEY_F7
        pg.K_F8=glfwApi.glfw.KEY_F8
        pg.K_F9=glfwApi.glfw.KEY_F9
        pg.K_F10=glfwApi.glfw.KEY_F10
        pg.K_F11=glfwApi.glfw.KEY_F11
        pg.K_F12=glfwApi.glfw.KEY_F12
        pg.K_NUMLOCK=glfwApi.glfw.KEY_NUM_LOCK
        pg.K_CAPSLOCK=glfwApi.glfw.KEY_CAPS_LOCK
        pg.K_SCROLLOCK=glfwApi.glfw.KEY_SCROLL_LOCK
        #pg.K_=glfwApi.glfw.KEY_
        def renderLoop(*threads):
            global fps
            global all
            global GUIelements
            global events,events2
            global key
            global mouse
            import time
            global inCmdConsole
            global player,winfo
            global scrwidth,scrheight,window
            global renderCommands
            lastFrameStart=time.time()
            frameStart=time.time()+1
            lastFpses=[50,50,50]
            try:
                while 1:
                    #backgroundObg.add(all)
                    #all.change_layer(backgroundObg,-1000000)

                    #print('Render is alive')
                    #pg.mouse.set_cursor((16, 16), (8, 8), *cursor)
                    #winfo=pg.display.Info()
                    scrwidth,scrheight=glfwApi.getWindowSize()#940,480#window._rect.width,window._rect.height
                    lastFrameStart=frameStart
                    frameStart=time.time()
                    eventsall=glfwApi.get_events()
                    glfwApi.clear_events()
                    #inCmdConsole=0
                    if(inCmdConsole):
                        events2+=eventsall
                    else:
                        events+=eventsall
                    #print(all.sprites().__len__())
                    try:
                        #print('att add renderelements')
                        drawAll(all)
                        #print('yay')
                    except:
                        print('Invalid render sprite!')
                    try:
                        #print('att add guielements')
                        drawGUI(GUIelements)
                        #print('suceed')
                    except:
                        print('Invalid GUI sprite!')
                    try:
                        #print('att render')
                        glfwApi.updateWindow(renderCommands,player.pos,sum(lastFpses)/lastFpses.__len__())
                        #print('WHAT')
                    except Exception as x:
                        print(f'Rendering error!\n{x}')
                    renderCommands=[]
                    pg.display.flip()
                    spf=frameStart-lastFrameStart
                    if spf!=0:
                        fps[0]=1/spf
                    else:
                        fps[0]=100000
                    lastFpses=[fps[0]]+lastFpses
                    lastFpses=lastFpses[:(100)]
                    print('Avg FPS:',int(sum(lastFpses)/lastFpses.__len__()*10)/10) #reenable
                    #print(fps)
                    #clock.tick(FRAMERATE)
                    stopall=0
                    for i in threads:
                        if i._is_stopped==1:
                            print("Bad thread")
                            stopall=1
                    if stopall:
                        for i in threads:
                            if i._is_stopped==0:
                                i._stop()
                        #return
                print('goodclose')
                inCmdConsole=-1
                glfwApi.closeWindow()
            except Exception as x:
                inCmdConsole=-1
                player.kill()
                print(x,'CRASH')
                #print(e)
                glfwApi.closeWindow()
                return
            finally:
                print('wow im good at making untraceable errors')
        for i in cmdsys.commands:
            print(i)
        for i in initFiles:
            executeFile(i)
        scrwidth,scrheight=940,480
        chatthread=threading.Thread(target=executeCmdConsoleupdate)
        chatthread.start()
        updatethread=threading.Thread(target=updateLoop)
        updatethread.start()
        
        







        
        
        #allVariables=[vars()]
        #print(allVariables)
        #renderthread=threading.Thread(target=renderLoop,args=[chatthread,updatethread])
        #renderthread.start()
        #renderthread.join()
        pg.time.wait(100)
        renderLoop(chatthread,updatethread)
        
        #if pg.mixer:
        #    pg.mixer.music.fadeout(1000)
        #pg.time.wait(1000)
    
    
    # call the "main" function if running this script
    if __name__ == "__main__":
        main(pg.OPENGL)
        pg.quit()











#executeCode movableTile.gravity=[0,0]
#executeCode global player,newObjects;newObjects.append([3,player.pos[0]+40,player.pos[1]-20])