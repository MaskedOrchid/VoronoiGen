# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'creationdialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

import HomeController

class Ui_CreationView(object):
    def setupUi(self, CreationView):
        if not CreationView.objectName():
            CreationView.setObjectName(u"CreationView")
        CreationView.setEnabled(True)
        CreationView.resize(395, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreationView.sizePolicy().hasHeightForWidth())
        CreationView.setSizePolicy(sizePolicy)
        CreationView.setMaximumSize(QSize(400, 300))
        font = QFont()
        font.setFamilies([u"Merge"])
        CreationView.setFont(font)
        CreationView.setStyleSheet(u"")
        self.buttonBox = QDialogButtonBox(CreationView)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.verticalLayoutWidget = QWidget(CreationView)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 10, 356, 211))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Fuku Catch"])
        font1.setPointSize(20)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QSize(250, 25))
        self.lineEdit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, -1, 50, -1)
        self.horizontalSpacer_8 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_8)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        font2 = QFont()
        font2.setFamilies([u"Merge"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(True)
        self.label_9.setFont(font2)

        self.horizontalLayout_12.addWidget(self.label_9)

        self.lineEdit_9 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_9)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, 50, -1)
        self.horizontalSpacer = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(CreationView)
        self.buttonBox.accepted.connect(CreationView.accept)
        self.buttonBox.rejected.connect(CreationView.reject)

        QMetaObject.connectSlotsByName(CreationView)
    # setupUi

    def retranslateUi(self, CreationView):
        CreationView.setWindowTitle(QCoreApplication.translate("CreationView", u"Create a New Project", None))
        self.label.setText(QCoreApplication.translate("CreationView", u"New Project", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("CreationView", u"Enter New Project Name...", None))
        self.label_9.setText(QCoreApplication.translate("CreationView", u"Canvas Width", None))
        self.label_2.setText(QCoreApplication.translate("CreationView", u"Canvas Height", None))
    # retranslateUi


class CreationDialog(QDialog):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.ui = Ui_CreationView()
        self.ui.setupUi(self)

    def accept(self):

        # Allow controller to handle input logic.
        if self.controller.alterModel(self.ui.lineEdit.text(), self.ui.lineEdit_9.text(), self.ui.lineEdit_2.text()):
            self.controller.initializeMainApp()
            super().accept()
        return


