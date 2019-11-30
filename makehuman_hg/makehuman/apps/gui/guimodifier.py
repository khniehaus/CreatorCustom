#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Modifier taskview
**Project Name:**      MakeHuman
**Product Home Page:** http://www.makehuman.org/
**Code Home Page:**    https://bitbucket.org/MakeHuman/makehuman/
**Authors:**           Glynn Clements, Jonas Hauquier
**Copyright(c):**      MakeHuman Team 2001-2017
**Licensing:**         AGPL3
    This file is part of MakeHuman (www.makehuman.org).
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
Common taskview for managing modifier sliders
"""

import gui
import gui3d
import mh
import qtgui
import humanmodifier
import modifierslider
import getpath
import module3d
from core import G
import log
from collections import OrderedDict
import language
from PyQt4 import QtCore

catMod = [] #YOU ARE HERE. SHOULD THIS BE A DEQUE?

class ModifierTaskView(gui3d.TaskView):
    def __init__(self, category, name, label=None, saveName=None, cameraView=None):
        if label is None:
            label = name.capitalize()
        if saveName is None:
            saveName = name

        super(ModifierTaskView, self).__init__(category, name, label=label)

        self.saveName = saveName
        self.cameraFunc = _getCamFunc(cameraView)

        self.groupBoxes = OrderedDict()
        self.radioButtons = []
        self.radioButtonGroup = []
        self.sliders = []
        self.modifiers = {}

        #self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        #self.groupBox = self.addRightWidget(gui.StackedBox())
        #self.box2 = self.addRightWidget(gui.GroupBox('Detail'))
        self.toolbar = mh.addToolBar(name)

        self.toolbar.setOrientation(QtCore.Qt.Vertical)
        tBarWidget = self.addLeftWidget(self.toolbar)
        self.groupBoxes[category.name] = tBarWidget

        #self.newAct = qtgui.Actions()

        #self.newAct.frick = qtgui.Action('Fuck', self.getModifiers)

        #self.boxBox = self.addLeftWidget(self.toolbar)
        self.hi = gui3d.View()
        self.showMacroStats = False
        self.human = gui3d.app.selectedHuman

    def addSlider(self, sliderCategory, slider, enabledCondition=None):
        # Get category groupbox
        categoryName = sliderCategory.capitalize()
        # # self.toolbar.addAction(self.newAct.frick)
        #print "frick", sliderCategory
        #

        if categoryName not in self.groupBoxes:
            # Create box
            #box = self.groupBox.addWidget(gui.GroupBox(categoryName))
            #box3 = self.addLeftWidget(self.toolbar)
            # self.toolbar.setOrientation(QtCore.Qt.Vertical)
            # hey = self.addLeftWidget(self.toolbar)
            # self.createActs(sliderCategory)
            # self.groupBoxes[categoryName] = hey

            # Create radiobutton
            isFirstBox = len(self.radioButtons) == 0
            #self.box2.addWidget(GroupBoxRadioButton(self, self.radioButtons, categoryName, box, selected=isFirstBox))
            if isFirstBox:
                #self.groupBox.showWidget(self.groupBoxes.values()[0])
                pass
        else:
            box = self.groupBoxes[categoryName]
            pass
        #box3 = self.addLeftWidget(self.toolbar)

        #self.createActs()
        # Add slider to groupbox
        #self.modifiers[slider.modifier.fullName] = slider.modifier
        #box3.setCurrentIndex(0)
        #butt = gui.Button(sliderCategory)
        #box.addWidget(butt)

    #def low(self):
        # slide = humanmodifier.
        # slide.groupName = ['hip']
        # print slide.groupName
        #print "DAMN YOU ALL", modifier.groupName.name
        #return modifier.groupName
        #self.hi.testMe()
    def low(self):
        #hi = gui3d.TaskView()
        for key in catMod:
            print key
            #hi.getModifiers(key)
            #else:
                #pass
        #print fuck

    def medium(self):
        pass

    def high(self):
        pass

    def changeCat(self):
        pass

    # def mod3(self):
    #     pass
    #
    # def mod4(self):
    #     pass
    #
    # def mod5(self):
    #     pass

    def createActs(self, sliderCategory):

        self.actions = gui.Actions()

        #cName = sliderCategory.capitalize()

        def action(*args, **kwargs):
            action = gui.Action(*args, **kwargs)
            self.toolbar.addAction(action)
            return action

        if sliderCategory == "Low":

            self.actions.low = action('Low', gui.getLanguageString('Low'), self.low)
        elif sliderCategory == "Medium":
            self.actions.medium = action ('Medium', gui.getLanguageString('Medium'), self.hi.medium)
        elif sliderCategory == "High":
            self.actions.high = action('High', gui.getLanguageString('High'), self.high)
        else:
            return None
        # self.actions.mod2 = action('modifier 2', gui.getLanguageString('Modifier 2'), self.mod2())
        # self.actions.mod3 = action('modifier 3', gui.getLanguageString('Modifier 3'), self.mod3())
        # self.actions.mod4 = action('modifier 4', gui.getLanguageString('Modifier 4'), self.mod4())
        # self.actions.mod5 = action('modifier 5', gui.getLanguageString('Modifier 5'), self.mod5())

        #slider.enabledCondition = enabledCondition
        #self.sliders.append(slider)

    # def boxMode(self):
    #     # We make the first one selected
    #     self.aRadioButton1 = self.box2.addWidget(gui.RadioButton(self.radioButtonGroup, 'Low', selected=True))
    #     self.aRadioButton2 = self.box2.addWidget(gui.RadioButton(self.radioButtonGroup, 'Medium'))
    #     self.aRadioButton3 = self.box2.addWidget(gui.RadioButton(self.radioButtonGroup, 'High'))
    #
    #     self.aRadioButtonLabel1 = self.box2.addWidget(gui.TextView('Low is selected'))
    #     self.aRadioButtonLabel2 = self.box2.addWidget(gui.TextView('Medium is not selected'))
    #     self.aRadioButtonLabel3 = self.box2.addWidget(gui.TextView('High is not selected'))
    #
    #     @self.aRadioButton1.mhEvent
    #     def onClicked(event):
    #         self.aRadioButtonLabel1.setText('Low is selected')
    #         self.aRadioButtonLabel2.setText('Medium is not selected')
    #         self.aRadioButtonLabel3.setText('High is not selected')
    #
    #     @self.aRadioButton2.mhEvent
    #     def onClicked(event):
    #         self.aRadioButtonLabel2.setText('Medium is selected')
    #         self.aRadioButtonLabel1.setText('Low is not selected')
    #         self.aRadioButtonLabel3.setText('High is not selected')
    #
    #     @self.aRadioButton3.mhEvent
    #     def onClicked(event):
    #         self.aRadioButtonLabel2.setText('Medium is not selected')
    #         self.aRadioButtonLabel1.setText('Low is not selected')
    #         self.aRadioButtonLabel3.setText('High is selected')


    def updateMacro(self):
        self.human.updateMacroModifiers()

    def getModifiers(self):
        return self.modifiers

    def onShow(self, event):
        #self.createActs()
        #self.task.groupBox.showWidget(self.boxBox)
        gui3d.TaskView.onShow(self, event)

        # Only show macro statistics in status bar for Macro modeling task
        # (depends on the correct task name being defined)
        # if self.showMacroStats:
        #     self.showMacroStatus()

        if G.app.getSetting('cameraAutoZoom'):
            self.setCamera()

        self.syncSliders()
        #self.boxMode()

    def syncSliders(self):
        for slider in self.sliders:
            slider.update()

            if slider.enabledCondition:
                enabled = getattr(slider.modifier.human, slider.enabledCondition)()
                slider.setEnabled(enabled)

    def onHide(self, event):
        super(ModifierTaskView, self).onHide(event)

        if self.name == "Macro modelling":
            pass
            #self.setStatus('')

    def onHumanChanged(self, event):
        # Update sliders to modifier values
        self.syncSliders()

        if event.change in ('reset', 'load', 'random'):
            self.updateMacro()

        if self.showMacroStats and self.isVisible():
            self.showMacroStatus()

    def loadHandler(self, human, values, strict):
        pass

    def saveHandler(self, human, file):
        pass

    def setCamera(self):
        if self.cameraFunc:
            f = getattr(G.app, self.cameraFunc)
            f()

    # def showMacroStatus(self):
    #     human = G.app.selectedHuman
    #
    #     if human.getGender() == 0.0:
    #         gender = G.app.getLanguageString('female')
    #     elif human.getGender() == 1.0:
    #         gender = G.app.getLanguageString('male')
    #     elif abs(human.getGender() - 0.5) < 0.01:
    #         gender = G.app.getLanguageString('neutral')
    #     else:
    #         gender = G.app.getLanguageString('%.2f%% demon, %.2f%% monster') % ((1.0 - human.getGender()) * 100, human.getGender() * 100)
    #
    #     age = human.getAgeYears()
    #     muscle = (human.getMuscle() * 100.0)
    #     weight = (50 + (150 - 50) * human.getWeight())
    #     height = human.getHeightCm()
    #     if G.app.getSetting('units') == 'metric':
    #         units = 'cm'
    #     else:
    #         units = 'in'
    #         height *= 0.393700787
    #
    #     self.setStatus([ ['Supernatural status',': %s '], ['Age',': %d '], ['Muscle',': %.2f%% '], ['Weight',': %.2f%% '], ['Height',': %.2f %s'] ], gender, age, muscle, weight, height, units)
    #
    # def setStatus(self, format, *args):
    #     G.app.statusPersist(format, *args)


class GroupBoxRadioButton(gui.RadioButton):

    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task
        self.aRadioButtonGroup = []
        self.label = label

    def onClicked(self, event):
        # global oTest
        #print "SHIT", self.task.label
        self.task.groupBox.showWidget(self.groupBox)
        #print self.groupBox
        # if self.label == "Medium":
        #     oTest = True
        # else:
        #     oTest = False
        # return oTest
        #self.task.onSliderFocus(self.groupBox.children[0]) # TODO needed for measurement

# class tBarNew(gui.ActionGroup):
# #
#     def __init__(self, task, name):
#         super(tBarNew, self).__init__(name)
#         self.task = task
#         self.name = self.label
#         self.toolbar = mh.addToolBar('Modelling')
#
#     def onClicked(self, event):
#         self.task.groupBox.showWidget(self.boxBox)
#
#         self.toolbar.setOrientation(QtCore.Qt.Vertical)
#
#         self.boxBox = self.addLeftWidget(self.toolbar)
#
#
#     def mod1(self):
#         pass
#
#     def mod2(self):
#         pass
#
#     def mod3(self):
#         pass
#
#     def mod4(self):
#         pass
#
#     def mod5(self):
#         pass
#
#     def createActs(self):
#
#         self.actions = gui.Actions()
#
#         def action(*args, **kwargs):
#             action = gui.Action(*args, **kwargs)
#             self.toolbar.addAction(action)
#             return action
#
#         self.actions.mod1 = action('modifier 1', gui.getLanguageString('Modifier 1'), self.mod1())
#         self.actions.mod2 = action('modifier 2', gui.getLanguageString('Modifier 2'), self.mod2())
#         self.actions.mod3 = action('modifier 3', gui.getLanguageString('Modifier 3'), self.mod3())
#         self.actions.mod4 = action('modifier 4', gui.getLanguageString('Modifier 4'), self.mod4())
#         self.actions.mod5 = action('modifier 5', gui.getLanguageString('Modifier 5'), self.mod5())
#
#     def onClicked(self, event):
#         self.createActs()
#         self.task.showLeftWidget(self.boxBox)



def _getCamFunc(cameraName):
    if cameraName:
        if hasattr(gui3d.app, cameraName) and callable(getattr(gui3d.app, cameraName)):
            return cameraName

        return "set" + cameraName.upper()[0] + cameraName[1:]
    else:
        return None



def loadModifierTaskViews(filename, human, category, taskviewClass=None):
    """
    Create modifier task views from modifiersliders defined in slider definition
    file.
    """
    import json
    global catMod

    if not taskviewClass:
        taskviewClass = ModifierTaskView

    data = json.load(open(filename, 'rb'), object_pairs_hook=OrderedDict)
    taskViews = []
    #ModifierTaskView.createActs(taskView)
    # Create task views
    for taskName, taskViewProps in data.items():
        sName = taskViewProps.get('saveName', None)
        label = taskViewProps.get('label', None)
        taskView = taskviewClass(category, taskName, label, sName)
        taskView.sortOrder = taskViewProps.get('sortOrder', None)
        taskView.showMacroStats = taskViewProps.get('showMacroStats', None)
        category.addTask(taskView)

        # Create sliders
        for sliderCategory, sliderDefs in taskViewProps['modifiers'].items():
            category.addModCat(sliderCategory)
            taskView.createActs(sliderCategory)
            for sDef in sliderDefs:
                modifierName = sDef['mod']
                if sliderCategory == 'Low':
                    catMod.append(modifierName)
                    print "what the hell", modifierName
                modifier = human.getModifier(modifierName)
                category.getModsHere(modifierName)
                # label = sDef.get('label', None)
                # camFunc = _getCamFunc( sDef.get('cam', None) )
                # slider = modifierslider.ModifierSlider(modifier, label=label, cameraView=camFunc)
                # enabledCondition = sDef.get("enabledCondition", None)
                # taskView.addSlider(sliderCategory, slider, enabledCondition)
        print "It me", catMod


        if taskView.saveName is not None:
            gui3d.app.addLoadHandler(taskView.saveName, taskView.loadHandler)
            gui3d.app.addSaveHandler(taskView.saveHandler)

        taskViews.append(taskView)

    return taskViews
