from PySide6.QtGui import QColor


class Label:
    def __init__(self, name="", color = QColor(255,255,255)):
        self.Name = name
        self.FillColor = color
        self.SiteColor = QColor(0, 0, 0)
        self.Sites = []

    def setFillColor(self, color):
        self.FillColor = color

    def setSiteColor(self, color):
        self.SiteColor = color

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    def getName(self):
        return self.Name

    def addSite(self, site):
        if site not in self.Sites:
            self.Sites.append(site)

    def getSites(self):
        return self.Sites

    def removeSite(self, site):
        if site in self.Sites:
            self.Sites.remove(site)

    def __str__(self):
        return self.Name

    def __eq__(self, other):
        if other is None:
            return False
        return self.Name == other.getName()

    def __neg__(self):
        return self.Name
