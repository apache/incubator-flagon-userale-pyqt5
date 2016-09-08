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

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QMessageBox
from PyQt5.QtCore import QCoreApplication, QObject, QEvent

from userale.ale import Ale

# Widget #1
class TestApplication (QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        qbtn = QPushButton('Quit', self)
        qbtn.setObjectName ("testApplicationButton")
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)       
         
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()
        
def test_app ():
    app = QApplication(sys.argv)    
    app.setObjectName ("testApplication")
    ex = TestApplication()
    ale = Ale (output="mouse.log", user="testUser", toolname="mousetest", toolversion="0.0.1")
    # install globally
    app.installEventFilter (ale)

    sys.exit (app.exec_())