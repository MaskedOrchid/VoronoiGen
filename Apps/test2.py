# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test2.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDial, QPushButton, QSizePolicy,
    QWidget, QMainWindow)

import sys

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.dial = QDial(Form)
        self.dial.setObjectName(u"dial")
        self.dial.setGeometry(QRect(120, 40, 151, 161))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 270, 62, 19))
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

    def click(self):
        print("Clicked")

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form = QWidget()
        self.ud = Ui_Form()
        self.ud.setupUi(self.form)

        self.setCentralWidget(self.form)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TestMainWindow()
    w.show()
    sys.exit(app.exec())