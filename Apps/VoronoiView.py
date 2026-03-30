"""
VoronoiView Module
Handles the visual rendering of Voronoi diagrams on a QWidget canvas.
Displays Voronoi cells and sites, handles user interactions, and manages painting.
"""

from PySide6.QtCore import QSize, Qt, QPointF
from PySide6.QtGui import QImage, QPainter, QPen, QBrush, QPaintEvent, QMouseEvent, QColor
from PySide6.QtWidgets import QWidget


class VoronoiView(QWidget):
    """
    A custom QWidget for displaying Voronoi diagrams.
    
    Manages canvas rendering, site and cell visualization, user mouse interactions,
    and updates to the Voronoi diagram.
    """
    def __init__(self, voronoicontroller, dimX, dimY):
        """
        Initialize the Voronoi view with specified dimensions.
        
        Args:
            voronoicontroller: The controller managing Voronoi diagram updates
            dimX: Canvas width in pixels
            dimY: Canvas height in pixels
        """
        super().__init__()

        # Store reference to the controller for diagram updates
        self.voro = voronoicontroller

        # Store canvas dimensions and create QSize object
        self.Dimensions = [dimX, dimY]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        # Set fixed canvas size
        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        # Create the main image buffer for rendering (ARGB32 for transparency support)
        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.BG = Qt.white  # Default background color
        self.Image.fill(self.BG)

        # Initialize pen and brush for drawing operations
        self.LineColor = QColor(0, 0, 0)
        self.LineThickness = 10
        self.SiteSize = 5
        self.Pen = QPen()
        self.Brush = QBrush(Qt.SolidPattern)

        self.Pen.setWidthF(self.LineThickness)


    def getCanvasSize(self):
        """
        Retrieve the current canvas dimensions.
        
        Returns:
            list: [width, height] of the canvas
        """
        return self.Dimensions

    def setCanvasSize(self, dimX, dimY):
        """
        Resize the canvas and recreate the image buffer.
        
        This will remake the canvas with new dimensions and reset the background.
        
        Args:
            dimX: New canvas width in pixels
            dimY: New canvas height in pixels
        """
        # Update stored dimensions
        self.Dimensions = [dimX, dimY]
        self.CanvasSize = QSize(self.Dimensions[0], self.Dimensions[1])

        # Update widget size constraints
        self.setFixedSize(self.CanvasSize)
        self.setMinimumSize(self.CanvasSize)

        # Recreate image buffer with new dimensions
        self.Image = QImage(self.CanvasSize, QImage.Format.Format_ARGB32)
        self.Image.fill(Qt.white)


    def renderSites(self):
        """
        Draw Voronoi site points on the canvas.
        
        Renders small circles at each site location with their respective colors.
        Called to visualize the seed points of the Voronoi diagram.
        """
        # Create painter for drawing on the image buffer
        painter = QPainter(self.Image)
        # Retrieve all polygons from the Voronoi data
        sites= self.voro.getData().getSites()

        # Draw a colored dot at each site location
        for s in sites:
            cell=self.voro.getData().getCell(s)
            label=cell.getLabel()
            if label is None:
                self.Brush.setColor(QColor(255,255,255))
                self.Pen.setColor(QColor(0,0,0))
            else:
                # Set pen and brush to the site's color
                self.Brush.setColor(label.getSiteColor())
                self.Pen.setColor(label.getSiteColor())


            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            # Draw small circle (radius of 3 pixels) at site point
            painter.drawEllipse(QPointF(s.x, s.y),self.SiteSize,self.SiteSize)

        # Finish painting and update the widget display
        painter.end()
        self.update()

    def renderCells(self):
        """
        Draw all Voronoi cells on the canvas.
        
        Renders the filled polygons representing each Voronoi cell, with customizable
        cell fill colors and optional cell boundary lines.
        """
        # Create painter for drawing on the image buffer
        painter = QPainter(self.Image)
        # Retrieve all polygons from the Voronoi data
        cells = self.voro.getData().getCells()

        # Clear canvas with background color
        self.Image.fill(self.BG)

        # Draw each Voronoi cell polygon
        for c in cells:
            # Set the fill color for this cell
            label=c.getLabel()

            if label is None:
                self.Brush.setColor(QColor(255, 255, 255))
            else:
                self.Brush.setColor(label.getFillColor())

            # Determine line color: either user-specified or match cell fill color
            if self.voro.getLineToggle():
                # Use controller's line color setting if enabled
                self.Pen.setColor(self.LineColor)
            else:
                # Otherwise use the cell's fill color (invisible borders)
                self.Pen.setColor(label.getFillColor())

            painter.setPen(self.Pen)
            painter.setBrush(self.Brush)
            # Draw the filled polygon representing the Voronoi cell
            painter.drawPolygon(c.getPolygon())

        # Finish painting and update the widget display
        painter.end()
        self.update()

    def paintEvent(self, event: QPaintEvent):
        """
        Handle the paint event - redraw the widget when needed.
        
        Called automatically by Qt when the widget needs to be redrawn.
        Copies the internal image buffer to the widget's display area.
        
        Args:
            event: Qt paint event containing the region that needs repainting
        """
        painter = QPainter(self)
        # Draw the internal image buffer onto the widget
        painter.drawImage(event.rect(), self.Image, self.Image.rect())

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse click events on the canvas.
        
        Updates the Voronoi diagram by adding a new site at the clicked position.
        
        Args:
            event: Qt mouse event containing the click position
        """
        # Get the click position from the mouse event
        pos = event.position()
        # Update diagram with new site at clicked coordinates
        self.voro.updateDiagram([pos.x(), pos.y()])

    def clearCanvas(self):
        """
        Clear the canvas by filling it with the background color.
        
        Erases all previously drawn content on the canvas.
        """
        self.Image.fill(Qt.white)

    def setLineThickness(self, t):
        """
        Set the thickness of the pen used for drawing cell borders.
        
        Args:
            t: Thickness value (float) in pixels for the pen stroke width
        """
        self.LineThickness=t
        self.Pen.setWidthF(t)

    def setLineColor(self, c):
        """Set the color for drawing cell borders.

        Args:
            c: QColor for the lines
        """
        self.LineColor = c

    def setSiteSize(self, s):
        """
        Set the size of the site dots used for drawing cell borders.

        Args:
            s: radius value (float) in pixels for the site dots
        """
        self.SiteSize = s

    def getLineColor(self):
        """Get the current line color.

        Returns:
            QColor: The color of cell borders
        """
        return self.LineColor

    def getLineThickness(self):
        """Get the current line thickness for cell borders.

        Returns:
            int: The thickness in pixels
        """
        return self.LineThickness

    def getSiteSize(self):
        """Get the current site size

        Returns:
            int: The radius in pixels
        """
        return self.SiteSize
