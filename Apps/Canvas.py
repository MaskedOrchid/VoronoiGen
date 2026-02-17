#this class will handle the rendering and drawing of the voronoi

#need to update with past work/ research how to do this

#imports

'''
From Demo

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

      def mousePressEvent(self, event: QMouseEvent):
        #translating to scipy numbers
        pos=event.position()
        newpoint=[pos.x(),pos.y()]
        #adding the point to the voronoi diagram
        sucess=self.addPoint(newpoint)
        self.updatePolys()
        self.renderCells()
        #self.renderSites()

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

'''

