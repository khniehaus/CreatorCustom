'''OpenGL extension ARB.texture_float

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.texture_float to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds texture internal formats with 16- and 32-bit
	floating-point components.  The 32-bit floating-point components
	are in the standard IEEE float format.  The 16-bit floating-point
	components have 1 sign bit, 5 exponent bits, and 10 mantissa bits.
	Floating-point components are clamped to the limits of the range
	representable by their format.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/texture_float.txt
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.ARB.texture_float import *
### END AUTOGENERATED SECTION