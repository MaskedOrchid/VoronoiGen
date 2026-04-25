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

from Apps.MainApplicationClasses import CellDialog
from Apps.MainApplicationClasses.VoronoiView import VoronoiView
import Apps.MainApplicationClasses.CellDialog

class Cell:
    """
    Represents a single Voronoi cell with its associated metadata.
    
    A container class that holds information about an abstract cell in the Voronoi diagram,
    including the site point, cell polygon, and display colors.
    
    Attributes:
        polygon: QPolygonF representing the cell boundaries
        label: a Label object for this cell/Site
    """
    def __init__(self, p, l):
        """Initialize a Poly object with site, polygon, and colors.
        
        Args:
            p: QPolygonF representing the cell boundary
            l: a Label object representing the label associated to this cell
        """
        self.polygon = p
        self.label=l

    def getPolygon(self):
        """Get the QPolygonF representing the cell boundary."""
        return self.polygon

    def getLabel(self):
        """Get the QColor used to fill the cell."""
        return self.label

    def setLabel(self, l):
        """Set the Label for the site/cell
        
        Args:
            l: the site's label
        """
        self.label=l

    def setPolygon(self, p):
        """Set the boundary polygon for the cell.
        
        Args:
            p: QPolygonF representing the cell boundary
        """
        self.polygon = p

    def removeSelfFromLabel(self):
        """Removes self from the Label"""
        if self.label is not None:
            self.label.removeSite(self)



class VoronoiModel:
    """
    Data model for Voronoi diagram.
    
    Manages the sites (seed points) and their associated cells (Poly objects).
    Sites are stored as Shapely Point objects, and cells are stored as Poly objects.
    This class handles data storage and retrieval for the Voronoi diagram.
    """
    def __init__(self):
        """Initialize the Voronoi model with empty sites and polygons."""

        self.Sites = {}   # Dictionary of Shapely Point objects representing sites and their cell

    def addSite(self, newsite,l):
        """Add a new site to the model if it doesn't already exist.
        
        Args:
            newsite: [x, y] coordinates for the new site
            l: this site's label
            
        Returns:
            bool: True if site was added, False if it already exists
        """
        new_point = Point(newsite[0], newsite[1])
        if new_point in self.Sites:
            return False
        self.Sites[new_point]=Cell(QPolygonF(),l)
        return True

    def removeSite(self, point):
        """Remove a site based on point coordinates.
        
        Finds the polygon containing the point and removes its associated site
        
        Args:
            point: [x, y] coordinates of the point to remove
            
        Returns:
            bool: True if site was removed, False if not found
        """
        s = self.findSiteContainPoint(point)
        if s is not None:
            c=self.Sites.get(s)
            c.removeSelfFromLabel() #making the cell remove itself from the label
            self.Sites.pop(s) #removing the site from the dictionary
            return True

        print("Error could not find target site to remove")
        return False

    def clearPolys(self):
        """Clear all sites and polygons from the model."""
        self.Sites.clear()

    def setCell(self, s, p):
        """Set a new polygon to a site
        
        Args:
            s: Shapely Point for the site
            p: QPolygonF for the cell's edges
        """
        c=self.Sites.get(s)
        c.setPolygon(p)

    def setSite(self,oldsite,nsite):
        """Set a new polygon to a site

        Args:
            oldsite: the former Shapely point
            nsite: the new Shapely point to replace the old
        """
        c = self.Sites.get(oldsite)
        self.Sites.pop(oldsite)
        self.Sites[nsite] = c

    def setLabel(self,s,l):
        """sets a site's label to the model.

        Args:
           s: Shapely Point for the site
           l: A label object
         """
        c = self.Sites.get(s)
        c.setLabel(l)

    def getCells(self):
        """Get all polygon objects in the model.
        
        Returns:
            list: List of Poly objects
        """
        return self.Sites.values()

    def getSites(self):
        """Get all site points in the model.
        
        Returns:
            list: List of Shapely Point objects
        """
        return list(self.Sites.keys())

    def findSiteContainPoint(self, point):
        """Find the polygon containing the given point coordinates.
        
        Args:
            point: [x, y] coordinates to try to find the closest site point
            
        Returns:
            s: the cell's site that contains this point
        """
        pt = QPointF(point[0], point[1])
        for s in self.Sites:
            p=self.Sites.get(s)
            # Use odd-even fill rule for point containment check
            if p.getPolygon().containsPoint(pt, Qt.FillRule.OddEvenFill):
                return s
        return None

    def getCellFromSite(self, site):
        """Find the polygon associated with a given site.
        
        Args:
            site: Shapely Point representing the site
            
        Returns:
            C: The cell object for this site, or None if not found
        """
        c=self.Sites.get(site)
        return c
    def getCell(self,site):
        """Find the polygon associated with a given site.

        Args:
            site: Shapely Point representing the site

        Returns:
            C: The cell object for this site, or None if not found
        """
        return self.Sites.get(site)

    def cleanUpCellLabels(self,defaultL,l):
        """Searches and replaces any cells with null label to the default label

        Args:
            defaultL: the default label
            l: the label being removed
        """
        for c in  self.Sites.values():
            if c.getLabel() is None or c.getLabel()==l[0]:
                #assumes that there will always be one label in the arg tuple
                c.setLabel(defaultL)


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
        # Tolerance for degenerate data handling for sites being too close
        self.Tolerance = 0.001

        # View for rendering the diagram
        self.can = VoronoiView(self, dimX, dimY)
        # Current interaction mode (Add, Remove, or Select)
        self.mode = DrawModes.Add

        # Display settings
        self.SitesEnabled = True       # Show/hide site points
        self.LinesEnabled = True       # Show/hide cell borders
        self.LineColor = QColor(0, 0, 0)  # Color for cell borders (black)

        # Define the bounding area for Voronoi computation
        self.area = MultiPoint(
            [[0, 0], [dimX, 0], [dimX, dimY], [0, dimY]]
        )
        # label model for associating labels with cells
        self.label_model = None
        self.cell_dialog = None

    def setUpFromModel(self,packages,options):
        """Creates the Voronoi Diagram from parsed data.

        Args:
            packages= package that contains the parsed data.
        """
        for package in packages:
            self.addSite([package.xPosition, package.yPosition])
            site = self.data.getSites()[-1]
            self.data.setLabel(site,package.label)
            self.assignCellToLabel(site, package.label)

        self.toggleLines(options.lineToggle)
        self.toggleSites(options.siteToggle)
        self.setLineColor(QColor(options.lineColor))
        self.setLineThickness(options.lineWeight)

        self.regenerateVoronoi()
        self.updatePolys()
        self.updateCanvas()

    def grabCorrectLabel(self, label):
        """Finds the label that this cell uses

            Args:
                label: the label we are trying to find
        """
        for lbl in self.label_model.getAllLabels():
            if lbl == label:
                return lbl
        return None

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

    def setLabelModel(self, l):
        """Set the label model for managing cell labels.
        
        Args:
            l: Label model object to associate with this controller
        """
        self.label_model = l
        self.connectLabelSignals()

    def connectLabelSignals(self):
        """Connects onLabelChange and onLabelRemove to label_model signals
        """

        if self.label_model is not None:
            #connecting the label model signals to the related functions
            self.label_model.label_updated.connect(self.onLabelChange)
            self.label_model.label_removed.connect(self.onLabelRemove)

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

        This is a testing function.
        
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
        l=None
        # Add site to the currently selected label.
        if self.label_model is not None:

            if self.label_model.getSelectedLabel() is None:
                l=self.label_model.getDefaultLabel()
                self.label_model.addSiteToLabel(newsite,self.label_model.getSelectedLabel())
            else:
                l=self.label_model.getSelectedLabel()
                self.label_model.addSiteToSelectedLabel(newsite)
        # Add site to the data model
        return self.data.addSite(newsite,l)

    def removeSite(self, pos):
        """Remove a site at the given coordinates.
        
        Removes the site from the label model(s) and the data model.
        
        Args:
            pos: [x, y] coordinates of the mouse click event
            
        Returns:
            bool: True if site was removed, False if not found
        """
        # Finding the closest site that will approximate which site needs to be removed
        s=self.data.findSiteContainPoint(pos)
        self.label_model.removeSiteFromAllLabels(s)

        return self.data.removeSite(pos)

    def regenerateVoronoi(self):
        """Recompute the Voronoi diagram from current sites.
        
        Uses Shapley's voronoi_polygons function to compute the diagram
        based on the current set of sites, with result clipped to the canvas dimensions
        """
        sites = self.data.getSites()
        # Don't regenerate if no sites or no bounding area
        if len(sites) <= 0 or self.area is None:
            return

        # Convert sites to Shapely MultiPoint
        tempMulti = MultiPoint(sites)
        # Compute Voronoi polygons clipped to the canvas area
        #ordered must be true
        #   polygons and sites will not share the same index otherwise

        oldvoro=self.Voro
        try:
            #trying to regenerate the voronoi diagram from updated data
            self.Voro = voronoi_polygons(
                tempMulti,
                tolerance=self.Tolerance,
                extend_to=self.area,
                only_edges=False,
                ordered=True,
            )
        except:
            #if it failed, will revert to previous version of diagram
            #note, will not revert site data which can cause a softlock
            print("ERROR: Failed to regenerate Voronoi Diagram")
            self.Voro=oldvoro

    def updatePolys(self):
        """Convert computed Voronoi polygons to Poly objects in the data model.
        
        Transforms Shapely voronoi geometry into QPolygons and creates Poly objects
        with appropriate colors from the label model.
        """
        sites = self.data.getSites()
        # If no sites, clear the model and return
        if len(sites) <= 0:
            self.data.clearPolys()
            return

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

            # setting this site's cell's polygon
            self.data.setCell(site,polygon)
            i += 1

    def assignCellToLabel(self, site, label):
        """Assign a cell to a label in the label model.
        
        Removes the site from all current labels and assigns it to the selected label.
        
        Args:
            site: Shapely Point representing the site to assign
            label: the Label that the cell needs to be assigned too
        """
        if self.label_model is None:
            return
        # Remove site from all current labels
        self.label_model.removeSiteFromAllLabels(site)
        # Add site to the currently selected label
        self.label_model.addSiteToLabel(site,label)

    def assignLabelToCell(self, site):
        """Assign a label's colors to a cell at the given position.
        
        Updates the cell's fill and site colors based on the currently selected label.
        
        Args:
            site: Shapely Point representing the site to assign
        """
        if self.label_model is None:
            return

        # Get the currently selected label
        selected_label = self.label_model.getSelectedLabel()
        if selected_label is None:
            return

        # Find the cell at the given position
        if site is None:
            return
        # Update the cell's colors from the label
        self.data.setLabel(site,selected_label)

    def updateDiagram(self, pos):
        """Update the Voronoi diagram based on the current mode and position.
        
        Handles Add, Remove, or Select mode operations at the given coordinates.
        In Add/Remove modes, regenerates the diagram and updates the view.
        In Select mode, assigns the cell to a label.
        
        Args:
            pos: [x, y] the mouse coordinates for the operation with in the Voronoi View widget
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
            site = self.data.findSiteContainPoint(pos)
            if site is not None:
                self.assignLabelToCell(site)
                self.cell_dialog = CellDialog.CellCustomizationDialog(self, site)
                self.cell_dialog.exec()
                # Render the updated canvas
                self.updateCanvas()

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
        """Toggle the visibility of cell borderlines.
        
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
        self.SitesEnabled = bool(s)
        self.updateCanvas()

    def setSiteSize(self, s):
        """
        Set the size of the site dots used for drawing cell borders.

        Args:
            s: radius value (float) in pixels for the site dots
        """
        self.can.setSiteSize(s)
        self.updateCanvas()

    def setLineColor(self, c):
        """Set the color for drawing cell borders.
        
        Args:
            c: QColor for the lines
        """
        self.can.setLineColor(c)
        self.updateCanvas()

    def setLineThickness(self, t):
        """
        Set the thickness of the pen used for drawing cell borders.

        Args:
            t: Thickness value (float) in pixels for the pen stroke width
        """
        self.can.setLineThickness(t)

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
        return self.can.getLineThickness()

    def getLineColor(self):
        """Get the current line color for cell borders.

        Returns:
            Qcolor: The color of the lines
        """
        return self.can.getLineColor()


    def getSiteSize(self):
        """Get the current site size

        Returns:
            int: The radius in pixels
        """
        return self.can.getSiteSize()

    def onLabelChange(self, *args):
        """Handle changes to a label by updating all associated cells.
        
        When a label's properties change (e.g., color), this method updates
        all cells associated with that label to reflect the new properties.
        
        Args:
            *args: The label object that was changed
        """
        self.updateCanvas()

    def onLabelRemove(self,*args):
        """Handles the removal of a label by correcting the data and setting the
        cells with invalid label back to the default label
        """
        self.data.cleanUpCellLabels(self.label_model.getDefaultLabel(),args)
        self.updateCanvas()

    def acceptCellDialogChanges(self, site, label, x, y):
        """Handles accepting the Cell Dialog changes

        Sets the label, and the new position of the site.

        Args:
            site: The original site
            label: The cell's label
            x: the new x coord
            y: the new y coord
        """
        #replacing the old point with the new point
        self.data.setSite(site,Point(x, y))

        self.regenerateVoronoi()
        self.updatePolys()
        site = self.data.findSiteContainPoint([x,y])
        if site is None:
            return
        else:

            self.assignCellToLabel(site,label)
            self.data.setLabel(site, label)

        self.updateCanvas()

    def exportToNoi(self, filepath, window):
        """Exports and packs the Voronoi Data into a noi file

            Args:
                filepath= the file path of the save file
                window= window parameter
            """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("canvas_x,canvas_y,name,line_toggle,line_color,line_weight,site_toggle\n")
            f.write(f"{self.getCanvas.getCanvasSize()[0]},{self.getCanvas.getCanvasSize()[1]},{window},"
                    f"{int(self.getLineToggle())},{self.getLineColor().name()},{self.getLineThickness()},"
                    f"{int(self.getSiteToggle())}\n")
            f.write("x-coordinate,y-coordinate,label title,cell color\n")
            controller = self.getData()
            for site in controller.getSites():
                label = controller.getCell(site).getLabel()
                f.write(f"{site.x},{site.y},{label.getName()},{label.getFillColor().name()},{label.getSiteColor().name()}\n")
