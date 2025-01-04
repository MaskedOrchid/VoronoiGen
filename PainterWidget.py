import sys
from math import isqrt, pow
from random import randint

from PyQt6.QtCore import Qt, QPoint, QSize, QPointF
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QMouseEvent,
    QPaintEvent,
    QPolygon,
    QImage, QPen, QPolygonF)

import numpy
from PyQt6.QtWidgets import QWidget

from scipy.spatial import Voronoi


def distance(x1, y1, x2, y2):
    return isqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

def findColor(point):
    #finding the distance and then finding the total distance
    return QColor(randint(0,255),randint(0,255),randint(0,255))

class PainterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Cize=QSize(500,500)
        self.setFixedSize(self.Cize)
        #Voronoir set up
        self.points = numpy.random.randint(50, size=(50, 2))
        self.vor = Voronoi(self.points, False, True)
        self.cells = []
        self.image=QImage(self.Cize,QImage.Format.Format_ARGB32)
        self.painter = QPainter()
        self.pen=QPen()
        #the colors
        self.Color1 = QColor()
        self.Color2 = QColor()
        self.lineColor=QColor.black

        self.renderCells()


    def addPoint(self,newpoints):
        #adding new points
        self.vor.add_points(newpoints)
        numpy.append(self.points,newpoints)
        return True

    def mousePressEvent(self, event: QMouseEvent):
        #translating to scipy numbers
        pos=event.position()
        newarray=numpy.array([[pos.x(),pos.y()]])
        #adding the point to the voronoi diagram
        sucess=self.addPoint(newarray)
        colors=[]
        i=0
        if sucess:
            self.renderCells()

    def renderCells(self):
        i = 0
        painter=QPainter(self.image)
        painter.setPen(self.pen)
        for region in self.vor.regions:
            if -1 not in region:
                i += 1
                poly = QPolygonF()
                for p in region:
                    # finding the coords of the points from the region
                    vert = self.vor.vertices[p]
                    # building the poly gon and saving it
                    poly.append(QPointF(vert[0], vert[1]))
                painter.drawPolygon(poly)
                self.update()


    def paintEvent(self, event: QPaintEvent):
        #drawing the diagram
        painter=QPainter(self)
        painter.setPen(self.pen)
        painter.drawImage(event.rect(),self.image,self.image.rect())