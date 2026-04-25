from enum import Enum
import os


class Styles(Enum):
    GREENBUTTON = 0
    GRAYBUTTON = 1


class QSSGrabber:
    """
        Allows for pulling QSS files from the Stylesheets directory.
    """
    def grabStyle(self, style: Styles):
        """
            Returns a stylesheet based on a given enum value.
            Args:
                style: An enum value from Styles
            Returns:
                A stylesheet string from the QSS files.

        """
        base_dir = os.path.dirname(__file__)
        base_dir = base_dir.split("Apps")[0] + "Apps\\_UI Documents"

        match style:
            case Styles.GRAYBUTTON:
                image_path = os.path.join(base_dir, "Stylesheets", "GrayButton.qss")
            case Styles.GREENBUTTON:
                image_path = os.path.join(base_dir, "Stylesheets", "GreenButton.qss")
            case _:
                return None

        with open(image_path, "r") as fh:
            return fh.read()
