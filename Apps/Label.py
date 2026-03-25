# Imports
from PySide6.QtGui import QColor
from VoronoiHandler import Poly


# Label Class:
class Label:

    def __init__(self, name="", color=QColor(255, 255, 255)):
        self.Name = name
        self.FillColor = color
        self.SiteColor = QColor(0, 0, 0)
        self.Sites = []  # List of Sites
        self.Polys = []  # list of polygons

    def setFillColor(self, C):
        self.FillColor = C

    def setSiteColor(self, S):
        self.SiteColor = S

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    def getName(self):
        return self.Name

    def addSite(self, S):
        if S not in self.Sites:  # Prevent duplicates
            self.Sites.append(S)

    def addPoly(self, P):
        if P not in self.Polys:  # Prevent duplicates
            self.Polys.append(P)

    def removeSite(self, S):
        if S in self.Sites:
            self.Sites.remove(S)

    def removePoly(self, P):
        if P in self.Polys:
            self.Polys.remove(P)

    def __str__(self):
        return self.Name