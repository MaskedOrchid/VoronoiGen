import pandas as pd

from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QFileDialog, QLabel,
                               QGridLayout)

import sys



class SubWindow(QWidget):
    def __init__(self):
        super().__init__()

        filename = ""
        self.button = QPushButton("Open File")
        self.button.clicked.connect(self.open_dialog)

        self.setGeometry(100,100,300,150)
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.label = QLabel()

        self.dialog = QFileDialog()


    def open_dialog(self, checked):

        filename = self.dialog.getOpenFileName(self,"Text Files (*.txt), *.txt")
        if not filename :
            self.label = QLabel("No File Selected")
        else:
            self.label = QLabel(filename[0])

        # DESTROY THE OLD BUTTON
        self.layout.removeWidget(self.button)
        self.button.deleteLater()
        self.button = None

        # ADD THE NAME OF THE FILE
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parser Testing Page")
        self.setGeometry(100,100,300,150)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.button = QPushButton("Start Parse Testing")

        self.button.clicked.connect(self.open_dialog)

        self.setCentralWidget(self.button)

        self.childWindow = SubWindow()

    def open_dialog(self, checked):
        self.childWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())