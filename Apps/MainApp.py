
#imports
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QLabel, QVBoxLayout,
                               QWidget)

import sys
#Replace with actual Classes and more logic
class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        #This defines a vertical box layout group
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        #setting this window to have this layout as the main layout
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Push for Window")
        #connecting a button click action to a class functions
        self.button.clicked.connect(self.show_new_window)
        #setting the central widget ( widgets are like larger object
        # classes that can be docked in a window
        self.setCentralWidget(self.button)
        #creating a sub window class
        self.childWindow = SubWindow()

    def show_new_window(self, checked):
        #this shows the new window, note this object does exist  without being shown
        #and gets instantiated during MainWindow creation
        self.childWindow.show()


#this starts up the process to open and run the main window object
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()