#The Main File for the app
import sys


from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import (
    QPainter,
    QColor)
from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QFileDialog,
    QStyle,
    QColorDialog
)
from PainterWidget import PainterWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas=PainterWidget()
        #setting up the menu bars and system actions
        self.bar=self.addToolBar("Menu")
        self.Color1 = QColor()
        self.Color2 = QColor()
        self.lineColor = QColor.black
        #setting the painter as the central widget
        self.setCentralWidget(self.canvas)

    # @Slot()
    # def Save(self):
    #     #adding the save functionalities
    #     filedialog=QFileDialog(self,"Save Voronoi")
    #     # filedialog.setFileMode(QFileDialog.AnyFile)
    #     # filedialog.setAcceptMode(QFileDialog.AcceptSave)
    #     filedialog.setDefaultSuffix("png")
    #
    #     if filedialog.exec()== QFileDialog.Accepted:
    #         if filedialog.selectedFiles():
    #             self.canvas.Save(filedialog.selectedFiles()[0])
    #
    # #color functions
    # @Slot()
    # def selectColor1(self):
    #     color=QColorDialog.getColor(Color1,self)
    #     if color:
    #         self.setColor(color,Color2)
    #
    # @Slot()
    # def selectColor2(self):
    #     color=QColorDialog.getColor(Color2,self)
    #     if color:
    #         self.setColor(Color1,color)
    #
    # #set colors
    # @Slot()
    # def setColor(self,color1,color2):
    #     Color1=color1
    #     Color2=color2
    #
    #     #creating a color Icons
    #     pixIcon1=QPixmap(32,32)
    #     pixIcon1.fill(Color1)
    #     pixIcon2 = QPixmap(32, 32)
    #     pixIcon2.fill(Color2)
    #     #setting the button colors
    #     self.color1Action.setIcon(QIcon(pixIcon1))
    #     self.color2Action.setIcon(QIcon(pixIcon2))
    #     self.color1Action.setText(QColor(Color1).name())
    #     self.color2Action.setText(QColor(Color2).name())
if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())



