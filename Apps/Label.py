"""
Label Module
Manages a label's data which are its name, fillcolor,
sitecolor, and the amount of sites connected to this label
"""

from PySide6.QtGui import QColor


class Label:
    """
        Represents a single label with its associated metadata.

        A container class that holds information about an abstract label in the label system
        including the name, fillcolor, site color, and the amount of sites connected to this label

        Attributes:
            Name: The label's name
            FillColor: The label's Fillcolor
            SiteColor: The label's Site color
            Sites: The label's Sites
    """
    def __init__(self, name="", fill = QColor(255,255,255), site = QColor(0,0,0)):
        """Initialize a Poly object with site, polygon, and colors.

        Args:
            name: The label's name
            fill: The label's Fillcolor
            site: The label's Site color
        """
        self.Name = name
        self.FillColor = fill
        self.SiteColor = site
        self.Sites = []

    def setFillColor(self, color):
        """Sets the fill color of the label

        Args:
            color: the new color that the fillcolor should be
        """
        self.FillColor = color

    def setSiteColor(self, color):
        """Sets the sites color of the label

        Args:
            color: the new color that the site color should be
        """
        self.SiteColor = color

    def getFillColor(self):
        """Returns the fill color of the label

        Returns:
            self.FillColor: the label's fillcolor
        """
        return self.FillColor

    def getSiteColor(self):
        """Returns the site color of the label

        Returns:
            self.Sitecolor: the label's site color
        """
        return self.SiteColor

    def getName(self):
        """Returns the name of the label

        Returns:
            self.Name: the label's name
        """
        return self.Name

    def addSite(self, site):
        """Adds a site to this label's list

        Args:
            site: the site to add
        """
        if site not in self.Sites:
            self.Sites.append(site)

    def getSites(self):
        """Returns the list of sites

         Returns:
            self.sites: the list of sites
        """
        return self.Sites

    def removeSite(self, site):
        """Removes a site to this label's list

        Args:
            site: the site to remove
        """
        if site in self.Sites:
            self.Sites.remove(site)

    def __str__(self):
        """Overriding the str function to use the label's name

        Returns:
            self.Name: the label's name
        """
        return self.Name

    def __eq__(self, other):
        """Overriding the eq function to have proper equality testing

        Args:
            other: the other label we are compared too

        Returns:
            bool: whether the two labels have the same name
        """
        if other is None:
            return False
        return self.Name == other.getName()

    def __neg__(self):
        """Overriding the neg function to handle negation...
            what is the negative of a label?

        Returns:
            self.Name: The label's name
        """
        return self.Name
