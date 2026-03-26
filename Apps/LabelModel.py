from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from Label import Label
import json


class LabelModel(QObject):
    """
    Model class that stores and manages a list of Labels.
    """

    # Signals to notify when model changes
    label_added = Signal(object)  # Emits the added Label
    label_removed = Signal(object)  # Emits the removed Label
    label_updated = Signal(object)  # Emits the updated Label
    labels_changed = Signal()  # Generic signal for any change

    def __init__(self):
        super().__init__()
        self._labels = []  # List of Label objects

        # Add initial labels
        self.add_label("Group 1")
        self.add_label("Group 2")
        self.add_label("Group 3")
        self.add_label("Group 5")

    # ==================== CRUD Operations ====================

    def add_label(self, name, color=None):
        """Add a new label to the model."""
        if not name or not name.strip():
            raise ValueError("Label name cannot be empty")

        if self.find_label(name):
            raise ValueError(f"Label '{name}' already exists")

        if color is None:
            color = QColor(255, 255, 255)

        new_label = Label(name, color)
        self._labels.append(new_label)

        self.label_added.emit(new_label)
        self.labels_changed.emit()

        return new_label

    def remove_label(self, name):
        """Remove a label by name."""
        label = self.find_label(name)
        if label:
            self._labels.remove(label)
            self.label_removed.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def remove_label_by_object(self, label):
        """Remove a label by object reference."""
        if label in self._labels:
            self._labels.remove(label)
            self.label_removed.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def update_label_name(self, old_name, new_name):
        """Update a label's name."""
        label = self.find_label(old_name)
        if not label:
            return False

        if not new_name or not new_name.strip():
            raise ValueError("Label name cannot be empty")

        existing = self.find_label(new_name)
        if existing and existing != label:
            raise ValueError(f"Label '{new_name}' already exists")

        label.Name = new_name
        self.label_updated.emit(label)
        self.labels_changed.emit()
        return True

    def update_label_color(self, name, color):
        """Update a label's fill color."""
        label = self.find_label(name)
        if label:
            label.setFillColor(color)
            self.label_updated.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def update_label_site_color(self, name, color):
        """Update a label's site color."""
        label = self.find_label(name)
        if label:
            label.setSiteColor(color)
            self.label_updated.emit(label)
            self.labels_changed.emit()
            return True
        return False

    # ==================== Query Operations ====================

    def find_label(self, name):
        """Find a label by name."""
        for label in self._labels:
            if label.Name == name:
                return label
        return None

    def get_all_labels(self):
        """Get all labels."""
        return self._labels.copy()

    def get_label_count(self):
        """Get number of labels."""
        return len(self._labels)

    def get_label_at_index(self, index):
        """Get label at specific index."""
        if 0 <= index < len(self._labels):
            return self._labels[index]
        return None

    def get_label_names(self):
        """Get list of all label names."""
        return [label.Name for label in self._labels]

    # ==================== Site/Polygon Association ====================

    def add_site_to_label(self, label_name, site):
        """Add a site to a label."""
        label = self.find_label(label_name)
        if label:
            label.addSite(site)
            self.label_updated.emit(label)
            return True
        return False

    def add_poly_to_label(self, label_name, poly):
        """Add a polygon to a label."""
        label = self.find_label(label_name)
        if label:
            label.addPoly(poly)
            self.label_updated.emit(label)
            return True
        return False

    # ==================== Bulk Operations ====================

    def clear_all(self):
        """Remove all labels."""
        self._labels.clear()
        self.labels_changed.emit()

    # ==================== Persistence ====================

    def save_to_file(self, filepath):
        """Save labels to JSON file."""
        try:
            data = []
            for label in self._labels:
                data.append({
                    'name': label.Name,
                    'fill_color': [
                        label.FillColor.red(),
                        label.FillColor.green(),
                        label.FillColor.blue()
                    ],
                    'site_color': [
                        label.SiteColor.red(),
                        label.SiteColor.green(),
                        label.SiteColor.blue()
                    ]
                })

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            return True, f"Saved {len(data)} labels"
        except Exception as e:
            return False, f"Error saving: {str(e)}"

    def load_from_file(self, filepath):
        """Load labels from JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.clear_all()

            for item in data:
                fill_color = QColor(*item['fill_color'])
                label = Label(item['name'], fill_color)

                if 'site_color' in item:
                    site_color = QColor(*item['site_color'])
                    label.setSiteColor(site_color)

                self._labels.append(label)

            self.labels_changed.emit()
            return True, f"Loaded {len(data)} labels"
        except Exception as e:
            return False, f"Error loading: {str(e)}"