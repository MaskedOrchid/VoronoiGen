
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QColorDialog,
    QFrame, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class CanvasOptions(QWidget):
    """
    A sidebar panel widget for controlling Voronoi canvas
    display options.

    Provides UI controls for toggling lines/sites, changing
    line color, and adjusting line thickness. Communicates
    directly with VoronoiController.
    """

    def __init__(self, vc):
        """
        Initialize the CanvasOptions panel.

        Args:
            vc: VoronoiController instance to send display
                commands to

        Returns:
            None
        """
        super().__init__()
        self.voroController = vc

        # Track current toggle states
        self.linesOn = self.voroController.getLineToggle()
        self.sitesOn = self.voroController.getSiteToggle()

        self.buildUi()

    def buildUi(self):
        """
        Construct and lay out all UI elements.

        Args:
            None

        Returns:
            None
        """
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(14)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # Section title
        title = QLabel("Canvas Options")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: white;"
        )
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.makeDivider())

        # VM-51: Line Toggle
        lineToggleLabel = QLabel("Cell Border Lines")
        lineToggleLabel.setStyleSheet("color: #ccc; font-size: 11px;")
        mainLayout.addWidget(lineToggleLabel)

        self.lineToggleBtn = QPushButton()
        self.updateLineToggleBtnText()
        self.lineToggleBtn.setFixedHeight(36)
        self.lineToggleBtn.clicked.connect(self.toggleLines)
        self.lineToggleBtn.setStyleSheet(self.toggleBtnStyle())
        mainLayout.addWidget(self.lineToggleBtn)
        mainLayout.addWidget(self.makeDivider())

        # VM-52: Line Color
        lineColorLabel = QLabel("Line Color")
        lineColorLabel.setStyleSheet("color: #ccc; font-size: 11px;")
        mainLayout.addWidget(lineColorLabel)

        colorRow = QHBoxLayout()

        # Color preview swatch
        self.colorPreview = QFrame()
        self.colorPreview.setFixedSize(28, 28)
        self.updateColorPreview(self.voroController.getLineColor())
        colorRow.addWidget(self.colorPreview)

        self.colorBtn = QPushButton("Pick Color")
        self.colorBtn.setFixedHeight(28)
        self.colorBtn.clicked.connect(self.pickLineColor)
        self.colorBtn.setStyleSheet(self.actionBtnStyle())
        colorRow.addWidget(self.colorBtn)
        mainLayout.addLayout(colorRow)
        mainLayout.addWidget(self.makeDivider())

        thicknessLabel = QLabel("Line Thickness")
        thicknessLabel.setStyleSheet("color: #ccc; font-size: 11px;")
        mainLayout.addWidget(thicknessLabel)

        thicknessRow = QHBoxLayout()

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(20)
        self.thicknessSlider.setValue(
            int(self.voroController.getLineThickness())
        )
        self.thicknessSlider.setTickInterval(1)
        self.thicknessSlider.valueChanged.connect(
            self.onThicknessSliderChanged
        )
        thicknessRow.addWidget(self.thicknessSlider)

        self.thicknessSpinbox = QDoubleSpinBox()
        self.thicknessSpinbox.setMinimum(0.5)
        self.thicknessSpinbox.setMaximum(20.0)
        self.thicknessSpinbox.setSingleStep(0.5)
        self.thicknessSpinbox.setDecimals(1)
        self.thicknessSpinbox.setFixedWidth(60)
        self.thicknessSpinbox.setValue(
            self.voroController.getLineThickness()
        )
        self.thicknessSpinbox.valueChanged.connect(
            self.onThicknessSpinboxChanged
        )
        thicknessRow.addWidget(self.thicknessSpinbox)
        mainLayout.addLayout(thicknessRow)
        mainLayout.addWidget(self.makeDivider())

        # VM-54: Site Toggle
        siteToggleLabel = QLabel("Site Points")
        siteToggleLabel.setStyleSheet("color: #ccc; font-size: 11px;")
        mainLayout.addWidget(siteToggleLabel)

        self.siteToggleBtn = QPushButton()
        self.updateSiteToggleBtnText()
        self.siteToggleBtn.setFixedHeight(36)
        self.siteToggleBtn.clicked.connect(self.toggleSites)
        self.siteToggleBtn.setStyleSheet(self.toggleBtnStyle())
        mainLayout.addWidget(self.siteToggleBtn)

        mainLayout.addStretch()
        self.setLayout(mainLayout)

    def toggleLines(self):
        """
        Toggle cell border line visibility on/off.

        Args:
            None

        Returns:
            None
        """
        self.linesOn = not self.voroController.getLineToggle()
        self.voroController.toggleLines(self.linesOn)
        self.updateLineToggleBtnText()

    def updateLineToggleBtnText(self):
        """
        Refresh the line toggle button label to reflect
        current state.

        Args:
            None

        Returns:
            None
        """
        if self.voroController.getLineToggle():
            self.lineToggleBtn.setText("Lines: ON")
        else:
            self.lineToggleBtn.setText("Lines: OFF")

    def pickLineColor(self):
        """
        Open a color dialog and apply the chosen color to
        cell borders.

        Args:
            None

        Returns:
            None
        """
        current = self.voroController.getLineColor()
        color = QColorDialog.getColor(
            current, self, "Choose Line Color"
        )
        if color.isValid():
            self.voroController.setLineColor(color)
            self.updateColorPreview(color)

    def updateColorPreview(self, color):
        """
        Update the small color swatch to show the current
        line color.

        Args:
            color: QColor to display in the swatch

        Returns:
            None
        """
        self.colorPreview.setStyleSheet(
            f"background-color: {color.name()};"
            "border: 1px solid #888;"
            "border-radius: 3px;"
        )


    def onThicknessSliderChanged(self, value):
        """
        Handle slider movement, sync spinbox and update
        controller.

        Args:
            value: New integer slider value

        Returns:
            None
        """
        self.thicknessSpinbox.blockSignals(True)
        self.thicknessSpinbox.setValue(float(value))
        self.thicknessSpinbox.blockSignals(False)
        self.voroController.setLineThickness(float(value))
        self.voroController.updateCanvas()

    def onThicknessSpinboxChanged(self, value):
        """
        Handle spinbox change, sync slider and update
        controller.

        Args:
            value: New float spinbox value

        Returns:
            None
        """
        self.thicknessSlider.blockSignals(True)
        self.thicknessSlider.setValue(int(value))
        self.thicknessSlider.blockSignals(False)
        self.voroController.setLineThickness(value)
        self.voroController.updateCanvas()

    def toggleSites(self):
        """
        Toggle site point visibility on/off.

        Args:
            None

        Returns:
            None
        """
        self.sitesOn = not self.voroController.getSiteToggle()
        self.voroController.toggleSites(self.sitesOn)
        self.updateSiteToggleBtnText()

    def updateSiteToggleBtnText(self):
        """
        Refresh the site toggle button label to reflect
        current state.

        Args:
            None

        Returns:
            None
        """
        if self.voroController.getSiteToggle():
            self.siteToggleBtn.setText("Sites: ON")
        else:
            self.siteToggleBtn.setText("Sites: OFF")

    def renderText(self):
        """
        Re-render the toggle button text to reflect the
        current controller state.

        Args:
            None

        Returns:
            None
        """
        self.updateLineToggleBtnText()
        self.updateSiteToggleBtnText()

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #

    def makeDivider(self):
        """
        Create a thin horizontal divider line.

        Args:
            None

        Returns:
            QFrame: A styled horizontal line widget
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #444;")
        return line

    def toggleBtnStyle(self):
        """
        Return the stylesheet for toggle buttons.

        Args:
            None

        Returns:
            str: QSS stylesheet string
        """
        return """
            QPushButton {
                background-color: #2a2f38;
                color: white;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3f48;
            }
            QPushButton:pressed {
                background-color: #1a1f28;
            }
        """

    def actionBtnStyle(self):
        """
        Return the stylesheet for action buttons.

        Args:
            None

        Returns:
            str: QSS stylesheet string
        """
        return """
            QPushButton {
                background-color: #1565c0;
                color: white;
                border-radius: 5px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """