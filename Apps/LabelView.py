from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QPushButton, QLabel, QColorDialog, QInputDialog,
                               QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from LabelModel import LabelModel


class LabelItemWidget(QWidget):
    """Widget that displays a single label's name and color."""

    # Signals to communicate with parent view
    edit_requested = Signal(object)
    delete_requested = Signal(object)
    color_change_requested = Signal(object)

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.label = label
        self.init_ui()
        self.update_display()

    def init_ui(self):
        """Initialize UI components: color preview, name, count, and action buttons."""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # Color preview square
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 30)
        self.color_preview.setFrameStyle(QFrame.Box)
        layout.addWidget(self.color_preview)

        # Label name display
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 11))
        self.name_label.setMinimumWidth(150)
        layout.addWidget(self.name_label)

        # Site count display
        self.site_count = QLabel()
        self.site_count.setFont(QFont("Arial", 9))
        self.site_count.setStyleSheet("color: #666;")
        layout.addWidget(self.site_count)

        layout.addStretch()

        # Action buttons
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.label))
        self.edit_btn.setFixedWidth(60)
        layout.addWidget(self.edit_btn)

        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(lambda: self.color_change_requested.emit(self.label))
        self.color_btn.setFixedWidth(60)
        layout.addWidget(self.color_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.label))
        self.delete_btn.setStyleSheet("""
            QPushButton { background-color: #f44336; color: white; }
            QPushButton:hover { background-color: #da190b; }
        """)
        self.delete_btn.setFixedWidth(60)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.setStyleSheet("""
            LabelItemWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 2px;
            }
            LabelItemWidget:hover {
                background-color: #f5f5f5;
                border-color: #4CAF50;
            }
        """)

    def update_display(self):
        """Update UI to reflect current label state (color, name, site count)."""
        color = self.label.getFillColor()
        # Update color preview
        self.color_preview.setStyleSheet(f"""
            background-color: rgb({color.red()}, {color.green()}, {color.blue()});
            border: 1px solid #999;
            border-radius: 3px;
        """)
        self.name_label.setText(self.label.Name)
        self.site_count.setText(f"Sites: {len(self.label.Sites)}")

        # Adjust text color for contrast against label color
        brightness = (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000
        self.name_label.setStyleSheet("color: white;" if brightness < 128 else "color: black;")


class LabelView(QWidget):
    """Label manager widget with scroll view and add button."""

    labels_modified = Signal()  # Emitted when any label change occurs

    def __init__(self, model=None, parent=None):
        super().__init__(parent)

        self.model = model if model else LabelModel()

        # Connect model signals to view handlers
        self.model.label_added.connect(self.on_label_added)
        self.model.label_removed.connect(self.on_label_removed)
        self.model.label_updated.connect(self.on_label_updated)

        self.init_ui()
        self.refresh_label_list()

    def init_ui(self):
        """Set up main UI layout with header, scroll area, and count display."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header with title and add button
        header_layout = QHBoxLayout()
        title = QLabel("Label Manager")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.add_btn = QPushButton("+ Add Label")
        self.add_btn.clicked.connect(self.on_add_clicked)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        header_layout.addWidget(self.add_btn)
        main_layout.addLayout(header_layout)

        # Scroll area for label items
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setSpacing(5)
        self.container.setLayout(self.container_layout)
        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

        # Footer with label count
        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("color: #666; padding: 5px;")
        main_layout.addWidget(self.count_label)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f8f9fa;")

    def refresh_label_list(self):
        """Clear and rebuild the entire label list from model."""
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for label in self.model.get_all_labels():
            self.add_label_widget(label)

        self.update_count()

    def add_label_widget(self, label):
        """Create and add a LabelItemWidget for the given label."""
        item_widget = LabelItemWidget(label)
        item_widget.edit_requested.connect(self.on_edit_label)
        item_widget.delete_requested.connect(self.on_delete_label)
        item_widget.color_change_requested.connect(self.on_change_label_color)
        self.container_layout.addWidget(item_widget)

    def update_count(self):
        """Update the total label count display."""
        self.count_label.setText(f"Total labels: {self.model.get_label_count()}")

    def on_add_clicked(self):
        """Handle add button click: prompt for label name and create."""
        name, ok = QInputDialog.getText(
            self, "Add Label", "Enter label name:",
            text=f"Group {self.model.get_label_count() + 1}"
        )
        if ok and name:
            try:
                self.model.add_label(name)
                self.labels_modified.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def on_edit_label(self, label):
        """Handle edit request: prompt for new name and update."""
        new_name, ok = QInputDialog.getText(
            self, "Edit Label", "Enter new label name:",
            text=label.Name
        )
        if ok and new_name and new_name != label.Name:
            try:
                self.model.update_label_name(label.Name, new_name)
                self.labels_modified.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def on_change_label_color(self, label):
        """Handle color change request: open color picker and update."""
        color = QColorDialog.getColor(
            label.getFillColor(), self, f"Select color for {label.Name}"
        )
        if color.isValid():
            self.model.update_label_color(label.Name, color)
            self.labels_modified.emit()

    def on_delete_label(self, label):
        """Handle delete request: confirm if sites exist, then remove."""
        if label.Sites:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Label '{label.Name}' has {len(label.Sites)} site(s).\n"
                "Deleting it will remove all associated sites.\n\n"
                "Are you sure you want to delete this label?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        if self.model.remove_label_by_object(label):
            self.labels_modified.emit()

    # Model signal handlers
    def on_label_added(self, label):
        """Add label widget when model emits label_added."""
        self.add_label_widget(label)
        self.update_count()

    def on_label_removed(self, label):
        """Refresh list when model emits label_removed."""
        self.refresh_label_list()
        self.update_count()

    def on_label_updated(self, label):
        """Update specific widget when model emits label_updated."""
        for i in range(self.container_layout.count()):
            widget = self.container_layout.itemAt(i).widget()
            if isinstance(widget, LabelItemWidget) and widget.label == label:
                widget.update_display()
                break
        self.update_count()

    def get_model(self):
        """Return the underlying model."""
        return self.model