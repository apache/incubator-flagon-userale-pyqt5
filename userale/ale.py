# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from userale.version import __version__
from userale.format import JsonFormatter
from PyQt5.QtCore import QObject, QEvent
import datetime
import logging
import uuid

_ = JsonFormatter

class Ale (QObject):

    def __init__(self, 
                 output="userale.log",
                 user=None,
                 session=None,
                 toolname=None,
                 toolversion=None,
                 keylog=False,
                 resolution=100,   
                 shutoff=[]):
        """
        :param output: [str] The file or url path to which logs will be sent
        :param user: [str] Identifier for the user of the application
        :param session: [str] Session tag to track same user with multiple sessions. If a session is not provided, one will be created
        :param toolname: [str] The application name
        :param toolversion: [str] The application version
        :param keylog: [bool] Should detailed key logs be recorded. Default is False
        :param resolution: [int] Delay in ms between instances of high frequency logs like mousemoves, scrolls, etc. Default is 100ms (10Hz).
        :param shutoff: [list] Turn off logging for specific events
    
        An example log will appear like this:

        .. code-block:: python

            {
                'target': 'testLineEdit',
                'path': ['Example', 'testLineEdit'],
                'clientTime': '2016-08-03 16:12:03.460573',
                'location': {'x': 82, 'y': 0},
                'type': 'mousemove',
                'userAction': 'true',
                'details' : {},
                'userId': 'userABC1234',
                'session': '5ee42ccc-852c-44d9-a937-28d7901e4ead',
                'toolName': 'myApplication',
                'toolVersion': '3.5.0',
                'useraleVersion': '0.1.0'
            }
        """

        QObject.__init__(self)
        # UserAle Configuration
        self.output = output
        self.user = user
        # Autogenerate session id if session is not configured
        self.session = session if session is not None else str (uuid.uuid4 ())
        self.toolname = toolname
        self.toolversion = toolversion
        self.keylog = keylog
        self.resolution = resolution
        self.shutoff = shutoff

        # Configure logging
        self.logger = logging
        self.logger.basicConfig(level=logging.INFO,
                                filename=self.output,
                                format='%(message)s')

        # Mapping of all events to methods
        self.map = {
            QEvent.MouseButtonPress: {'mousedown': self.handleMouseEvents},
            QEvent.MouseButtonRelease: {'mouseup': self.handleMouseEvents},
            QEvent.MouseMove: {'mousemove': self.handleMouseEvents},
            QEvent.Enter: {'mouseenter': self.handleMouseEvents},
            QEvent.Leave: {'mouseleave': self.handleMouseEvents},
            QEvent.DragEnter: {'dragenter': self.handleDragEvents},
            QEvent.DragLeave: {'dragleave': self.handleDragEvents},
            QEvent.DragMove: {'dragmove': self.handleDragEvents},
            QEvent.Drop: {'dragdrop': self.handleDragEvents},
            QEvent.KeyPress: {'keypress': self.handleKeyEvents},
            QEvent.KeyRelease: {'keyrelease': self.handleKeyEvents},
            QEvent.Move: {'move': self.handleMoveEvents},
            QEvent.Resize: {'resize': self.handleResizeEvents},
            QEvent.Scroll: {'scroll': self.handleScrollEvents}
        }

        # Turn on/off keylogging & remove specific filters
        for key in list (self.map):
            name = list (self.map[key]) [0]
            if name in self.shutoff or (not self.keylog and (name == 'keypress' or name == 'keyrelease')):
                del self.map [key]

        # Sample rate 
        self.hfreq = [QEvent.MouseMove, QEvent.DragMove, QEvent.Scroll]
        self.logs = []
        self.last = None
        self.timer = None
        self.flag = False

    def eventFilter (self, object, event):
        '''
        :param object: [QObject] The object being watched.
        :param event: [QEvent] The event triggered by a user action.
        :return: [bool] Propagate filter up if other objects needs to be handled
        
        Filters events for the watched widget (in this case, QApplication)
        '''

        if self.flag == False:
            self.flag = True
            self.timer = datetime.datetime.now ()

        data = None
        t = event.type ()

        if t in self.map:        
            # Handle leaf node 
            if object.isWidgetType () and len(object.children ()) == 0:
                name = list (self.map [t].keys())[0]
                method = list (self.map [t].values())[0]
                data = method (name, event, object)

            # Handle window object
            else:
                # How to handle events on windows? It comes before the child widgets in window? 
                # Either an event actually ocurred on window or is an effect of event propagation. 
                pass

        # Sample data
        self.logs.append (data)

        # Check time elapsed
        elapsed = datetime.datetime.now () - self.timer
        if elapsed.seconds == 1:
            # print ("count = %d", len (self.logs)) 
            self.flag = False
            self.logs = []

        if data is not None:
            self.logger.info (_(data))

        return super(Ale, self).eventFilter (object, event)

    def getSender (self, object):
        '''
        :param object: [QObject] The object being watched.
        :return: [QObject] The QObject 
        '''

        sender = None
        try:
            sender = object.sender () if object.sender() is not None else None   
        except:
            pass
        return sender

    def getSelector (self, object):
        """
        :param object: [QObject] The base class for all Qt objects.
        :return: [str] The Qt object's name

        Get target object's name (object defined by user or object's meta class name).
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
        :return: [list] List of QObjects.

        Generate the entire object hierachy from root to leaf node. 
        """

        if object.parent() is not None:
            return self.getPath (object.parent()) + [self.getSelector (object)]
        else:
            return [self.getSelector (object)]

    def getClientTime (self):
        """
        :return: [str] String representation of the time the event was captured.
        
        Capture the time the event was captured in milliseconds since the UNIX epoch (January 1, 1970 00:00:00 UTC)
        """

        return int (time.time() * 1000)

    def handleMouseEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a mouse event.

        Returns the userale log representing all mouse event data. 
        """

        details = {}
        return self.__create_msg (event_type, event, object, details=details)

    def handleKeyEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a key event.

        Returns the userale log representing all key events, including key name and key code.
        """

        details = {"key" : event.text (), "keycode" : event.key ()}
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

        try:
            details ["source"] = self.getSelector (event.source ())      
        except:
            details ["source"] = None

        return self.__create_msg (event_type, event, object, details=details)

    def handleMoveEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a drag event.

        Returns the userale log representing all move events. 
        """

        details = {"oldPos" : {"x" : event.oldPos ().x (), "y" : event.oldPos ().y ()}}
        return self.__create_msg (event_type, event, object, details=details)
        
    def handleResizeEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a resize event.

        Returns the userale log representing all resize events. 
        """

        details = {"size" : {"height" : event.size ().height (), "width" : event.size ().width ()},
                   "oldSize":  {"height" : event.oldSize ().height (), "width" : event.oldSize ().width ()}}
        return self.__create_msg (event_type, event, object, details=details)

    def handleScrollEvents (self, event_type, event, object):
        """
        :param event_type: [str] The string representation of the type of event being triggered by the user.
        :param event: [QEvent] The base class for all event classes.
        :param object: [QObject] The base class for all Qt objects.
        :return: [dict] A userale log describing a scroll event.

        Returns the userale log representing all scroll events. 
        """

        return self.__create_msg (event_type, event, object)

    def __create_msg (self, event_type, event, object, details={}):
        """
        Geneate UserAle log describing an event.
        """

        data = {
            "target": self.getSelector (object) ,
            "path": self.getPath (object),
            "clientTime": self.getClientTime (),    
            "location": self.getLocation (event),
            "type": event_type ,
            "userAction": True,   # legacy field
            "details" : details,
            "userId": self.user,
            "session": self.session,
            "toolName": self.toolname,
            "toolVersion": self.toolversion,
            "useraleVersion": __version__
        }

        return data
