"""
Labelview Module
Manages the Label's and label widget UI and visuals
Handles label datas, passing labels and emitting signals
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QColorDialog,
    QInputDialog, QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from Apps.MainApplicationClasses.LabelModel import LabelModel


class LabelItemWidget(QWidget):
    """
    Represents a single label Item and it's UI

    A widget class that manages updating and showing the labels visually.

    Attributes:
        label: the label to visualize
        is_selected: whether this label item widget is selected

    Signals:
        edit_requested: the signal emitted when the item widget is trying to be edited
        delete_requested: the signal emitted when the item widget is trying to be deleted
        color_change_requested: the signal emitted when the item widget
            is trying to change it's color
        selected: the signal emitted when the item widget is selected
    """
    edit_requested = Signal(object)
    delete_requested = Signal(object)
    color_change_requested = Signal(object)
    selected = Signal(object)

    def __init__(self, label, parent=None):
        super().__init__(parent)
        """Initialize a label item widget

        Args:
             label: label to represent
             parent: the parent object of this label item widget
        """
        self.label = label
        self.is_selected = False
        self.initUi()
        self.updateDisplay()


    def initUi(self):
        """Initialize the label item widget's UI layout
        """
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
        self.name_label.setMinimumWidth(30)
        self.name_label.setMaximumWidth(60)
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
        """handles when the label item widget receives a mouse event and selects this label
        emitting the selected label signal

        Args:
             event: the mouse press event
        """
        self.selected.emit(self.label)
        super().mousePressEvent(event)

    def setSelected(self, selected):
        """Sets the is_selected bool

        Args:
             selected: a bool to set is_selected too
        """
        self.is_selected = selected
        self.applyStyle()

    def applyStyle(self):
        """Sets the label item widget to appear highlighted

        """
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

    def updateDisplay(self):
        """Updates the UI with current label information

        """
        color = self.label.getFillColor()
        self.color_preview.setStyleSheet(
            f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});"
            "border: 1px solid #999;"
        )
        self.name_label.setText(self.label.Name)
        self.site_count.setText(f"Sites: {len(self.label.Sites)}")


class LabelView(QWidget):
    """
        Represent Label view, handling the label systems visual view.

        A widget class that manages updating and showing the label system visuals

        Attributes:
            model:label's model
            item_widgets: the list of all the label item widgets

        Signals:
             labels_modified: the signals emitted when the labels are modified
        """
    labels_modified = Signal()

    def __init__(self, model=None, parent=None):
        super().__init__(parent)
        """Initalizes the label view object

        arg:
            model: the label model/controller object
            parent: the parent object for the label viewer object

        """

        self.model = model if model else LabelModel()
        self.item_widgets = []

        self.model.label_added.connect(self.refresh)
        self.model.label_removed.connect(self.refresh)
        self.model.label_updated.connect(self.refresh)
        self.model.selection_changed.connect(self.updateSelectionDisplay)

        self.initUi()
        self.refresh()

    def initUi(self):
        """Initializes the UI of the Label View

        """
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
        self.add_btn.clicked.connect(self.onAddClicked)

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
        """Refreshes the Label systems UI with current information

        Args:
            *args: passed information from the signals

        """
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.item_widgets = []

        for label in self.model.getAllLabels():
            item_widget = LabelItemWidget(label)
            item_widget.selected.connect(self.onLabelSelected)
            item_widget.edit_requested.connect(self.onEditLabel)
            item_widget.delete_requested.connect(self.onDeleteLabel)
            item_widget.color_change_requested.connect(self.onChangeLabelColor)
            self.container_layout.addWidget(item_widget)
            self.item_widgets.append(item_widget)

        self.updateCount()
        self.updateSelectionDisplay(self.model.getSelectedLabel())

    def updateCount(self):
        """Updates the UI's representation of the amount of labels

        """
        self.count_label.setText(f"Total labels: {self.model.getLabelCount()}")

    def updateSelectionDisplay(self, selected_label):
        """Updates the label item widget to be selected if selected

        args:
            selected_label: the label to be selected

        """
        for widget in self.item_widgets:
            widget.setSelected(widget.label == selected_label)

    def onLabelSelected(self, label):
        """Receives the selected signal and sets the label as the selected label

        args:
            label: the label that is going to be selected

        """
        self.model.setSelectedLabel(label)

    def onAddClicked(self):
        """Adds a new label to the list and emits the labels_modified signal
        """
        name, ok = QInputDialog.getText(
            self,
            "Add Label",
            "Enter label name:",
            text=f"group{self.model.getLabelCount() + 1}"
        )
        if ok and name:
            self.model.addLabel(name)
            self.labels_modified.emit()

    def onEditLabel(self, label):
        """Receives the edited signal from the edit button
            and opens the edit dialogue to take in changes.
            Emits the label_modified signal

        args:
            label: the label that is being edited

        """
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Label",
            "Enter new label name:",
            text=label.Name
        )
        if ok and new_name:
            self.model.updateLabelName(label.Name, new_name)
            self.labels_modified.emit()

    def onChangeLabelColor(self, label):
        """Receives the edited signal from the edit color button
            and opens the color dialogue to take in changes.
            Emits the label_modified signal

        args:
            label: the label that is being edited

        """
        color = QColorDialog.getColor(label.getFillColor(), self, f"Color for {label.Name}")
        if color.isValid():
            self.model.updateLabelColor(label.Name, color)
            self.labels_modified.emit()

    def onDeleteLabel(self, label):
        """Receives the delete signal from the trash button
            and opens the delete message to confirm
            Emits the label_modified signal

        args:
            label: the label that is being deleted

        """
        reply = QMessageBox.question(
            self,
            "Delete Label",
            f"Delete '{label.Name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.removeLabelByObject(label)
            self.labels_modified.emit()

    def getModel(self):
        """returns the label's mode/controller

        returns:
            model: the label model objects
        """
        return self.model
