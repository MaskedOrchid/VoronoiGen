from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QFont, QColor)
from PySide6.QtWidgets import (
    QDialogButtonBox, QLabel, QComboBox, QPushButton,
    QLineEdit, QDialog, QColorDialog, QFrame
)

class Ui_CellCustomizationDialog(object):
    def setupUi(self, CellCustomizationDialog):
        if not CellCustomizationDialog.objectName():
            CellCustomizationDialog.setObjectName(u"CellCustomizationDialog")
        CellCustomizationDialog.resize(400, 260)

        self.buttonBox = QDialogButtonBox(CellCustomizationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 220, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.label = QLabel(CellCustomizationDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 354, 38))
        font = QFont()
        font.setFamilies([u"Fuku Catch"])
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.dropdown = QComboBox(CellCustomizationDialog)
        self.dropdown.setObjectName(u"dropdown")
        self.dropdown.setGeometry(QRect(100, 60, 200, 25))

        self.cellColorLabel = QLabel(CellCustomizationDialog)
        self.cellColorLabel.setObjectName(u"cellColorLabel")
        self.cellColorLabel.setGeometry(QRect(40, 100, 120, 25))

        self.cellColorFrame = QFrame(CellCustomizationDialog)
        self.cellColorFrame.setObjectName(u"cellColorFrame")
        self.cellColorFrame.setGeometry(QRect(180, 100, 40, 25))
        self.cellColorFrame.setStyleSheet("background-color: white; border: 1px solid black;")

        self.siteColorLabel = QLabel(CellCustomizationDialog)
        self.siteColorLabel.setObjectName(u"siteColorLabel")
        self.siteColorLabel.setGeometry(QRect(40, 130, 120, 25))

        self.siteColorFrame = QFrame(CellCustomizationDialog)
        self.siteColorFrame.setObjectName(u"siteColorFrame")
        self.siteColorFrame.setGeometry(QRect(180, 130, 40, 25))
        self.siteColorFrame.setStyleSheet("background-color: white; border: 1px solid black;")

        self.xLabel = QLabel(CellCustomizationDialog)
        self.xLabel.setObjectName(u"xLabel")
        self.xLabel.setGeometry(QRect(80, 170, 20, 25))

        self.xInput = QLineEdit(CellCustomizationDialog)
        self.xInput.setObjectName(u"xInput")
        self.xInput.setGeometry(QRect(100, 170, 60, 25))

        self.yLabel = QLabel(CellCustomizationDialog)
        self.yLabel.setObjectName(u"yLabel")
        self.yLabel.setGeometry(QRect(200, 170, 20, 25))

        self.yInput = QLineEdit(CellCustomizationDialog)
        self.yInput.setObjectName(u"yInput")
        self.yInput.setGeometry(QRect(220, 170, 60, 25))

        self.retranslateUi(CellCustomizationDialog)

        self.buttonBox.accepted.connect(CellCustomizationDialog.accept)
        self.buttonBox.rejected.connect(CellCustomizationDialog.reject)

        QMetaObject.connectSlotsByName(CellCustomizationDialog)


    def retranslateUi(self, CellCustomizationDialog):
        CellCustomizationDialog.setWindowTitle(
            QCoreApplication.translate("CellCustomizationDialog", u"Dialog", None)
        )
        self.label.setText(
            QCoreApplication.translate("CellCustomizationDialog", u"customize cell", None)
        )
        self.cellColorLabel.setText(
            QCoreApplication.translate("CellCustomizationDialog", u"Cell Fill Color", None)
        )
        self.siteColorLabel.setText(
            QCoreApplication.translate("CellCustomizationDialog", u"Site Fill Color", None)
        )
        self.xLabel.setText("X:")
        self.yLabel.setText("Y:")


class CellCustomizationDialog(QDialog):

    def __init__(self, controller, p):
        super().__init__()
        self.controller = controller
        self.poly = p


        self.ui = Ui_CellCustomizationDialog()
        self.ui.setupUi(self)

        self.ui.cellColorFrame.mousePressEvent = self.changeCellColor
        self.ui.siteColorFrame.mousePressEvent = self.changeSiteColor
        self.ui.dropdown.currentTextChanged.connect(self.changeLabel)

        self.dialog = QColorDialog()
        self.dialog2 = QColorDialog()

        self.ui.dropdown.clear()
        labels = list(map(lambda label: label.Name, controller.label_model.get_all_labels()))
        self.ui.dropdown.addItem("")
        self.ui.dropdown.addItems(labels)

        self.selectedLabel = ""
        self.fillColor = p.FillColor
        self.siteColor = p.SiteColor
        self.xPos = p.Site.x
        self.yPos = p.Site.y

        self.ui.xInput.setText(str(self.xPos))
        self.ui.yInput.setText(str(self.yPos))

        label = controller.label_model.get_label_with_site(p.Site)
        if label:
            self.ui.dropdown.setCurrentText(label.Name)
            self.selectedLabel = label.Name

    def changeLabel(self, name):

        if name == "":
            self.selectedLabel = ""
            return

        labels = self.controller.label_model.get_all_labels()
        label = next(lbl for lbl in labels if lbl.getName() == name)

        self.fillColor = label.FillColor
        self.ui.cellColorFrame.setStyleSheet(
            f"background-color: {label.FillColor.name()}; border: 1px solid black;")
        self.selectedLabel = label.getName()




    def changeCellColor(self, event):
        color = self.dialog.getColor()
        if color.isValid():
            if self.fillColor != color :
                self.selectedLabel = ""
                self.ui.dropdown.setCurrentText("")
                self.fillColor = color
                self.ui.cellColorFrame.setStyleSheet(
                    f"background-color: {color.name()}; border: 1px solid black;")
        return

    def changeSiteColor(self, event):
        color = self.dialog2.getColor()
        if color.isValid():
            self.siteColor = color
            self.ui.siteColorFrame.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid black;")
        return


    def accept(self):
        try:
            self.xPos = float(self.ui.xInput.text())
            self.yPos = float(self.ui.yInput.text())
        except ValueError:
            return

        label = None
        if self.selectedLabel == "":
            label = None
        else:
            labels = self.controller.label_model.get_all_labels()
            label = next(lbl for lbl in labels if lbl.getName() == self.selectedLabel)

        self.controller.acceptCellDialogChanges(self.poly, label, self.fillColor, self.siteColor, self.xPos, self.yPos)
        super().accept()
