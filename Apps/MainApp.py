import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QScrollArea
)
from PySide6.QtCore import Qt, QCoreApplication

from VoronoiHandler import VoronoiHandler, DrawModes
from VoronoiCanvas import VoronoiCanvas
from LabelView import LabelView


class MainWindow(QMainWindow):
    def __init__(self, cx, cy, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setMinimumSize(1200, 700)

        self.handler = VoronoiHandler()

        self.canvas = VoronoiCanvas(self.handler, cx, cy)
        self.handler.setCanvas(self.canvas)

        self.label_view = LabelView()
        self.handler.label_model = self.label_view.get_model()

        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(15)
        tool_layout.setContentsMargins(10, 10, 10, 10)

        add_btn = QPushButton("Add")
        add_btn.setFixedHeight(40)
        add_btn.clicked.connect(lambda: self.handler.setMode(DrawModes.Add))

        remove_btn = QPushButton("Remove")
        remove_btn.setFixedHeight(40)
        remove_btn.clicked.connect(lambda: self.handler.setMode(DrawModes.Remove))

        edit_btn = QPushButton("Edit")
        edit_btn.setFixedHeight(40)
        edit_btn.clicked.connect(lambda: self.handler.setMode(DrawModes.Select))

        tool_layout.addWidget(add_btn)
        tool_layout.addWidget(remove_btn)
        tool_layout.addWidget(edit_btn)

        header_layout = QHBoxLayout()
        label_title = QLabel("Label Manager")

        add_label_btn = QPushButton("+ Add Label")
        add_label_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border-radius: 6px;
                padding: 6px 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)
        add_label_btn.clicked.connect(self.label_view.on_add_clicked)

        header_layout.addWidget(label_title)
        header_layout.addWidget(add_label_btn)
        tool_layout.addLayout(header_layout)

        self.label_view.setMinimumWidth(350)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.label_view)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        tool_layout.addWidget(scroll)
        tool_layout.addStretch()

        tool_panel = QWidget()
        tool_panel.setLayout(tool_layout)
        tool_panel.setMinimumWidth(350)
        tool_panel.setMaximumWidth(450)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)

        main_layout.addStretch(1)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        content_layout.addWidget(tool_panel)
        content_layout.addWidget(self.canvas)

        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)

        # adding the new action
        new_action = QAction("New Project", self)
        new_action.setStatusTip("This creates a new Project")
        new_action.triggered.connect(self.New)
        # adding the Open action
        open_action = QAction("Open Project", self)
        open_action.setStatusTip("This Opens a Project")
        open_action.triggered.connect(self.Open)
        # adding the Export action
        save_action = QAction("Save Project", self)
        save_action.setStatusTip("This saves the current Project")
        save_action.triggered.connect(self.Save)
        # adding the Export action
        export_action = QAction("Export Diagram", self)
        export_action.setStatusTip("This exports the Voronoi Diagram as an image")
        export_action.triggered.connect(self.Export)
        # adding the Quit action
        quit_action = QAction("Quit", self)
        quit_action.setStatusTip("Closes Program")
        quit_action.triggered.connect(QCoreApplication.quit)

        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(export_action)
        file_menu.addAction(quit_action)

        # Voronoi_menus
        Line_menu = self.menu.addMenu("&Line Options")
        # adding the Line toggle on action
        lineOn_action = QAction("Toggle lines on", self)
        lineOn_action.triggered.connect(self.ToggleLinesOn)
        # adding the Line toggle on action
        lineOff_action = QAction("Toggle lines off", self)
        lineOff_action.triggered.connect(self.ToggleLinesOff)
        Line_menu.addActions([lineOn_action, lineOff_action])

        Site_menu = self.menu.addMenu("&Site Options")
        # adding the Line toggle on action
        siteOn_action = QAction("Toggle sites on", self)
        siteOn_action.triggered.connect(self.ToggleSitesOn)
        # adding the Line toggle on action
        siteOff_action = QAction("Toggle sites off", self)
        siteOff_action.triggered.connect(self.ToggleSitesOff)
        Site_menu.addActions([siteOn_action, siteOff_action])


        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

#This need to be the toolbar widget--> Needs to be refactored
    def ToggleAdd(self):
        self.handler.setMode(DrawModes.Add)

    def ToggleRemove(self):
        self.handler.setMode(DrawModes.Remove)

    #toolbar functions --> Need to be refactored
    def Save(self):
        #this function will save the project
        print("Saving Project")

    def Export(self):
        #this function will export the voronoi diagram as an image
        print("Exporting Voronoi Diagram")

    def Open(self):
        #this function will open a project
        print("Open Project")
        self.Parser.show()

    def New(self):
        #this function will create a new project
        print("Create new Project")

    def ToggleLinesOn(self):
        self.handler.toggleLines(True)

    def ToggleLinesOff(self):
        self.handler.toggleLines(False)

    def ToggleSitesOn(self):
        self.handler.toggleSites(True)

    def ToggleSitesOff(self):
        self.handler.toggleSites(False)


