'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_memory_attachment'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_memory_attachment',error_checker=_errors._error_checker)
GL_ATTACHED_MEMORY_OBJECT_NV=_C('GL_ATTACHED_MEMORY_OBJECT_NV',0x95A4)
GL_ATTACHED_MEMORY_OFFSET_NV=_C('GL_ATTACHED_MEMORY_OFFSET_NV',0x95A5)
GL_DETACHED_BUFFERS_NV=_C('GL_DETACHED_BUFFERS_NV',0x95AB)
GL_DETACHED_MEMORY_INCARNATION_NV=_C('GL_DETACHED_MEMORY_INCARNATION_NV',0x95A9)
GL_DETACHED_TEXTURES_NV=_C('GL_DETACHED_TEXTURES_NV',0x95AA)
GL_MAX_DETACHED_BUFFERS_NV=_C('GL_MAX_DETACHED_BUFFERS_NV',0x95AD)
GL_MAX_DETACHED_TEXTURES_NV=_C('GL_MAX_DETACHED_TEXTURES_NV',0x95AC)
GL_MEMORY_ATTACHABLE_ALIGNMENT_NV=_C('GL_MEMORY_ATTACHABLE_ALIGNMENT_NV',0x95A6)
GL_MEMORY_ATTACHABLE_NV=_C('GL_MEMORY_ATTACHABLE_NV',0x95A8)
GL_MEMORY_ATTACHABLE_SIZE_NV=_C('GL_MEMORY_ATTACHABLE_SIZE_NV',0x95A7)
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLuint64)
def glBufferAttachMemoryNV(target,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLint,_cs.GLsizei,arrays.GLuintArray)
def glGetMemoryObjectDetachedResourcesuivNV(memory,pname,first,count,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint64)
def glNamedBufferAttachMemoryNV(buffer,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum)
def glResetMemoryObjectParameterNV(memory,pname):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLuint64)
def glTexAttachMemoryNV(target,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint64)
def glTextureAttachMemoryNV(texture,memory,offset):pass
