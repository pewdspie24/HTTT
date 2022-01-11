# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'httt.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 471, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Text")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vn_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.vn_text.setGeometry(QtCore.QRect(50, 170, 361, 81))
        self.vn_text.setObjectName("vn_text")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 140, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.translate_button = QtWidgets.QPushButton(self.centralwidget)
        self.translate_button.setGeometry(QtCore.QRect(50, 290, 361, 41))
        self.translate_button.setObjectName("translate_button")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 370, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.en_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.en_text.setEnabled(True)
        self.en_text.setGeometry(QtCore.QRect(50, 400, 361, 81))
        self.en_text.setReadOnly(True)
        self.en_text.setObjectName("en_text")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(450, 160, 301, 311))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 299, 309))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.table_translate = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.table_translate.setGeometry(QtCore.QRect(-5, 1, 311, 311))
        self.table_translate.setObjectName("table_translate")
        self.table_translate.setColumnCount(4)
        self.table_translate.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(3, item)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "VIETNAMESE-ENGLISH TRANSLATOR"))
        self.label_2.setText(_translate("MainWindow", "Vietnamese Sentence Input"))
        self.translate_button.setText(_translate("MainWindow", "PushButton"))
        self.label_3.setText(_translate("MainWindow", "English Sentence Output"))
        item = self.table_translate.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "c"))
        item = self.table_translate.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "d"))
        item = self.table_translate.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "VN Char"))
        item = self.table_translate.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ENG Char"))
        item = self.table_translate.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Suggested Word"))
        item = self.table_translate.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Word Type"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
