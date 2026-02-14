from shapely.ops import voronoi_diagram
import Label


#The Poly Class
class Poly:
    def __init__(self):
        self.label= Label()
        self.Lines=[]
    def getLabel(self):
        return self.label
    def GetColor(self):
        return self.label.getFillColor()
    def setlabel(self,L):
        self.label=L

#the Voronoi Handler Class
    #this class will manage and allow access to the voronoi diagram
class VoronoiHandler:
    def __init__(self):
        self.Voro=voronoi_diagram()
        self.Polys=[] #this would be a poly class list
        self.Sites=[] #this would be sites in Shapely Point form
    def UpdateSites(self,S):
        #this function will replace Sites with Shapely point form of S

    def GenerateVoronoi(self,S):
        #this function will generate a voronoi from a list of coordnet data

    def getPolys(self):
        #returns the polygons to be rendered
        return self.Polys

