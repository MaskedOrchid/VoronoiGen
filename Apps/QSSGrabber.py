from enum import Enum
import os



class Styles(Enum):
    GREENBUTTON = 0
    GRAYBUTTON = 1


# QSSGrabber allows for pulling QSS files from the Stylesheets directory
class QSSGrabber:

    def grabStyle(self, style: Styles):
        """Returns a stylesheet based on a given enum value.
        """
        base_dir = os.path.dirname(__file__)

        match style:
            case Styles.GRAYBUTTON:
                image_path = os.path.join(base_dir, "Stylesheets", "GrayButton.qss")
            case Styles.GREENBUTTON:
                image_path = os.path.join(base_dir, "Stylesheets", "GreenButton.qss")
            case _:
                return None

        image_path = image_path.replace("\\", "/")
        with open(image_path, "r") as fh:
            return fh.read()
