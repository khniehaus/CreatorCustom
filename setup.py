import os
from setuptools import setup

APP = ['makehuman.py']
PLIST_OPTIONS = {
                  'CFBundleIdentifier':'org.makehuman',
                  'CFBundleGetInfoString':'MakeHuman for Mac OS X',
                  'CFBundleShortVersionString':os.getenv('MAKEHUMAN_VERSION'),
                  'CFBundleName':os.getenv('MAKEHUMAN_APP_BUNDLE_NAME'),
                }

isRelease = (os.getenv('MAKEHUMAN_BUILD_TYPE') == 'RELEASE')

iconFile = 'icons/makehuman.icns'

OPTIONS = {
            'argv_emulation': True,
            'plist': PLIST_OPTIONS,
            'includes': ['sip', 'PyQt4', 'OpenGL', 'cProfile', 'numpy','code','Queue','csv'],
            'packages': ['logging'],
            'iconfile': iconFile,
          }
DATA_FILES = ['apps','core','data','lib','plugins','shared']

print "Py2App summary:"
print "  version: "+ os.getenv('MAKEHUMAN_VERSION')
print "  app bundle name: " + os.getenv('MAKEHUMAN_APP_BUNDLE_NAME')
print "  build type: %s" % ("RELEASE" if isRelease else "NIGHTLY")

setup(
      app=APP,
      options={'py2app': OPTIONS},
      data_files=DATA_FILES,
      setup_requires=['py2app'],
     )
