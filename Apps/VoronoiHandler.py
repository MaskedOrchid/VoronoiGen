import sys
from enum import Enum
import random

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPolygonF
from PySide6.QtWidgets import QMainWindow, QApplication
from shapely import MultiPoint, Point
from shapely import voronoi_polygons
from shapely.creation import geometrycollections

from VoronoiCanvas import VoronoiCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.voro=VoronoiHandler()
        self.isadding=True
        self.can=self.voro.GetCanvas
        self.setCentralWidget(self.can)


#The Poly Class
class Poly:
    def __init__(self, S, P, FC, SC):
        self.Site=S
        self.polygon=P
        self.FillColor = FC
        self.SiteColor = SC
    def GetSite(self):
        return self.Site
    def GetPolygon(self):
        return self.polygon
    def getFillColor(self):
        return self.FillColor
    def getSiteColor(self):
        return self.SiteColor
    def setFillColor(self, FC):
        self.FillColor = FC
    def SetSiteColor(self, SC):
        self.SiteColor = SC
    def SetPolygon(self, P):
        self.polygon=P
    def SetSite(self, S):
        self.Site=S

#The SiteData Class
class SiteData:
    def __init__(self):
        self.Polys = []  # this would be a poly class list
        self.Sites = []  # this would be sites in Shapely Point form

    def AddSite(self, NewSite):
        #adds a site to the data structure
        self.Sites.append(Point(NewSite[0], NewSite[1]))
        return True

    def RemoveSite(self,Site):
        #Removes a site, and it's cell
        # if successful clears the polygons
        for p in self.Polys:
            pt= QPointF(Site[0], Site[1])
            if p.GetPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                #contains this site, now remove the cell and it's site
                self.Sites.remove(p.GetSite())
                self.ClearPolys()
                return True
        #did not find a valid cell/site to remove
        return False

    def ClearPolys(self):
        self.Polys.clear()

    def AddPoly(self, S, P):
        self.Polys.append(Poly(S, P, QColor(255, 255, 255), QColor(255, 0, 0)))

    def GetPolys(self):
        return self.Polys

    def GetSites(self):
        return self.Sites

class DrawModes(Enum):
    Select=1
    Add=2
    Remove=3

#the Voronoi Handler Class
    #this class will manage and allow access to the voronoi diagram
    #this class
class VoronoiHandler:
    def __init__(self):
        self.Voro=geometrycollections([])
        self.data=SiteData()
        self.Tolerance = 0.0

        #Drawing Stuff
        self.can=VoronoiCanvas()
        self.can.GiveVoronoiDiagram(self)
        self.mode=DrawModes.Add

        self.SitesEnabled = True
        self.LinesEnabled = True
        self.LineColor=QColor(0, 0, 0)

        #setting up bounds
        cansize=self.can.GetCanvasSize()
        self.area=MultiPoint([[0,0],[cansize[0],0],
                             cansize,[0,cansize[1]]])

        #for testing

        for i in range(0,10,1):
            newpos=[random.randrange(100,400),random.randrange(100,400)]
            self.UpdateDiagram(newpos)
        self.mode = DrawModes.Remove

    def AddSite(self,NewSite):
        #this function will add a new site to the data and regenerate the voronoi
        return self.data.AddSite(NewSite)

    def RemoveSite(self,Pos):
        #this function will remove the site/cell that contains Pos
        return self.data.RemoveSite(Pos)

    def RegenerateVoronoi(self):
        #this function will generate a voronoi from a list of sites
        sites=self.data.GetSites()
        if len(sites)>0:
            tempMulti = MultiPoint(sites)
            #this will generate a voronoi diagram
            self.Voro = voronoi_polygons(tempMulti,tolerance=self.Tolerance,extend_to=self.area,only_edges=False,ordered=True)

    def UpdatePolys(self):
        #need to somehow update the label class--> maybe tell Label that things changed
        #assumes that SiteData as Polygons and Sites have the same Indices
        sites = self.data.GetSites()
        if len(sites) <=0:
            # if we do not have the minimum number of points in order to generate the voronoi
            print("Error: Minimum Site amount not met")
            return
        self.data.ClearPolys()
        i=0
        for p in self.Voro.geoms:
            templist = []  # a list of Qpointf of this cell
            for v in p.exterior.coords:
                templist.append(QPointF(v[0], v[1]))
            # adding that list of vertices as a polygon to make it easier to render the voronoi diagram
            p=QPolygonF(templist)
            s=sites[i]
            self.data.AddPoly(s,p)
            i+=1

        #update labels
    @property
    def GetCanvas(self):
        return self.can

    def UpdateDiagram(self, Pos):
        #Updating voronoi and communicates the drawing functions to the canvas class
        if self.mode==DrawModes.Add:
            if self.AddSite(Pos):
                self.RegenerateVoronoi()
                self.UpdatePolys()
                self.UpdateCanvas()
        elif self.mode==DrawModes.Remove:
            if self.RemoveSite(Pos):
                self.RegenerateVoronoi()
                self.UpdatePolys()
                self.UpdateCanvas()
        else:
            print("Selecting the closest Cell")
            return

    def UpdateCanvas(self):

        self.can.renderCells()
        if self.SitesEnabled:
            self.can.renderSites()

    def setMode(self, M):
        self.mode=M

    def toggleLines(self,L):
        # Sets whether the Lines are enabled
        self.LinesEnabled=L

    def toggleSites(self,S):
        #Sets whether the sites are enabled
        self.SitesEnabled = S

    def SetLineColor(self, C):
        self.LineColor=C

    def GetMode(self):
        return self.mode

    def GetLineToggle(self):
        return self.LinesEnabled

    def GetSiteToggle(self):
        return self.SitesEnabled

    def GetLineColor(self):
        return self.LineColor

    def GetData(self):
        return self.data

    def AddLabel(self):
        #does label stuff
        return


#this starts up the process to open and run the main window object
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()