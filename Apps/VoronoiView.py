from PySide6.QtCore import QSize, Qt, QPointF
from PySide6.QtGui import QImage, QPainter, QPen, QBrush, QPaintEvent, QMouseEvent
from PySide6.QtWidgets import QWidget


class VoronoiView(QWidget):
    """
         VoronoiView:
            The viewer class of the Voronoi Controller. This class is responsible
            for rendering the diagram using the pyside (QT) paint events. This
            class manages its own mouse press events.
         """
    def __init__(self, voronoicontroller, dimX, dimY):
        super().__init__()

        self.voro = voronoicontroller

        self.Dimensions = [dimX, dimY]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.BG=Qt.white
        self.Image.fill(self.BG)

        self.Pen = QPen()
        self.Brush = QBrush(Qt.SolidPattern)

    def getCanvasSize(self):
        return self.Dimensions

    def setCanvasSize(self, dimX, dimY):
        #This function will resize the canvas creating a new canvas
        self.Dimensions = [dimX, dimY]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.Image.fill(Qt.white)


    def renderSites(self):
        #this function triggers paint events to render the sites as points on the image
        painter = QPainter(self.Image)
        polys = self.voro.getData().getPolys()

        for p in polys:
            sitepoint = p.getSite()
            self.Brush.setColor(p.getSiteColor())
            self.Pen.setColor(p.getSiteColor())

            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            painter.drawEllipse(QPointF(sitepoint.x, sitepoint.y), 3, 3)

        painter.end()
        self.update()

    def renderCells(self):
        # this function triggers paint events to render the cells as Qpolygons on the image
        painter = QPainter(self.Image)
        polys = self.voro.getData().getPolys()

        self.Image.fill(self.BG)

        for p in polys:
            self.Brush.setColor(p.getFillColor())

            if self.voro.getLineToggle():
                self.Pen.setColor(self.voro.getLineColor())
            else:
                self.Pen.setColor(p.getFillColor())

            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            painter.drawPolygon(p.getPolygon())

        painter.end()
        self.update()

    def paintEvent(self, event: QPaintEvent):
        #overriding the paint event to only draw with in the bounding
        #square of all the changes
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.Image, self.Image.rect())

    def mousePressEvent(self, event: QMouseEvent):
        #overriding the mouse press event to track the user's mouse movements
        # over the canvas
        pos = event.position()
        self.voro.updateDiagram([pos.x(), pos.y()])

    def clearCanvas(self):
        #clears the Canvas back to white
        self.Image.fill(Qt.white)

    def setLineThickness(self, t):
        self.Pen.setWidthF(t)
