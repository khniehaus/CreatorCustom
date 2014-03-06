'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_EXT_texture_array'
_p.unpack_constants( """GL_TEXTURE_1D_ARRAY_EXT 0x8C18
GL_PROXY_TEXTURE_1D_ARRAY_EXT 0x8C19
GL_TEXTURE_2D_ARRAY_EXT 0x8C1A
GL_PROXY_TEXTURE_2D_ARRAY_EXT 0x8C1B
GL_TEXTURE_BINDING_1D_ARRAY_EXT 0x8C1C
GL_TEXTURE_BINDING_2D_ARRAY_EXT 0x8C1D
GL_MAX_ARRAY_TEXTURE_LAYERS_EXT 0x88FF
GL_COMPARE_REF_DEPTH_TO_TEXTURE_EXT 0x884E""", globals())
glget.addGLGetConstant( GL_TEXTURE_BINDING_1D_ARRAY_EXT, (1,) )
glget.addGLGetConstant( GL_TEXTURE_BINDING_2D_ARRAY_EXT, (1,) )
glget.addGLGetConstant( GL_MAX_ARRAY_TEXTURE_LAYERS_EXT, (1,) )


def glInitTextureArrayEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
