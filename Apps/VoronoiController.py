import random
from enum import Enum

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPolygonF
from shapely import MultiPoint, Point
from shapely import voronoi_polygons
from shapely.creation import geometrycollections


from Apps.VoronoiView import VoronoiView


class Poly:
    """
    Poly:
        A container class that holds information about an abstract cell
        in the voronoi diagram
        Args: site ( Shapely point ), Qpolygon, QColor and another QColor
    """
    def __init__(self, s, p, sc, fc):
        self.Site = s
        self.polygon = p
        self.FillColor = fc
        self.SiteColor = sc

    def getSite(self):
        return self.Site

    def getPolygon(self):
        return self.polygon

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    def setFillColor(self, fc):
        self.FillColor = fc

    def setSiteColor(self, sc):
        self.SiteColor = sc

    def setPolygon(self, p):
        self.polygon = p

    def setSite(self, s):
        self.Site = s

    def __eq__(self, other):
        if isinstance(other, Poly):
            return other.Site == self.Site
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class VoronoiModel:
    """
     VoronoiModel:
        A class model that manages the site and their associated cells for the voronoi Diagram.
        Sites are stored as a list of Shapely points, and Cells are stored as a
        list of Poly objects
     """
    def __init__(self):
        self.Polys = []
        self.Sites = []

    def addSite(self, newsite):
        new_point = Point(newsite[0], newsite[1])
        if new_point in self.Sites:
            return False
        self.Sites.append(new_point)
        return True

    def removeSite(self, site):

        p = self.findPolyContainPoint(site)
        if p is not None:
            self.Sites.remove(p.getSite())
            self.clearPolys()
            return True
        return False

    def clearPolys(self):
        self.Polys.clear()

    def addPoly(self, s, p,sc,fc):
        self.Polys.append(Poly(s, p, sc, fc))

    def getPolys(self):
        return self.Polys

    def getSites(self):
        return self.Sites

    def findPolyContainPoint(self, site):
        pt = QPointF(site[0], site[1])
        for p in self.Polys:
            if p.getPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                return p
        return None
    def getPolyFromSite(self,site):
        for p in self.Polys:
            if p.getSite()==site:
                return p


class DrawModes(Enum):
    Select = 1
    Add = 2
    Remove = 3


class VoronoiController:
    """
      VoronoiController:
         A controller class that manages the voronoi diagram, as well as it's models, and view.
         This class handles and communicates for the Voronoi suite and should
         be where other classes main contact
      """
    def __init__(self, dimX, dimY):
        self.Voro = geometrycollections([])
        self.data = VoronoiModel()
        self.Tolerance = 0.001

        self.can = VoronoiView(self,dimX,dimY)
        self.mode = DrawModes.Add

        self.SitesEnabled = True
        self.LinesEnabled = True
        self.LineColor = QColor(0, 0, 0)
        self.LineThickness = 3

        self.area = MultiPoint(
            [[0, 0], [dimX, 0], [dimX, dimY], [0, dimY]]
            )
        self.label_model = None


    def setCanvasSize(self, dimX, dimY):
        self.can.setCanvasSize(dimX,dimY)
        self.area = MultiPoint(
            [[0, 0], [dimX, 0], [dimX, dimY], [0, dimY]]
        )
        self.can.setLineThickness(self.LineThickness)

    def setLabelModel(self,l):
        self.label_model=l
        self.label_model.give_model_vc(self)

    @property
    def getCanvas(self):
        return self.can

    def generateRandomPoints(self, n):
        if self.can is None:
            return

        size = self.can.getCanvasSize()
        for _ in range(n):
            newpos = [
                random.randrange(10, size[0] - 10),
                random.randrange(10, size[1] - 10),
            ]
            self.updateDiagram(newpos)

    def addSite(self, newsite):
        if self.label_model is not None:
            self.label_model.add_site_to_label(newsite)
        return self.data.addSite(newsite)

    def removeSite(self, pos):
        if self.label_model is not None:
            rmpoly=self.data.findPolyContainPoint(pos)
            if rmpoly is None:
                print("Error could not find target site to remove")
            else:
                rmsite = self.data.findPolyContainPoint(pos).getSite()
                self.label_model.remove_site_from_all_labels(rmsite)

        return self.data.removeSite(pos)

    def regenerateVoronoi(self):
        sites = self.data.getSites()
        if len(sites) <= 0 or self.area is None:
            return

        tempMulti = MultiPoint(sites)
        self.Voro = voronoi_polygons(
            tempMulti,
            tolerance=self.Tolerance,
            extend_to=self.area,
            only_edges=False,
            ordered=True,
        )

    def updatePolys(self):
        sites = self.data.getSites()
        if len(sites) <= 0:
            self.data.clearPolys()
            return

        self.data.clearPolys()
        i = 0

        for p in self.Voro.geoms:
            templist = []
            for v in p.exterior.coords:
                templist.append(QPointF(v[0], v[1]))

            polygon = QPolygonF(templist)
            site = sites[i]

            l=self.label_model.get_label_with_site(site)
            if l is None:
                self.data.addPoly(site, polygon,Qt.black,Qt.white)
            else:
                self.data.addPoly(site, polygon,l.getSiteColor(),l.getFillColor())
            i += 1

    def assignCellToLabel(self,site):
        if self.label_model is None:
            return
        self.label_model.remove_site_from_all_labels(site)
        self.label_model.add_site_to_label(site)

    def assignLabelToCell(self, pos):
        # This function assigns a color to the Poly object
        if self.label_model is None:
            return

        selected_label = self.label_model.get_selected_label()
        if selected_label is None:
            return

        p = self.data.findPolyContainPoint(pos)
        p.setFillColor(selected_label.getFillColor())
        p.setSiteColor(selected_label.getSiteColor())

        self.updateCanvas()

    def updateDiagram(self, pos):
        if self.mode == DrawModes.Add:
            if self.addSite(pos):
                self.regenerateVoronoi()
                self.updatePolys()
                self.updateCanvas()

        elif self.mode == DrawModes.Remove:
            if self.removeSite(pos):
                self.regenerateVoronoi()
                self.updatePolys()
                self.updateCanvas()
            else:
                if len(self.data.getSites()) <= 0 and self.can:
                    self.clearCanvas()

        elif self.mode == DrawModes.Select:
            p=self.data.findPolyContainPoint(pos)
            self.assignCellToLabel(p.getSite())
            self.assignLabelToCell(pos)

    def updateCanvas(self):
        if not self.can:
            return

        self.can.renderCells()

        if self.SitesEnabled:
            self.can.renderSites()

    def setMode(self, m):
        self.mode = m

    def toggleLines(self, l):
        self.LinesEnabled = l
        self.updateCanvas()

    def toggleSites(self, s):
        self.SitesEnabled = s
        self.updateCanvas()

    def setLineColor(self, c):
        self.LineColor = c
        self.updateCanvas()

    def getMode(self):
        return self.mode

    def getLineToggle(self):
        return self.LinesEnabled

    def getSiteToggle(self):
        return self.SitesEnabled

    def getLineColor(self):
        return self.LineColor

    def getData(self):
        return self.data

    def addLabel(self):
        return

    def clearCanvas(self):
        if self.can:
            self.can.clearCanvas()

    def getLineThickness(self):
        return self.LineThickness

    def setLineThickness(self, t):
        self.LineThickness = t
        if self.can:
            self.can.setLineThickness(t)

    def onLabelChange(self,label):
        #This will update all the polys with the updated information of their label
        sites=label.getSites()
        for s in sites:
            p=self.data.getPolyFromSite(s)
            if p is not None:
                p.setFillColor(label.getFillColor())
                p.setSiteColor(label.getSiteColor())

        self.updateCanvas()
