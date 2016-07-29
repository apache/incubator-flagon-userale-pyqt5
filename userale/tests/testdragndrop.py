# -*- coding: utf-8 -*-

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


class Example(QWidget):
  
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


def test_drag ():
    app = QApplication(sys.argv)
    # Turn off mouse click's and keylogging
    ale = Ale (shutoff=['mousedown', 'mouseup'], keylog=True)
    # install globally
    app.installEventFilter (ale)
    ex = Example()
    ex.show()
    app.exec_()  