# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import main
from functools import partial


myModule = main.MainProcess()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 598) #800, 598 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 571, 61))
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
        self.scrollArea.setGeometry(QtCore.QRect(450, 160, 411, 311))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 411, 309))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.table_translate = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.table_translate.setGeometry(QtCore.QRect(0, 0, 411, 309))
        self.table_translate.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_translate.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_translate.setObjectName("table_translate")
        self.table_translate.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_translate.setHorizontalHeaderItem(3, item)
        header = self.table_translate.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
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
        self.translate_button.setText(_translate("MainWindow", "Translate!"))
        self.label_3.setText(_translate("MainWindow", "English Sentence Output"))
        item = self.table_translate.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "VN Char"))
        item = self.table_translate.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ENG Char"))
        item = self.table_translate.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Word Type"))
        item = self.table_translate.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Suggested Word"))
        self.backend()
    
    def backend(self):
        self.translate_button.clicked.connect(self.translate)
    
    def translate(self):
        sentence = self.vn_text.toPlainText()
        print(sentence)
        vi_sentence, eng_sentence, result, tense, self.list_chars = myModule.process(sentence)
        self.en_text.setPlainText(result)
        print(eng_sentence)
        print(tense)
        print(self.list_chars)
        self.table_translate.setRowCount(len(self.list_chars))
        combo_list = [] 
        for idx, i in enumerate(self.list_chars):   
            self.table_translate.setItem(idx, 0, QtWidgets.QTableWidgetItem(i.get('word')))
            types = []
            try:
                for it in i.get('type'):
                    types.append(it)
            except Exception:
                types.append('unknown')
            combo = QtWidgets.QComboBox()
            combo.addItems(types)
            combo.currentTextChanged.connect(partial(self.showText,idx))
            combo_list.append(combo)
            self.showText(idx, types[0])
            self.table_translate.setCellWidget(idx, 2, combo_list[idx])
            if eng_sentence[idx][0][0] != None:
                self.table_translate.setItem(idx, 1, QtWidgets.QTableWidgetItem(eng_sentence[idx][0][0]))

    def showText(self, idx, value):
        res_txt = ''
        res = {}
        trans_idx = 0
        try:
            types = self.list_chars[idx].get('type')
            for index, type1 in enumerate(types):
                if 'trans'+str(trans_idx) in self.list_chars[idx]:
                    res.update({type1:'trans'+str(trans_idx)})
                else:
                    trans_idx+=1
                    res.update({type1:'trans'+str(trans_idx)})
                trans_idx+=1
            # print(idx)
            trans_name = res.get(value)
            for index, i in enumerate(self.list_chars[idx].get(trans_name)):
                res_txt += i
                if index != len(self.list_chars[idx].get(trans_name))-1:
                    res_txt += '\n'
        except Exception:
            for keys in self.list_chars[idx]:
                if keys[0:4] == 'trans':
                    print(keys)
                    print(self.list_chars[idx])
                    list_texts = self.list_chars[idx].get(keys)
                    for text in list_texts:
                        res_txt += text
                        if index != len(self.list_chars[idx].get(keys))-1:
                            res_txt += '\n'
        self.table_translate.setItem(idx, 3, QtWidgets.QTableWidgetItem(res_txt))
        self.table_translate.resizeRowsToContents()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
