
import pandas as pd
import re
import os
from PySide6.QtGui import QColor


from Apps import Label

excel_set = {".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"}

# xls, xlsx, xlsm, xlsb, odf, ods and odt

class ParsedPackage:
    """
        Stores parsed data for a point.
    """
    def __init__(self, x, y, l):
        self.xPosition = x
        self.yPosition = y
        self.label = l

class Parser:
    """

        The base class for all parsers.
        Provides label creation, an abstract parse function,
        and a default behavior for parsing.
    """
    def __init__(self):
        self.labels = []
        self.packages = []

    def createLabel(self, n, c, c2):
        lbl = Label.Label(n,QColor(c), QColor(c2))
        if lbl in self.labels:
            return lbl # will refactor later TO DO
        else:
            self.labels.append(lbl)
            return lbl

    def parse(self, filepath : str):
        pass

    def parseBehavior(self, filedata : pd.DataFrame):
        for i, row in filedata.iterrows():
            try:
                x = float(row[0])
                y = float(row[1])

                n = ""
                if len(row) > 2 and pd.notna(row[2]):
                    n = str(row[2])

                c = ""
                if len(row) > 3 and pd.notna(row[3]):
                    color = str(row[3])
                    match = re.search(r'^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
                    if match:
                        if color[0] != '#':
                            c = '#' + color
                        else:
                            c = color
                    else:
                        c = "#FFFFFF"
                c2 = ""
                if len(row) > 4 and pd.notna(row[4]):
                    color = str(row[4])
                    match = re.search(r'^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
                    if match:
                        if color[0] != '#':
                            c2 = '#' + color
                        else:
                            c2 = color
                    else:
                        c2 = "#000000"

                lbl = self.createLabel(n, c, c2)
                pkg = ParsedPackage(x, y, lbl)
                self.packages.append(pkg)

            except(ValueError, KeyError):
                continue


class ExcelParser(Parser):
    """
        The parser for Excel files.
        Includes *.xlsx, *.xls, *.xlsm, *.xlsb, *.odf, *.ods, and *.odt filetypes.
    """
    def parse(self, filepath):
        filedata = pd.read_excel(filepath, header=None, dtype=str)
        self.parseBehavior(filedata)


class CsvParser(Parser):
    """
        The parser for *.csv files.
    """
    def parse(self, filepath):
        filedata = pd.read_csv(filepath, header=None, dtype=str)
        self.parseBehavior(filedata)

class NoiParser(Parser):
    """
        The parser for *.noi files.

        Params:
            cx: the width of the canvas
            cy: the height of the canvas
            title: the title of the project
            lineToggle: the line toggle setting for the canvas
            lineColor: the color of the lines on the canvas
            lineThickness: the line weight/thickness for the canvas
            siteToggle: the site toggle setting for the canvas

     """
    def __init__(self):
        super().__init__()
        self.cx = 0
        self.cy = 0
        self.title = ""
        self.lineToggle = 0
        self.lineColor = "#000000"
        self.lineThickness = 0.0
        self.siteToggle = 0

    def parse(self, filepath):
        filedata = pd.read_csv(filepath, header=None, dtype=str)

        for row_num, (index, row) in enumerate(filedata.iterrows()):

            if row_num == 1:
                self.cx = round(float(row[0]))
                self.cy = round(float(row[1]))
                self.title = str(row[2])
                self.lineToggle = int(row[3])
                self.lineColor = str(row[4])
                self.lineThickness = float(row[5])
                self.siteToggle = int(row[6])
            else:
                try:
                    x = float(row[0])
                    y = float(row[1])

                    n = ""
                    if len(row) > 2 and pd.notna(row[2]):
                        n = str(row[2])

                    c = ""
                    if len(row) > 3 and pd.notna(row[3]):
                        color = str(row[3])
                        match = re.search(r'^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
                        if match:
                            if color[0] != '#':
                                c = '#' + color
                            else:
                                c = color
                        else:
                            c = "#FFFFFF"

                    c2 = ""
                    if len(row) > 4 and pd.notna(row[4]):
                        color = str(row[4])
                        match = re.search(r'^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
                        if match:
                            if color[0] != '#':
                                c2 = '#' + color
                            else:
                                c2 = color
                        else:
                            c2 = "#000000"

                    lbl = self.createLabel(n,c,c2)
                    pkg = ParsedPackage(x, y, lbl)
                    self.packages.append(pkg)

                except(ValueError, KeyError):
                    continue


def create_parser(filepath : str) -> Parser:
    """
        Generates the correct parser based on the provided path's file extension.

        Args:
            filepath: name of file to be parsed

        Returns:
            Parser: A subtype of the Parser class.
     """
    filename, file_extension = os.path.splitext(filepath)

    if file_extension == ".csv":
        return CsvParser()
    elif file_extension in excel_set:
        return ExcelParser()
    elif file_extension == ".noi":
        return NoiParser()

    return CsvParser()