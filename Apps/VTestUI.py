import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QLabel, QSpacerItem,
                                QLayout, QDialog
                               )

from PySide6.QtGui import (QImage,QPalette,QBrush,QPixmap,QIcon,QFontDatabase, QFont)

from PySide6.QtCore import QSize, Qt

import sys
import os
import Parser
import CreationView
import MainApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        current_directory = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(current_directory, "Fonts/VanillaExtractRegular.ttf")

        font_id = QFontDatabase.addApplicationFont(file)

        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font_family_name = font_families[0]
        custom_font = QFont(font_family_name, 20)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setObjectName("MainWindow")
        self.setWindowTitle("VoronoiGen")
        self.setFixedSize(800, 450)

        self.childWindow = Parser.MyMainWindow(self)

        file = os.path.join(current_directory, "Images/BG_IMG_TEST.png")

        img = QImage(file)
        img = img.scaled(QSize(800, 450))

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(img))
        self.setPalette(palette)

        file = os.path.join(current_directory, "Images/Logo.png")
        img2 = QPixmap(file)

        label = QLabel(self)
        label.setPixmap(img2)
        label.setScaledContents(True)
        label.resize(700, 125)

        label.show()

        self.button = QPushButton('Create New Project')
        file = os.path.join(current_directory, "Images/Button1.png")

        self.button.setFixedSize(300, 70)

        base_dir = os.path.dirname(__file__)
        image_path = os.path.join(base_dir, "Images", "Button1.png")
        image_path = image_path.replace("\\", "/")

        # TO DO: figure out how to call this shit without needing the absolute directory
        self.button.setStyleSheet(f"""
                                QPushButton {{ border-image: url({image_path});
                                    background-color: transparent;
                                    font-family: {font_family_name};
                                    font-size: 16pt; 
                                    color: #6D9A50;
                                }} 
                                QPushButton:hover {{
                                    border: 10px solid #FFCE75;
                                }}
                                """)



        self.button.clicked.connect(self.open_dialog)

        self.button3 = QPushButton('Open Project')
        file = os.path.join(current_directory, "Images/Button1.png")

        self.button3.setFixedSize(300, 70)

        # TO DO: figure out how to call this shit without needing the absolute directory
        self.button3.setStyleSheet(f"""
                                QPushButton {{ border-image: url({image_path});
                                    background-color: transparent;
                                    font-family: {font_family_name};
                                    font-size: 16pt; 
                                    color: #6D9A50;
                                }} 
                                QPushButton:hover {{
                                    border: 10px solid #FFCE75;
                                }}
                                """)



        self.button3.clicked.connect(self.open_dialog)



        self.button2 = QPushButton('Exit')

        file = os.path.join(current_directory, "Images/Button2.png")

        self.button2.setFixedSize(QSize(160, 40))

        base_dir = os.path.dirname(__file__)
        image_path = os.path.join(base_dir, "Images", "Button2.png")
        image_path = image_path.replace("\\", "/")

        self.button2.setStyleSheet(f"""
                                QPushButton {{ border-image: url({image_path});
                                    background-color: transparent;
                                    font-family: {font_family_name};
                                    font-size: 14pt; 
                                    color: #8D8D8D;
                                }} 
                                QPushButton:hover {{
                                    border: 5px solid #FFCE75;
                                }}
                                """)



        self.button2.clicked.connect(self.exit_app)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.insertStretch(0)
        self.layout.addSpacerItem(QSpacerItem(100,75))
        self.layout.setContentsMargins(50, 0, 0, 0)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.central_widget.setLayout(self.layout)


    def open_dialog(self, checked):
        #self.childWindow.show()
       # self.childWindow.mainWindow = self
        dialog = CreationDialog(self)
        dialog.exec()

    def open_dialog2(self, checked):
       # self.childWindow.show()
       dialog = CreationDialog(self)
       dialog.exec()

    def exit_app(self):
        self.close()

class CreationDialog(QDialog):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainWin = mainwindow
        self.ui = CreationView.Ui_CreationView()
        self.ui.setupUi(self)

        self.name = ""
        self.width = 0
        self.height = 0
        self.mainApp = ()

    def accept(self):

        self.name = self.ui.lineEdit.text()
        try:
            self.width = int(self.ui.lineEdit_9.text())
            self.height = int(self.ui.lineEdit_2.text())
        except ValueError:
            print("Width and height must be numbers!")
            return
        mainapp = MainApp.MainWindow(self.width, self.height, self.name)
        mainapp.show()
        self.mainWin.close()
        super().accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())