import pandas as pd

from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QFileDialog, QLabel,
                               QGridLayout, QLineEdit)

from PySide6.QtCore import Qt


import sys
import VTestUI

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000,800)

class MyMainWindow(QMainWindow):
    def __init__(self, par):
        super().__init__()

        self.mainWindow = par
        self.dialog = QFileDialog()

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
    sys.exit(app.exec())