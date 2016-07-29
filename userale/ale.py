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
from userale.format import StructuredMessage

from PyQt5.QtCore import QObject, QEvent
import datetime
import logging

_ = StructuredMessage

class Ale (QObject):

    def __init__(self, 
                 output="userale.log",
                 interval=5000,
                 user=None,
                 version=None,
                 keylog=False,
                 resolution=500,
                 shutoff=[]):
        """
        :param output: [str] The file or url path to which logs will be sent
        :param interval: [int] The minimum time interval in ms betweeen batch transmission of logs
        :param user: [str] Identifier for the user of the application
        :param version: [str] The application version
        :param keylog: [bool] Should detailed key logs be recorded. Default is False
        :param resolution: [int] Delay in ms between instances of high frequency logs like mouseovers, scrolls, etc
        :param shutoff: [list] Turn off logging for specific events
    
        An example log will appear like this:

        .. code-block:: python

            {
                'target': 'testLineEdit',
                'path': ['Example', 'testLineEdit'],
                'clientTime': ,
                'location': {'x': 82, 'y': 0},
                'type': 'mousemove',
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
        self.interval = interval
        self.user = user
        self.version = version
        self.keylog = keylog
        self.resolution = resolution
        self.shutoff = shutoff

        # Store logs
        self.logs = []

        # Configure logging
        self.logger = logging
        self.logger.basicConfig(level=logging.INFO,
                                filename=self.output,
                                format='%(message)s')

        # Drag/Drop - track duration
        self.dd = datetime.datetime.now ()

        # Mapping of all events to methods
        self.map = {
            QEvent.MouseButtonPress: {'mousedown': self.handleMouseEvents},
            QEvent.MouseButtonRelease: {'mouseup': self.handleMouseEvents},
            QEvent.MouseMove: {'mousemove': self.handleMouseEvents},
            QEvent.DragEnter: {'dragstart': self.handleDragEvents},
            QEvent.DragLeave: {'dragleave': self.handleDragEvents},
            QEvent.DragMove: {'dragmove': self.handleDragEvents},
            QEvent.Drop: {'dragdrop': self.handleDragEvents},
            QEvent.KeyPress: {'keypress': self.handleKeyEvents},
            QEvent.KeyRelease: {'keyrelease': self.handleKeyEvents}
        }

        # Turn on/off keylogging & remove specific filters
        for key in list (self.map):
            name = list (self.map[key]) [0]
            if name in self.shutoff or (not self.keylog and (name == 'keypress' or name == 'keyrelease')):
                del self.map [key]

    def eventFilter(self, object, event):
        '''
        :param object: [QObject] The object being watched.
        :param event: [QEvent] 
        :return: [bool] Return true in order to filter the event out (stop it from being handled further). Otherwise return false.
        
        Filters events for the watched object (in this case, QApplication)
        '''

        data = None
        t = event.type ()

        if len (object.children ()) > 0 and t in self.map:
            name = list (self.map [t].keys())[0]
            method = list (self.map [t].values())[0]
            data = method (name, event, object)

        # self.logs.append (data)
        if data is not None:
            self.logger.info (_(data))
        return super(Ale, self).eventFilter (object, event)

    def getSelector (self, object):
        """
        :param object: [QObject] The base class for all Qt objects.
        :return: [str] The Qt object's name

        Get target object's name (object defined by user or object's meta class name)
        """

        return object.objectName () if object.objectName () else object.staticMetaObject.className ()

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
            details = {"source" : self.getSelector (event.source())}
        elif event_type == 'dragdrop':
            details = {"elapsed" : str (datetime.datetime.now () - self.dd),
                       "source" : self.getSelector (event.source())}
            self.dd = datetime.datetime.now ()
        else:
            # drag move/leave event - ignore
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
            'location': self.getLocation (event),
            'type': event_type ,
            'userAction': 'true',
            'details' : details,
            'userId': self.user,
            'toolVersion': self.version,
            'useraleVersion': __version__
        }

        return data
