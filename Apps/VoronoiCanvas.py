#this class will handle the rendering and drawing of the voronoi


from PySide6.QtCore import QSize, Qt, QPointF
from PySide6.QtGui import QColor, QImage, QPainter, QPen, QBrush, Qt, QPaintEvent, QMouseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class VoronoiCanvas(QWidget):
    def __init__(self, voronoi_handler):
        super().__init__()

        self.handler = voronoi_handler
        self.voro = self.handler  # ✅ keep this

        self.Dimensions = [500, 500]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        # setting up voronoi related controls
        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        # drawing functionality
        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.Image.fill(Qt.white)

        self.BGImage = ""
        self.Painter = QPainter()

        self.Pen = QPen()
        self.Pen.setCapStyle(Qt.RoundCap)
        self.Pen.setJoinStyle(Qt.RoundJoin)

        self.Brush = QBrush(Qt.SolidPattern)

    def GetCanvasSize(self):
        return self.Dimensions

    def GiveVoronoiDiagram(self, V):
        self.voro=V


    def renderSites(self):
        #this renders the sites only
        #this is the top most layer
        painter = QPainter(self.Image)
        polys = self.voro.GetData().GetPolys()

        for p in polys:
            #setting up the Pen
            sitepoint=p.GetSite()
            self.Brush.setColor(p.getSiteColor())
            self.Pen.setColor(p.getSiteColor())
            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)

            #calling the draw event
            painter.drawPoint(QPointF(sitepoint.x,sitepoint.y))
            self.update()
        return True

    def renderCells(self):
        #this render cells and their lines
        #this is the  bottom most layer
        painter = QPainter(self.Image)

        polys = self.voro.GetData().GetPolys()
        for p in polys:
            #setting up brush and pen
            self.Brush.setColor(p.getFillColor())

            #setting up outlines
            if self.voro.GetLineToggle():
                self.Pen.setColor(self.voro.GetLineColor())
            else:
                self.Pen.setColor(p.getFillColor())
            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)

            #calling draw event
            painter.drawPolygon(p.GetPolygon())
            self.update()
        return True

    def paintEvent(self, event: QPaintEvent):
        # drawing the diagram
        painter = QPainter(self)
        painter.setPen(self.Pen)
        painter.drawImage(event.rect(), self.Image, self.Image.rect())

    #resize

    #SetCanvasSize

    #save image

    #load image/set as BG

    #set line thickness

    def GetCanvasSize(self):
        return self.Dimensions

    def sizeHint(self):
        return self.CanvasSize

    def mousePressEvent(self, event: QMouseEvent):
        # translating to scipy numbers
        pos = event.position()
        # adding the point to the voronoi diagram
        newpoint = [pos.x(), pos.y()]

        self.handler.UpdateDiagram(newpoint)  # refresh reference
        self.renderCells()
        self.renderSites()
        self.update()

    def ClearCanvas(self):
        #this need to be fixed to just clear the canvas and not regenerate a few image
        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.Image.fill(Qt.white)
        self.update()

    def SetLineThickness(self,T):
        self.Pen.setWidthF(T)

