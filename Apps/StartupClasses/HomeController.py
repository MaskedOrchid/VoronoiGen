from PySide6.QtWidgets import QDialog, QApplication, QMessageBox, QWidget

from Apps.StartupClasses import (HomeView, CreationModel, CreationView)
from Apps.MainApplicationClasses import MainApp
from Apps.HelperClasses import Parser

import sys

class HomeController:
    """

    Main controller class for the home application. Handles input logic and communicates with
    Creation and Home classes.

    """
    def __init__(self):

        self.view = HomeView.MainWindow(self)
        self.view.show()

        self.model = CreationModel.CreationModel()
        self.w = None
        self.parser = Parser.Parser()

    def open_dialog(self):
        dialog = CreationView.CreationDialog(self)
        dialog.exec()

    def exit_app(self):
        self.view.close()

    def setFile(self, value):
        """
            Allows files to be set in the model from UI/other classes.
            Args:
                value: new filepath
        """
        if value != "":
            self.model.changeFile(value)
            return True
        return False

    def alterModel(self, title = "", width = "", height = ""):
        """
            Takes in input from the creation view and updates the model accordingly.
            Args:
                title: new title for the project
                width: new width for the project's canvas
                height: new height for the project's canvas
        """
        self.model.changeName(title)
        try:
            intedWidth = int(width)
            intedHeight = int(height)
        except ValueError:
            QMessageBox.critical(QWidget(), "Error", "Invalid canvas dimensions given.")
            return False

        self.model.changeWidth(intedWidth)
        self.model.changeHeight(intedHeight)
        return True


    def initializeMainApp(self):

        if self.model.file != "":
            self.parser = Parser.create_parser(self.model.file)
            self.parser.parse(self.model.file)
            self.model.labels = self.parser.labels
            self.model.packages = self.parser.packages

        self.w = MainApp.MainWindow(self.model)
        self.w.show()
        self.view.close()

    def openNoiDialog(self):
        # called for open project.
        noi_dialog = CreationView.NoiDialog(self)

    def noiParser(self, filepath):

        """
            Parses the data from a *.noi file into the model.
        """

        if(filepath != ""):
            self.setFile(filepath)
            self.parser = Parser.NoiParser()
            self.parser.parse(filepath)
            self.alterModel(self.parser.title, str(self.parser.cx), str(self.parser.cy))
            self.model.labels = self.parser.labels
            self.model.packages = self.parser.packages
            self.model.setOptionsModel(self.parser.lineToggle, self.parser.lineThickness,
                                       self.parser.lineColor, self.parser.siteToggle)

            self.w = MainApp.MainWindow(self.model)
            self.w.show()
            self.view.close()
            return
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hc = HomeController()
    if len(sys.argv) > 1:
        hc.noiParser(sys.argv[1])
    sys.exit(app.exec())

