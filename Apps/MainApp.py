import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton
)

# MVC Components
from VoronoiHandler import VoronoiHandler, DrawModes
from VoronoiCanvas import VoronoiCanvas

# Label system
from LabelView import LabelView


# -------------------------------
# Label Manager Window
# -------------------------------
class LabelManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label Manager")
        self.setMinimumSize(300, 400)

        layout = QVBoxLayout()
        self.label_view = LabelView()
        layout.addWidget(self.label_view)

        self.setLayout(layout)

    def get_model(self):
        return self.label_view.get_model()


# -------------------------------
# Main Application Window
# -------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VoronoiGen")

        #  CONTROLLER
        self.handler = VoronoiHandler()

        #  VIEW (YOU)
        self.canvas = VoronoiCanvas(self.handler)

        #  CONNECT MVC
        self.handler.setCanvas(self.canvas)

        #  LABEL WINDOW
        self.label_window = LabelManagerWindow()

        # -------------------------------
        # TOOL PANEL (simple for now)
        # -------------------------------
        tool_layout = QVBoxLayout()

        # Mode buttons
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(lambda: self.handler.setMode(DrawModes.Add))

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.handler.setMode(DrawModes.Remove))

        # Label manager button
        label_btn = QPushButton("Labels")
        label_btn.clicked.connect(self.label_window.show)

        tool_layout.addWidget(add_btn)
        tool_layout.addWidget(remove_btn)
        tool_layout.addWidget(label_btn)

        tool_panel = QWidget()
        tool_panel.setLayout(tool_layout)

        # -------------------------------
        # MAIN LAYOUT
        # -------------------------------
        main_layout = QHBoxLayout()
        main_layout.addWidget(tool_panel)
        main_layout.addWidget(self.canvas)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())