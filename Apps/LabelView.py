from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QColorDialog, QInputDialog,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from LabelModel import LabelModel


class LabelItemWidget(QWidget):
    edit_requested = Signal(object)
    delete_requested = Signal(object)
    color_change_requested = Signal(object)
    selected = Signal(object)  # 🔥 NEW

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.label = label
        self.init_ui()
        self.update_display()

    def init_ui(self):
        layout = QHBoxLayout()

        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 30)
        layout.addWidget(self.color_preview)

        self.name_label = QLabel()
        layout.addWidget(self.name_label)

        layout.addStretch()

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.label))
        layout.addWidget(self.edit_btn)

        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(lambda: self.color_change_requested.emit(self.label))
        layout.addWidget(self.color_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.label))
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        # 🔥 CLICK TO SELECT
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        self.selected.emit(self.label)

    def update_display(self):
        color = self.label.getFillColor()
        self.color_preview.setStyleSheet(
            f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});"
        )
        self.name_label.setText(self.label.Name)


class LabelView(QWidget):
    def __init__(self):
        super().__init__()

        self.model = LabelModel()

        self.model.label_added.connect(self.refresh)
        self.model.label_removed.connect(self.refresh)
        self.model.label_updated.connect(self.refresh)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.add_btn = QPushButton("+ Add Label")
        self.add_btn.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_btn)

        self.container = QVBoxLayout()
        layout.addLayout(self.container)

        self.setLayout(layout)

    def refresh(self):
        while self.container.count():
            widget = self.container.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        for label in self.model.get_all_labels():
            self.add_label_widget(label)

    def add_label_widget(self, label):
        item = LabelItemWidget(label)

        item.selected.connect(self.on_label_selected)  # 🔥 IMPORTANT
        item.edit_requested.connect(self.on_edit_label)
        item.delete_requested.connect(self.on_delete_label)
        item.color_change_requested.connect(self.on_color_change)

        self.container.addWidget(item)

    def on_label_selected(self, label):
        self.model.set_selected_label(label)

    def on_add_clicked(self):
        name, ok = QInputDialog.getText(self, "Add Label", "Label name:")
        if ok and name:
            self.model.add_label(name)

    def on_edit_label(self, label):
        name, ok = QInputDialog.getText(self, "Edit Label", "New name:", text=label.Name)
        if ok:
            self.model.update_label_name(label.Name, name)

    def on_color_change(self, label):
        color = QColorDialog.getColor(label.getFillColor())
        if color.isValid():
            self.model.update_label_color(label.Name, color)

    def on_delete_label(self, label):
        self.model.remove_label_by_object(label)

    def get_model(self):
        return self.model