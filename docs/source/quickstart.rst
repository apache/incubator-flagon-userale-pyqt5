.. _quickstart:

Quickstart Guide
================

Instrumenting Your Application Globally with UserAle
----------------------------------------------------

It's very simple to instrument a PyQt5 application with UserAle. Simply import the UserAle library and register it with your application. 

Below is an example PyQt5 application taken from ZetCode PyQt5 tutorial instrumented with UserAle.

::

	import sys
	from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QMessageBox
	from PyQt5.QtCore import QCoreApplication, QObject, QEvent

	from userale.ale import Ale

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
	        
	if __name__ == '__main__':
	    app = QApplication(sys.argv)    
	    ex = TestApplication()
	    # Initiate UserAle
	    ale = Ale ()
	    # install globally
	    app.installEventFilter (ale)

	    sys.exit (app.exec_())

Before we enter the mainloop of the application, UserAle needs to register the application to be instrumented. 
Simply instantiate UserAle and install it as an event filter in your application. 

::

	# Initiate UserAle
	ale = Ale ()
	# install globally
	app.installEventFilter (ale)