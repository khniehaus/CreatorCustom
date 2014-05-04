import os
from setuptools import setup

APP = ['makehuman.py']
PLIST_OPTIONS = {
                  'CFBundleIdentifier':'org.makehuman',
                  'CFBundleGetInfoString':'MakeHuman for Mac OS X',
                  'CFBundleShortVersionString':'1.0.0',
                  'CFBundleName':os.getenv('MAKEHUMAN_APP_BUNDLE_NAME'),
                }
OPTIONS = {
            'argv_emulation': True,
            'plist': PLIST_OPTIONS,
            'includes': ['sip', 'PyQt4', 'OpenGL', 'cProfile', 'numpy','code','Queue'],
            'packages': ['logging'],
            'iconfile':'icons/makehuman_nb.icns',
          }
DATA_FILES = ['apps','core','data','lib','plugins','shared']

setup(
      app=APP,
      options={'py2app': OPTIONS},
      data_files=DATA_FILES,
      setup_requires=['py2app'],
     )