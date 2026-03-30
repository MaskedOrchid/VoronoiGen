import os

from PySide6.QtGui import (QFontDatabase, QFont)


# Class for initializing the custom UI fonts
class FontInitialization:

    def __init__(self):
        self.loadFonts("Fonts/VanillaExtractRegular.ttf")
        self.loadFonts("Fonts/FukuCatch.otf")

    def loadFonts(self, fp):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(current_directory, fp)
        QFontDatabase.addApplicationFont(file.__str__())
