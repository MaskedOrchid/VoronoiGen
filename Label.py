#Imports
from PySide6.QtGui import QColor

#Label Class:
class Label:
    def __init__(self):
        self.Name=""
        self.FillColor=QColor.White
        self.SiteColor=QColor.Black

    def setFillColor(self,C):
        self.FillColor=C

    def setSiteColor(self,C):
        self.SiteColor=C

    def getFillColor(self):
        return self.FillColor

    def getSiteColor(self):
        return self.SiteColor

    def getName(self):
        return self.Name
