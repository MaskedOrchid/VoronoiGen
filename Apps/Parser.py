# -=-=-=-=-=-=-=-=-= IGNORE THIS -=-=-=-=-=-=-=-=-=

import pandas as pd
import re
from PySide6.QtGui import QColor


from Apps import Label

class ParsedPackage:

    def __init__(self, x, y, l):
        self.xPosition = x
        self.yPosition = y
        self.label = l




class Parser:

    def __init__(self):
        self.labels = []
        self.packages = []

    def createLabel(self, n, c):
        lbl = Label.Label(n,QColor(c))
        if lbl in self.labels:
            return lbl # will refactor later TO DO
        else:
            self.labels.append(lbl)
            return lbl

    def parse(self, filepath):
        fileData = pd.read_csv(filepath, header=None, dtype=str)
        for i, row in fileData.iterrows():
            try:
                x = int(row[0])
                y = int(row[1])

                n = ""
                if len(row) > 2 and pd.notna(row[2]):
                    n = str(row[2])

                c = ""
                if len(row) > 3 and pd.notna(row[3]):
                    color = str(row[3])
                    match = re.search(r'^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
                    if match:
                        if color[0] != '#':
                            c = '#' + color
                        else:
                            c = color
                    else:
                        c = "#FFFFFF"
                lbl = self.createLabel(n,c)
                pkg = ParsedPackage(x, y, lbl)
                self.packages.append(pkg)

            except(ValueError, KeyError):
                continue




"""import pandas as pd

from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QFileDialog, QLabel,
                               QGridLayout, QLineEdit)

from PySide6.QtCore import Qt


import sys
import HomeView
import CreationView

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000,800)

class MyMainWindow(QMainWindow):
    def __init__(self, par):
        super().__init__()

        self.mainWindow = par

        self.setWindowTitle("Create a New Project")
        self.setFixedSize(800,450)

        self.layout = QGridLayout()


        self.button0 = QPushButton("Import Custom Dataset")
        self.button0.setFixedSize(175,25)

        self.button = QPushButton("Create")
        self.button.setFixedSize(100,25)

        self.button2 = QPushButton("Close")
        self.button2.setFixedSize(100,25)





        self.button0.clicked.connect(self.open_dialog)
        self.button.clicked.connect(self.open_canvas)

        self.button2.clicked.connect(self.close_dialog)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        lineedit = QLineEdit()
        lineedit.setFixedSize(175, 25)
        lineedit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        lineedit.setPlaceholderText("Input File Name Here...")

        self.layout = QVBoxLayout()
        self.layout.addWidget(lineedit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button,alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.label = QLabel()
        self.label.setText("No File Selected.")
        self.layout.addWidget(self.label)

        self.central_widget.setLayout(self.layout)

        self.childWindow = SubWindow()

    def close_dialog(self):
        self.close()

    def open_canvas(self):
        self.childWindow.show()
        if self.mainWindow:
            self.mainWindow.close()
        self.close()
    def open_dialog(self, checked):

        filename = self.dialog.getOpenFileName(self, caption="Open Data File", filter="CSV Files (*.csv)")
        if not filename:
            #self.label = QLabel("No File Selected")
            self.label.setText("No File Selected.")
        else:
           # self.label = QLabel(filename[0])
           if filename[0]:
                self.label.setText(f"Selected File: {filename[0]}")
                print(pd.read_csv(filename[0]))
           else:
               self.label.setText("No File Selected.")

        # DESTROY THE OLD BUTTON
       # self.layout.removeWidget(self.button)
        #self.button0.deleteLater()
       # self.button0 = None

        # ADD THE NAME OF THE FILE
        #self.layout.addWidget(self.label)
        #self.setLayout(self.layout)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = MyMainWindow(0)
    w.show()
    sys.exit(app.exec())"""