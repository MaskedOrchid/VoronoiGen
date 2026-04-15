from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QColorDialog,
    QInputDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from Apps.LabelModel import LabelModel


class LabelItemWidget(QWidget):
    edit_requested = Signal(object)
    delete_requested = Signal(object)
    color_change_requested = Signal(object)
    selected = Signal(object)

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.label = label
        self.is_selected = False
        self.init_ui()
        self.update_display()


    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Color square
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(24, 24)
        self.color_preview.setStyleSheet("border-radius: 4px;")
        layout.addWidget(self.color_preview)

        # Name
        self.name_label = QLabel()
        self.name_label.setMinimumWidth(80)
        self.name_label.setStyleSheet("font-weight: 500;")
        layout.addWidget(self.name_label)

        # Sites
        self.site_count = QLabel()
        self.site_count.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.site_count)

        layout.addStretch()

        # Buttons (smaller + consistent)
        btn_style = """
            QPushButton {
                padding: 4px 8px;
                border-radius: 5px;
                background-color: #2a2f38;
                color: white;
            }
            QPushButton:hover {
                background-color: #3a3f48;
            }
        """

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet(btn_style)
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.label))
        layout.addWidget(self.edit_btn)

        self.color_btn = QPushButton("Color")
        self.color_btn.setStyleSheet(btn_style)
        self.color_btn.clicked.connect(lambda: self.color_change_requested.emit(self.label))
        layout.addWidget(self.color_btn)

        self.delete_btn = QPushButton("Del")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #c62828;
                color: white;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.label))
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.selected.emit(self.label)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.is_selected = selected
        self.apply_style()

    def apply_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2c3440;
                    border: 2px solid #4CAF50;
                    border-radius: 6px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #20232a;
                    border: 1px solid #333;
                    border-radius: 6px;
                }
            """)

    def update_display(self):
        color = self.label.getFillColor()
        self.color_preview.setStyleSheet(
            f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});"
            "border: 1px solid #999;"
        )
        self.name_label.setText(self.label.Name)
        self.site_count.setText(f"Sites: {len(self.label.Sites)}")


class LabelView(QWidget):
    labels_modified = Signal()

    def __init__(self, model=None, parent=None):
        super().__init__(parent)

        self.model = model if model else LabelModel()
        self.item_widgets = []

        self.model.label_added.connect(self.refresh)
        self.model.label_removed.connect(self.refresh)
        self.model.label_updated.connect(self.refresh)
        self.model.selection_changed.connect(self.update_selection_display)

        self.init_ui()
        self.refresh()



    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Add button (top)
        self.add_btn = QPushButton("+ Add Label")
        self.add_btn.setFixedHeight(36)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)
        self.add_btn.clicked.connect(self.on_add_clicked)

        main_layout.addWidget(self.add_btn)

        # Container
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setSpacing(10)

        self.container_widget.setLayout(self.container_layout)
        main_layout.addWidget(self.container_widget)

        # Footer count
        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("color: #aaa; font-size: 11px;")

        main_layout.addWidget(self.count_label)

        self.setLayout(main_layout)

    def refresh(self, *args):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.item_widgets = []

        for label in self.model.get_all_labels():
            item_widget = LabelItemWidget(label)
            item_widget.selected.connect(self.on_label_selected)
            item_widget.edit_requested.connect(self.on_edit_label)
            item_widget.delete_requested.connect(self.on_delete_label)
            item_widget.color_change_requested.connect(self.on_change_label_color)
            self.container_layout.addWidget(item_widget)
            self.item_widgets.append(item_widget)

        self.update_count()
        self.update_selection_display(self.model.get_selected_label())

    def update_count(self):
        self.count_label.setText(f"Total labels: {self.model.get_label_count()}")

    def update_selection_display(self, selected_label):
        for widget in self.item_widgets:
            widget.set_selected(widget.label == selected_label)

    def on_label_selected(self, label):
        self.model.set_selected_label(label)

    def on_add_clicked(self):
        name, ok = QInputDialog.getText(
            self,
            "Add Label",
            "Enter label name:",
            text=f"group{self.model.get_label_count() + 1}"
        )
        if ok and name:
            self.model.add_label(name)
            self.labels_modified.emit()

    def on_edit_label(self, label):
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Label",
            "Enter new label name:",
            text=label.Name
        )
        if ok and new_name:
            self.model.update_label_name(label.Name, new_name)
            self.labels_modified.emit()

    def on_change_label_color(self, label):
        color = QColorDialog.getColor(label.getFillColor(), self, f"Color for {label.Name}")
        if color.isValid():
            self.model.update_label_color(label.Name, color)
            self.labels_modified.emit()

    def on_delete_label(self, label):
        reply = QMessageBox.question(
            self,
            "Delete Label",
            f"Delete '{label.Name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_label_by_object(label)
            self.labels_modified.emit()

    def get_model(self):
        return self.model