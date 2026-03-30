from PySide6.QtWidgets import QDialog, QApplication

from Apps import (HomeView, CreationModel, CreationView, MainApp)

import sys


# Main controller class for the home application. Handles input logic and communicates with
# Creation and Home classes.
class HomeController():
    def __init__(self):

        self.view = HomeView.MainWindow(self)
        self.view.show()

        self.model = CreationModel.CreationModel()
        self.w = None

    def open_dialog(self):
        dialog = CreationView.CreationDialog(self)
        dialog.exec()

    #   TO DO: Implement opening existing project files.
    #   def open_existing(self, checked):

    def exit_app(self):
        self.view.close()

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
        self.w = MainApp.MainWindow(self.model)
        self.w.show()
        self.view.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    hc = HomeController()
    sys.exit(app.exec())