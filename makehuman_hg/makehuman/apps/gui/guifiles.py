#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
**Project Name:**      CreatorCustom
**Product Home Page:** http://www.kh-niehaus.com
**Code Home Page:**    https://github.com/khniehaus/CreatorCustom/
**Authors:**           Marc Flerackers
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

This module implements the top-level 'Files' tab.
"""

import gui3d
from guisave import SaveTaskView
from guiload import LoadTaskView
from guiexport import ExportTaskView

class FilesCategory(gui3d.Category):
    def __init__(self, parent):
        super(FilesCategory, self).__init__('Files')

        parent.addCategory(self)

        self.load = LoadTaskView(self)
        self.save = SaveTaskView(self)
        self.export = ExportTaskView(self)

        self.addTask(self.load)
        self.addTask(self.save)
        self.addTask(self.export)
