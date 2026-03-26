import random
from enum import Enum

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPolygonF
from shapely import MultiPoint, Point
from shapely import voronoi_polygons
from shapely.creation import geometrycollections


class Poly:
    def __init__(self, S, P, FC, SC):
        self.Site = S
        self.polygon = P
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
        self.polygon = P

    def SetSite(self, S):
        self.Site = S

    def __eq__(self, other):
        if isinstance(other, Poly):
            return other.Site == self.Site
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class SiteData:
    def __init__(self):
        self.Polys = []
        self.Sites = []

    def AddSite(self, NewSite):
        new_point = Point(NewSite[0], NewSite[1])
        if new_point in self.Sites:
            return False
        self.Sites.append(new_point)
        return True

    def RemoveSite(self, Site):
        pt = QPointF(Site[0], Site[1])

        for p in self.Polys:
            if p.GetPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                self.Sites.remove(p.GetSite())
                self.ClearPolys()
                return True

        return False

    def ClearPolys(self):
        self.Polys.clear()

    def AddPoly(self, S, P):
        self.Polys.append(Poly(S, P, QColor(235, 235, 235), QColor(255, 0, 0)))

    def GetPolys(self):
        return self.Polys

    def GetSites(self):
        return self.Sites


class DrawModes(Enum):
    Select = 1
    Add = 2
    Remove = 3


class VoronoiHandler:
    def __init__(self):
        self.Voro = geometrycollections([])
        self.data = SiteData()
        self.Tolerance = 0.001

        self.can = None
        self.mode = DrawModes.Add

        self.SitesEnabled = True
        self.LinesEnabled = True
        self.LineColor = QColor(0, 0, 0)
        self.LineThickness = 3

        self.area = None
        self.label_model = None

    def setCanvas(self, canvas):
        self.can = canvas
        cansize = self.can.GetCanvasSize()
        self.area = MultiPoint([
            [0, 0],
            [cansize[0], 0],
            [cansize[0], cansize[1]],
            [0, cansize[1]]
        ])
        self.can.SetLineThickness(self.LineThickness)

    @property
    def GetCanvas(self):
        return self.can

    def GenerateRandomPoints(self, N):
        if self.can is None:
            return

        size = self.can.GetCanvasSize()
        for _ in range(N):
            newpos = [random.randrange(10, size[0] - 10), random.randrange(10, size[1] - 10)]
            self.UpdateDiagram(newpos)

    def AddSite(self, NewSite):
        return self.data.AddSite(NewSite)

    def RemoveSite(self, Pos):
        return self.data.RemoveSite(Pos)

    def RegenerateVoronoi(self):
        sites = self.data.GetSites()
        if len(sites) <= 0 or self.area is None:
            return

        tempMulti = MultiPoint(sites)
        self.Voro = voronoi_polygons(
            tempMulti,
            tolerance=self.Tolerance,
            extend_to=self.area,
            only_edges=False,
            ordered=True
        )

    def UpdatePolys(self):
        sites = self.data.GetSites()
        if len(sites) <= 0:
            self.data.ClearPolys()
            return

        self.data.ClearPolys()
        i = 0

        for p in self.Voro.geoms:
            templist = []
            for v in p.exterior.coords:
                templist.append(QPointF(v[0], v[1]))

            polygon = QPolygonF(templist)
            site = sites[i]
            self.data.AddPoly(site, polygon)
            i += 1

    def assignLabelToCell(self, pos):
        if self.label_model is None:
            return

        selected_label = self.label_model.get_selected_label()
        if selected_label is None:
            return

        pt = QPointF(pos[0], pos[1])

        for poly in self.data.GetPolys():
            if poly.GetPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                poly.setFillColor(QColor(selected_label.getFillColor()))
                break

        self.UpdateCanvas()

    def UpdateDiagram(self, Pos):
        if self.mode == DrawModes.Add:
            if self.AddSite(Pos):
                self.RegenerateVoronoi()
                self.UpdatePolys()
                self.UpdateCanvas()

        elif self.mode == DrawModes.Remove:
            if self.RemoveSite(Pos):
                self.RegenerateVoronoi()
                self.UpdatePolys()
                self.UpdateCanvas()
            else:
                if len(self.data.GetSites()) <= 0 and self.can:
                    self.clearCanvas()

        elif self.mode == DrawModes.Select:
            self.assignLabelToCell(Pos)

    def UpdateCanvas(self):
        if not self.can:
            return

        self.can.ClearCanvas()
        self.can.renderCells()

        if self.SitesEnabled:
            self.can.renderSites()

    def setMode(self, M):
        self.mode = M

    def toggleLines(self, L):
        self.LinesEnabled = L
        self.UpdateCanvas()

    def toggleSites(self, S):
        self.SitesEnabled = S
        self.UpdateCanvas()

    def SetLineColor(self, C):
        self.LineColor = C
        self.UpdateCanvas()

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
        return

    def clearCanvas(self):
        if self.can:
            self.can.ClearCanvas()

    def GetLineThickness(self):
        return self.LineThickness

    def SetLineThickness(self, T):
        self.LineThickness = T
        if self.can:
            self.can.SetLineThickness(T)