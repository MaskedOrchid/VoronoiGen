from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from Label import Label
import json


class LabelModel(QObject):
    """
    Model class that stores and manages a list of Labels.
    Implements MVC pattern with signals for view updates.
    """

    # Signals to notify when model changes
    label_added = Signal(object)    # Emits the added Label
    label_removed = Signal(object)  # Emits the removed Label
    label_updated = Signal(object)  # Emits the updated Label
    labels_changed = Signal()       # Generic signal for any change

    def __init__(self):
        super().__init__()
        self._labels = []  # List of Label objects

        # Add initial labels for testing/demo
        self.add_label("Group 1")
        self.add_label("Group 2")
        self.add_label("Group 3")
        self.add_label("Group 5")

    # ==================== CRUD Operations ====================

    def add_label(self, name, color=None):
        """Add a new label to the model. Emits label_added signal."""
        if not name or not name.strip():
            raise ValueError("Label name cannot be empty")

        if self.find_label(name):
            raise ValueError(f"Label '{name}' already exists")

        if color is None:
            color = QColor(255, 255, 255)  # Default white

        new_label = Label(name, color)
        self._labels.append(new_label)

        self.label_added.emit(new_label)
        self.labels_changed.emit()

        return new_label

    def remove_label(self, name):
        """Remove a label by name. Emits label_removed signal."""
        label = self.find_label(name)
        if label:
            self._labels.remove(label)
            self.label_removed.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def remove_label_by_object(self, label):
        """Remove a label by object reference. Emits label_removed signal."""
        if label in self._labels:
            self._labels.remove(label)
            self.label_removed.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def update_label_name(self, old_name, new_name):
        """Update a label's name. Emits label_updated signal."""
        label = self.find_label(old_name)
        if not label:
            return False

        if not new_name or not new_name.strip():
            raise ValueError("Label name cannot be empty")

        # Check for duplicate name (excluding self)
        existing = self.find_label(new_name)
        if existing and existing != label:
            raise ValueError(f"Label '{new_name}' already exists")

        label.Name = new_name
        self.label_updated.emit(label)
        self.labels_changed.emit()
        return True

    def update_label_color(self, name, color):
        """Update a label's fill color. Emits label_updated signal."""
        label = self.find_label(name)
        if label:
            label.setFillColor(color)
            self.label_updated.emit(label)
            self.labels_changed.emit()
            return True
        return False

    def update_label_site_color(self, name, color):
        """Update a label's site/polygon color. Emits label_updated signal."""
        label = self.find_label(name)
        if label:
            label.setSiteColor(color)
            self.label_updated.emit(label)
            self.labels_changed.emit()
            return True
        return False

    # ==================== Query Operations ====================

    def find_label(self, name):
        """Find and return a label by name, or None if not found."""
        for label in self._labels:
            if label.Name == name:
                return label
        return None

    def get_all_labels(self):
        """Return a copy of all labels (prevents external modification)."""
        return self._labels.copy()

    def get_label_count(self):
        """Return the total number of labels."""
        return len(self._labels)

    def get_label_at_index(self, index):
        """Return label at specific index, or None if out of range."""
        if 0 <= index < len(self._labels):
            return self._labels[index]
        return None

    def get_label_names(self):
        """Return list of all label names."""
        return [label.Name for label in self._labels]

    # ==================== Site/Polygon Association ====================

    def add_site_to_label(self, label_name, site):
        """Associate a site with a label. Emits label_updated signal."""
        label = self.find_label(label_name)
        if label:
            label.addSite(site)
            self.label_updated.emit(label)
            return True
        return False

    def add_poly_to_label(self, label_name, poly):
        """Associate a polygon with a label. Emits label_updated signal."""
        label = self.find_label(label_name)
        if label:
            label.addPoly(poly)
            self.label_updated.emit(label)
            return True
        return False

    # ==================== Bulk Operations ====================

    def clear_all(self):
        """Remove all labels. Emits labels_changed signal."""
        self._labels.clear()
        self.labels_changed.emit()

    # ==================== Persistence ====================

    def save_to_file(self, filepath):
        """Save all labels to a JSON file. Returns (success, message)."""
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
        """Load labels from a JSON file. Returns (success, message)."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.clear_all()

            for item in data:
                fill_color = QColor(*item['fill_color'])
                label = Label(item['name'], fill_color)

                # Load optional site_color if present (backward compatibility)
                if 'site_color' in item:
                    site_color = QColor(*item['site_color'])
                    label.setSiteColor(site_color)

                self._labels.append(label)

            self.labels_changed.emit()
            return True, f"Loaded {len(data)} labels"
        except Exception as e:
            return False, f"Error loading: {str(e)}"