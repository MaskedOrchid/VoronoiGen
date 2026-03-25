# imports
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QLabel, QVBoxLayout,
                               QWidget)
import sys

# NEW: Import your label system
from LabelView import LabelView
from LabelModel import LabelModel


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

        self.button = QPushButton("Push for Window")
        # connecting a button click action to a class functions
        self.button.clicked.connect(self.show_new_window)

        # NEW: Add label manager button
        self.label_btn = QPushButton("Open Label Manager")
        self.label_btn.clicked.connect(self.show_label_manager)

        # NEW: Create layout to hold both buttons
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.addWidget(self.button)
        layout.addWidget(self.label_btn)
        self.setCentralWidget(central_widget)

        # creating a sub window class
        self.childWindow = SubWindow()

        # NEW: Create label manager window
        self.labelManagerWindow = None

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


# this starts up the process to open and run the main window object
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()