# imports
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QLabel, QVBoxLayout,
                               QWidget, QHBoxLayout, QToolBar)
import sys

# NEW: Import your label system
from LabelView import LabelView
from LabelModel import LabelModel

#class imports
from VoronoiHandler import VoronoiHandler, DrawModes
from Parser import MyMainWindow


# Replace with actual Classes and more logic
class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        # This defines a vertical box layout group
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        # setting this window to have this layout as the main layout
        self.setLayout(layout)


# NEW: Label manager window class
class LabelManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label Manager")
        self.setMinimumSize(400, 500)
        layout = QVBoxLayout()
        self.label_view = LabelView()
        layout.addWidget(self.label_view)
        self.setLayout(layout)

    def get_label_model(self):
        return self.label_view.get_model()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VoronoiGen")

        # This is made just for the UI interface test!!!--> should be refactored into actual code/project
        mainlayout = QHBoxLayout()
        ToolPanelLayout=QVBoxLayout()

        #main classes
        self.VoronoiDiagram=VoronoiHandler()
        # NEW: Create label manager window
        self.labelManagerWindow = LabelManagerWindow()
        self.Parser=MyMainWindow(self)

        #setting up toolbar buttons--> could be done by a toolbar object
        self.ToggleAddButton=QPushButton("Add")
        self.ToggleAddButton.clicked.connect(self.ToggleAdd)

        self.ToggleRemoveButton=QPushButton("Remove")
        self.ToggleRemoveButton.clicked.connect(self.ToggleRemove)

        #setting up basic toolbar
        ToolPanelLayout.addWidget(self.ToggleAddButton)
        ToolPanelLayout.addWidget(self.ToggleRemoveButton)
        ToolPanelLayout.addWidget(self.labelManagerWindow)

        # toolbar widget
        self.ToolPanel = QWidget()
        self.ToolPanel.setLayout(ToolPanelLayout)

        #setting up the main layout toolbar+Canvas
        mainlayout.addWidget(self.ToolPanel)
        mainlayout.addWidget(self.VoronoiDiagram.GetCanvas)

        #Center Widget
        self.CenterPanel=QWidget()
        self.CenterPanel.setLayout(mainlayout)

        self.setCentralWidget(self.CenterPanel)

        #adding the new action
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
        #adding the Export action
        export_action = QAction("Export Diagram", self)
        export_action.setStatusTip("This exports the Voronoi Diagram as an image")
        export_action.triggered.connect(self.Export)
        #adding the Quit action
        quit_action = QAction("Quit", self)
        quit_action.setStatusTip("Closes Program")
        quit_action.triggered.connect(QCoreApplication.quit)

        #adding relevant buttons to the file menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(export_action)
        file_menu.addAction(quit_action)

        #Voronoi_menus
        Line_menu=self.menu.addMenu("&Line Options")
        # adding the Line toggle on action
        lineOn_action = QAction("Toggle lines on", self)
        lineOn_action.triggered.connect(self.ToggleLinesOn)
        # adding the Line toggle on action
        lineOff_action = QAction("Toggle lines off", self)
        lineOff_action.triggered.connect(self.ToggleLinesOff)
        Line_menu.addActions([lineOn_action,lineOff_action])

        Site_menu = self.menu.addMenu("&Site Options")
        # adding the Line toggle on action
        siteOn_action = QAction("Toggle sites on", self)
        siteOn_action.triggered.connect(self.ToggleSitesOn)
        # adding the Line toggle on action
        siteOff_action = QAction("Toggle sites off", self)
        siteOff_action.triggered.connect(self.ToggleSitesOff)
        Site_menu.addActions([siteOn_action, siteOff_action])


        # # NEW: Add label manager button
        # self.label_btn = QPushButton("Open Label Manager")
        # self.label_btn.clicked.connect(self.show_label_manager)
        #
        # # NEW: Create layout to hold both buttons
        # central_widget = QWidget()
        # layout = QVBoxLayout()
        # central_widget.setLayout(layout)
        # layout.addWidget(self.label_btn)
        # self.setCentralWidget(central_widget)
        #
        # # creating a sub window class
        # self.childWindow = SubWindow()

    def show_new_window(self, checked):
        # this shows the new window, note this object does exist without being shown
        # and gets instantiated during MainWindow creation
        self.childWindow.show()

    # NEW: Show label manager window
    def show_label_manager(self, checked):
        if self.labelManagerWindow is None:
            self.labelManagerWindow = LabelManagerWindow()
        self.labelManagerWindow.show()

    # NEW: Get label model for other components
    def get_label_model(self):
        if self.labelManagerWindow:
            return self.labelManagerWindow.get_label_model()
        return None

    #This need to be the toolbar widget--> Needs to be refactored
    def ToggleAdd(self):
        self.VoronoiDiagram.setMode(DrawModes.Add)

    def ToggleRemove(self):
        self.VoronoiDiagram.setMode(DrawModes.Remove)

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
        self.VoronoiDiagram.toggleLines(True)

    def ToggleLinesOff(self):
        self.VoronoiDiagram.toggleLines(False)

    def ToggleSitesOn(self):
        self.VoronoiDiagram.toggleSites(True)

    def ToggleSitesOff(self):
        self.VoronoiDiagram.toggleSites(False)


# this starts up the process to open and run the main window object
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()