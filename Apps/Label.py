#Imports
from PySide6.QtGui import QColor
from VoronoiHandler import Poly

#Label Class:
class Label:
    def __init__(self):
        self.Name=""
        self.FillColor=QColor(255,255,255)
        self.SiteColor=QColor(0,0,0)
        self.Sites=[] #List of Sites
        self.Polys=[] #list of polygons
    def setFillColor(self,C):
        self.FillColor=C

    def setSiteColor(self,S):
        self.SiteColor=S

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    def getName(self):
        return self.Name

    def addSite(self, S):
        self.Sites.append(S)

    def addPoly(self, P):
        self.Polys.append(P)

    def removeSite(self, S):
        #need to ensure that both the site and cell get added together
        self.Sites.remove(S)

    def removePoly(self, P):
        self.Polys.remove(P)
