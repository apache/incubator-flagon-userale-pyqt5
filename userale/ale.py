# Copyright 2016 The Charles Stark Draper Laboratory, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from userale.version import __version__
from PyQt5.QtCore import QObject, QEvent
import datetime
import time
import logging
from userale.format import StructuredMessage

_ = StructuredMessage

class Ale (QObject):

    def __init__(self, 
                 output="userale.log",
                 autostart=True,
                 interval=5000,
                 user=None,
                 version=None,
                 details=False,
                 resolution=500,
                 shutoff=[]):
        """
        :param output: [str] The file or url path to which logs will be sent
        :param autostart: [bool] Should UserAle start auotmatically on app rendering
        :param interval: [int] The minimum time interval in ms betweeen batch transmission of logs
        :param user: [str] Identifier for the user of the application
        :param version: [str] The application version
        :param details: [bool] Should detailed logs (key strokes, input/change values) be recorded
        :param resolution: [int] Delay in ms between instances of high frequency logs like mouseovers, scrolls, etc
        :param shutoff: [list] Turn off logging for specific events. For example, to ignore mousedown events, ['mousedown']
    
        An example log will appear like this:

        .. code-block:: python

            {
                'target': 'testLineEdit',
                'path': ['Example', 'testLineEdit'],
                'clientTime': ,
                'location': {'x': 82, 'y': 0},
                'type': 'mouseHover',
                'userAction': 'true',
                'details' : [],
                'userId': 'userABC1234',
                'toolVersion': 'myApplication',
                'useraleVersion': '1.0.0 alpha'
            }
        """

        QObject.__init__(self)

        # UserAle Configuration
        self.output = output
        self.autostart = autostart
        self.interval = interval
        self.user = user
        self.version = version
        self.details = details
        self.resolution = resolution

        # Store logs
        self.logs = []

        # Configure logging
        self.logger = logging
        self.logger.basicConfig(level=logging.INFO,
                                filename=self.output,
                                format='%(message)s')

        # Drag/Drop - track duration
        self.dd = datetime.datetime.now ()

    def eventFilter(self, object, event):
        '''
        :param object: [QObject] The object being watched.
        :param event: [QEvent] 
        :return: [bool] Return true in order to filter the event out (stop it from being handled further). Otherwise return false.
        
        Filters events for the watched object (in this case, QApplication)
        '''

        data = None
        
        if (event.type () == QEvent.MouseButtonPress):
            data = self.handleMouseEvents ("mousedown", event, object)
        elif (event.type () == QEvent.MouseButtonRelease):
            data = self.handleMouseEvents ("mouseup", event, object)
        elif (event.type () == QEvent.MouseMove):
            data = self.handleMouseEvents ("mousemove", event, object)
        elif (event.type () == QEvent.KeyPress):
            data = self.handleKeyEvents ("keypress", event, object)
        elif (event.type () == QEvent.KeyRelease):
            data = self.handleKeyEvents ("keyrelease", event, object)
        elif (event.type () == QEvent.Leave):
            data = self.handleLeaveEvents ("keyrelease", event, object)         
        elif (event.type () == QEvent.Move):
            data = self.handleMoveEvents ("keyrelease", event, object)          
        elif (event.type () == QEvent.Resize):
            data = self.handleResizeEvents ("keyrelease", event, object)            
        elif (event.type () == QEvent.Scroll):
            data = self.handleScrollEvents ("keyrelease", event, object)            
        elif (event.type () == QEvent.DragEnter):
            data = self.handleDragEvents ("dragstart", event, object)   
        elif (event.type () == QEvent.DragLeave):
            data = self.handleDragEvents ("dragleave", event, object)   
        elif (event.type () == QEvent.DragMove):
            data = self.handleDragEvents ("dragmove", event, object)    
        elif (event.type () == QEvent.Drop):
            data = self.handleDragEvents ("dragdrop", event, object)    
        else:
            pass    

        # self.logs.append (data)
        if data is not None:
            self.logger.info (_(data))
        # return super(Ale, self).eventFilter(object, event)
        return False

    def getSelector (self, object):
        """
        :param object: [QObject] The base class for all Qt objects.
        :return: [str] The Qt object's name

        Get target object's name (object defined by user or object's meta class name)
        """

        return object.objectName() if object.objectName() else object.staticMetaObject.className()

    def getLocation (self, event):
        """
        :param event: [QEvent] The base class for all event classes.
        :return: [dict] A dictionary representation of the x and y positions of the mouse cursor.

        Grab the x and y position of the mouse cursor, relative to the widget that received the event.
        """

        try: 
            return {"x" : event.pos ().x (), "y" : event.pos ().y ()}
        except:
            return None

    def getPath (self, object):
        """
        :param object: [QObject] The base class for all Qt objects.
        :return: [list] List of QObjects up to the child object.

        Fetch the entire path up the root of the tree for a leaf node object.
        Recursive operation.
        """

        if object.parent() is not None:
            return self.getPath (object.parent()) + [self.getSelector (object)]
        else:
            return [self.getSelector (object)]

    def getClientTime (self):
        """
        :return: [str] String representation of the time the event was triggered.
        
        Capture the time the event was captured. 
        """

        return str (datetime.datetime.now ())

    def handleMouseEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a mouse event.

        Returns the userale log representing all mouse event data. 

        .. code-block:: python

        """
        
        return self.__create_msg (event_type, event, object)

    def handleKeyEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a key event.

        Returns the userale log representing all key events, including key name and key code.
        """

        details = {'key' : event.text (), 'keycode' : event.key ()}
        return self.__create_msg (event_type, event, object, details=details)

    def handleDragEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a drag event.

        Returns the userale log representing all drag events. 
        """

        details = {}
        if event_type == 'dragstart':
            # start timer
            self.dd = datetime.datetime.now ()
        elif event_type == 'dragdrop' or event_type == 'dragleave':
            details = {"elapsed" : str (datetime.datetime.now () - self.dd)}
            self.dd = datetime.datetime.now ()
        else:
            # drag move event - ignore
            pass

        return self.__create_msg (event_type, event, object, details=details)

    def handleMoveEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a drag event.

        Returns the userale log representing all move events. 
        """

        pass

    def handleLeaveEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a leave event.

        Returns the userale log representing all leave events. 
        """

        pass

    def handleResizeEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a resize event.

        Returns the userale log representing all resize events. 
        """

        pass

    def handleScrollEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a scroll event.

        Returns the userale log representing all scroll events. 
        """

        pass

    def __create_msg (self, event_type, event, object, details={}):
        """
        Geneate UserAle log describing an event.
        """

        data = {
            'target': self.getSelector (object) ,
            'path': self.getPath (object),
            'clientTime': self.getClientTime (),    
            'location': self.getLocation(event),
            'type': event_type ,
            'userAction': 'true',
            'details' : details,
            'userId': self.user,
            'toolVersion': self.version,
            'useraleVersion': __version__
        }

        return data
