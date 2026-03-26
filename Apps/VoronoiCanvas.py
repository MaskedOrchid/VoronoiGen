from PySide6.QtCore import QSize, Qt, QPointF
from PySide6.QtGui import QImage, QPainter, QPen, QBrush, QPaintEvent, QMouseEvent
from PySide6.QtWidgets import QWidget


class VoronoiCanvas(QWidget):
    def __init__(self, voronoi_handler, dimX, dimY):
        super().__init__()

        self.handler = voronoi_handler
        self.voro = self.handler

        self.Dimensions = [dimX, dimY]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.Image.fill(Qt.white)

        self.Pen = QPen()
        self.Brush = QBrush(Qt.SolidPattern)

    def GetCanvasSize(self):
        return self.Dimensions

    def renderSites(self):
        painter = QPainter(self.Image)
        polys = self.voro.GetData().GetPolys()

        for p in polys:
            sitepoint = p.GetSite()
            self.Brush.setColor(p.getSiteColor())
            self.Pen.setColor(p.getSiteColor())

            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            painter.drawEllipse(QPointF(sitepoint.x, sitepoint.y), 3, 3)

        painter.end()
        self.update()

    def renderCells(self):
        painter = QPainter(self.Image)
        polys = self.voro.GetData().GetPolys()

        for p in polys:
            self.Brush.setColor(p.getFillColor())

            if self.voro.GetLineToggle():
                self.Pen.setColor(self.voro.GetLineColor())
            else:
                self.Pen.setColor(p.getFillColor())

            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            painter.drawPolygon(p.GetPolygon())

        painter.end()
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.Image, self.Image.rect())

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position()
        newpoint = [pos.x(), pos.y()]
        self.handler.UpdateDiagram(newpoint)

    def ClearCanvas(self):
        self.Image.fill(Qt.white)

    def SetLineThickness(self, T):
        self.Pen.setWidthF(T)