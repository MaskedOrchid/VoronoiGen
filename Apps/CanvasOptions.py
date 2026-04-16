"""
CanvasOptions Module (VM-49, VM-50)
A UI panel widget that provides controls for customizing the Voronoi canvas display.
Handles line toggling (VM-51), line color changing (VM-52),
line thickness changing (VM-53), and site toggling (VM-54).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QColorDialog,
    QFrame, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class CanvasOptions(QWidget):
    """
    A sidebar panel widget for controlling Voronoi canvas display options.

    Provides UI controls for toggling lines/sites, changing line color,
    and adjusting line thickness. Communicates directly with VoronoiController.
    """

    def __init__(self, vc):
        """
        Initialize the CanvasOptions panel.

        Args:
            vc: VoronoiController instance to send display commands to
        """
        super().__init__()
        self.voroController = vc

        # Track current toggle states
        self.lines_on = self.voroController.getLineToggle()
        self.sites_on = self.voroController.getSiteToggle()

        self._build_ui()

    def _build_ui(self):
        """Construct and lay out all UI elements."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ----- Section title -----
        title = QLabel("Canvas Options")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 13px; color: white;")
        main_layout.addWidget(title)

        main_layout.addWidget(self._make_divider())

        # ----- VM-51: Line Toggle -----
        line_toggle_label = QLabel("Cell Border Lines")
        line_toggle_label.setStyleSheet("color: #ccc; font-size: 11px;")
        main_layout.addWidget(line_toggle_label)

        self.line_toggle_btn = QPushButton()
        self._update_line_toggle_btn_text()
        self.line_toggle_btn.setFixedHeight(36)
        self.line_toggle_btn.clicked.connect(self._toggle_lines)
        self.line_toggle_btn.setStyleSheet(self._toggle_btn_style())
        main_layout.addWidget(self.line_toggle_btn)

        main_layout.addWidget(self._make_divider())

        # ----- VM-52: Line Color -----
        line_color_label = QLabel("Line Color")
        line_color_label.setStyleSheet("color: #ccc; font-size: 11px;")
        main_layout.addWidget(line_color_label)

        color_row = QHBoxLayout()

        # Color preview swatch
        self.color_preview = QFrame()
        self.color_preview.setFixedSize(28, 28)
        self._update_color_preview(self.voroController.getLineColor())
        color_row.addWidget(self.color_preview)

        self.color_btn = QPushButton("Pick Color")
        self.color_btn.setFixedHeight(28)
        self.color_btn.clicked.connect(self._pick_line_color)
        self.color_btn.setStyleSheet(self._action_btn_style())
        color_row.addWidget(self.color_btn)

        main_layout.addLayout(color_row)

        main_layout.addWidget(self._make_divider())

        # ----- VM-53: Line Thickness -----
        thickness_label = QLabel("Line Thickness")
        thickness_label.setStyleSheet("color: #ccc; font-size: 11px;")
        main_layout.addWidget(thickness_label)

        thickness_row = QHBoxLayout()

        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(20)
        self.thickness_slider.setValue(int(self.voroController.getLineThickness()))
        self.thickness_slider.setTickInterval(1)
        self.thickness_slider.valueChanged.connect(self._on_thickness_slider_changed)
        thickness_row.addWidget(self.thickness_slider)

        self.thickness_spinbox = QDoubleSpinBox()
        self.thickness_spinbox.setMinimum(0.5)
        self.thickness_spinbox.setMaximum(20.0)
        self.thickness_spinbox.setSingleStep(0.5)
        self.thickness_spinbox.setDecimals(1)
        self.thickness_spinbox.setFixedWidth(60)
        self.thickness_spinbox.setValue(self.voroController.getLineThickness())
        self.thickness_spinbox.valueChanged.connect(self._on_thickness_spinbox_changed)
        thickness_row.addWidget(self.thickness_spinbox)

        main_layout.addLayout(thickness_row)

        main_layout.addWidget(self._make_divider())

        # ----- VM-54: Site Toggle -----
        site_toggle_label = QLabel("Site Points")
        site_toggle_label.setStyleSheet("color: #ccc; font-size: 11px;")
        main_layout.addWidget(site_toggle_label)

        self.site_toggle_btn = QPushButton()
        self._update_site_toggle_btn_text()
        self.site_toggle_btn.setFixedHeight(36)
        self.site_toggle_btn.clicked.connect(self._toggle_sites)
        self.site_toggle_btn.setStyleSheet(self._toggle_btn_style())
        main_layout.addWidget(self.site_toggle_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

    # ------------------------------------------------------------------ #
    #  VM-51: Line toggling
    # ------------------------------------------------------------------ #

    def _toggle_lines(self):
        """Toggle cell border line visibility on/off."""
        self.lines_on = not self.voroController.getLineToggle()
        self.voroController.toggleLines(self.lines_on)
        self._update_line_toggle_btn_text()

    def _update_line_toggle_btn_text(self):
        """Refresh the line toggle button label to reflect current state."""
        if self.voroController.getLineToggle():
            self.line_toggle_btn.setText("Lines: ON")
        else:
            self.line_toggle_btn.setText("Lines: OFF")
    # ------------------------------------------------------------------ #
    #  VM-52: Line color changing
    # ------------------------------------------------------------------ #

    def _pick_line_color(self):
        """Open a color dialog and apply the chosen color to cell borders."""
        current = self.voroController.getLineColor()
        color = QColorDialog.getColor(current, self, "Choose Line Color")
        if color.isValid():
            self.voroController.setLineColor(color)
            self._update_color_preview(color)

    def _update_color_preview(self, color: QColor):
        """Update the small color swatch to show the current line color.

        Args:
            color: QColor to display in the swatch
        """
        self.color_preview.setStyleSheet(
            f"background-color: {color.name()};"
            "border: 1px solid #888;"
            "border-radius: 3px;"
        )

    # ------------------------------------------------------------------ #
    #  VM-53: Line thickness changing
    # ------------------------------------------------------------------ #

    def _on_thickness_slider_changed(self, value: int):
        """Handle slider movement — sync spinbox and update controller.

        Args:
            value: New integer slider value
        """
        # Block spinbox signals to avoid a feedback loop
        self.thickness_spinbox.blockSignals(True)
        self.thickness_spinbox.setValue(float(value))
        self.thickness_spinbox.blockSignals(False)
        self.voroController.setLineThickness(float(value))
        self.voroController.updateCanvas()

    def _on_thickness_spinbox_changed(self, value: float):
        """Handle spinbox change — sync slider and update controller.

        Args:
            value: New float spinbox value
        """
        self.thickness_slider.blockSignals(True)
        self.thickness_slider.setValue(int(value))
        self.thickness_slider.blockSignals(False)
        self.voroController.setLineThickness(value)
        self.voroController.updateCanvas()

    # ------------------------------------------------------------------ #
    #  VM-54: Site toggling
    # ------------------------------------------------------------------ #

    def _toggle_sites(self):
        """Toggle site point visibility on/off."""
        self.sites_on = not self.voroController.getSiteToggle()
        self.voroController.toggleSites(self.sites_on)
        self._update_site_toggle_btn_text()

    def _update_site_toggle_btn_text(self):
        """Refresh the site toggle button label to reflect current state."""
        if self.voroController.getSiteToggle():
            self.site_toggle_btn.setText("Sites: ON")
        else:
            self.site_toggle_btn.setText("Sites: OFF")

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #

    def _make_divider(self):
        """Create a thin horizontal divider line.

        Returns:
            QFrame: A styled horizontal line widget
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #444;")
        return line

    def _toggle_btn_style(self):
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

    def _action_btn_style(self):
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
    def renderText(self):
        self._update_line_toggle_btn_text()
        self._update_site_toggle_btn_text()