# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selector_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Converter_dialog_base(object):
    def setupUi(self, Converter_dialog_base):
        Converter_dialog_base.setObjectName("Converter_dialog_base")
        Converter_dialog_base.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Converter_dialog_base)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnLoadXML = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnLoadXML.setObjectName("btnLoadXML")
        self.horizontalLayout.addWidget(self.btnLoadXML)
        self.btnConvert = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnConvert.setObjectName("btnConvert")
        self.horizontalLayout.addWidget(self.btnConvert)
        self.verticalLayout.addLayout(self.horizontalLayout)
        Converter_dialog_base.setCentralWidget(self.centralwidget)

        self.retranslateUi(Converter_dialog_base)
        QtCore.QMetaObject.connectSlotsByName(Converter_dialog_base)

    def retranslateUi(self, Converter_dialog_base):
        _translate = QtCore.QCoreApplication.translate
        Converter_dialog_base.setWindowTitle(_translate("Converter_dialog_base", "Converter_dialog_base"))
        self.btnLoadXML.setText(_translate("Converter_dialog_base", "Загрузить XML"))
        self.btnConvert.setText(_translate("Converter_dialog_base", "Преобразовать в GeoJSON"))