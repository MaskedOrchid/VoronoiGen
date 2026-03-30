
# TODO: Add and implement parsed file information, background image, custom filetype, etc.
# Model for converting data from the CreationView into the Main Application and Canvas.
class CreationModel:

    def __init__(self, tt = "", cx = 0, cy = 0):
        self.title = tt
        self.canvasWidth = cx
        self.canvasHeight = cy

    def changeName(self, newName):
        self.title = newName

    def changeWidth(self, newWidth):
        self.canvasWidth = newWidth

    def changeHeight(self, newHeight):
        self.canvasHeight = newHeight

    def getTitle(self):
        return self.title

    def width(self):
        return self.canvasWidth

    def height(self):
        return self.canvasHeight