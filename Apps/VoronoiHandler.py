from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPolygonF
from shapely import voronoi_polygons
from shapely import MultiPoint, Point
from shapely.creation import geometrycollections
import Label

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

#the Voronoi Handler Class
    #this class will manage and allow access to the voronoi diagram
class VoronoiHandler:
    def __init__(self):
        self.Voro=geometrycollections([])
        self.Polys=[] #this would be a poly class list
        self.Sites=[] #this would be sites in Shapely Point form
        self.Tolerance = 0.0

    def AddSite(self,NewSite):
        #this function will add a point and regenerate the voronoi
        self.Sites.append(Point(NewSite[0],NewSite[1]))

    def UpdateSites(self,S):
        #this function will replace all Sites with Shapely point form of S
        #Assumes that S is a list of Tuples
        self.Sites.clear()
        for i in range(len(S)-1):
            self.AddSite(S[i])

        self.RegenerateVoronoi()

    def RegenerateVoronoi(self):
        #this function will generate a voronoi from a list of sites
        if len(self.Sites)>1:
            tempMulti = MultiPoint(self.Sites)
            #this will generate a voronoi diagram
            self.Voro = voronoi_polygons(tempMulti,self.Tolerance,None,False,True)

    def UpdatePolys(self):
        #need to somehow update the label class
        #maybe does not need to save the polygons
        if len(self.Sites) < 2:
            # if we do not have the minimum number of points in order to generate the voronoi
            print("Error: Minimum points not met")
            return
        self.Polys.clear()
        i=0
        for p in self.Voro.geoms:
            templist = []  # a list of Qpointf of this cell
            for v in p.exterior.coords:
                templist.append(QPointF(v[0], v[1]))
            # adding that list of vertices as a polygon to make it easier to render the voronoi diagram
            p=QPolygonF(templist)
            s=self.Sites[i]
            self.Polys.append(Poly(s,p,QColor(255,255,255),QColor(0,0,0)))
            i+=1

    def getPolys(self):
        #returns the polygons to be rendered
        return self.Polys

