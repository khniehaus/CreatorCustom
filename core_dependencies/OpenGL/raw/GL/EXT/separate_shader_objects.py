'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_EXT_separate_shader_objects'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_EXT_separate_shader_objects',False)
_p.unpack_constants( """GL_ACTIVE_PROGRAM_EXT 0x8B8D""", globals())
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glUseShaderProgramEXT( type,program ):pass
@_f
@_p.types(None,_cs.GLuint)
def glActiveProgramEXT( program ):pass
@_f
@_p.types(_cs.GLuint,_cs.GLenum,arrays.GLcharArray)
def glCreateShaderProgramEXT( type,string ):pass


def glInitSeparateShaderObjectsEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
