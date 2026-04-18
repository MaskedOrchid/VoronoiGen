from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout,
                                QWidget, QLabel, QSpacerItem)

from PySide6.QtGui import (QImage, QPalette, QBrush, QPixmap)

from PySide6.QtCore import (QSize, Qt)

import os

from Apps.StartupClasses import HomeController
from Apps.HelperClasses.FontInitialization import FontInitialization
from Apps.HelperClasses.QSSGrabber import (QSSGrabber, Styles)


class MainWindow(QMainWindow):
    """

        The main UI renderer for the home/startup window.

    """

    def __init__(self, hc):
        super().__init__()

        self.homeController = hc

        # Initialize UI style classes
        self.fi = FontInitialization()
        self.grabber = QSSGrabber()

        # Set up the core window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setObjectName("MainWindow")
        self.setWindowTitle("VoronoiGen")
        self.setFixedSize(800, 450)

        # -=-=-=- Add background image -=-=-=-
        current_directory = os.path.dirname(os.path.realpath(__file__))
        temp_dir = current_directory.split("Apps")[0] + "Apps\\_UI Documents"
        file = os.path.join(temp_dir, "Images/BG_IMG_TEST.png")

        img = QImage(file)
        img = img.scaled(QSize(800, 450))

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(img))
        self.setPalette(palette)

        # -=-=-=- Add logo image -=-=-=-
        file = os.path.join(temp_dir, "Images/Logo.png")
        img2 = QPixmap(file)

        label = QLabel(self)
        label.setPixmap(img2)
        label.setScaledContents(True)
        label.resize(700, 125)

        label.show()

        # -=-=-=- Create new project button -=-=-=-
        self.createButton = QPushButton('Create New Project')
        self.createButton.setFixedSize(300, 70)
        self.createButton.setStyleSheet(self.grabber.grabStyle(Styles.GREENBUTTON))
        self.createButton.clicked.connect(self.homeController.open_dialog)

        # -=-=-=- Open project button -=-=-=-
        self.openButton = QPushButton('Open Project')
        self.openButton.setFixedSize(300, 70)
        self.openButton.setStyleSheet(self.grabber.grabStyle(Styles.GREENBUTTON))
        self.openButton.clicked.connect(self.homeController.openNoiDialog)

        # -=-=-=- Exit Program Button -=-=-=-
        self.exitButton = QPushButton('Exit')
        self.exitButton.setFixedSize(QSize(160, 40))
        self.exitButton.setStyleSheet(self.grabber.grabStyle(Styles.GRAYBUTTON))
        self.exitButton.clicked.connect(self.homeController.exit_app)

        # Setup window layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.createButton)
        self.layout.addWidget(self.openButton)
        self.layout.addWidget(self.exitButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.insertStretch(0)
        self.layout.addSpacerItem(QSpacerItem(100,75))
        self.layout.setContentsMargins(50, 0, 0, 0)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


        self.central_widget.setLayout(self.layout)


