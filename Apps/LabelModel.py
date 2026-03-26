from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from Label import Label


class LabelModel(QObject):
    # Signals for UI updates
    label_added = Signal(object)
    label_removed = Signal(object)
    label_updated = Signal(object)

    def __init__(self):
        super().__init__()

        self.labels = []
        self.selected_label = None  # 🔥 IMPORTANT

    # -------------------------
    # LABEL MANAGEMENT
    # -------------------------
    def add_label(self, name):
        new_label = Label(name, QColor(200, 200, 255))
        self.labels.append(new_label)
        self.label_added.emit(new_label)

    def remove_label_by_object(self, label):
        if label in self.labels:
            self.labels.remove(label)
            self.label_removed.emit(label)
            return True
        return False

    def update_label_name(self, old_name, new_name):
        for label in self.labels:
            if label.Name == old_name:
                label.Name = new_name
                self.label_updated.emit(label)
                return

    def update_label_color(self, name, color):
        for label in self.labels:
            if label.Name == name:
                label.setFillColor(color)
                self.label_updated.emit(label)
                return

    # -------------------------
    # GETTERS
    # -------------------------
    def get_all_labels(self):
        return self.labels

    def get_label_count(self):
        return len(self.labels)

    # -------------------------
    # 🔥 SELECTION (CRITICAL)
    # -------------------------
    def set_selected_label(self, label):
        self.selected_label = label

    def get_selected_label(self):
        return self.selected_label