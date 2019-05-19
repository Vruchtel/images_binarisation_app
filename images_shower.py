# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'images_shower.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImagesShower(object):
    def setupUi(self, ImagesShower):
        ImagesShower.setObjectName("ImagesShower")
        ImagesShower.resize(1103, 708)
        self.layoutWidget = QtWidgets.QWidget(ImagesShower)
        self.layoutWidget.setGeometry(QtCore.QRect(19, 19, 1061, 671))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.originalImageFrame = QtWidgets.QFrame(self.layoutWidget)
        self.originalImageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.originalImageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.originalImageFrame.setObjectName("originalImageFrame")
        self.horizontalLayout.addWidget(self.originalImageFrame)
        self.resultImageFrame = QtWidgets.QFrame(self.layoutWidget)
        self.resultImageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.resultImageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resultImageFrame.setObjectName("resultImageFrame")
        self.horizontalLayout.addWidget(self.resultImageFrame)

        self.retranslateUi(ImagesShower)
        QtCore.QMetaObject.connectSlotsByName(ImagesShower)

    def retranslateUi(self, ImagesShower):
        _translate = QtCore.QCoreApplication.translate
        ImagesShower.setWindowTitle(_translate("ImagesShower", "Images showing"))

