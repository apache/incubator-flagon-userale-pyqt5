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

"""
ZetCode PyQt5 tutorial

This is a simple drag and
drop example. 

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QPushButton, QWidget, 
    QLineEdit, QApplication)

from userale.ale import Ale

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super().__init__(title, parent)
        
        self.setAcceptDrops(True)
        

    def dragEnterEvent(self, e):
      
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        
        self.setText(e.mimeData().text()) 


class ExampleWidget(QWidget):
  
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):

        edit = QLineEdit('', self)
        edit.setObjectName ("testLineEdit")
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.setObjectName ("testButton")
        button.move(190, 65)
        
        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 150)
        self.setObjectName ("examplewidget1")

def test_drag ():
    app = QApplication(sys.argv)
    app.setObjectName ("dragApplication")
    # Turn off mouse click's and keylogging
    ale = Ale (shutoff=['mousemove', 'mousedown', 'dragmove'], keylog=True)
    # install globally
    app.installEventFilter (ale)
    ex = ExampleWidget()
    ex.show()
    app.exec_()  