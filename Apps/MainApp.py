import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QScrollArea
)
from PySide6.QtCore import Qt

# MVC components
from VoronoiHandler import VoronoiHandler, DrawModes
from VoronoiCanvas import VoronoiCanvas
from LabelView import LabelView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VoronoiGen")
        self.setMinimumSize(1200, 700)

        # -------------------------
        # CONTROLLER
        # -------------------------
        self.handler = VoronoiHandler()

        # -------------------------
        # CANVAS
        # -------------------------
        self.canvas = VoronoiCanvas(self.handler)
        self.handler.setCanvas(self.canvas)

        # -------------------------
        # LABEL SYSTEM
        # -------------------------
        self.label_view = LabelView()
        self.handler.label_model = self.label_view.get_model()

        # -------------------------
        # LEFT PANEL (TOOLS + LABELS)
        # -------------------------
        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(15)
        tool_layout.setContentsMargins(10, 10, 10, 10)

        # ---- Buttons ----
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

        # ---- Label Header ----
        header_layout = QHBoxLayout()

        label_title = QLabel("Label Manager")

        add_label_btn = QPushButton("+ Add Label")
        add_label_btn.setStyleSheet("background-color: green; color: white;")
        add_label_btn.clicked.connect(self.label_view.on_add_clicked)

        header_layout.addWidget(label_title)
        header_layout.addWidget(add_label_btn)

        tool_layout.addLayout(header_layout)

        # ---- Label View ----
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

        # -------------------------
        # MAIN LAYOUT (CENTERED FIX)
        # -------------------------
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # LEFT SPACE
        main_layout.addStretch(1)

        # CENTER CONTENT (panel + canvas)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        content_layout.addWidget(tool_panel)
        content_layout.addWidget(self.canvas)

        main_layout.addLayout(content_layout)

        # RIGHT SPACE
        main_layout.addStretch(1)

        # -------------------------
        # SET CENTRAL
        # -------------------------
        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())