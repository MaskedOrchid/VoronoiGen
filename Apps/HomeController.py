from PySide6.QtWidgets import QDialog, QApplication

from Apps import (HomeView, CreationModel, CreationView, MainApp)

import sys

class HomeController():
    def __init__(self):

        self.view = HomeView.MainWindow(self)
        self.view.show()

        self.model = CreationModel.CreationModel()
        self.w = None

    def open_dialog(self):
        dialog = CreationView.CreationDialog(self)
        dialog.exec()

 #   def open_existing(self, checked):

    def exit_app(self):
        self.view.close()

    def alterModel(self, title = "", width = "", height = ""):
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