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
        self.widget = QtWidgets.QWidget(ImagesShower)
        self.widget.setGeometry(QtCore.QRect(20, 20, 1061, 671))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.originalGraphicsView = QtWidgets.QGraphicsView(self.widget)
        self.originalGraphicsView.setObjectName("originalGraphicsView")
        self.horizontalLayout.addWidget(self.originalGraphicsView)
        self.resultGraphicsView = QtWidgets.QGraphicsView(self.widget)
        self.resultGraphicsView.setObjectName("resultGraphicsView")
        self.horizontalLayout.addWidget(self.resultGraphicsView)

        self.retranslateUi(ImagesShower)
        QtCore.QMetaObject.connectSlotsByName(ImagesShower)

    def retranslateUi(self, ImagesShower):
        _translate = QtCore.QCoreApplication.translate
        ImagesShower.setWindowTitle(_translate("ImagesShower", "Показ картинок"))

