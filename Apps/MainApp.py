"""
MainApp Module
Main application window for the Voronoi Diagram Generator.
Manages the UI layout, menu bar, and coordinates between the controller and views.
"""



from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QScrollArea, QFileDialog
)
from PySide6.QtCore import Qt, QCoreApplication

from Apps.VoronoiController import VORONOICONTROLLER
from Apps.CanvasTools import CanvasTools
from Apps.LabelView import LABELVIEW
from Apps.CreationModel import CreationModel
from Apps.CanvasOptions import CANVASOPTIONS



class MainWindow(QMainWindow):
    """Main application window for the Voronoi Diagram Generator.
    
    Manages the UI layout with a Voronoi canvas, toolbar, and label manager.
    Acts as the central hub coordinating between the controller, views, and menus.
    """
    def __init__(self, creationModel = None, width = 0, height = 0, name = ""):
        """Initialize the main application window.
        
        Args:
            creationModel: Optional creation model with project data
            width: Canvas width in pixels
            height: Canvas height in pixels
            name: Window title
        """
        super().__init__()

        self.model = creationModel
        if creationModel:
            self.setWindowTitle(creationModel.getTitle())
            self.width, self.height = self.clampCanvasSize(creationModel.width(),creationModel.height(), 800)
        else:
            self.setWindowTitle(name)
            self.width = width
            self.height = height

        self.setMinimumSize(1200, 700)
        self.showMaximized()
        self.menu = self.menuBar()

        #Voronoi Controller
        self.voroController=VORONOICONTROLLER(self.width, self.height)
        #Label Controller
        self.label_view =LABELVIEW()
        self.label_model = self.label_view.getModel()
        #Toolbar
        self.toolBar=CanvasTools(self.voroController)
        #Canvas Options
        self.CANVASOPTIONS = CANVASOPTIONS(self.voroController)
        #Parser

        #setting up UI and classes

        self.setUpMenuBar()
        self.setUpLabels()
        self.setUpVoronoi(self.width, self.height)
        self.setUpParser()
        self.setUpLayouts()

    def setUpMenuBar(self):
        """Create and configure the menu bar with File menu options."""
        # Create File menu actions
       # new_action = QAction("New Project", self)
       # new_action.setStatusTip("This creates a new Project")
       # new_action.triggered.connect(self.newProject)

       # open_action = QAction("Open Project", self)
       # open_action.setStatusTip("This Opens a Project")
       # open_action.triggered.connect(self.openProject)

        save_action = QAction("Save Project", self)
        save_action.setStatusTip("This saves the current Project")
        save_action.triggered.connect(self.saveProject)

        export_action = QAction("Export Diagram", self)
        export_action.setStatusTip("This exports the Voronoi Diagram as an image")
        export_action.triggered.connect(self.exportDiagram)

        quit_action = QAction("Quit", self)
        quit_action.setStatusTip("Closes Program")
        quit_action.triggered.connect(QCoreApplication.quit)

        # Add actions to File menu
        file_menu = self.menu.addMenu("&File")
       # file_menu.addAction(new_action)
       # file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(export_action)
        file_menu.addAction(quit_action)


    def setUpVoronoi(self, cx, cy):
        """Configure the Voronoi controller and connect it to the label model."""
        self.voroController.setUpFromModel(self.model.packages, self.model.getOptions())
        self.CANVASOPTIONS.renderText()


    def setUpLabels(self):
        """Sets the label system"""
        for label in self.model.getLabels():
            if label.getName() == "Default":
                continue
            self.label_model.AddOldLabel(label)
        self.voroController.setLabelModel(self.label_model)

    def setUpParser(self):
        """Initialize parser (placeholder)."""
        pass

    def setUpLayouts(self):
        """Construct the main UI layout with toolbar, canvas, and label panel."""
        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(15)
        tool_layout.setContentsMargins(10, 10, 10, 10)
        tool_layout.addWidget(self.toolBar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.label_view)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMinimumHeight(400)




        tool_layout.addWidget(scroll)
        tool_layout.addStretch()

        tool_panel = QWidget()
        tool_panel.setLayout(tool_layout)
        tool_panel.setMinimumWidth(350)
        tool_panel.setMaximumWidth(450)

        self.CANVASOPTIONS.setMinimumWidth(250)
        self.CANVASOPTIONS.setMaximumWidth(350)

        left_wrapper = QVBoxLayout()
        left_wrapper.addStretch(1)
        left_wrapper.addWidget(tool_panel)
        left_wrapper.addStretch(1)

        left_container = QWidget()
        left_container.setLayout(left_wrapper)

        right_wrapper = QVBoxLayout()
        right_wrapper.addStretch(1)
        right_wrapper.addWidget(self.CANVASOPTIONS)
        right_wrapper.addStretch(1)

        right_container = QWidget()
        right_container.setLayout(right_wrapper)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        content_layout.addWidget(left_container)
        content_layout.addWidget(self.voroController.getCanvas, 1)  # canvas expands
        content_layout.addWidget(right_container)

        main_layout.addStretch(1)
        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def newProject(self):
        """Create a new project (placeholder)."""
        print("Create new Project")

    def openProject(self):
        """Open an existing project (placeholder)."""
        print("Open Project")

    def saveProject(self):
        """Saves the project as a .noi file"""
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setNameFilters(["VoronoiGen File (*.noi)"])
        dialog.setDefaultSuffix("noi")

        if dialog.exec():
            filepath = dialog.selectedFiles()[0]
            if filepath:
                self.voroController.exportToNoi(filepath, self.windowTitle())

    def exportDiagram(self):
        """Export the Voronoi diagram as an image."""
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setNameFilters([
            "PNG Image (*.png)",
            "JPEG Image (*.jpg *.jpeg)",
            "Bitmap Image (*.bmp)"
        ])
        dialog.setDefaultSuffix("png")

        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            if file_path:
                saved = self.voroController.getCanvas.Image.save(file_path)
                if saved:
                    print(f"Diagram exported to: {file_path}")
                else:
                    print(f"Failed to export diagram to: {file_path}")

    def clampCanvasSize(self, x, y, mx):
        """Clamps the canvas to a currently a quick fix about

        args:
            x: the canvas width
            y: the canvas height
            mx: the width to height ratio

         returns:
            tuple: the scaled width and height of the canvas
        """
        scalar_x = mx / x if x > mx else 1.0
        scalar_y = mx / y if y > mx else 1.0
        scalar = min(scalar_x, scalar_y)
        return x * scalar, y * scalar

