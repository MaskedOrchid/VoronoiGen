from math import isqrt, pow
from random import randint

from PyQt6.QtCore import Qt,QSize, QPointF
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QMouseEvent,
    QPaintEvent,
    QImage, QPen, QPolygonF, QBrush)


from PyQt6.QtWidgets import QWidget
from shapely import voronoi_polygons
from shapely import LineString, MultiPoint, normalize, Point
from shapely.creation import geometrycollections


def distance(x1, y1, x2, y2):
    return isqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

def findColor(point):
    #finding the distance and then finding the total distance
    return QColor(randint(0,255),randint(0,255),randint(0,255))

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Cize=QSize(500,500)
        self.setFixedSize(self.Cize)

        #Voronoi set up
        self.points=[] #minimum size is 2
        self.Voro=geometrycollections([])
        self.cells=[]

        #the colors
        self.Color1 = QColor(255,255,255)
        self.Color2 = QColor()
        self.lineColor=QColor.black
        self.siteColor=QColor(255,0,0)

        #setting the painter objects
        self.image=QImage(self.Cize,QImage.Format.Format_ARGB32)
        self.painter = QPainter()
        self.pen=QPen()
        self.brush=QBrush(Qt.BrushStyle.SolidPattern)

    def addPoint(self, newpoint):
        # adding new points
        self.points.append(newpoint)
        print(self.points)
        #checking if the minimum number of sites is met
        if len(self.points)>1 :
            #if the list of points is now the minimum size of 2 we have to regenerate the voronoi
            tempMulti=MultiPoint(self.points) #converting to a multipoint for shapely's voronoi algo
            self.Voro=voronoi_polygons(tempMulti) # going to return a polygon object


    def mousePressEvent(self, event: QMouseEvent):
        #translating to scipy numbers
        pos=event.position()
        newpoint=[pos.x(),pos.y()]
        #adding the point to the voronoi diagram
        sucess=self.addPoint(newpoint)
        self.updatePolys()
        self.renderCells()
        #self.renderSites()

    def updatePolys(self):
        #this function Updates the Qt polygons to match the latest voronoi generated
        if len(self.points)<2:
            # if we do not have the minimum number of points in order to generate the voronoi
            print("Error: Minimum points not met")
            return
        i=0
        self.cells.clear()
        for p in self.Voro.geoms:
            templist=[] #a list of Qpointf of this cell
            for v in p.exterior.coords:
                templist.append(QPointF(v[0],v[1]))
            #adding that list of vertices as a polygon to make it easier to render the voronoi diagram
            self.cells.append(QPolygonF(templist))


    def renderSites(self):
        self.brush.setColor(self.siteColor)
        painter = QPainter(self.image)
        painter.setPen(self.pen)
        for p in self.points:
            painter.drawPoint(QPointF(p[0],p[1]))
            self.update()

    def renderCells(self):
        #else we can render the voronoi

        #setting the painter colors
        self.brush.setColor(self.Color1)
        painter=QPainter(self.image)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for poly in self.cells:
            painter.drawPolygon(poly)
            self.update()


    def paintEvent(self, event: QPaintEvent):
        #drawing the diagram
        painter=QPainter(self)
        painter.setPen(self.pen)
        painter.drawImage(event.rect(),self.image,self.image.rect())