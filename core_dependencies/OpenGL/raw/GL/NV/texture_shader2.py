'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_NV_texture_shader2'
_p.unpack_constants( """GL_DOT_PRODUCT_TEXTURE_3D_NV 0x86EF""", globals())


def glInitTextureShader2NV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
