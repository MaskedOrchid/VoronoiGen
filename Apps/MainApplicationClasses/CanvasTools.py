from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup

from Apps.MainApplicationClasses.VoronoiController import DrawModes

class CanvasTools(QWidget):
    """
    The UI implementation for adding, removing, and selecting cells.
    """
    def __init__(self, vc):
        super().__init__()
        self.voroController = vc

        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(15)
        tool_layout.setContentsMargins(10, 10, 10, 10)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_modes = {}

        self.add_btn = self._createModeButton("Add Site", DrawModes.Add)
        self.remove_btn = self._createModeButton("Remove Site", DrawModes.Remove)
        self.select_btn = self._createModeButton("Select Cell", DrawModes.Select)

        tool_layout.addWidget(self.add_btn)
        tool_layout.addWidget(self.remove_btn)
        tool_layout.addWidget(self.select_btn)

        self.setLayout(tool_layout)
        self._applyStyles()
        self.setActiveMode(self.voroController.getMode())

    def _createModeButton(self, text, mode):
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, m=mode: self.setActiveMode(m))
        self.button_group.addButton(btn)
        self.button_modes[btn] = mode
        return btn

    def setActiveMode(self, mode):
        self.voroController.setMode(mode)
        for button, button_mode in self.button_modes.items():
            button.setChecked(button_mode == mode)

    def _applyStyles(self):
        self.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #a0a0a0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                border-color: #1976d2;
            }
            QPushButton:checked {
                border: 2px solid #1976d2;
            }
            """
        )
