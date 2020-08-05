#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
**Project Name:**      CreatorCustom
**Product Home Page:** http://www.kh-niehaus.com
**Code Home Page:**    https://github.com/khniehaus/CreatorCustom/
**Authors:**           Kiona Hagen Niehaus, derived from Glynn Clements, Jonas Hauquier
**Copyright(c):**      Kiona Hagen Niehaus 2020
**Licensing:**         AGPL3
    This file is derived from MakeHuman (www.makehuman.org).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

Generic modifiers
TODO
"""

import humanmodifier
import guimodifier
import getpath


def load(app):
    category = app.getCategory('Modelling')

    humanmodifier.loadModifiers(getpath.getSysDataPath('modifiers/modeling_modifiers.json'), app.selectedHuman)
    #guimodifier.loadModifierTaskViews(getpath.getSysDataPath('modifiers/modeling_modifiers.json'), app.selectedHuman, category)
    guimodifier.loadModifierTaskViews(getpath.getSysDataPath('modifiers/modeling_sliders.json'), app.selectedHuman, category)
    #gui3d.loadModifiers(getpath.getSysDataPath('modifiers/modeling_sliders.json'))

def unload(app):
    pass
