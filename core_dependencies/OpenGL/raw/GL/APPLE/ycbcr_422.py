'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_APPLE_ycbcr_422'
_p.unpack_constants( """GL_YCBCR_422_APPLE 0x85B9
GL_UNSIGNED_SHORT_8_8_APPLE 0x85BA
GL_UNSIGNED_SHORT_8_8_REV_APPLE 0x85BB""", globals())


def glInitYcbcr422APPLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
