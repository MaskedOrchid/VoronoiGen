# Imports
from PySide6.QtGui import QColor


class Label:
    def __init__(self, name="", color=QColor(255, 255, 255)):
        self.Name = name
        self.FillColor = color
        self.SiteColor = QColor(0, 0, 0)

        self.Sites = []   # list of sites
        self.Polys = []   # list of polygons

    # -------------------------
    # COLOR METHODS
    # -------------------------
    def setFillColor(self, color):
        self.FillColor = color

    def setSiteColor(self, color):
        self.SiteColor = color

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    # -------------------------
    # NAME
    # -------------------------
    def getName(self):
        return self.Name

    # -------------------------
    # RELATIONS
    # -------------------------
    def addSite(self, site):
        if site not in self.Sites:
            self.Sites.append(site)

    def addPoly(self, poly):
        if poly not in self.Polys:
            self.Polys.append(poly)

    def removeSite(self, site):
        if site in self.Sites:
            self.Sites.remove(site)

    def removePoly(self, poly):
        if poly in self.Polys:
            self.Polys.remove(poly)

    # -------------------------
    # STRING
    # -------------------------
    def __str__(self):
        return self.Name