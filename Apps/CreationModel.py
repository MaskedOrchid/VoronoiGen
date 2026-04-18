
class OptionsModel:

    """
        Model for storing canvas options data.
    """

    def __init__(self):
        self.lineToggle = 1
        self.lineWeight = 10.0
        self.lineColor = "#000000"
        self.siteToggle = 1

class CreationModel:
    """
        Model for converting data from the CreationView into the Main Application and Canvas.
    """
    def __init__(self, tt = "", cx = 0, cy = 0):
        """
            Args:
                tt: The title of the canvas.
                cx: The width of the canvas.
                cy: The height of the canvas.
        """
        self.title = tt
        self.canvasWidth = cx
        self.canvasHeight = cy
        self.file = ""
        self.labels = []
        self.packages = []
        self.options = OptionsModel()

    def setOptionsModel(self, lt, lw, lc, st):
        """
            Args:
                lt: The line toggle state.
                lw: The line thickness/weight.
                lc: The line color.
                st: The site toggle state.
        """
        self.options.lineToggle = lt
        self.options.lineWeight = lw
        self.options.lineColor = lc
        self.options.siteToggle = st

    def getOptions(self):
        """
        Returns:
            The canvas options data.
        """
        return self.options

    def changeName(self, newName):
        """
            Args:
                The new title of the project.
        """
        self.title = newName

    def changeWidth(self, newWidth):
        """
            Args:
                The new pixel width of the canvas.
        """
        self.canvasWidth = newWidth

    def changeHeight(self, newHeight):
        self.canvasHeight = newHeight

    def getTitle(self):
        """
            Returns:
                The project title.
        """
        return self.title

    def width(self):
        """
            Returns:
                The project width.
        """
        return self.canvasWidth

    def height(self):
        """
            Returns:
                The project height.
        """
        return self.canvasHeight

    def getLabels(self):
        """
            Returns:
                The list of labels in the project.
        """
        return self.labels

    def changeFile(self, newFile):
        """
            Args:
                The filepath of the new file.
        """
        self.file = newFile

    def getFile(self):
        """
            Returns:
                The filepath used when opening the project.
        """
        return self.file