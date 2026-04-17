"""
LabelModel Module
Manages the Label's data and internal implementation
Handles label datas, passing labels and emitting signals
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from Apps.Label import LABEL


class LABELMODEL(QObject):
    """
        Represents the Label's internal implementation with its associated metadata.

        A container class that holds information about an abstract label in the label system
        including the name, fillcolor, site color, and the amount of sites connected to this label

        Attributes:
            self.labels: List of all the existing labels
            self.selected_label: currently
            self.defaultLabel: default label

        Signals:
                label_added: the signal emitted when a label is added
                label_removed: the signal emitted when a label is deleted
                label_updated: the signal emitted when a label is updated
                selection_changed: the signal emitted when the current selected label has changed
    """
    label_added = Signal(object)
    label_removed = Signal(object)
    label_updated = Signal(object)
    selection_changed = Signal(object)

    def __init__(self):
        super().__init__()
        """Initialize the label model, and the default label which has 
            white fill color and red sites
            
        """
        self.labels = []
        self.selected_label = None
        self.defaultLabel=LABEL("Default")
        self.defaultLabel.setSiteColor( QColor(255, 0, 0))

    def addLabel(self, name):
        """Add a new label to the project

        Args:
            name: the name of this new label

        """
        new_label = LABEL(name)
        self.labels.append(new_label)
        self.label_added.emit(new_label)

    def AddOldLabel(self, l):
        """Add an existing label to the project

           Args:
               l: the label to add to the data structure

        """
        self.labels.append(l)
        self.label_added.emit(l)

    def removeLabelByObject(self, label):
        """Remove a label from the data structure

           Args:
               label: the label to add to the data structure

            Returns:
                bool: if the label got removed or not

        """
        if label in self.labels:
            if self.selected_label == label:
                self.selected_label = None
                self.selection_changed.emit(None)
            self.labels.remove(label)
            self.label_removed.emit(label)
            return True
        return False

    def updateLabelName(self, old_name, new_name):
        """Updates a label's name

           Args:
               old_name: the old name of the label
               new_name: the new name of the label

            Returns:
                bool: if the label got renamed
        """
        for label in self.labels:
            if label.Name == old_name:
                label.Name = new_name
                self.label_updated.emit(label)
                return

    def updateLabelColor(self, name, color):
        """Updates a label's color

           Args:
               name: the name of the label
               color: the new color of the label

            Returns:
                bool: if the label's got changed
        """
        for label in self.labels:
            if label.Name == name:
                label.setFillColor(color)
                # self.voronoiController.onLabelChange(label)
                self.label_updated.emit(label)
                return

    def getAllLabels(self):
        """Returns a list of all the labels

            Returns:
                self.labels: returns a list of all the labels
        """
        return self.labels

    def getLabelCount(self):
        """Returns the amount of labels

            Returns:
                int: amount of labels
        """
        return len(self.labels)

    def setSelectedLabel(self, label):
        """sets the currently selected label and emits the selection_change signals

            arg:
                label: the label we are selected
        """
        self.selected_label = label
        self.selection_changed.emit(label)

    def getSelectedLabel(self):
        """gives the current selected label

            return:
                self.selected_label: the currently selected label
        """
        return self.selected_label

    def addSiteToSelectedLabel(self,site):
        """adds a site to a selected label and emits the label_updated signals

            arg:
                site: the site to add
        """
        if self.selected_label is not None:
            self.selected_label.addSite(site)
            self.label_updated.emit(self.selected_label)

    def addSiteToLabel(self,site, label):
        """adds a site to a label and emits the label_updated signals

            arg:
                site: the site to add
                label: the label that the site is getting added too
        """
        if label is not None:
            label.addSite(site)
            self.label_updated.emit(label)

    def getLabelWithSite(self,site):
        """get the label with the specified site

            arg:
                site: the site that we want the label for

            return:
                l: the label that has this site
        """
        for l in self.labels:
            if site in l.getSites():
                return l

    def removeSiteFromAllLabels(self,site):
        """Remove a site from all labels and emits the label_updated signal

            arg:
                site: the site that we want to remove from all labels

        """
        for l in  self.labels:
            if site in l.getSites():
                l.getSites().remove(site)
                self.label_updated.emit(l)

    def getDefaultLabel(self):
        """return the default

            return:
                self.defaultLabel: the default label
        """
        return self.defaultLabel
