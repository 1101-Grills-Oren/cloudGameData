from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.GL import shaders
import pygame as pg
import glfw
import freetype
from pyglm import glm as glm

import numpy as np
from numpy import array
from PIL import Image
import math
import time


fontfile = "Vera.ttf"
fontfile = r'M:\fonts\arial.ttf'

class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')

class TextureSlot:
    def __init__(self, texture, size):
        self.texture = texture
        self.textureSize = (size[0],size[1])
def _get_rendering_buffer(xpos, ypos, w, h, zfix=0.0):
    return np.asarray([
        xpos,     ypos - h, 0, 0,
        xpos,     ypos,     0, 1,
        xpos + w, ypos,     1, 1,
        xpos,     ypos - h, 0, 0,
        xpos + w, ypos,     1, 1,
        xpos + w, ypos - h, 1, 0
    ], np.float32)
def _get_rendering_bufferb(xpos, ypos, w, h, zfix=0.0):
    return np.asarray([
        xpos,     ypos - h, 0, 0,
        xpos,     ypos,     0, -h,
        xpos + w, ypos,     w, -h,
        xpos,     ypos - h, 0, 0,
        xpos + w, ypos,     w, -h,
        xpos + w, ypos - h, w, 0
    ], np.float32)

def _get_rendering_buffer_textured(xpos, ypos, w, h,texX,texY,texW,texH, zfix=0.0):
    return np.asarray([
        xpos,     ypos - h, texX, texY,
        xpos,     ypos,     texX, texY+texH,
        xpos + w, ypos,     texX+texW, texY+texH,
        xpos,     ypos - h, texX, texY,
        xpos + w, ypos,     texX+texW, texY+texH,
        xpos + w, ypos - h, texX+texW, texY
    ], np.float32)

def _get_rendering_buffer_quad(x1, y1, x2,y2,x4,y4,x3,y3, zfix=0.0):
    return np.asarray([
        x1, y1, 0, 0,
        x2, y2,     0, 1,
        x4, y4,     1, 1,
        x1, y1, 0, 0,
        x4, y4,     1, 1,
        x3, y3, 1, 0
    ], np.float32)

def _get_rendering_buffer_quad_textured(x1, y1, x2,y2,x4,y4,x3,y3,tx1, ty1, tx2,ty2,tx4,ty4,tx3,ty3, zfix=0.0):
    return np.asarray([
        x1, y1, tx1, ty1,
        x2, y2,     tx2, ty2,
        x4, y4,     tx4, ty4,
        x1, y1, tx1, ty1,
        x4, y4,     tx4, ty4,
        x3, y3, tx3, ty3
    ], np.float32)







VERTEX_SHADER = """
        #version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;

        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            TexCoords = vertex.zw;
        }
       """


FRAGMENT_SHADER_WAVE = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            vec2 TexCoords2=TexCoords+vec2(sin(TexCoords.y*64+(time)*2)/64/3,0);
            vec4 sampled = vec4(texture(text, TexCoords2).r, texture(text, TexCoords2).g, texture(text, TexCoords2).b, texture(text, TexCoords2).a);
            color = vec4(1,1,1, 1.0) * sampled;
            
        }
        """
FRAGMENT_SHADER_COLORCONVOLVE = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;
        const float offset = 1.0 / 640.0;  
        void main()
        {   
            vec2 offsets[9] = vec2[](
                vec2(-offset,  offset), // top-left
                vec2( 0.0f,    offset), // top-center
                vec2( offset,  offset), // top-right
                vec2(-offset,  0.0f),   // center-left
                vec2( 0.0f,    0.0f),   // center-center
                vec2( offset,  0.0f),   // center-right
                vec2(-offset, -offset), // bottom-left
                vec2( 0.0f,   -offset), // bottom-center
                vec2( offset, -offset)  // bottom-right    
            );
            float kernel[9] = float[](
                 -1,  -1,  -1,
                 -1,   8,  -1,
                 -1,  -1,  -1
            );
            vec3 sampleTex[9];
            for(int i = 0; i < 9; i++)
            {
                sampleTex[i] = vec3(texture(text, TexCoords.xy + offsets[i]));
            }
            vec3 col = vec3(0.0);
            for(int i = 0; i < 9; i++)
                col += sampleTex[i] * kernel[i];

            
            //vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            //color = vec4(1,1,1, 1.0) * sampled;
            color=vec4(1,1,1, 1.0) *vec4(col.x,col.y,col.z,1);
            
        }
        """

FRAGMENT_SHADER_COPY = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            color = vec4(1,1,1, 1.0) * sampled;
            
        }
        """

VERTEX_SHADER_TO_FROM = """
        #version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;
        uniform vec4 fromRect;
        
        uniform mat4 projection;
        uniform vec4 toRect;
        
        void main()
        {
            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            gl_Position.x=gl_Position.x/640*toRect[2]+toRect[0];
            gl_Position.y=gl_Position.y/640*toRect[3]+toRect[1];
            TexCoords =vec2(vertex.z*fromRect[2]+fromRect[0],vertex.w*fromRect[3]+fromRect[1]);
        }
       """

FRAGMENT_SHADER_BLIT_COLORKEY = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform vec3 colorkey;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            color = vec4(1,1,1, 1.0) * sampled;
            if(sampled.xyz==colorkey){
                color=vec4(0,0,0,0);
            }
        }
        """

FRAGMENT_SHADER_COPY_TORIGHTFROMLEFT = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            if(TexCoords.x<0.5){discard;}
            vec2 TexCoords2=TexCoords;
            TexCoords2.x-=0.5;
            vec4 sampled = vec4(texture(text, TexCoords2).r, texture(text, TexCoords2).g, texture(text, TexCoords2).b, texture(text, TexCoords2).a);
            color = vec4(sampled.xyz,1);
            
        }
        """
FRAGMENT_SHADER_COPY_TOLEFTFROMRIGHT = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            if(TexCoords.x>0.5){discard;}
            vec2 TexCoords2=TexCoords;
            TexCoords2.x+=0.5;
            vec4 sampled = vec4(texture(text, TexCoords2).r, texture(text, TexCoords2).g, texture(text, TexCoords2).b, texture(text, TexCoords2).a);
            color = vec4(sampled.xyz,1);
            
        }
        """


FRAGMENT_SHADER_SUM = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform sampler2D texta;

        void main()
        {   
            vec4 sampled1 = vec4(texture(texta, TexCoords).r, texture(texta, TexCoords).g, texture(texta, TexCoords).b, texture(texta, TexCoords).a);
            color = sampled1;//vec4(sampled1.x+gl_FragColor.r,sampled1.y+gl_FragColor.g,sampled1.z+gl_FragColor.b,gl_FragColor.a+min(sampled1.a,0));
            
        }
        """

FRAGMENT_SHADER_ADD_CLAMP = """
        #version 330 core
        in vec2 TexCoords;
        uniform vec3 colorShift;
        uniform vec3 colorMultiplier;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {   
            vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            float r=sampled.x+colorShift.x;
            float g=sampled.y+colorShift.y;
            float b=sampled.z+colorShift.z;
            r=r*colorMultiplier.x;
            g=g*colorMultiplier.y;
            b=b*colorMultiplier.z;
            color = vec4(r,g,b,sampled.w);
            
        }
        """

FRAGMENT_SHADER_MULTIPLY = """
        #version 330 core
        //#define GL_compatibility_profile 1
        in vec2 TexCoords;
        out vec4 color;
        uniform sampler2D text;
        uniform bool toRight;
        void main()
        {   
            
            vec2 TexCoords2=TexCoords;
            vec2 TexCoords3;
            if(toRight){
                if(TexCoords.x<0.5){discard;}
            TexCoords2.x=TexCoords2.x;
            TexCoords3=vec2(TexCoords.x-0.5,TexCoords.y);
            }else{
                if(TexCoords.x>0.5){discard;}
            TexCoords2.x=TexCoords2.x;
            TexCoords3=vec2(TexCoords.x+0.5,TexCoords.y);
            }
            vec4 sampled = vec4(texture(text, TexCoords2).r, texture(text, TexCoords2).g, texture(text, TexCoords2).b, texture(text, TexCoords2).a);
            sampled.x=min(sampled.x,1.5);
            sampled.y=min(sampled.y,1.5);
            sampled.z=min(sampled.z,1.5);
            
            vec4 sampledb = vec4(texture(text, TexCoords3).r, texture(text, TexCoords3).g, texture(text, TexCoords3).b, texture(text, TexCoords3).a);
            sampledb.x=min(sampledb.x,1.5);
            sampledb.y=min(sampledb.y,1.5);
            sampledb.z=min(sampledb.z,1.5);
            color = vec4(sampled.x*sampledb.x,sampled.y*sampledb.y,sampled.z*sampledb.z,1);
            
        }
        """





FRAGMENT_SHADER_GAUSSBLUR="""#version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;
uniform bool horizontal;
uniform float weight[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main()
{             
    vec2 tex_offset = 1.0 / textureSize(text, 0); // gets size of single texel
    vec3 result = texture(text, TexCoords).rgb * weight[0]; // current fragment's contribution
    if(horizontal)
    {
        for(int i = 1; i < 5; ++i)
        {
            result += (texture(text, TexCoords + vec2(tex_offset.x * i, 0.0)).rgb) * weight[i];
            result += (texture(text, TexCoords - vec2(tex_offset.x * i, 0.0)).rgb) * weight[i];
        }
    }
    else
    {
        for(int i = 1; i < 5; ++i)
        {
            result += (texture(text, TexCoords + vec2(0.0, tex_offset.y * i)).rgb) * weight[i];
            result += (texture(text, TexCoords - vec2(0.0, tex_offset.y * i)).rgb) * weight[i];
        }
    }
    color = vec4(max(texture(text, TexCoords).rgb*0,result), 1.0);
    
}"""


FRAGMENT_SHADER_LIGHTINGSPREAD="""#version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform float time;
        uniform sampler2D text;
        uniform vec3 textColor;
uniform bool horizontal;
const float fadeAmount=0.01;
void main()
{             
    vec2 tex_offset = 1.0 / textureSize(text, 0); // gets size of single texel
    vec3 result = texture(text, TexCoords).rgb;
    for(int j = -2; j < 3; ++j)
    {
        for(int i = -2; i < 3; ++i)
        {
            result = max(result,texture(text, TexCoords + vec2(tex_offset.x * i, tex_offset.y * j)).rgb-vec3(fadeAmount*sqrt(i*i+j*j),fadeAmount*sqrt(i*i+j*j),fadeAmount*sqrt(i*i+j*j)));
            
        }
    }
    
    color = vec4(result, 1.0);
    
}"""






global currentFrameCenter,lastFrameCenter
currentFrameCenter=lastFrameCenter=(0,0)








numFramebuffers=5+3+1+1+1
layout=[5,1,1,1,1]+[1,1,1,1,1,1]
sizes=[None]*20
postProcessEffectList=[]
postProcessEffectList.append({'id':0,'from':1,'to':5,'args':{}})
postProcessEffectList.append({'id':0,'from':2,'to':2,'args':{}})

global lightingupdateeveryValue
lightingupdateeveryValue=2
def lightingupdateevery():
    global lightingupdateeveryValue
    return 1;#lightingupdateeveryValue




#postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ONE})
#postProcessEffectList.append({'id':0,'from':3,'to':6,'args':{}})\
#postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})

def getVisualShift():
    global currentFrameCenter,lastFrameCenter
    return ('4f',(-(currentFrameCenter[0]-lastFrameCenter[0])/640*5.657*0.75,(currentFrameCenter[1]-lastFrameCenter[1])/640*5.657*0.75,640,640))

postProcessEffectList.append({'id':9,'from':10,'to':7,'args':{'fromRect':('4f',(0,0,1,1)),'toRect':getVisualShift}})
postProcessEffectList.append({'id':0,'from':11,'to':6,'args':{}})

postProcessEffectList.append({'id':3,'from':10,'to':6,'args':{'colorMultiplier':('3f',(0.8,0.8,0.8))},'every':lightingupdateevery})

postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ONE})
postProcessEffectList.append({'id':3,'from':3,'to':6,'args':{'colorMultiplier':('3f',(0.2,0.2,0.2))},'every':lightingupdateevery})
postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})

postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})

postProcessEffectList.append({'id':7,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':7,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})

postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})


#startexperiment
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})

postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':10,'to':7,'args':{'horizontal':('bool',False)},'every':lightingupdateevery})
postProcessEffectList.append({'id':1,'from':11,'to':6,'args':{'horizontal':('bool',True)},'every':lightingupdateevery})
#endexperiment



postProcessEffectList.append({'id':1,'from':6,'to':3,'args':{'horizontal':('bool',False)}})
postProcessEffectList.append({'id':1,'from':7,'to':2,'args':{'horizontal':('bool',True)}})
postProcessEffectList.append({'id':1,'from':6,'to':3,'args':{'horizontal':('bool',False)}})
postProcessEffectList.append({'id':1,'from':7,'to':2,'args':{'horizontal':('bool',True)}})
postProcessEffectList.append({'id':1,'from':6,'to':3,'args':{'horizontal':('bool',False)}})
postProcessEffectList.append({'id':1,'from':7,'to':2,'args':{'horizontal':('bool',True)}})
postProcessEffectList.append({'id':1,'from':6,'to':3,'args':{'horizontal':('bool',False)}})
postProcessEffectList.append({'id':1,'from':7,'to':2,'args':{'horizontal':('bool',True)}})
postProcessEffectList.append({'id':1,'from':6,'to':3,'args':{'horizontal':('bool',False)}})
postProcessEffectList.append({'id':1,'from':7,'to':2,'args':{'horizontal':('bool',True)}})

postProcessEffectList.append({'id':0,'from':9,'to':4,'args':{}})

postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ZERO})
postProcessEffectList.append({'id':0,'from':10,'to':10,'args':{}})
postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ONE})
postProcessEffectList.append({'id':2,'from':5,'to':10,'args':{}})
postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})

postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ZERO})
postProcessEffectList.append({'id':0,'from':14,'to':8,'args':{}})
postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})
postProcessEffectList.append({'id':5,'from':8,'to':8,'args':{}})

postProcessEffectList.append({'id':4,'from':12,'to':9,'args':{'toRight':('bool',True)}})

postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ZERO})
postProcessEffectList.append({'id':0,'from':14,'to':8,'args':{}})
postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})
postProcessEffectList.append({'id':6,'from':8,'to':8,'args':{}})

postProcessEffectList.append({'id':4,'from':12,'to':9,'args':{'toRight':('bool',False)}})
#postProcessEffectList.append({'id':0,'from':10,'to':9,'args':{'toRight':('bool',False)}})

postProcessEffectList.append({'id':-1,'a':GL_ONE,'b':GL_ONE})
postProcessEffectList.append({'id':2,'from':6,'to':9,'args':{}})
postProcessEffectList.append({'id':-1,'a':GL_SRC_ALPHA,'b':GL_ONE_MINUS_SRC_ALPHA})


#postProcessEffectList.append({'id':0,'from':13,'to':0,'args':{}})
postProcessEffectList.append({'id':0,'from':13,'to':0,'args':{}})
postProcessEffectList.append({'id':8,'from':4,'to':0,'args':{'colorkey':('3f',(0,0,0))}})


global postProcessEffects
postProcessEffects=[]
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_COPY])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_GAUSSBLUR])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_SUM])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_ADD_CLAMP])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_MULTIPLY])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_COPY_TOLEFTFROMRIGHT])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_COPY_TORIGHTFROMLEFT])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_LIGHTINGSPREAD])
postProcessEffects.append([VERTEX_SHADER,FRAGMENT_SHADER_BLIT_COLORKEY])
postProcessEffects.append([VERTEX_SHADER_TO_FROM,FRAGMENT_SHADER_COPY])

VERTEX_SHADER = """
        #version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;
        out vec2 ScreenCoords;

        uniform mat4 projection;

        void main()
        {
            vec4 gT_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            gl_Position = vec4(gT_Position.x,gT_Position.y,gT_Position.z,gT_Position.w);
            
            TexCoords = vertex.zw;
            ScreenCoords= vertex.xy;
        }
       """

FRAGMENT_SHADER = """
        #version 330 core
        in vec2 TexCoords;
        in vec2 ScreenCoords;
        layout (location = 0) out vec4 FragColor;
        layout (location = 1) out vec4 BrightColor;
        layout (location = 2) out vec4 LightColor;
        layout (location = 4) out vec4 LightColor2;
        layout (location = 3) out vec4 GuiColor;
        out vec2 position;
        uniform sampler2D text;
        uniform vec3 textColor;
        uniform bool isGui;
        uniform float isGlowy;
        uniform int shadowLevel;

        void main()
        {    
            float fadeAmount=1;
            if(ScreenCoords.x>640){
                discard;
            }
            if(ScreenCoords.y>640){
                discard;
            }
            if(TexCoords.x>1) discard;
            if(TexCoords.y>1) discard;
            if(TexCoords.x<0) discard;
            if(TexCoords.y<0) discard;
            if(isGui==false){
                fadeAmount=(1-sqrt((ScreenCoords.x-320)*(ScreenCoords.x-320)+(ScreenCoords.y-320)*(ScreenCoords.y-320))/(900-shadowLevel));
            
            //if((fadeAmount<=0)&&(isGlowy==0)&&((texture(text, TexCoords).a==1)||(texture(text, TexCoords).a==0))){
            //    discard;
            //}
            vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            FragColor = vec4(textColor.xyz, 1) * vec4(sampled.xyz,sampled.w);
            //if(fadeAmount<=0){
            //    FragColor.w=0;
            //}
            if(isGlowy>=0){
            BrightColor=vec4(sampled.xyz*isGlowy*sampled.w,sampled.w);

            LightColor=BrightColor;
            LightColor2=vec4(max(0,fadeAmount),max(0,fadeAmount),max(0,fadeAmount),sampled.w/2);
            LightColor=vec4(BrightColor.xyz+vec3(max(0,fadeAmount),max(0,fadeAmount),max(0,fadeAmount)),BrightColor.w);
            }else{
            BrightColor=vec4(vec3(1,1,1)*isGlowy*sampled.w,sampled.w);

            LightColor=BrightColor;
            LightColor2=vec4(max(0,fadeAmount)*(1-sampled.w),max(0,fadeAmount)*(1-sampled.w),max(0,fadeAmount)*(1-sampled.w),sampled.w);
            }
            GuiColor=vec4(0,0,0,0);
            }else{
            vec4 sampled = vec4(texture(text, TexCoords).r, texture(text, TexCoords).g, texture(text, TexCoords).b, texture(text, TexCoords).a);
            GuiColor=sampled;
            BrightColor=LightColor=FragColor=LightColor2=vec4(0,0,0,0);
            }
        }
        """

shaderProgram = None
Characters = dict()
Textures = dict()
VBO = None
VAO = None
global currentTexture
currentTexture=-1

def initliaze(textures):
    global VERTEXT_SHADER
    global FRAGMENT_SHADER
    global shaderProgram
    global Characters
    global Textures
    global VBO
    global VAO
    #compiling shaders
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    #creating shaderProgram
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    glUseProgram(shaderProgram)

    #get projection
    #problem
    
    shader_projection = glGetUniformLocation(shaderProgram, "projection")
    projection = glm.ortho(0, 640, 640, 0)
    glUniformMatrix4fv(shader_projection, 1, GL_FALSE, glm.value_ptr(projection))
    
    #disable byte-alignment restriction
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    face = freetype.Face(fontfile)
    face.set_char_size( 48*64 )

    #load first 128 characters of ASCII set
    for i in range(0,128):
        face.load_char(chr(i))
        glyph = face.glyph
        
        #generate texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                     GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

        #texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        #now store character for later use
        Characters[chr(i)] = CharacterSlot(texture,glyph)

    for i in textures:
        width,height=textures[i]['size']
        x=textures[i]['data']
        #generate texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, array(x))

        #texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        #now store character for later use
        Textures[i] = TextureSlot(texture,[width,height])
        
    #glBindTexture(GL_TEXTURE_2D, 0)

    #configure VAO/VBO for texture quads
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    _framebuffer_start(*getWindowSize())




def render_rect(window,x,y,w,h,txt):
    render_rect_textured(window,x,y,w,h,0,0,1,1,txt)

def render_rect_textured(window,x,y,w,h,texX,texY,texW,texH,txt):
    global shaderProgram
    global Textures
    global VBO
    global VAO
    if type(txt) in [str,int]:
        txt=Textures[txt].texture
    
    y+=h
    #face = freetype.Face(fontfile)
    #face.set_char_size(48*64)
    glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),
                1,1,1)
               
    glActiveTexture(GL_TEXTURE0)
    
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindVertexArray(VAO)
    w = w
    h = h
    vertices = _get_rendering_buffer_textured(x,y,w,h,texX,texY,texW,texH)

    global currentTexture
    if txt!=currentTexture:
        #render glyph texture over quad
        glBindTexture(GL_TEXTURE_2D, txt)
        currentTexture=txt
    #update content of VBO memory
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    #render quad
    glDrawArrays(GL_TRIANGLES, 0, 6)
    #now advance cursors for next glyph (note that advance is number of 1/64 pixels)

    glBindVertexArray(0)
    #glBindTexture(GL_TEXTURE_2D, 0)

    #glfw.swap_buffers(window)
    #print(glfw.poll_events())

def render_quad(window,x1,y1,x2,y2,x3,y3,x4,y4,txt):
    global shaderProgram
    global Textures
    global VBO
    global VAO
    #face = freetype.Face(fontfile)
    #face.set_char_size(48*64)
    glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),
                1,1,1)
               
    glActiveTexture(GL_TEXTURE0)
    
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindVertexArray(VAO)
    #w = w
    #h = h
    vertices = _get_rendering_buffer_quad(x1,y1,x2,y2,x3,y3,x4,y4)

    #render glyph texture over quad
    global currentTexture
    if txt!=currentTexture:
        #render glyph texture over quad
        glBindTexture(GL_TEXTURE_2D, txt)
        currentTexture=txt
    #update content of VBO memory
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    #render quad
    glDrawArrays(GL_TRIANGLES, 0, 6)
    #now advance cursors for next glyph (note that advance is number of 1/64 pixels)

    glBindVertexArray(0)
    #glBindTexture(GL_TEXTURE_2D, 0)

    #glfw.swap_buffers(window)
    #print(glfw.poll_events())

def render_quad_textured(window,p1,p2,p3,p4,t1,t2,t3,t4,txt,flgs=[0,0,0]):
    global shaderProgram
    global Textures
    global VBO
    global VAO
    #face = freetype.Face(fontfile)
    #face.set_char_size(48*64)

    x1,y1,x2,y2,x3,y3,x4,y4=*p1,*p2,*p3,*p4
    tx1,ty1,tx2,ty2,tx3,ty3,tx4,ty4=*t1,*t2,*t3,*t4

    while flgs.__len__()<3:
        flgs.append(0)
    
    glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),
                1,1,1)
    glUniform1i(glGetUniformLocation(shaderProgram, "isGui"),
                flgs[0])
    glUniform1i(glGetUniformLocation(shaderProgram, "shadowLevel"),
                flgs[1])
    glUniform1f(glGetUniformLocation(shaderProgram, "isGlowy"),
                flgs[2])
               
    glActiveTexture(GL_TEXTURE0)
    
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindVertexArray(VAO)
    #w = w
    #h = h
    vertices = _get_rendering_buffer_quad_textured(x1,y1,x2,y2,x3,y3,x4,y4,tx1,ty1,tx2,ty2,tx3,ty3,tx4,ty4)
    if txt not in Textures:
        txt=0
    #render glyph texture over quad
    global currentTexture
    if Textures[txt].texture!=currentTexture:
        #render glyph texture over quad
        glBindTexture(GL_TEXTURE_2D, Textures[txt].texture)
        currentTexture=Textures[txt].texture
    #update content of VBO memory
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    #render quad
    glDrawArrays(GL_TRIANGLES, 0, 6)
    #now advance cursors for next glyph (note that advance is number of 1/64 pixels)

    glBindVertexArray(0)
    #glBindTexture(GL_TEXTURE_2D, 0)

    #glfw.swap_buffers(window)
    #print(glfw.poll_events())


def render_text(window,text,x,y,scale,color):
    global shaderProgram
    global Characters
    global VBO
    global VAO
    
    face = freetype.Face(fontfile)
    face.set_char_size(48*64)
    glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),
                color[0]/255,color[1]/255,color[2]/255)
               
    glActiveTexture(GL_TEXTURE0)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindVertexArray(VAO)
    for c in text:
        ch = Characters[c]
        w, h = ch.textureSize
        w = w*scale
        h = h*scale
        vertices = _get_rendering_buffer(x,y,w,h)

        #render glyph texture over quad
        glBindTexture(GL_TEXTURE_2D, ch.texture)
        #update content of VBO memory
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        #print(vertices)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindVertexArray(VBO);
        #render quad
        glDrawArrays(GL_TRIANGLES, 0, 6)
        #now advance cursors for next glyph (note that advance is number of 1/64 pixels)
        x += (ch.advance>>6)*scale

    glBindVertexArray(0)
    glBindTexture(GL_TEXTURE_2D, 0)
    

def update(window):
    #glfw.swap_buffers(window)
    (glfw.poll_events())
#pg.init()
#bestdepth = pg.display.mode_ok([500,500], pg.OPENGL, 32)
#screen = pg.display.set_mode([500,500], pg.OPENGL|pg.RESIZABLE|pg.DOUBLEBUF, bestdepth,vsync=1)


global window
#print(window)
#print([i for i in vars(window)])
#print(window.__doc__)
global vp_size_changed
vp_size_changed = False
def _start(textures,windowwidth,windowheight,windowtitle):
    global window
    glfw.init()
    window = glfw.create_window(windowwidth, windowheight,windowtitle,None,None)
    
    glfw.make_context_current(window)
    def resize_cb(window, w, h):
        global vp_size_changed
        vp_size_changed = True
    glfw.set_window_size_callback(window, resize_cb)
    initliaze(textures)
    glfw.set_key_callback(window,lambda *args:[events.append(('kpress',*args[1:])),print(events[-1])])
    glfw.set_char_callback(window,lambda *args:[events.append(('char',*args[1:])),print(events[-1])])
    glfw.set_mouse_button_callback(window,lambda *args:[events.append(('mouse',*args[1:])),print(events[-1])])
    
global keys
keys=[]
global cursorPos
cursorPos=(0,0)
global buttons
buttons=[]
global windowSize
windowSize=(940,480)
global matrix
global shouldWindowClose

global events
events=[]
global projectionB
projectionB=(0,0,1,1)
shouldWindowClose=0
matrix=[940/2,940/2,480/50,-940/50]
def get_events():
    global events
    return events
def clear_events():
    global events
    events=[]
def getMatrix():
    global matrix
    return matrix
def setOffset(x,y):
    global matrix
    matrix[0]=x
    matrix[1]=y
def setScale(x,y):
    global matrix
    matrix[2]=x
    matrix[3]=y
def shouldWindowClose():
    global shouldWindowClose
    return glfw.window_should_close(window)#shouldWindowClose
def getKeys():
    global keys
    return keys
def getCursorPos():
    global cursorPos
    return cursorPos
def getMouseButtons():
    global buttons
    return buttons
def getWindowSize():
    global windowSize
    return windowSize
def getProjection():
    global projectionB
    return projectionB
import random
import time
starttime=time.time()
global frameCount
frameCount=0




def updateWindow(commands,frameLoc,fpsAvg):
    global lightingupdateeveryValue
    if fpsAvg>(50-lightingupdateeveryValue):
        if lightingupdateeveryValue!=1:
            lightingupdateeveryValue-=1
    elif fpsAvg<(41-lightingupdateeveryValue):
        if lightingupdateeveryValue!=3:
            lightingupdateeveryValue+=1
    global projectionB
    global lastFrameCenter
    global currentFrameCenter
    global windowSize
    global matrix
    lastFrameCenter=currentFrameCenter
    currentFrameCenter=(frameLoc[0]*640/windowSize[0],frameLoc[1]*640/windowSize[1])
    #print(currentFrameCenter[0]-lastFrameCenter[0],currentFrameCenter[1]-lastFrameCenter[1])
    global window
    global frameCount
    frameCount+=1
    global vp_size_changed
    if vp_size_changed:
        vp_size_changed = False
        w, h = glfw.get_framebuffer_size(window)
        glViewport(0, 0, w, h)
        windowSize=(w,h)
        matrix=[940/2,480*w/h/2,480/50,-480*w/h/50]
        print("new viewport size:", w, h)
        on_reshape(w,h)
    global vbo_fbo_vertices,fbo_vertices
    fbo_vertices = np.array((
    (-1, -1),
    ( 1, -1),
    (-1,  1),
    ( 1,  1),
    ));
    vbo_fbo_vertices=glGenBuffers(1);
    glBindBuffer(GL_ARRAY_BUFFER, vbo_fbo_vertices);
    glBufferData(GL_ARRAY_BUFFER, fbo_vertices.__len__(), fbo_vertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    global shaderProgram
    global program_postproc
    global fbo,fbo_texture,rbo_depth
    #print(commands)
    global keys,cursorPos,buttons
    glBindFramebuffer(GL_FRAMEBUFFER, 1);
    glUseProgram(shaderProgram);
    shader_projection = glGetUniformLocation(shaderProgram, "projection")
    projection = glm.ortho(0, 640, 640, 0)
    
    glUniformMatrix4fv(shader_projection, 1, GL_FALSE, glm.value_ptr(projection))
    keys=[glfw.get_key(window,i) if ((i>31)&(i<349)) else 0 for i in range(500)]
    buttons=[glfw.get_mouse_button(window,i) for i in range(8)]
    cursorPos=glfw.get_cursor_pos(window)
    glClearColor(0,0,0,0.5)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glDrawBuffers(layout[0], [GL_COLOR_ATTACHMENT0+i for i in range(layout[0])]);  
    for i in commands:
            i[-1]=i[-1]
            #print('render command',*i)
            if i[0]=='rect':
                i[1]+=matrix[0]
                i[2]+=matrix[1]
                i[3]*=matrix[2]
                i[4]*=matrix[3]
                render_rect(window, *i[1:])
            elif i[0]=='quad':
                for _ in range(4):
                    i[1+_*2]*=matrix[2]
                    i[1+_*2]+=matrix[0]
                    i[2+_*2]*=matrix[3]
                    i[2+_*2]+=matrix[1]
                render_quad(window, *i[1:])
            elif i[0]=='quad_textured':
                for _ in range(4):
                    i[1+_]=[*i[1+_]]
                    i[1+_][0]-=15
                    i[1+_][0]*=matrix[2]
                    i[1+_][0]+=matrix[0]
                    i[1+_][1]+=8
                    i[1+_][1]*=matrix[3]
                    i[1+_][1]+=matrix[1]
                try:
                    render_quad_textured(window, *i[1:])
                except Exception as err:
                    print('error!',err)
            elif i[0]=='text':
                i[2]+=matrix[0]
                i[3]+=matrix[1]
                i[4]*=matrix[2]
                render_text(window, *i[1:])
            elif i[0]=='textured_rect':
                i[1]+=matrix[0]
                i[2]+=matrix[1]
                i[3]*=matrix[2]
                i[4]*=matrix[3]
                render_rect_textured(window, *i[1:])
    global postProcessEffectList
    for effect in postProcessEffectList:
        if effect['id']==-1:
            glBlendFunc(effect['a'],effect['b'])
        else:
            every=1
            if 'every' in effect:
                every=effect['every']
                if type(every)!=int:
                    every=every()
            if frameCount%every==0:
                #({'id':0,'from':1,'to':3,'args':{}})
                if effect['to']==0:
                    glBindFramebuffer(GL_FRAMEBUFFER, 0);
                else:
                    glBindFramebuffer(GL_FRAMEBUFFER, fbo[effect['to']-1]);
                    glDrawBuffers(layout[effect['to']-1], [GL_COLOR_ATTACHMENT0+i for i in range(layout[effect['to']-1])]);  
                #glfw.swap_buffers(window);
                #glDrawBuffers(1,[0]);
                #glClearColor(0.0, 1.0, 0.0, 1.0);
                #glClear(GL_COLOR_BUFFER_BIT);
                size=(1,1)
                if effect['to']!=0:                                                
                    size=sizes[effect['to']-1]
                if size==None:
                    size=(1,1)
                v=_get_rendering_buffer(0,0,640,-640)
                glUseProgram(program_postproc[effect['id']]);
                shader_projection = glGetUniformLocation(program_postproc[effect['id']], "projection")
                projection = glm.ortho(0, 640, 640, 0)
                glUniformMatrix4fv(shader_projection, 1, GL_FALSE, glm.value_ptr(projection))
                #glUniform1f(glGetUniformLocation(program_postproc, "time"),
                #            starttime-time.time())
                for argument in effect['args']:
                    argn=argument
                    if type(effect['args'][argn]) not in [list,tuple]:
                        argt,argv=effect['args'][argn]()
                    else:    
                        argt=effect['args'][argn][0]
                        argv=effect['args'][argn][1]
                    
                    if argt=='1f':
                        glUniform1f(glGetUniformLocation(program_postproc[effect['id']], argn),argv)
                    elif argt=='2f':
                        glUniform2f(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    elif argt=='3f':
                        glUniform3f(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    elif argt=='4f':
                        glUniform4f(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    elif argt=='bool':
                        glUniform1i(glGetUniformLocation(program_postproc[effect['id']], argn),argv)
                    elif argt=='1i':
                        glUniform1i(glGetUniformLocation(program_postproc[effect['id']], argn),argv)
                    elif argt=='2i':
                        glUniform2i(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    elif argt=='3i':
                        glUniform3i(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    elif argt=='4i':
                        glUniform4i(glGetUniformLocation(program_postproc[effect['id']], argn),*argv)
                    
                
                #v=np.asarray([262.,  22.,   0.,   0., 262., 100.,   0.,   1., 331., 100.,   1.,   1., 262.,  22.,
               #0.,   0., 331., 100.,   1.,   1., 331.,  22.,   1.,   0.],np.float32)
                
                if type(effect['from'])==int:
                    effect['from']=[effect['from']]
                glBindBuffer(GL_ARRAY_BUFFER, VBO)
                glBufferSubData(GL_ARRAY_BUFFER, 0, v.nbytes, v)
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                glBindVertexArray(VBO);
                glDisable(GL_DEPTH_TEST);
                exec(f"glActiveTexture(GL_TEXTURE{0})")
                glBindTexture(GL_TEXTURE_2D, fbo_texture[effect['from'][0]-1]);
                glDrawArrays(GL_TRIANGLES, 0, 6); 
    update(window)
    glfw.swap_buffers(window);
    
def closeWindow():
    glfw.terminate()








global fbo, fbo_texture, rbo_depth;
fbo=[]
fbo_texture=[]
rbo_depth=[]

global program_postproc
program_postproc=[]


def _framebuffer_start(screen_width,screen_height):
  global fbo,fbo_texture,rbo_depth
  global program_postproc
  for _ in range(numFramebuffers):
    size=sizes[_]
    if size==None:
        size=(1,1)
    screen_width*=size[0]
    screen_height*=size[1]
      #/* Create back-buffer, used for post-processing */
    #/* Texture */
    glActiveTexture(GL_TEXTURE0);
    n=glGenTextures(layout[_])
    if type(n)!=np.uintc:
        for j in n:
            fbo_texture.append(j);
    else:
        fbo_texture.append(n);
    
    for i in range(layout[_]):
        
        glBindTexture(GL_TEXTURE_2D, fbo_texture[-layout[_]+i]);
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, screen_width, screen_height, 0, GL_RGBA, GL_UNSIGNED_BYTE,None);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16F, screen_width, screen_height, 0, GL_RGBA, GL_FLOAT,None);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glBindTexture(GL_TEXTURE_2D, 0);
    
    #/* Depth buffer */
    rbo_depth.append(glGenRenderbuffers(1));
    glBindRenderbuffer(GL_RENDERBUFFER, rbo_depth[-1]);
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, screen_width, screen_height);
    glBindRenderbuffer(GL_RENDERBUFFER, 0);
    
    #/* Framebuffer to link everything together */
    fbo.append(glGenFramebuffers(1));
    glBindFramebuffer(GL_FRAMEBUFFER, fbo[-1]);
    for i in range(layout[_]):
        x=[glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0+i, GL_TEXTURE_2D, fbo_texture[-layout[_]+i], 0)][0];
    (glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo_depth[-1]))
    status = glCheckFramebufferStatus(GL_FRAMEBUFFER);
    if (status) != GL_FRAMEBUFFER_COMPLETE:
      fprintf(stderr, "glCheckFramebufferStatus: error %p", status);
      return 0;
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    screen_width/=size[0]
    screen_height/=size[1]
    screen_width=int(screen_width)
    screen_height=int(screen_height)

  
  
  #/* init_resources */
  #/* Post-processing */
  global postProcessEffects
  for postProcessEffect in postProcessEffects:
        vs = shaders.compileShader(postProcessEffect[0], GL_VERTEX_SHADER)
        if (vs   == 0):
          return 0;
        fs = shaders.compileShader(postProcessEffect[1], GL_FRAGMENT_SHADER)
        if (fs == 0):
          return 0;
        print(postProcessEffects.index(postProcessEffect))
        program_postproc.append(shaders.compileProgram(vs,fs))#glCreateProgram();
        #shader_projection = glGetUniformLocation(shaderProgram, "projection")
        #projection = glm.ortho(0, 640, 640, 0)
        #glUniformMatrix4fv(shader_projection, 1, GL_FALSE, glm.value_ptr(projection))
        #glAttachShader(program_postproc, vs);
        #glAttachShader(program_postproc, fs);
        glLinkProgram(program_postproc[-1]);
        link_ok=glGetProgramiv(program_postproc[-1], GL_LINK_STATUS);
        if (0==link_ok) :
          fprintf(stderr, "glLinkProgram:");
          print(program_postproc[-1]);
          return 0;
        
        glValidateProgram(program_postproc[-1]);
        validate_ok=glGetProgramiv(program_postproc[-1], GL_VALIDATE_STATUS); 
        if (0==validate_ok):
          fprintf(stderr, "glValidateProgram:");
          print(program_postproc);
        

  #attribute_name = "v_coord";
  #global attribute_v_coord_postproc
  #attribute_v_coord_postproc = glGetAttribLocation(program_postproc, attribute_name);
  #if (attribute_v_coord_postproc == -1) :
  #  print(stderr, "Could not bind attribute %s\n", attribute_name);
  #  return 0;
  

  #uniform_name = "fbo_texture";
  #global uniform_fbo_texture
  #uniform_fbo_texture = glGetUniformLocation(program_postproc, uniform_name);
  #if (uniform_fbo_texture == -1) :
  #  print(stderr, "Could not bind uniform %s\n", uniform_name);
  #  return 0;
  






def on_reshape(screen_width,screen_height):
  global fbo,fbo_texture,rbo_depth
  j=0
  for i in range(numFramebuffers):
      size=sizes[i]
      if size==None:
        size=(1,1)
      for _ in range(layout[i]):
          glBindTexture(GL_TEXTURE_2D, fbo_texture[j]);
          glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
          glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
          #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, screen_width, screen_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None);
          glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16F, screen_width*size[0], screen_height*size[1], 0, GL_RGBA, GL_FLOAT, None);
          glBindTexture(GL_TEXTURE_2D, 0);
          j+=1
      glBindRenderbuffer(GL_RENDERBUFFER, rbo_depth[i]);
      glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, screen_width*size[0], screen_height*size[1]);
      glBindRenderbuffer(GL_RENDERBUFFER, 0);

#_start({},200,200,'..')
#_framebuffer_start(200,200)
#glBindBuffer(GL_ARRAY_BUFFER, 0);
import time
starttime=time.time()
if __name__=='__main__':
    try:
        _start({},*getWindowSize(),'..')
        while not shouldWindowClose():
            updateWindow([['text','Xbc',10,20,3,(255*10,0,255)],['text','Obc',10,20,3,(255*10,0,255)]])



















    finally:
        pass
#finally:
#  glDeleteRenderbuffers(1, rbo_depth);
#  glDeleteTextures(1, fbo_texture);
#  glDeleteFramebuffers(1, fbo);
