"""
VoronoiController Module
Manages the Voronoi diagram generation, data model, and view rendering.
Handles site management, diagram updates, and user interactions.
"""

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
    Represents a single Voronoi cell with its associated metadata.
    
    A container class that holds information about an abstract cell in the Voronoi diagram,
    including the site point, cell polygon, and display colors.
    
    Attributes:
        Site: Shapely Point object representing the Voronoi site
        polygon: QPolygonF representing the cell boundaries
        FillColor: QColor for filling the cell
        SiteColor: QColor for drawing the site point
    """
    def __init__(self, s, p, sc, fc):
        """Initialize a Poly object with site, polygon, and colors.
        
        Args:
            s: Shapely Point representing the site
            p: QPolygonF representing the cell boundary
            sc: QColor for the site point
            fc: QColor for filling the cell
        """
        self.Site = s
        self.polygon = p
        self.FillColor = fc
        self.SiteColor = sc

    def getSite(self):
        """Get the Shapely Point representing the site."""
        return self.Site

    def getPolygon(self):
        """Get the QPolygonF representing the cell boundary."""
        return self.polygon

    def getFillColor(self):
        """Get the QColor used to fill the cell."""
        return self.FillColor

    def getSiteColor(self):
        """Get the QColor used to draw the site point."""
        return self.SiteColor

    def setFillColor(self, fc):
        """Set the fill color for the cell.
        
        Args:
            fc: QColor for filling the cell
        """
        self.FillColor = fc

    def setSiteColor(self, sc):
        """Set the color for the site point.
        
        Args:
            sc: QColor for drawing the site
        """
        self.SiteColor = sc

    def setPolygon(self, p):
        """Set the boundary polygon for the cell.
        
        Args:
            p: QPolygonF representing the cell boundary
        """
        self.polygon = p

    def setSite(self, s):
        """Set the site point for the cell.
        
        Args:
            s: Shapely Point representing the site
        """
        self.Site = s

    def __eq__(self, other):
        """Compare two Poly objects by their site points."""
        if isinstance(other, Poly):
            return other.Site == self.Site
        return False

    def __ne__(self, other):
        """Check inequality of two Poly objects."""
        return not self.__eq__(other)


class VoronoiModel:
    """
    Data model for Voronoi diagram.
    
    Manages the sites (seed points) and their associated cells (Poly objects).
    Sites are stored as Shapely Point objects, and cells are stored as Poly objects.
    This class handles data storage and retrieval for the Voronoi diagram.
    """
    def __init__(self):
        """Initialize the Voronoi model with empty sites and polygons."""
        self.Polys = []   # List of Poly objects representing cells
        self.Sites = []   # List of Shapely Point objects representing sites

    def addSite(self, newsite):
        """Add a new site to the model if it doesn't already exist.
        
        Args:
            newsite: [x, y] coordinates for the new site
            
        Returns:
            bool: True if site was added, False if it already exists
        """
        new_point = Point(newsite[0], newsite[1])
        if new_point in self.Sites:
            return False
        self.Sites.append(new_point)
        return True

    def removeSite(self, site):
        """Remove a site based on point coordinates.
        
        Finds the polygon containing the point and removes its associated site.
        
        Args:
            site: [x, y] coordinates of the point to remove
            
        Returns:
            bool: True if site was removed, False if not found
        """
        p = self.findPolyContainPoint(site)
        if p is not None:
            self.Sites.remove(p.getSite())
            self.clearPolys()
            return True
        return False

    def clearPolys(self):
        """Clear all polygons from the model."""
        self.Polys.clear()

    def addPoly(self, s, p, sc, fc):
        """Add a new polygon to the model.
        
        Args:
            s: Shapely Point for the site
            p: QPolygonF for the cell boundary
            sc: QColor for the site
            fc: QColor for filling the cell
        """
        self.Polys.append(Poly(s, p, sc, fc))

    def getPolys(self):
        """Get all polygon objects in the model.
        
        Returns:
            list: List of Poly objects
        """
        return self.Polys

    def getSites(self):
        """Get all site points in the model.
        
        Returns:
            list: List of Shapely Point objects
        """
        return self.Sites

    def findPolyContainPoint(self, site):
        """Find the polygon containing the given point coordinates.
        
        Args:
            site: [x, y] coordinates to search for
            
        Returns:
            Poly: The polygon object containing the point, or None if not found
        """
        pt = QPointF(site[0], site[1])
        for p in self.Polys:
            # Use odd-even fill rule for point containment check
            if p.getPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                return p
        return None
        
    def getPolyFromSite(self, site):
        """Find the polygon associated with a given site.
        
        Args:
            site: Shapely Point representing the site
            
        Returns:
            Poly: The polygon object for this site, or None if not found
        """
        for p in self.Polys:
            if p.getSite() == site:
                return p


class DrawModes(Enum):
    """Enumeration for the different interaction modes in the Voronoi diagram.
    
    Attributes:
        Select: Mode for selecting and changing existing cells
        Add: Mode for adding new sites to the diagram
        Remove: Mode for removing sites from the diagram
    """
    Select = 1
    Add = 2
    Remove = 3


class VoronoiController:
    """
    Main controller for the Voronoi diagram application.
    
    Manages the Voronoi diagram generation, data model, view rendering, and user interactions.
    Acts as the central hub for communication between different components of the Voronoi suite.
    Handles site management, diagram updates, and display configuration.
    """
    def __init__(self, dimX, dimY):
        """Initialize the Voronoi controller with canvas dimensions.
        
        Args:
            dimX: Canvas width in pixels
            dimY: Canvas height in pixels
        """
        # Shapely geometry collection for storing computed Voronoi polygons
        self.Voro = geometrycollections([])
        # Data model for managing sites and cells
        self.data = VoronoiModel()
        # Tolerance for Voronoi computation
        self.Tolerance = 0.001

        # View for rendering the diagram
        self.can = VoronoiView(self, dimX, dimY)
        # Current interaction mode (Add, Remove, or Select)
        self.mode = DrawModes.Add

        # Display settings
        self.SitesEnabled = True       # Show/hide site points
        self.LinesEnabled = True       # Show/hide cell borders
        self.LineColor = QColor(0, 0, 0)  # Color for cell borders (black)
        self.LineThickness = 3         # Width of cell border lines

        # Define the bounding area for Voronoi computation
        self.area = MultiPoint(
            [[0, 0], [dimX, 0], [dimX, dimY], [0, dimY]]
        )
        # Optional label model for associating labels with cells
        self.label_model = None


    def setCanvasSize(self, dimX, dimY):
        """Update the canvas dimensions and bounding area.
        
        Args:
            dimX: New canvas width in pixels
            dimY: New canvas height in pixels
        """
        self.can.setCanvasSize(dimX, dimY)
        # Update the bounding area for Voronoi computation
        self.area = MultiPoint(
            [[0, 0], [dimX, 0], [dimX, dimY], [0, dimY]]
        )
        self.can.setLineThickness(self.LineThickness)

    def setLabelModel(self, l):
        """Set the label model for managing cell labels.
        
        Args:
            l: Label model object to associate with this controller
        """
        self.label_model = l
        # Notify the label model about this controller
        self.label_model.give_model_vc(self)

    @property
    def getCanvas(self):
        """Get the canvas (view) object.
        
        Returns:
            VoronoiView: The canvas for rendering
        """
        return self.can

    def generateRandomPoints(self, n):
        """Generate n random sites on the canvas.
        
        Creates random points within the canvas bounds (with 10-pixel margin)
        and adds them to the diagram.
        
        Args:
            n: Number of random sites to generate
        """
        if self.can is None:
            return

        size = self.can.getCanvasSize()
        # Generate n random positions within the canvas bounds
        for _ in range(n):
            newpos = [
                random.randrange(10, size[0] - 10),
                random.randrange(10, size[1] - 10),
            ]
            # Add each random position to the diagram
            self.updateDiagram(newpos)

    def addSite(self, newsite):
        """Add a new site to the diagram.
        
        Adds the site to both the data model and any associated label model.
        
        Args:
            newsite: [x, y] coordinates for the new site
            
        Returns:
            bool: True if site was added successfully, False if it already exists
        """
        # Add site to label model if one is active
        if self.label_model is not None:
            self.label_model.add_site_to_label(newsite)
        # Add site to the data model
        return self.data.addSite(newsite)

    def removeSite(self, pos):
        """Remove a site at the given coordinates.
        
        Removes the site from the label model(s) and the data model.
        
        Args:
            pos: [x, y] coordinates of the site to remove
            
        Returns:
            bool: True if site was removed, False if not found
        """
        # Remove site from all labels if a label model is active
        if self.label_model is not None:
            rmpoly = self.data.findPolyContainPoint(pos)
            if rmpoly is None:
                print("Error could not find target site to remove")
            else:
                rmsite = self.data.findPolyContainPoint(pos).getSite()
                self.label_model.remove_site_from_all_labels(rmsite)

        # Remove from data model
        return self.data.removeSite(pos)

    def regenerateVoronoi(self):
        """Recompute the Voronoi diagram from current sites.
        
        Uses Shapely's voronoi_polygons function to compute the diagram
        based on the current set of sites, with result clipped to the canvas area.
        """
        sites = self.data.getSites()
        # Don't regenerate if no sites or no bounding area
        if len(sites) <= 0 or self.area is None:
            return

        # Convert sites to Shapely MultiPoint
        tempMulti = MultiPoint(sites)
        # Compute Voronoi polygons clipped to the canvas area
        self.Voro = voronoi_polygons(
            tempMulti,
            tolerance=self.Tolerance,
            extend_to=self.area,
            only_edges=False,
            ordered=True,
        )

    def updatePolys(self):
        """Convert computed Voronoi polygons to Poly objects in the data model.
        
        Transforms Shapely polygons to QPolygons and creates Poly objects
        with appropriate colors from the label model.
        """
        sites = self.data.getSites()
        # If no sites, clear the model and return
        if len(sites) <= 0:
            self.data.clearPolys()
            return

        # Clear old polygons and rebuild
        self.data.clearPolys()
        i = 0

        # Convert each Shapely polygon to a QPolygonF and create a Poly object
        for p in self.Voro.geoms:
            # Convert Shapely exterior coordinates to QPointF objects
            templist = []
            for v in p.exterior.coords:
                templist.append(QPointF(v[0], v[1]))

            # Create QPolygon from the points
            polygon = QPolygonF(templist)
            site = sites[i]

            # Get associated label for this site if it exists
            l = self.label_model.get_label_with_site(site) if self.label_model else None
            if l is None:
                # Use default colors if no label is assigned
                self.data.addPoly(site, polygon, Qt.black, Qt.white)
            else:
                # Use colors from the label
                self.data.addPoly(site, polygon, l.getSiteColor(), l.getFillColor())
            i += 1

    def assignCellToLabel(self, site):
        """Assign a cell to a label in the label model.
        
        Removes the site from all current labels and assigns it to the selected label.
        
        Args:
            site: Shapely Point representing the site to assign
        """
        if self.label_model is None:
            return
        # Remove site from all current labels
        self.label_model.remove_site_from_all_labels(site)
        # Add site to the currently selected label
        self.label_model.add_site_to_label(site)

    def assignLabelToCell(self, pos):
        """Assign a label's colors to a cell at the given position.
        
        Updates the cell's fill and site colors based on the currently selected label.
        
        Args:
            pos: [x, y] coordinates of the cell to update
        """
        if self.label_model is None:
            return

        # Get the currently selected label
        selected_label = self.label_model.get_selected_label()
        if selected_label is None:
            return

        # Find the polygon at the given position
        p = self.data.findPolyContainPoint(pos)
        if p is None:
            return
        # Update the cell's colors from the label
        p.setFillColor(selected_label.getFillColor())
        p.setSiteColor(selected_label.getSiteColor())

        # Render the updated canvas
        self.updateCanvas()

    def updateDiagram(self, pos):
        """Update the Voronoi diagram based on the current mode and position.
        
        Handles Add, Remove, or Select mode operations at the given coordinates.
        In Add/Remove modes, regenerates the diagram and updates the view.
        In Select mode, assigns the cell to a label.
        
        Args:
            pos: [x, y] coordinates for the operation
        """
        if self.mode == DrawModes.Add:
            # Add mode: add a new site and regenerate the diagram
            if self.addSite(pos):
                self.regenerateVoronoi()
                self.updatePolys()
                self.updateCanvas()

        elif self.mode == DrawModes.Remove:
            # Remove mode: remove the site under the click position
            if self.removeSite(pos):
                self.regenerateVoronoi()
                self.updatePolys()
                self.updateCanvas()
            else:
                # If no sites remain, clear the canvas
                if len(self.data.getSites()) <= 0 and self.can:
                    self.clearCanvas()

        elif self.mode == DrawModes.Select:
            # Select mode: assign cell to a label and update its colors
            p = self.data.findPolyContainPoint(pos)
            if p is not None:
                self.assignCellToLabel(p.getSite())
                self.assignLabelToCell(pos)

    def updateCanvas(self):
        """Render the current state of the diagram to the canvas.
        
        Renders cells and optionally renders sites based on the SitesEnabled flag.
        """
        if not self.can:
            return

        # Always render the cells
        self.can.renderCells()

        # Optionally render the sites
        if self.SitesEnabled:
            self.can.renderSites()

    def setMode(self, m):
        """Set the current interaction mode.
        
        Args:
            m: DrawModes value (Add, Remove, or Select)
        """
        self.mode = m

    def toggleLines(self, l):
        """Toggle the visibility of cell border lines.
        
        Args:
            l: bool - True to show lines, False to hide them
        """
        self.LinesEnabled = l
        self.updateCanvas()

    def toggleSites(self, s):
        """Toggle the visibility of site points.
        
        Args:
            s: bool - True to show sites, False to hide them
        """
        self.SitesEnabled = s
        self.updateCanvas()

    def setLineColor(self, c):
        """Set the color for drawing cell borders.
        
        Args:
            c: QColor for the lines
        """
        self.LineColor = c
        self.updateCanvas()

    def getMode(self):
        """Get the current interaction mode.
        
        Returns:
            DrawModes: The current mode
        """
        return self.mode

    def getLineToggle(self):
        """Check if cell borders are enabled.
        
        Returns:
            bool: True if lines are enabled, False otherwise
        """
        return self.LinesEnabled

    def getSiteToggle(self):
        """Check if site points are enabled.
        
        Returns:
            bool: True if sites are enabled, False otherwise
        """
        return self.SitesEnabled

    def getLineColor(self):
        """Get the current line color.
        
        Returns:
            QColor: The color of cell borders
        """
        return self.LineColor

    def getData(self):
        """Get the data model.
        
        Returns:
            VoronoiModel: The data model containing sites and polygons
        """
        return self.data

    def addLabel(self):
        """Placeholder for adding a new label.
        
        Currently not implemented.
        """
        return

    def clearCanvas(self):
        """Clear all content from the canvas.
        
        Fills the canvas with the background color.
        """
        if self.can:
            self.can.clearCanvas()

    def getLineThickness(self):
        """Get the current line thickness for cell borders.
        
        Returns:
            int: The thickness in pixels
        """
        return self.LineThickness

    def setLineThickness(self, t):
        """Set the thickness of cell border lines.
        
        Args:
            t: Thickness value in pixels
        """
        self.LineThickness = t
        # Update the canvas view with the new thickness
        if self.can:
            self.can.setLineThickness(t)

    def onLabelChange(self, label):
        """Handle changes to a label by updating all associated cells.
        
        When a label's properties change (e.g., color), this method updates
        all cells associated with that label to reflect the new properties.
        
        Args:
            label: The label object that was changed
        """
        # Get all sites associated with the changed label
        sites = label.getSites()
        # Update colors for all cells belonging to this label
        for s in sites:
            p = self.data.getPolyFromSite(s)
            if p is not None:
                p.setFillColor(label.getFillColor())
                p.setSiteColor(label.getSiteColor())

        # Render the updated diagram
        self.updateCanvas()
