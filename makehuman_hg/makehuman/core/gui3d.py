#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman
**Product Home Page:** http://www.makehuman.org/
**Code Home Page:**    https://bitbucket.org/MakeHuman/makehuman/
**Authors:**           Joel Palmius, Marc Flerackers
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
This module contains classes defined to implement widgets that provide utility functions
to the graphical user interface.
Importing this module loads OpenGL dependencies.
"""

import weakref
import events3d
import module3d
import humanmodifier
import human
import object3d
import gui
import modifierslider
import mhmain
import files3d
import qtgui
import qtui
import guicommon
import animation3d
import mh
import log
import selection
import collections
import time
from PyQt4 import QtGui, QtCore

from guicommon import Object, Action

sCheck = None

class MouAction(events3d.MouseEvent):
    dForce = collections.deque([0, 0, 0, 0], maxlen=4)
    def __init__(self, class_a):
        self.x = class_a.x
        self.y = class_a.y
        print "X is", self.x, "Y is", self.y
        #self.umOk = collections.deque()

        # FIX THIS FOR BETTER VALS

    def mVar(self):
        newY = self.y  # y value

        window = QtGui.QWidget()
        height = window.frameGeometry().height()

        mapVal = (((newY - 0.0) * (10.0 - -1.0)) / (height - 0.0)) + -1.0  # map range to 'slider' range
            # newVal = (newY / 300.0) # y value converted to more or less 0.0-1.0 range
        sVal = 5.0 + ((mapVal - -1.0) * (-1.0 - 5.0) / (5.0 - -1.0))  # reverse range so figure gets 'taller' as y val gets smaller
        #self.umOk.appendleft(sVal)
        sVal = sVal
        print "height val initial", sVal
        #print self.umOk
        return sVal
            # print sVal

    def nVar(self):
        newX = self.x
        window = QtGui.QWidget()
        width = window.frameGeometry().width()

        sVal = (((newX - 0.0) * (1.0 - -1.0)) / (width - 0.0)) + -1.0  # map range to 'slider' range
        sVal = sVal
        print "weight val initial", sVal
        return sVal

    def aVar(self):
        newY = self.y  # y value

        window = QtGui.QWidget()
        height = window.frameGeometry().height()

        mapVal = (((newY - 0.0) * (5.0 - -1.0)) / ((height/2) - 0.0)) + -1.0  # map range to 'slider' range
            # newVal = (newY / 300.0) # y value converted to more or less 0.0-1.0 range
        sVal = 1.0 + ((mapVal - -1.0) * (-1.0 - 1.0) / (1.0 - -1.0))

        sVal = sVal
        print sVal
        # print self.umOk
        return sVal

    def wiVar(self):
        newX = self.x

        mapVal = (((newX - 0.0) * (10.0 - -1.0)) / (800.0 - 0.0)) + -1.0  # map range to 'slider' range
        sVal = 1.0 + ((mapVal - -1.0) * (-1.0 - 1.0) / (1.0 - -1.0))
        return sVal

class View(events3d.EventHandler):

    """
    The base view from which all widgets are derived.
    """

    uniVal = 0.15
    umOk = collections.deque([0,0,0,0], maxlen=4)
    soOk = collections.deque([0,0,0,0], maxlen=4)
    yoOk = collections.deque([0,0,0,0], maxlen=4)
    FoOk = collections.deque([0,0,0,0], maxlen=4)

    def __init__(self):

        self.children = []
        self.objects = []
        self._visible = False
        self._totalVisibility = False
        self._parent = None
        self._attached = False
        self.widgets = []

        self.faceGroupLookup = {}

        print "App: ", mhmain.G.app.selectedHuman

        for modifier in mhmain.G.app.selectedHuman.modifiers:
            print modifier.fullName
            if hasattr(modifier, "faceGroup") and modifier.faceGroup != None:
                sliderTest = modifierslider.ModifierSlider(modifier)
                self.faceGroupLookup[modifier.faceGroup] = sliderTest
                print "hello", modifier.faceGroup
                #put randomizer here!!! (at least try according to Marco)

    @property
    def parent(self):
        if self._parent:
            return self._parent();
        else:
            return None

    def _attach(self):

        self._attached = True

        for object in self.objects:
            object._attach()

        for child in self.children:
            child._attach()

    def _detach(self):
        self._attached = False

        for object in self.objects:
            object._detach()

        for child in self.children:
            child._detach()

    def addView(self, view):
        """
        Adds the view to this view. If this view is attached to the app, the view will also be attached.
        :param view: The view to be added.
        :type view: gui3d.View
        :return: The view, for convenience.
        :rvalue: gui3d.View
        """
        if view.parent:
            raise RuntimeError('The view is already added to a view')

        view._parent = weakref.ref(self)
        view._updateVisibility()
        if self._attached:
            view._attach()

        self.children.append(view)

        return view

    def removeView(self, view):
        """
        Removes the view from this view. If this view is attached to the app, the view will be detached.
        :param view: The view to be removed.
        :type view: gui3d.View
        """
        if view not in self.children:
            raise RuntimeError('The view is not a child of this view')

        view._parent = None
        if self._attached:
            view._detach()

        self.children.remove(view)

    def addObject(self, object):
        """
        Adds the object to the view. If the view is attached to the app, the object will also be attached and will get an OpenGL counterpart.
        :param object: The object to be added.
        :type object: gui3d.Object
        :return: The object, for convenience.
        :rvalue: gui3d.Object
        """
        if object._view:
            raise RuntimeError('The object is already added to a view')

        object._view = weakref.ref(self)
        if self._attached:
            object._attach()

        self.objects.append(object)

        return object

    def removeObject(self, object):
        """
        Removes the object from the view. If the object was attached to the app, its OpenGL counterpart will be removed as well.
        :param object: The object to be removed.
        :type object: gui3d.Object
        """
        if object not in self.objects:
            raise RuntimeError('The object is not a child of this view')

        object._view = None
        if self._attached:
            object._detach()

        self.objects.remove(object)

    def show(self):
        self._visible = True
        self._updateVisibility()

    def hide(self):
        self._visible = False
        self._updateVisibility()

    def isShown(self):
        return self._visible

    def isVisible(self):
        return self._totalVisibility

    def _updateVisibility(self):
        previousVisibility = self._totalVisibility

        self._totalVisibility = self._visible and (not self.parent or self.parent.isVisible())

        for o in self.objects:
            o.setVisibility(self._totalVisibility)

        for v in self.children:
            v._updateVisibility()

        if self._totalVisibility != previousVisibility:
            if self._totalVisibility:
                self.callEvent('onShow', None)
            else:
                self.callEvent('onHide', None)

    def onShow(self, event):
        self.show()

    def onHide(self, event):
        self.hide()

    def onMouseDown(self, event):
        self.parent.callEvent('onMouseDown', event)

    def onMouseMoved(self, event):
        self.parent.callEvent('onMouseMoved', event)

    def onMouseDragged(self, event):
        self.parent.callEvent('onMouseDragged', event)
        #self.parent.callEvent('sliderMousePressEvent', event)
        global dval, mVal, vVal, app

        print "it's me, your slider"
        y = event.y #mouse y
        x = event.x #mouse x

        global uniVal
        #mehah = bleh.rayCast()
        # modifier1 = human.gMod #instance of global from human class for modifier category
        # modifier2 = human.wMod
        # modifier3 = human.shoulderlMod
        # modifier4 = human.upArmlMod




        #print modifier3.facegroup
        # picked = mh.getPickedColor()
        # colVal = selection.selectionColorMap.getSelectedFaceGroup(picked)
        colVal = sCheck
        #print modifier1 #modifier2 # print to make sure it's the right one
        # directManipTest = modifierslider.ModifierSlider(modifier1) #instance of slider variable from slider class
        # secondManipTest = modifierslider.ModifierSlider(modifier2)
        # smallArm2 = modifierslider.ModifierSlider(modifier4)

        #faceGroupLookup["right-arm-upper"] = smallArm2


        mouseEventTransfer = events3d.MouseEvent(event.button, event.x, event.y) #variable for mouse event with coords
        mouseAction = MouAction(mouseEventTransfer) #instance of mouse variable (requires mouse event)
        #scaler = mouseAction.make_interpolater(280.0, 50.0, 0.0, 1.0)
        dmVal1 = MouAction.mVar(mouseAction) #instance of new 'slider' value conversion func
        amVal1 = MouAction.nVar(mouseAction)
        vVal1 = MouAction.aVar(mouseAction)
        cVal1 = MouAction.wiVar(mouseAction)

        #print "color is", colVal

        self.umOk.appendleft(dmVal1)
        self.soOk.appendleft(amVal1)
        self.yoOk.appendleft(vVal1)
        self.FoOk.appendleft(cVal1)
        if self.umOk[0] >= self.umOk[3]:
            dmVal = -(self.umOk[0] - self.umOk[3])
        elif self.umOk[0] < self.umOk[3]:
            dmVal = self.umOk[3] - self.umOk[0]
        if self.soOk[0] >= self.soOk[3]:
            amVal = self.soOk[3] + (self.soOk[0] - self.soOk[3])
        elif self.soOk[0] < self.soOk[3]:
            amVal = self.soOk[3] - (self.soOk[3] - self.soOk[0])
        print self.soOk
        if self.yoOk[0] >= self.yoOk[3]:
            vrVal = self.yoOk[0] - self.yoOk[3]
        elif self.yoOk[0] < self.yoOk[3]:
            vrVal = -(self.yoOk[0] - self.yoOk[3])
        if self.FoOk[0] >= self.FoOk[3]:
            cmVal = -(self.FoOk[0] - self.FoOk[3])
        elif self.FoOk[0] < self.FoOk[3]:
            cmVal = self.FoOk[3] - self.FoOk[0]


        dmVal = dmVal
        amVal = amVal
        vrVal = vrVal
        cmVal = cmVal

        print ("parent", app)
        print ("facegroup", app.selectedFaceGroup)

        if self.faceGroupLookup.has_key(app.selectedFaceGroup):
            print("vrVal", vrVal)
            self.faceGroupLookup[app.selectedFaceGroup].onChanging(vrVal)
            self.faceGroupLookup[app.selectedFaceGroup].onChange(vrVal)
            self.faceGroupLookup[app.selectedFaceGroup].update()

        # if colVal == (176, 0, 0):
        #     smallManipTest.onChanging(vrVal)
        #     smallManipTest.onChange(vrVal)
        #     smallManipTest.update()
        # if colVal == (192, 0, 0):
        #     smallArm2.onChanging(cmVal)
        #     smallArm2.onChange(cmVal)
        #     smallArm2.update()
        # else:
        #     pass
        #if y >= 100 & y <= 200:

        # directManipTest.onChanging(amVal) #change val of slider based on new slider value variable (dynamic)
        # directManipTest.onChange(amVal) #change val of slider based on new slider value variable (both required)
        # directManipTest.update()
        # secondManipTest.onChanging(dmVal)
        # secondManipTest.onChange(dmVal)
        # secondManipTest.update()
        uniVal = dmVal

        #directManipTest.update()
        ##s.setValue(dmVal)
        #s.onChange(event)
        #blah = humanmodifier.ModifierAction(directManipTest, dmVal, dmVal, directManipTest.update())
        #humanmodifier.MouAction.nVar(mouseAction)

        return uniVal, mouseAction, dmVal, amVal, vrVal, cmVal #return mouse call and new 'slider' val based on mouse


    def onMouseUp(self, event):
        self.parent.callEvent('onMouseUp', event)

    def onMouseEntered(self, event):
        self.parent.callEvent('onMouseEntered', event)

    def onMouseExited(self, event):
        self.parent.callEvent('onMouseExited', event)
        #I don't think this is the correct format here!! 9/7/18
        #self.parent.callEvent('sliderReleased()', event)

    def onClicked(self, event):
        self.parent.callEvent('onClicked', event)
        #self.parent.callEvent('sliderPressed()', event)

    def onMouseWheel(self, event):
        self.parent.callEvent('onMouseWheel', event)

    def addTopWidget(self, widget):
        mh.addTopWidget(widget)
        self.widgets.append(widget)
        widget._parent = self
        if self.isVisible():
            widget.show()
        else:
            widget.hide()
        return widget

    def removeTopWidget(self, widget):
        self.widgets.remove(widget)
        mh.removeTopWidget(widget)

    def showWidgets(self):
        for w in self.widgets:
            w.show()

    def hideWidgets(self):
        for w in self.widgets:
            w.hide()

class TaskView(View):

    def __init__(self, category, name, label=None):
        super(TaskView, self).__init__()
        self.name = name
        self.category = category
        self.label = label
        self.focusWidget = None
        self.tab = None
        self.left, self.right = mh.addPanels()
        self.sortOrder = None

    def getModifiers(self):
        return {}

    def showWidgets(self):
        super(TaskView, self).showWidgets()
        mh.showPanels(self.left, self.right)

    def addLeftWidget(self, widget):
        return self.left.addWidget(widget)

    def addRightWidget(self, widget):
        return self.right.addWidget(widget)

    def removeLeftWidget(self, widget):
        self.left.removeWidget(widget)

    def removeRightWidget(self, widget):
        self.right.removeWidget(widget)

class Category(View):

    def __init__(self, name, label = None):
        super(Category, self).__init__()
        self.name = name
        self.label = label
        self.tasks = []
        self.tasksByName = {}
        self.tab = None
        self.tabs = None
        self.panel = None
        self.task = None
        self.sortOrder = None


    def _taskTab(self, task):
        if task.tab is None:
            task.tab = self.tabs.addTab(task.name, task.label or task.name, self.tasks.index(task))


    def realize(self, app):
        self.tasks.sort(key = lambda t: t.sortOrder)
        for task in self.tasks:
            self._taskTab(task)
            #self.addTBar()

        @self.tabs.mhEvent
        def onTabSelected(tab):
            self.task = tab.name
            app.switchTask(tab.name)

    def addTask(self, task):
        if task.name in self.tasksByName:
            raise KeyError('A task with this name already exists', task.name)
        if task.sortOrder == None:
            orders = [t.sortOrder for t in self.tasks]
            o = 0
            while o in orders:
                o = o +1
            task.sortOrder = o

        self.tasks.append(task)
        self.tasks.sort(key = lambda t: t.sortOrder)

        self.tasksByName[task.name] = task
        self.addView(task)
        if self.tabs is not None:
            self._taskTab(task)
        self.task = self.tasks[0].name

        categories = sorted(self.parent.categories.values(), key=lambda c: c.sortOrder)
        categoryOrder = categories.index(self)
        # Ensure that event order is per category, per task
        eventOrder = 1000 * categoryOrder + task.sortOrder
        self.parent.addEventHandler(task, eventOrder)

        return task

    def getTaskByName(self, name):
        return self.tasksByName.get(name)

# The application
app = None

class Application(events3d.EventHandler):
    """
   The Application.
    """

    singleton = None

    def __init__(self):
        global app
        app = self
        self.parent = self
        self.children = []
        self.objects = []
        self.categories = {}
        self.currentCategory = None
        self.currentTask = None
        self.mouseDownObject = None
        self.enteredObject = None
        self.fullscreen = False
        self.selectedFaceGroup = None

        self.tabs = None    # Assigned in mhmain.py

    def addObject(self, object):
        """
        Adds the object to the application. The object will also be attached and will get an OpenGL counterpart.
        :param object: The object to be added.
        :type object: gui3d.Object
        :return: The object, for convenience.
        :rvalue: gui3d.Object
        """
        if object._view:
            raise RuntimeError('The object is already attached to a view')

        object._view = weakref.ref(self)
        object._attach()

        self.objects.append(object)

        return object

    def removeObject(self, object):
        """
        Removes the object from the application. Its OpenGL counterpart will be removed as well.
        :param object: The object to be removed.
        :type object: gui3d.Object
        """
        if object not in self.objects:
            raise RuntimeError('The object is not a child of this view')

        object._view = None
        object._detach()

        self.objects.remove(object)

    def addView(self, view):
        """
        Adds the view to the application.The view will also be attached.
        :param view: The view to be added.
        :type view: gui3d.View
        :return: The view, for convenience.
        :rvalue: gui3d.View
        """
        if view.parent:
            raise RuntimeError('The view is already attached')

        view._parent = weakref.ref(self)
        view._updateVisibility()
        view._attach()

        self.children.append(view)

        return view

    def removeView(self, view):
        """
        Removes the view from the application. The view will be detached.
        :param view: The view to be removed.
        :type view: gui3d.View
        """
        if view not in self.children:
            raise RuntimeError('The view is not a child of this view')

        view._parent = None
        view._detach()

        self.children.remove(view)

    def isVisible(self):
        return True

    def getSelectedFaceGroupAndObject(self):
        picked = mh.getPickedColor()
        return selection.selectionColorMap.getSelectedFaceGroupAndObject(picked)

    def getSelectedFaceGroup(self):
        picked = mh.getPickedColor()
        #print "picked color:", picked
        return selection.selectionColorMap.getSelectedFaceGroup(picked)

    def getChanger(self):
        global sCheck
        picked = mh.getPickedColor()

        sCheck = picked
        return sCheck

    def addCategory(self, category, sortOrder = None):
        if category.name in self.categories:
            raise KeyError('A category with this name already exists', category.name)

        if category.parent:
            raise RuntimeError('The category is already attached')

        if sortOrder == None:
            orders = [c.sortOrder for c in self.categories.values()]
            o = 0
            while o in orders:
                o = o +1
            sortOrder = o

        category.sortOrder = sortOrder
        self.categories[category.name] = category

        categories = self.categories.values()
        categories.sort(key = lambda c: c.sortOrder)

        category.tab = self.tabs.addTab(category.name, category.label or category.name, categories.index(category))
        category.tabs = category.tab.child
        self.addView(category)
        category.realize(self)

        return category

    def switchTask(self, name):
        if not self.currentCategory:
            return
        newTask = self.currentCategory.tasksByName[name]

        if self.currentTask and self.currentTask is newTask:
            return

        if self.currentTask:
            log.debug('hiding task %s', self.currentTask.name)
            self.currentTask.hide()
            self.currentTask.hideWidgets()

        self.currentTask = self.currentCategory.tasksByName[name]

        if self.currentTask:
            log.debug('showing task %s', self.currentTask.name)
            print "DUCK", self.currentTask.name
            self.currentTask.show()
            self.currentTask.showWidgets()

    def switchCategory(self, name):

        # Do we need to switch at all

        if self.currentCategory and self.currentCategory.name == name:
            return

        # Does the category exist

        if not name in self.categories:
            return

        category = self.categories[name]

        # Does the category have at least one view

        if len(category.tasks) == 0:
            return

        if self.currentCategory:
            log.debug('hiding category %s', self.currentCategory.name)
            self.currentCategory.hide()
            self.currentCategory.hideWidgets()

        self.currentCategory = category

        log.debug('showing category %s', self.currentCategory.name)
        self.currentCategory.show()
        self.currentCategory.showWidgets()
        self.switchTask(category.task)

    def getCategory(self, name, sortOrder = None):
        category = self.categories.get(name)
        if category:
            return category
        return self.addCategory(Category(name), sortOrder = sortOrder)

    def getTask(self, category, task):
        """
        Retrieve a task by category and name.
        Will not create a task or category if it does not exist.
        Set category to None or False to search for a task by name. Will raise
        an exception when the result is ambiguous (there are multiple tasks with
        the same name in different categories).
        This quickhand is mostly useful for shell usage, but dangerous to use in
        a plugin.
        """
        if category:
            if not category in self.categories.keys():
                raise RuntimeWarning('Category with name "%s" does not exist.' % category)
            c = self.getCategory(category)
            if not task in c.tasksByName.keys():
                raise RuntimeWarning('Category "%s" does not contain a task with name "%s".' % (category, task))
            return c.getTaskByName(task)
        else:
            tasks = []
            for c in self.categories.keys():
                if task in self.getCategory(c).tasksByName.keys():
                    tasks.append(self.getCategory(c).tasksByName[task])
            if len(tasks) == 0:
                raise RuntimeWarning('No task with name "%s" found.' % task)
            if len(tasks) > 1:
                raise RuntimeWarning('Ambiguous result for task "%s", there are multiple tasks with that name.' % task)
            return tasks[0]

    # called from native

    def onMouseDownCallback(self, event):
        # Get picked object
        pickedObject = self.getSelectedFaceGroupAndObject()
        fg = self.getSelectedFaceGroup()

        # Do not allow picking detached objects (in case of stale picking buffer)
        if pickedObject and hasattr(pickedObject, 'view') and not pickedObject.view:
            pickedObject = None

        if pickedObject:
            object = pickedObject[1].object
        else:
            object = self

        if fg == None:
            self.selectedFaceGroup = None
        else:
            self.selectedFaceGroup = fg.name
        print "facegroup is 2:(" + fg.name + ")"

        # It is the object which will receive the following mouse messages
        self.mouseDownObject = object

        # Send event to the object
        if object:
            object.callEvent('onMouseDown', event)

    def onMouseUpCallback(self, event):
        if event.button == 4 or event.button == 5:
            return

        # Get picked object
        pickedObject = self.getSelectedFaceGroupAndObject()

        # Do not allow picking detached objects (in case of stale picking buffer)
        if pickedObject and hasattr(pickedObject, 'view') and not pickedObject.view:
            pickedObject = None

        if pickedObject:
            object = pickedObject[1].object
        else:
            object = self

        # Clean up handles to detached (guicommon.Object) objects
        if self.mouseDownObject and hasattr(self.mouseDownObject, 'view') and not self.mouseDownObject.view:
            self.mouseDownObject = None

        if self.mouseDownObject:
            self.mouseDownObject.callEvent('onMouseUp', event)
            if self.mouseDownObject is object:
                self.mouseDownObject.callEvent('onClicked', event)

    def onMouseMovedCallback(self, event):
        # Get picked object

        picked = self.getSelectedFaceGroupAndObject()
        #ugh = self.getSelectedFaceGroup()

        # Do not allow picking detached objects (in case of stale picking buffer)
        if picked and hasattr(picked, 'view') and not picked.view:
            picked = None

        if picked and picked[1]:
            group = picked[0]
            object = picked[1].object or self
        else:
            group = None
            object = self
        #print "facegroup is:("+ ugh.name+ ")"
        event.object = object
        event.group = group

        # Clean up handles to detached (guicommon.Object) objects
        if self.mouseDownObject and hasattr(self.mouseDownObject, 'view') and not self.mouseDownObject.view:
            self.mouseDownObject = None
        if self.enteredObject and hasattr(self.enteredObject, 'view') and not self.enteredObject.view:
            self.enteredObject = None

        if event.button:
            if self.mouseDownObject:
                self.mouseDownObject.callEvent('onMouseDragged', event)
        else:
            if self.enteredObject != object:
                if self.enteredObject:
                    self.enteredObject.callEvent('onMouseExited', event)
                self.enteredObject = object
                self.enteredObject.callEvent('onMouseEntered', event)

                self.getChanger()
            if object != self:
                object.callEvent('onMouseMoved', event)
            elif self.currentTask:
                self.currentTask.callEvent('onMouseMoved', event)

    def onMouseWheelCallback(self, event):
        if self.currentTask:
            self.currentTask.callEvent('onMouseWheel', event)

    def onResizedCallback(self, event):
        if self.fullscreen != event.fullscreen:
            module3d.reloadTextures()

        self.fullscreen = event.fullscreen

        for category in self.categories.itervalues():
            category.callEvent('onResized', event)
            for task in category.tasks:
                task.callEvent('onResized', event)
