from operator import truediv

from PySide6.QtWidgets import QDialog, QApplication

from Apps import (HomeView, CreationModel, CreationView, MainApp, Parser)

import sys


# Main controller class for the home application. Handles input logic and communicates with
# Creation and Home classes.
class HomeController():
    def __init__(self):

        self.view = HomeView.MainWindow(self)
        self.view.show()

        self.model = CreationModel.CreationModel()
        self.w = None
        self.parser = Parser.Parser()

    def open_dialog(self):
        dialog = CreationView.CreationDialog(self)
        dialog.exec()

    #   TO DO: Implement opening existing project files.
    #   def open_existing(self, checked):

    def exit_app(self):
        self.view.close()

    def setFile(self, value):
        if value != "":
            self.model.changeFile(value)
            return True
        return False

    # Takes in input from the CreationView and updates the CreationModel accordingly
    def alterModel(self, title = "", width = "", height = ""):

        #   TO DO: Implement checks for file saving
        self.model.changeName(title)
        try:
            intedWidth = int(width)
            intedHeight = int(height)
        except ValueError:
            print("Width and height must be numbers!")
            return False

        self.model.changeWidth(intedWidth)
        self.model.changeHeight(intedHeight)
        return True


    def initializeMainApp(self):

        if self.model.file != "":
            self.parser.parse(self.model.file)
            self.model.labels = self.parser.labels
            self.model.packages = self.parser.packages

        self.w = MainApp.MainWindow(self.model)
        self.w.show()
        self.view.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    hc = HomeController()
    sys.exit(app.exec())