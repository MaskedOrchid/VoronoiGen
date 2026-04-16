# -=-=-=-=-=-=-=-=-= IGNORE THIS -=-=-=-=-=-=-=-=-=

import pandas as pd
import re
import os
from PySide6.QtGui import QColor


from Apps import Label

excel_set = {".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"}

"""
    Generates the correct parser based on the provided path's file extension.
        
    Args:
        filepath: name of file to be parsed
            
    Returns:
        Parser: A subtype of the Parser class.
 """

# xls, xlsx, xlsm, xlsb, odf, ods and odt

class ParsedPackage:
    def __init__(self, x, y, l):
        self.xPosition = x
        self.yPosition = y
        self.label = l

class Parser:
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

    def parse_behavior(self, filedata : pd.DataFrame):
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
    def parse(self, filepath):
        filedata = pd.read_excel(filepath, header=None, dtype=str)
        self.parse_behavior(filedata)


class CsvParser(Parser):
    def parse(self, filepath):
        filedata = pd.read_csv(filepath, header=None, dtype=str)
        self.parse_behavior(filedata)

class NoiParser(Parser):

    def __init__(self):
        super().__init__()
        self.cx = 0
        self.cy = 0
        self.title = ""

    def parse(self, filepath):
        filedata = pd.read_csv(filepath, header=None, dtype=str)

        for row_num, (index, row) in enumerate(filedata.iterrows()):

            if row_num == 1:
                self.cx = int(row[0])
                self.cy = int(row[1])
                self.title = str(row[2])
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
    filename, file_extension = os.path.splitext(filepath)

    if file_extension == ".csv":
        return CsvParser()
    elif file_extension in excel_set:
        return ExcelParser()
    elif file_extension == ".noi":
        return NoiParser()

    return CsvParser()