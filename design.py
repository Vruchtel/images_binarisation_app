# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyWowApp(object):
    def setupUi(self, MyWowApp):
        MyWowApp.setObjectName("MyWowApp")
        MyWowApp.resize(1108, 521)
        self.centralwidget = QtWidgets.QWidget(MyWowApp)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addTaskButton = QtWidgets.QPushButton(self.centralwidget)
        self.addTaskButton.setObjectName("addTaskButton")
        self.horizontalLayout_2.addWidget(self.addTaskButton)
        self.saveAllResultsButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAllResultsButton.setObjectName("saveAllResultsButton")
        self.horizontalLayout_2.addWidget(self.saveAllResultsButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tasksListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.tasksListWidget.setObjectName("tasksListWidget")
        self.horizontalLayout.addWidget(self.tasksListWidget)
        self.processListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.processListWidget.setObjectName("processListWidget")
        self.horizontalLayout.addWidget(self.processListWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MyWowApp.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MyWowApp)
        self.statusbar.setObjectName("statusbar")
        MyWowApp.setStatusBar(self.statusbar)

        self.retranslateUi(MyWowApp)
        QtCore.QMetaObject.connectSlotsByName(MyWowApp)

    def retranslateUi(self, MyWowApp):
        _translate = QtCore.QCoreApplication.translate
        MyWowApp.setWindowTitle(_translate("MyWowApp", "BinarisationApp"))
        self.addTaskButton.setText(_translate("MyWowApp", "Add new task"))
        self.saveAllResultsButton.setText(_translate("MyWowApp", "Save all results"))

