# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MyWowApp(object):
    def setupUi(self, MyWowApp):
        MyWowApp.setObjectName("MyWowApp")
        MyWowApp.resize(1108, 530)
        self.centralwidget = QtWidgets.QWidget(MyWowApp)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.deleteTaskButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteTaskButton.setObjectName("deleteTaskButton")
        self.verticalLayout.addWidget(self.deleteTaskButton)
        MyWowApp.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MyWowApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1108, 26))
        self.menubar.setObjectName("menubar")
        self.menuAdd_new_task = QtWidgets.QMenu(self.menubar)
        self.menuAdd_new_task.setObjectName("menuAdd_new_task")
        MyWowApp.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MyWowApp)
        self.statusbar.setObjectName("statusbar")
        MyWowApp.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAdd_new_task.menuAction())

        self.retranslateUi(MyWowApp)
        QtCore.QMetaObject.connectSlotsByName(MyWowApp)

    def retranslateUi(self, MyWowApp):
        _translate = QtCore.QCoreApplication.translate
        MyWowApp.setWindowTitle(_translate("MyWowApp", "MyWowApp"))
        self.deleteTaskButton.setText(_translate("MyWowApp", "Delete task"))
        self.menuAdd_new_task.setTitle(_translate("MyWowApp", "Add new task"))


