import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QScrollArea
)
from PySide6.QtCore import Qt

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

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(500,500)
    window.show()
    sys.exit(app.exec())