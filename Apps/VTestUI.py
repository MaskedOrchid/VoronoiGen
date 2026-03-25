import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QLabel, QSpacerItem,
                                QLayout
                               )

from PySide6.QtGui import (QImage,QPalette,QBrush,QPixmap,QIcon,QFontDatabase, QFont)

from PySide6.QtCore import QSize, Qt

import sys
import os
import Parser


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

        # TO DO: figure out how to call this shit without needing the absolute directory
        self.button.setStyleSheet(f"""
                                QPushButton {{ border-image: url(C:/Users/ciphe/Cloned Projects/VoronoiGen/Apps/Images/Button1.png);
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
                                QPushButton {{ border-image: url(C:/Users/ciphe/Cloned Projects/VoronoiGen/Apps/Images/Button1.png);
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

        self.button2.setStyleSheet(f"""
                                QPushButton {{ border-image: url(C:/Users/ciphe/Cloned Projects/VoronoiGen/Apps/Images/Button2.png);
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
        self.childWindow.show()
        self.childWindow.mainWindow = self
    def open_dialog2(self, checked):
        self.childWindow.show()
    def exit_app(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())