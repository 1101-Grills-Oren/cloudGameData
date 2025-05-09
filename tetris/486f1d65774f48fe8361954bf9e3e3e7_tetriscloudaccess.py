#!/usr/bin/env python
#from githubAlt import *
import os
#githubAlt
try:
    import github
except:
    os.system("py -m pip install github")
    import github

token="github_pa""t_11BADMTJI""0X4tKzBI9TZ8H_QEBLPpyG9PIB36""e7oyvCFk6r3""jRy0oU9MxrfHL1MToDMTJVJMYWczobPhHi"
githubAccessor=github.Github(token)
thisUser=githubAccessor.get_user('1101-Grills-Oren');
thisRepo=thisUser.get_repo('cloudGameData');
mainBranch=thisRepo.get_branch('main');
baseDir='tetris';
contents=thisRepo.get_contents(baseDir);
#path=[i for i in contents if i.path=='versions'][0]
#pathType=path.type
file=[i for i in contents if i.path==(baseDir+"/"+'highscores.txt')][0]
contents=file.decoded_content

import base64
import json
def updateHighscoresFile(content):
    contents=thisRepo.get_contents("tetris")
    file=[i for i in contents if i.path==('tetris'+"/"+'highscores.txt')][0]
    x=thisRepo.update_file("tetris/highscores.txt","mewo",json.dumps(content),file.sha)
    
def getHighScores():
    contents=thisRepo.get_contents("tetris")
    file=[i for i in contents if i.path==('tetris'+"/"+'highscores.txt')][0]
    #print(file.decoded_content)
    return json.loads(file.decoded_content)

def mergeHighscoresFile(user,score):
    a=getHighScores()
    b=a
    if(user in b):
        b[user]=max(b[user],score)
    else:
        b[user]=score
    updateHighscoresFile(b)
    
def sortHighScores(scores,count=9999999):
    count+=1
    a=scores;
    b=[[a[i],i] for i in a];
    b.sort();
    c={b[i][1]:b[i][0] for i in range(b.__len__()-1,-1,-1) if ((b.__len__()-i)<count)};
    return c

#END githubAlt

























import threading



import os
import random
from typing import List

import pygame as pg

username=os.getlogin()





# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


# game constants
GAME_TURN=0 
SCREENRECT = pg.Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]


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


# Each type of game object gets an init and an update function.
# The update function is called once per frame, and it is when each object should
# change its current position and state.
#
# The Player object actually gets a "move" function instead of update,
# since it is passed extra information about the keyboard.
def isColliding(a,b):
    return (a[0]<b[2])&(a[2]>b[0])&(a[1]<b[3])&(a[3]>b[1])
class State(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    def __init__(self,x,y,a,b,t,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.transform.scale(self.images[t], (20,20))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[x,y]
        self.groupcenteroffset=[a,b]
        self.type=t
        self.width=20
        self.height=20
        self.inGroup=1
        self.velocity=[0,0]
        self.physicsSteps=0
    def collideAndMove(self,objs):
        self.pos[0]+=self.velocity[0]
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
        #for obj in pg.sprite.spritecollide(self,objs,0):
        #    if(obj.inGroup==0):
        #        objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
        #        if(self.velocity[0]<0):
        #            self.pos[0]=max(objpos[2],self.pos[0])
        #        elif(self.velocity[0]>0):
        #            self.pos[0]=min(self.pos[0],objpos[0]-self.width)
        self.pos[1]+=self.velocity[1]
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
        #for obj in pg.sprite.spritecollide(self,objs,0):
        #    if(obj.inGroup==0):
        #        objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
        #        if(self.velocity[1]<0):
        #            retval
        #            self.pos[1]=max(objpos[3],self.pos[1])
        #        elif(self.velocity[1]>0):
        #            self.pos[1]=min(self.pos[1],objpos[1]-self.height)
        #        self.inGroup=0
        self.velocity=[0,0]
    def isValid(self,objs,ignore=0):
        self.rect.left+=4
        self.rect.top+=4
        self.rect.size=[12,12]
        retval=1
        for obj in pg.sprite.spritecollide(self,objs,0):
            if obj!=self:
                if(obj.inGroup!=1)|ignore:
                    retval=0
        self.rect.left-=4
        self.rect.top-=4
        #self.rect.size=[20,20]
        return retval
    def spinRight(self):
        if(self.inGroup==1):
            self.pos[0]-=self.groupcenteroffset[0]
            self.pos[1]-=self.groupcenteroffset[1]
            self.groupcenteroffset=[self.groupcenteroffset[1],-self.groupcenteroffset[0]]
            self.pos[0]+=self.groupcenteroffset[0]
            self.pos[1]+=self.groupcenteroffset[1]
    def spinLeft(self):
        if(self.inGroup==1):
            self.pos[0]-=self.groupcenteroffset[0]
            self.pos[1]-=self.groupcenteroffset[1]
            self.groupcenteroffset=[-self.groupcenteroffset[1],self.groupcenteroffset[0]]
            self.pos[0]+=self.groupcenteroffset[0]
            self.pos[1]+=self.groupcenteroffset[1]
    def moveRight(self):
        self.velocity[0]=20
    def moveLeft(self):
        self.velocity[0]=-20
    def playerInput(self,s,m):
        valid=1
        if(s==-1):
            self.spinRight()
        elif(s==1):
            self.spinLeft()
        if(m==-1):
            self.moveLeft()
        elif(m==1):
            self.moveRight()
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]

class collisionDetector(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    def __init__(self,x,y,w,h,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image=pg.transform.scale(self.images[0],(w,h))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[x,y]
        self.width=w
        self.height=h
        self.update()
    def getCollisionCount(self,objs):
        x=0
        for obj in pg.sprite.spritecollide(self,objs,0):
            if(obj.inGroup==0):
                x+=1
        return x
    def getCollisionObjs(self,objs):
        x=[]
        for obj in pg.sprite.spritecollide(self,objs,0):
            if(obj.inGroup==0):
                x+=[obj]
        return x
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]





class textButton(pg.sprite.Sprite):
    fonts: List[pg.Surface] = []
    def __init__(self,x,y,w,h,fontid,text,pixelationlevel,scale,color,bgcolor,randlevel,edgeeffect,edgesize,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        font=self.fonts[fontid]
        b=self.fonts[fontid].render(text,True,color)
        s=b.get_rect().size
        b=pg.transform.scale(b,(s[0]*scale,s[1]*scale))
        s=b.get_rect().size
        c=pg.surface.Surface((w,h))
        c.fill(bgcolor)
        c.blit(b,(w/2-s[0]/2,h/2-s[1]/2))
        self.image1 = pg.transform.scale(c, (int(w/pixelationlevel),int(h/pixelationlevel)))
        self.image2 = pg.transform.scale(c, (int(w/pixelationlevel),int(h/pixelationlevel)))
        self.state=0
        self.rect = self.image1.get_rect(midbottom=SCREENRECT.midbottom)
        for i in range(self.rect.size[0]):
            for j in range(self.rect.size[1]):
                b=self.image1.get_at((i,j))
                b2=(min(255,max(0,b[0]+randlevel*(random.random()-0.5))),min(255,max(0,b[1]+randlevel*(random.random()-0.5))),min(255,max(0,b[2]+randlevel*(random.random()-0.5))),int(b[3]/256*2)*255)
                b3=[b[0]/(b[0]+b[1]+b[2]),b[1]/(b[0]+b[1]+b[2]),b[2]/(b[0]+b[1]+b[2])]
                b5=[b[0]/(b[0]+b[1]+b[2]),b[1]/(b[0]+b[1]+b[2]),b[2]/(b[0]+b[1]+b[2])]
                if(i<edgesize):
                    b3[0]+=edgeeffect
                    b3[1]+=edgeeffect
                    b3[2]+=edgeeffect
                elif(j<edgesize):
                    b3[0]+=edgeeffect*2
                    b3[1]+=edgeeffect*2
                    b3[2]+=edgeeffect*2
                if(j>(self.rect.size[1]-1-edgesize)):
                    b3[0]-=edgeeffect*2
                    b3[1]-=edgeeffect*2
                    b3[2]-=edgeeffect*2
                elif(i>(self.rect.size[0]-1-edgesize)):
                    b3[0]-=edgeeffect
                    b3[1]-=edgeeffect
                    b3[2]-=edgeeffect
                if(i<edgesize):
                    b5[0]-=edgeeffect
                    b5[1]-=edgeeffect
                    b5[2]-=edgeeffect
                elif(j<edgesize):
                    b5[0]-=edgeeffect*2
                    b5[1]-=edgeeffect*2
                    b5[2]-=edgeeffect*2
                if(j>(self.rect.size[1]-1-edgesize)):
                    b5[0]+=edgeeffect*2
                    b5[1]+=edgeeffect*2
                    b5[2]+=edgeeffect*2
                elif(i>(self.rect.size[0]-1-edgesize)):
                    b5[0]+=edgeeffect
                    b5[1]+=edgeeffect
                    b5[2]+=edgeeffect
                b4=[min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[0])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[1])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[2])),b2[3]]
                b6=[min(255,max(0,(b2[0]+b2[1]+b2[2])*b5[0])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b5[1])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b5[2])),b2[3]]
                self.image1.set_at((i,j),b4)
                self.image2.set_at((i,j),b6)
        self.image1 = pg.transform.scale(self.image1, (int(w),int(h)))
        self.image2 = pg.transform.scale(self.image2, (int(w),int(h)))
        self.rect = self.image1.get_rect(midbottom=SCREENRECT.midbottom)
        self.image=self.image1
        self.pos=[x,y]
        self.width=w
        self.height=h
        self.update()
    def isPressed(self):
        cursorpos=pg.mouse.get_pos()
        pressed1=pg.mouse.get_pressed()[0]
        cursorhitbox=(cursorpos[0],cursorpos[1],cursorpos[0]+1,cursorpos[1]+1)
        if(pressed1):
            if(isColliding((*self.pos,self.pos[0]+self.width,self.pos[1]+self.height),cursorhitbox)):
                return 1
        return 0
    def isPressedb(self):
        x=self.isPressed()
        y=(x==0)&(self.state==1)
        if(x==1):
            self.image=self.image2
            self.state=1
        else:
            self.image=self.image1
            self.state=0
        self.rect=self.image.get_rect()
        return y
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]







class textDisplay(pg.sprite.Sprite):
    fonts: List[pg.Surface] = []
    def __init__(self,x,y,w,h,fontid,text,pixelationlevel,scale,color,bgcolor,randlevel,edgeeffect,edgesize,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        font=self.fonts[fontid]
        self.pixelationlevel=pixelationlevel
        self.scale=scale
        self.color=color
        self.randlevel=randlevel
        self.edgeffect=edgeeffect
        self.edgesize=edgesize
        self.fontid=fontid
        self.randomseed=random.random()
        sd=random.random()
        random.seed(self.randomseed)
        b=self.fonts[fontid].render(text,True,color)
        s=b.get_rect().size
        b=pg.transform.scale(b,(s[0]*scale,s[1]*scale))
        s=b.get_rect().size
        c=pg.surface.Surface((w,h))
        self.isNoBackground=(bgcolor==None)
        if(bgcolor==None):
            bgcolor=(1,1,1)
        self.bgcolor=bgcolor
        c.fill(bgcolor)
        c.blit(b,(w/2-s[0]/2,h/2-s[1]/2))
        self.image = pg.transform.scale(c, (int(w/pixelationlevel),int(h/pixelationlevel)))
        self.state=0
        if(self.isNoBackground):
            self.image.set_colorkey((1,1,1))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        for i in range(self.rect.size[0]):
            for j in range(self.rect.size[1]):
                b=self.image.get_at((i,j))
                b2=(min(255,max(0,b[0]+randlevel*(random.random()-0.5))),min(255,max(0,b[1]+randlevel*(random.random()-0.5))),min(255,max(0,b[2]+randlevel*(random.random()-0.5))),int(b[3]/256*2)*255)
                b3=[b[0]/(b[0]+b[1]+b[2]),b[1]/(b[0]+b[1]+b[2]),b[2]/(b[0]+b[1]+b[2])]
                b4=[min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[0])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[1])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[2])),b2[3]]
                self.image.set_at((i,j),b4)
        self.image = pg.transform.scale(self.image, (int(w),int(h)))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.image=self.image
        self.pos=[x,y]
        self.width=w
        self.height=h
        self.update()
        random.seed(sd)
    def updateV(self,text):

        lines=text.count('\n')
        linespacing=self.scale*20
        pixelationlevel=self.pixelationlevel
        scale=self.scale
        color=self.color
        bgcolor=self.bgcolor
        randlevel=self.randlevel
        edgeeffect=self.edgeffect
        edgesize=self.edgesize
        sd=random.random()
        random.seed(self.randomseed)
        fontid=self.fontid
        font=self.fonts[fontid]
        c=pg.surface.Surface((self.width,self.height))
        if bgcolor.__len__()<4:
            c.fill(bgcolor)
        else:
            if(bgcolor[3]>0):
                c.fill(bgcolor)
            else:
                c.fill((1,1,1,0))
                c.set_colorkey((1,1,1))
        line=0
        for text in text.split('\n'):
            b=self.fonts[fontid].render(text,True,color)
            s=b.get_rect().size
            b=pg.transform.scale(b,(s[0]*scale,s[1]*scale))
            s=b.get_rect().size
            c.blit(b,(self.width/2-s[0]/2,self.height/2-s[1]/2-lines*linespacing/2+line*linespacing))
            line+=1
        self.image = pg.transform.scale(c, (int(self.width/pixelationlevel),int(self.height/pixelationlevel)))
        
        if(self.isNoBackground):
            self.image.set_colorkey((1,1,1))
        self.state=0
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        for i in range(self.rect.size[0]):
            for j in range(self.rect.size[1]):
                b=self.image.get_at((i,j))
                b2=(min(255,max(0,b[0]+randlevel*(random.random()-0.5))),min(255,max(0,b[1]+randlevel*(random.random()-0.5))),min(255,max(0,b[2]+randlevel*(random.random()-0.5))),int(b[3]/256*2)*255)
                b3=[b[0]/(b[0]+b[1]+b[2]),b[1]/(b[0]+b[1]+b[2]),b[2]/(b[0]+b[1]+b[2])]
                b4=[min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[0])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[1])),min(255,max(0,(b2[0]+b2[1]+b2[2])*b3[2])),b2[3]]
                self.image.set_at((i,j),b4)
        self.image = pg.transform.scale(self.image, (int(self.width),int(self.height)))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.image=self.image
        self.update()
        random.seed(sd)
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]


















class Background(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    def __init__(self,x,y,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.transform.scale(self.images[0], (20,20))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[x,y]
        self.width=20
        self.height=20
        self.value=0
        self.image
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]



class YouLoseNote(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    def __init__(self,image,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[0,0]
        self.width=self.rect.size[0]
        self.height=self.rect.size[1]
    def setImage(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.width=self.rect.size[0]
        self.height=self.rect.size[1]
        self.update()
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
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
def getPoints(objs,objs2,objs3):
    shiftDownAmount=0
    for i in objs:
        if i.getCollisionCount(objs2)==width:
            b=i.getCollisionObjs(objs2)
            for j in b:
                j.inGroup=-1
                j.remove(objs2)
                j.add(objs3)
                j.type-=tileTypes.__len__()-1
                j.image=pg.transform.scale(j.images[j.type],(20,20))
                j.rect=j.image.get_rect()
                j.rect.left=j.pos[0]
                j.rect.top=j.pos[1]
            shiftDownAmount=shiftDownAmount+1
            print(shiftDownAmount)
        else:
            c=i.getCollisionObjs(objs2)
            for j in c:
                j.physicsSteps+=shiftDownAmount
    return (shiftDownAmount**2+shiftDownAmount)/2*100
import random
global width,height
width=10
height=30
global tileTypes











import subprocess
































def main(winstyle=0):
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
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode([420,620], winstyle, bestdepth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    alts=[(25,25,25)]+[(125,125,125)]*0+[(0,255,255),(0,0,255),(255,120,0),(255,255,0),(0,255,0),(255,0,255),(255,0,0)]*1
    #alts=[(25,25,25),(127,0,255),(63,0,127),(200,0,255),(127,0,200),(107,0,225),(127,0,255),(119,0,209)]
    global tileTypes
    tileTypes=[
        [
            (0,0,0,0,0),
            (0,0,1,0,0),
            (0,1,0,1,0),
            (0,0,1,0,0),
            (0,0,0,0,0)
        ]
    ]*0+1*[
        [
            (0,0,0,0,0),
            (0,0,0,0,0),
            (0,1,1,1,1),
            (0,0,0,0,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,1,0,0,0),
            (0,1,1,1,0),
            (0,0,0,0,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,0,0,1,0),
            (0,1,1,1,0),
            (0,0,0,0,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,0,0,0,0),
            (0,0,1,1,0),
            (0,0,1,1,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,0,0,0,0),
            (0,0,1,1,0),
            (0,1,1,0,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,0,1,0,0),
            (0,1,1,1,0),
            (0,0,0,0,0),
            (0,0,0,0,0)
        ],
        [
            (0,0,0,0,0),
            (0,0,0,0,0),
            (0,1,1,0,0),
            (0,0,1,1,0),
            (0,0,0,0,0)
        ]
    ]
    images2=[]
    images3=[]
    #imagevalues=[(0, 0, 0, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (0, 0, 0, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 132, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (0, 0, 0, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (0, 0, 0, 255), (0, 0, 0, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (146, 146, 146, 255), (0, 0, 0, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 132, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 132, 255), (131, 131, 132, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 132, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (111, 111, 111, 255), (163, 163, 163, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (111, 111, 111, 255), (0, 0, 0, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (128, 128, 128, 255), (0, 0, 0, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (26, 26, 26, 255), (46, 46, 46, 255), (46, 46, 46, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (26, 26, 26, 255), (46, 46, 46, 255), (46, 46, 46, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (113, 113, 113, 255), (113, 113, 113, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (26, 26, 26, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 0, 0, 255), (113, 113, 113, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 0, 0, 255), (255, 139, 0, 255), (255, 99, 0, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 99, 0, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (0, 0, 0, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (124, 124, 124, 255), (0, 0, 0, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 132, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (118, 118, 118, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (131, 131, 131, 255), (149, 149, 149, 255), (0, 0, 0, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (139, 139, 139, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 255, 0, 255), (0, 255, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)]
    imagevaluesid=0
    value=[]
    displayBottom=1
    for i in alts:
        images2.append(pg.Surface((20,20)))
        images2[-1].fill(i)
        for x in range(20):
            for y in range(20):
                v=images2[-1].get_at((x,y))
                
                
                u=0
                if(x<3):
                    u=20
                if(x>16):
                    u=-20
                if(y<3):
                    if(y<x):
                        if(y<(20-x)):
                            u=40
                    
                if(y>16):
                    if((19-y)<=x):
                        if((20-y)<(20-x)):
                            u=-40

                
                images2[-1].set_at((x,y),(min(max(v[0]+u,0),255),min(max(v[1]+u,0),255),min(max(v[2]+u,0),255)))
    if displayBottom:
        for i in alts[1:]:
            images2.append(pg.Surface((20,20)))
            images2[-1].fill((0,0,0))
            images2[-1].set_colorkey((0,0,0))
            for x in range(20):
                for y in range(20):
                    u=0
                    if(x<3):
                        u=1
                    if(x>16):
                        u=1
                    if(y<3):
                        u=1
                    if(y>16):
                        u=1
                    if(u!=0):
                        images2[-1].set_at((x,y),i)
            images2[-1].set_alpha(127)
    for i in range(tileTypes.__len__()):
        images3.append(pg.mask.Mask((5,5)))
        for x in range(5):
            for y in range(5):
                images3[-1].set_at((x,y),tileTypes[i][x][y])
    State.images = images2
    
    bg=pg.surface.Surface((1000,1000))
    bg.fill((0,0,0))
    bg.set_alpha(100)
    Background.image = [bg]
    collisionDetector.images = [images2[2]]
    textButton.fonts=[pg.font.Font(None,40)]
    textDisplay.fonts=[pg.font.Font(None,40)]
    # decorate the game window
    #icon = pg.transform.scale(Alien.images[0], (32, 32))
    pg.display.set_icon(pg.transform.scale(images2[1],(32,32)))
    pg.display.set_caption("Tetris")
    #pg.mouse.set_visible(0)

    # create the background, tile the bgd image
    pg.display.flip()

    # load the sound effects
    #sound_id=load_sound(filename)
    #if pg.mixer:
    #    music = os.path.join(main_dir, "data", "house_lo.wav")
    #    pg.mixer.music.load(music)
    #    pg.mixer.music.play(-1)

    # Initialize Game Groups
    pressableMoves = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()
    all_losescreen = pg.sprite.RenderUpdates()
    all_mainmenu = pg.sprite.LayeredUpdates()
    all_highscores = pg.sprite.LayeredUpdates()

    # Create Some Starting Values
    clock = pg.time.Clock()
    bg1 = pg.surface.Surface((20,20))
    # initialize our starting sprites
    tiles=pg.sprite.Group()
    vanishtiles=pg.sprite.Group()
    playing=0
    playergroup=[]
    playergroup2=[]
    nextplayergroup=[]
    nextTile=random.randrange(tileTypes.__len__())
    collisionDetectors=[]
    score=0
    
    for i in range(height+1):
        State(0,i*20,0,0,0,all,tiles).inGroup=2
        if(i!=0):
            collisionDetectors.append(collisionDetector(29,height*20-i*20+9,width*20-18,2,all))
        State(220,i*20,0,0,0,all,tiles).inGroup=2
    #for x in range(5):
    #    for y in range(5):
    #        if(tileTypes[nextTile][x][y]):
    #            playergroup.append(State(60+20*x,20+20*y,20*x-40,20*y-40,nextTile+1,all,tiles))
    #            playergroup[-1].inGroup=1
    #for i in playergroup:
    #    playergroup2.append(State(i.pos[0],i.pos[1],0,0,i.type+tileTypes.__len__(),all))
    #    playergroup2[-1].inGroup=1
    nextTile=random.randrange(tileTypes.__len__())
    
    for i in range(width):
        State(i*20+20,height*20,0,0,0,all,tiles).inGroup=2
    for i in range(7):
        State(i*20+width*20+40,0,0,0,0,all).inGroup=1
        State(i*20+width*20+40,20*6,0,0,0,all).inGroup=1
        State(i*20+width*20+40,20*7,0,0,0,all).inGroup=1
    for i in range(5):
        State(20*6+width*20+40,i*20+20,0,0,0,all).inGroup=1
        State(width*20+40,i*20+20,0,0,0,all).inGroup=1
    frame=0
    pg.key.set_repeat(0,500)
    pressedKeys1=[0,0,0,0,0]

    lastPlaying=-1


    scoreDisplay=textDisplay(width*20+40,20*6,20*7,40,0,str(int(score)),2,1,(0,255,0),None,0,0,0,all)


    potentialBadness=0
    screenshot=pg.surface.Surface((420,620))
    youLoseDisplayBackground=YouLoseNote(screenshot,all_losescreen)
    a=240
    b=40
    s=50
    retryButton=textButton(420/2-a/2,620/2-b/2-s,a,b,0,"Retry",2,1.2,(25,25,25),(127,127,127),0,0.1,3,all_losescreen)
    playButton=textButton(420/2-a/2,620/2-b/2-s,a,b,0,"Play",2,1,(25,255,25),(127,127,127),0,0.1,3,all_mainmenu)
    highScoresButton=textButton(420/2-a/2,620/2-b/2,a,b,0,"Highscores",2,1,(25,255,25),(127,127,127),0,0.1,3,all_mainmenu)
    quitButton=textButton(420/2-a/2,620/2-b/2+s,a,b,0,"Quit",2,1.2,(25,25,25),(127,127,127),0,0.1,3,all_losescreen)
    quitButton2=textButton(420/2-a/2,620/2-b/2+s,a,b,0,"Quit",2,1,(25,255,25),(127,127,127),0,0.1,3,all_mainmenu)
    toMainMenuButton=textButton(420/2-a/2,620/2-b/2,a,b,0,"To Main Menu",2,1,(25,25,25),(127,127,127),0,0.1,3,all_losescreen)
    toMainMenuButtonHighscores=textButton(20,20,a,b,0,"To Main Menu",2,1,(25,25,25),(127,127,127),0,0.1,3,all_highscores)
    highScores=textDisplay(20,70,400-20,620-70-20,0,"LOADING",2,1,(25,255,25),None,0,0,0,all_highscores)
    while 1:
        print(playing)
        frame+=1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen
        if (playing==0):
            if(1):
                playButton.add(all_mainmenu)
                all_mainmenu.update()
                if(1):
                    if(playButton.isPressed()):
                        all.update()
                        all.draw(screen)
                        playing=1
                        for i in playergroup:
                            i.kill()
                        for i in playergroup2:
                            i.kill()
                        for i in nextplayergroup:
                            i.kill()
                        playergroup=[]
                        playergroup2=[]
                        nextplayergroup=[]
                        tiles2=[]
                        for i in tiles:
                            i.kill()
                        tiles=pg.sprite.Group()
                        for i in all.sprites():
                            if(type(i)==State):
                                i.kill()
                        for i in range(width):
                            State(i*20+20,height*20,0,0,0,all,tiles).inGroup=2
                        for i in range(7):
                            State(i*20+width*20+40,0,0,0,0,all).inGroup=1
                            State(i*20+width*20+40,20*6,0,0,0,all).inGroup=1
                            State(i*20+width*20+40,20*7,0,0,0,all).inGroup=1
                        for i in range(5):
                            State(20*6+width*20+40,i*20+20,0,0,0,all).inGroup=1
                            State(width*20+40,i*20+20,0,0,0,all).inGroup=1
                        for i in range(height+1):
                            State(0,i*20,0,0,0,all,tiles).inGroup=2
                            State(220,i*20,0,0,0,all,tiles).inGroup=2
                        scoreDisplay.add(all)
                    if(quitButton2.isPressed()):
                        return
                    if(highScoresButton.isPressed()):
                        playing=4
                        n=getHighScores()
                        thisScore=None
                        if(username in n):
                            thisScore=n[username]
                        n=sortHighScores(n,5)
                        b="Highscores"
                        inHighscores=0
                        for i in n:
                            b+="\n"
                            b+=str(b.count('\n'))+". "+i+" - "+str(n[i])+" pts"
                            if(i==username):
                                inHighscores=1
                                b+=' (You)'
                        while(b.count('\n')<6):
                            b+='\n-'
                        if thisScore!=None:
                            if(inHighscores==0):
                                b+="\n"+username+" - "+str(thisScore)+" pts (You)"
                        highScores.updateV(b)
        if(playing==4):
            if(toMainMenuButtonHighscores.isPressedb()):
                playing=0
        if(playing==2):
            if 1:
                if(retryButton.isPressedb()):
                    all.update()
                    all.draw(screen)
                    playing=1
                    for i in playergroup:
                        i.kill()
                    for i in playergroup2:
                        i.kill()
                    for i in nextplayergroup:
                        i.kill()
                    playergroup=[]
                    playergroup2=[]
                    nextplayergroup=[]
                    tiles2=[]
                    for i in tiles:
                        i.kill()
                    tiles=pg.sprite.Group()
                    for i in all.sprites():
                        if(type(i)==State):
                            i.kill()
                    for i in range(width):
                        State(i*20+20,height*20,0,0,0,all,tiles).inGroup=2
                    for i in range(7):
                        State(i*20+width*20+40,0,0,0,0,all).inGroup=1
                        State(i*20+width*20+40,20*6,0,0,0,all).inGroup=1
                        State(i*20+width*20+40,20*7,0,0,0,all).inGroup=1
                    for i in range(5):
                        State(20*6+width*20+40,i*20+20,0,0,0,all).inGroup=1
                        State(width*20+40,i*20+20,0,0,0,all).inGroup=1
                    for i in range(height+1):
                        State(0,i*20,0,0,0,all,tiles).inGroup=2
                        State(220,i*20,0,0,0,all,tiles).inGroup=2
                    scoreDisplay.add(all)
                if(quitButton.isPressedb()):
                    return
                if(toMainMenuButton.isPressedb()):
                    playing=0
                    
        if(playing==1):
            isInvalid=0
            if(playergroup!=[]):
                for i in playergroup:
                    isInvalid=isInvalid+1-i.isValid(tiles,1)
                    print(i.isValid(tiles))
                if(isInvalid):
                    all.draw(screenshot)
                    youLoseDisplayBackground.setImage(screenshot)
                    playing=2
                    #subprocess.Popen("py -m githubAlt "+username+" "+str(int(score)))
                    threading.Thread(target=lambda:mergeHighscoresFile(username,int(score))).start()











            
            keystate = pg.key.get_pressed()
            #print([pg.key.name(i) for i in range(keystate.__len__()) if i==1])
            pressedKeys=[keystate[i] for i in [pg.K_UP,pg.K_DOWN,pg.K_RIGHT,pg.K_LEFT,pg.K_SPACE]]
            if(pressedKeys[0]==0):
                pressedKeys1[0]=0
            if(pressedKeys[1]==0):
                pressedKeys1[1]=0
            if(pressedKeys[2]==0):
                pressedKeys1[2]=0
            if(pressedKeys[3]==0):
                pressedKeys1[3]=0
            if(pressedKeys[4]==0):
                pressedKeys1[4]=0
            pressedKeys1[0]+=pressedKeys[0]
            pressedKeys1[1]+=pressedKeys[1]
            pressedKeys1[2]+=pressedKeys[2]
            pressedKeys1[3]+=pressedKeys[3]
            pressedKeys1[4]+=pressedKeys[4]
            print(pressedKeys1)
            pressedKeys=[i==1 for i in pressedKeys1]
            for i in range(4):
                if(pressedKeys1[i]>=1):
                    pressedKeys1[i]=-39
            
            if(pressedKeys1[4]>=1):
                pressedKeys1[4]=0
            print(pressedKeys1)
            isInvalid=0
            if(1):
                    action0=pressedKeys[0]-pressedKeys[1]
                    action1=pressedKeys[2]-pressedKeys[3]
                    isInvalid=0
                    for i in playergroup:
                        i.playerInput(action0,action1)
                    for i in playergroup:
                        isInvalid=isInvalid+1-i.isValid(tiles)
                    if(isInvalid):
                        for i in playergroup:
                            i.playerInput(-action0,action1)
                    if(pressedKeys[4]==2)&(playergroup2!=[]):
                        for i in playergroup:
                            i.kill()
                            del i
                        playergroup=playergroup2
                        for i in playergroup:
                            i.type-=tileTypes.__len__()
                            i.image= pg.transform.scale(i.images[i.type], (20,20))
                            i.rect = i.image.get_rect(midbottom=SCREENRECT.midbottom)
                            i.rect.left=i.pos[0]
                            i.rect.top=i.pos[1]
                            i.add(tiles)
                        playergroup2=[]
            direction=0
            if playergroup!=[]:
                direction=playergroup[0].velocity[0]
            for i in playergroup:
                if i.inGroup==1:
                    i.collideAndMove(tiles)
            isInvalid=0
            for i in playergroup:
                isInvalid=isInvalid+1-i.isValid(tiles)
            if(isInvalid):
                for i in playergroup:
                    i.pos[0]-=direction


            if(action0!=0)|(action1!=0):
                if 0==isInvalid:
                    for i in playergroup2:
                        i.kill()
                        del i
                    playergroup2=[]
                    for i in playergroup:
                        playergroup2.append(State(i.pos[0],i.pos[1],0,0,i.type+tileTypes.__len__(),all))
                        i.inGroup=1

                    isInvalid=0
                    iter=0
                    while (isInvalid==0)&(iter<height):
                        iter+=1
                        direction=0
                        if playergroup2!=[]:
                            direction=20
                        for i in playergroup2:
                            i.velocity[1]=20
                            i.collideAndMove(tiles)
                        isInvalid=0
                        for i in playergroup2:
                            isInvalid=isInvalid+1-i.isValid(tiles)
                        if(isInvalid):
                            for i in playergroup2:
                                i.pos[1]-=direction

            

            direction=0
            if playergroup!=[]:
                direction=playergroup[0].velocity[1]
                if(frame%10==0)|(pressedKeys[4]):
                    direction=20
            for i in playergroup:
                if i.inGroup==1:
                    if(frame%10==0)|(pressedKeys[4]):
                        i.velocity[1]=20
                    i.collideAndMove(tiles)
            for i in tiles:
                if i.physicsSteps>=1:
                    if(frame%10==0)|(pressedKeys[4]):
                        i.velocity[1]=20
                        i.physicsSteps-=1
                    i.collideAndMove(tiles)
            isInvalid=0
            for i in playergroup:
                isInvalid=isInvalid+1-i.isValid(tiles)
            
            if(isInvalid):
                for i in playergroup:
                    i.pos[1]-=direction
                    i.inGroup=0
                    print('clear')
                    i.add(tiles)
                playergroup=[]
            if(frame%10)==0:
                for i in vanishtiles:
                    i.kill()
                    del i
            if(frame%10==5):
                if playergroup==[]:
                    potentialBadness=1
                    playergroup=nextplayergroup
                    nextplayergroup=[]
                    for i in playergroup:
                        i.pos[0]-=20*width
                        i.inGroup=1
                    for i in playergroup2:
                        i.kill()
                        del i
                    playergroup2=[]
                    for i in playergroup:
                        playergroup2.append(State(i.pos[0],i.pos[1],0,0,i.type+tileTypes.__len__(),all))
                        playergroup2[-1].inGroup=1

                    isInvalid=0
                    iter=0
                    while (isInvalid==0)&(iter<height):
                        iter+=1
                        direction=0
                        if playergroup2!=[]:
                            direction=20
                        for i in playergroup2:
                            i.inGroup=1
                            i.velocity[1]=20
                            i.collideAndMove(tiles)
                        isInvalid=0
                        for i in playergroup2:
                            isInvalid=isInvalid+1-i.isValid(tiles)
                        if(isInvalid):
                            for i in playergroup2:
                                i.pos[1]-=direction
                    #isInvalid=0
                    #for i in playergroup:
                    #    isInvalid=isInvalid+1-i.isValid(tiles,1)
                    #    print('validationcheckb',isInvalid,i.isValid(tiles,1))
                    #if(isInvalid):
                    #    all.draw(screenshot)
                    #    youLoseDisplayBackground.setImage(screenshot)
                    #    playing=2












                
                if(nextplayergroup==[]):
                    for x in range(5):
                        for y in range(5):
                            if(tileTypes[nextTile][x][y]):
                                nextplayergroup.append(State(20*width+60+20*x,20+20*y,20*x-40,20*y-40,nextTile+1,all,tiles))
                    nextTile=random.randrange(tileTypes.__len__())
                score1=score
                if(pressedKeys[4]==0):
                    score+=getPoints(collisionDetectors,tiles,vanishtiles)
                if(score!=score1):
                    scoreDisplay.updateV(str(int(score)))
            
            # clear/erase the last drawn sprites
            #all.clear(screen, bg1)
    
            # update all the sprites

        if(playing!=-1):
            #screen.blit(pg.transform.scale(bg1,(5000,5000)),(0,0))
            screen.blit(bg,(0,0))
        if(playing==1):
            all.update()
            dirty=all.draw(screen)
            if playing!=lastPlaying:
                lastPlaying=playing
                scoreDisplay=textDisplay(width*20+40,20*6,20*7,40,0,str(int(score)),2,1,(0,255,0),None,0,0,0,all)
                score=0
        elif(playing==2):
            
            all_losescreen.update()
            dirty=all_losescreen.draw(screen)
            
            if playing!=lastPlaying:
                lastPlaying=playing
        elif(playing==0):
            all_mainmenu.update()
            dirty=all_mainmenu.draw(screen)
            
            if playing!=lastPlaying:
                lastPlaying=playing
        elif(playing==4):
            all_highscores.update()
            dirty=all_highscores.draw(screen)
            
            if playing!=lastPlaying:
                lastPlaying=playing
        pg.display.flip()
        decaytime=1
        clock.tick(40)

    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()
