# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Load_Main_EQP_Local_ver1_chg_size.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1249, 859) #여기
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.push_e_back = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_e_back.sizePolicy().hasHeightForWidth())
        self.push_e_back.setSizePolicy(sizePolicy)
        self.push_e_back.setMaximumSize(QtCore.QSize(40, 16777215))
        self.push_e_back.setObjectName("push_e_back")
        self.horizontalLayout_5.addWidget(self.push_e_back)
        self.push_e_foward = QtWidgets.QPushButton(self.groupBox)
        self.push_e_foward.setMaximumSize(QtCore.QSize(40, 16777215))
        self.push_e_foward.setObjectName("push_e_foward")
        self.horizontalLayout_5.addWidget(self.push_e_foward)
        self.push_e_new = QtWidgets.QPushButton(self.groupBox)
        self.push_e_new.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_e_new.setObjectName("push_e_new")
        self.horizontalLayout_5.addWidget(self.push_e_new)
        self.push_e_del = QtWidgets.QPushButton(self.groupBox)
        self.push_e_del.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_e_del.setObjectName("push_e_del")
        self.horizontalLayout_5.addWidget(self.push_e_del)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.list_e_path5 = QtWidgets.QListWidget(self.groupBox)
        self.list_e_path5.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_e_path5.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path5.setObjectName("list_e_path5")
        self.verticalLayout_9.addWidget(self.list_e_path5)
        self.gridLayout.addLayout(self.verticalLayout_9, 1, 3, 3, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.list_e_path3 = QtWidgets.QListWidget(self.groupBox)
        self.list_e_path3.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_e_path3.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path3.setObjectName("list_e_path3")
        self.verticalLayout_7.addWidget(self.list_e_path3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.list_e_path4 = QtWidgets.QListWidget(self.groupBox)
        self.list_e_path4.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_e_path4.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path4.setObjectName("list_e_path4")
        self.verticalLayout_8.addWidget(self.list_e_path4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_8)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.line_e_cur_path = QtWidgets.QLineEdit(self.groupBox)
        self.line_e_cur_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_e_cur_path.setObjectName("line_e_cur_path")
        self.verticalLayout_4.addWidget(self.line_e_cur_path)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(100, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list_e_line = QtWidgets.QListWidget(self.groupBox)
        self.list_e_line.setMaximumSize(QtCore.QSize(100, 200)) #여기
        self.list_e_line.setObjectName("list_e_line")
        self.verticalLayout.addWidget(self.list_e_line)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setMaximumSize(QtCore.QSize(100, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_12.addWidget(self.label_12)
        self.list_e_eqp = QtWidgets.QListWidget(self.groupBox)
        self.list_e_eqp.setMaximumSize(QtCore.QSize(100, 200)) #여기
        self.list_e_eqp.setObjectName("list_e_eqp")
        self.verticalLayout_12.addWidget(self.list_e_eqp)
        self.horizontalLayout.addLayout(self.verticalLayout_12)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(100, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.list_e_drive = QtWidgets.QListWidget(self.groupBox)
        self.list_e_drive.setMaximumSize(QtCore.QSize(100, 200)) #여기
        self.list_e_drive.setObjectName("list_e_drive")
        self.verticalLayout_2.addWidget(self.list_e_drive)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMaximumSize(QtCore.QSize(100, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.list_e_ext = QtWidgets.QListWidget(self.groupBox)
        self.list_e_ext.setMaximumSize(QtCore.QSize(100, 200)) #여기
        self.list_e_ext.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_ext.setObjectName("list_e_ext")
        self.verticalLayout_3.addWidget(self.list_e_ext)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.push_eqp_info = QtWidgets.QPushButton(self.groupBox)
        self.push_eqp_info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_eqp_info.setObjectName("push_eqp_info")
        self.verticalLayout_13.addWidget(self.push_eqp_info)
        self.push_ext_info = QtWidgets.QPushButton(self.groupBox)
        self.push_ext_info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_ext_info.setObjectName("push_ext_info")
        self.verticalLayout_13.addWidget(self.push_ext_info)
        self.horizontalLayout.addLayout(self.verticalLayout_13)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.list_e_path1 = QtWidgets.QListWidget(self.groupBox)
        self.list_e_path1.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_e_path1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path1.setObjectName("list_e_path1")
        self.verticalLayout_5.addWidget(self.list_e_path1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.list_e_path2 = QtWidgets.QListWidget(self.groupBox)
        self.list_e_path2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_e_path2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path2.setObjectName("list_e_path2")
        self.verticalLayout_6.addWidget(self.list_e_path2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.push_manual = QtWidgets.QPushButton(self.groupBox)
        self.push_manual.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_manual.setObjectName("push_manual")
        self.verticalLayout_17.addWidget(self.push_manual)
        self.push_hotkey = QtWidgets.QPushButton(self.groupBox)
        self.push_hotkey.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_hotkey.setObjectName("push_hotkey")
        self.verticalLayout_17.addWidget(self.push_hotkey)
        self.horizontalLayout_9.addLayout(self.verticalLayout_17)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_status = QtWidgets.QLabel(self.groupBox_3)
        self.label_status.setMinimumSize(QtCore.QSize(0, 0))
        self.label_status.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout_7.addWidget(self.label_status)
        self.label_image = QtWidgets.QLabel(self.groupBox_3)
        self.label_image.setMinimumSize(QtCore.QSize(0, 0))
        self.label_image.setMaximumSize(QtCore.QSize(800, 16777215))
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName("label_image")
        self.horizontalLayout_7.addWidget(self.label_image)
        self.horizontalLayout_9.addWidget(self.groupBox_3)
        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 30)
        self.gridLayout.setRowStretch(0, 4) #여기
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 7)
        self.gridLayout.setRowStretch(3, 7)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.list_c_path = QtWidgets.QListWidget(self.groupBox_2)
        self.list_c_path.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.list_c_path.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_c_path.setObjectName("list_c_path")
        self.gridLayout_2.addWidget(self.list_c_path, 3, 0, 1, 2)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.line_c_cur_path = QtWidgets.QLineEdit(self.groupBox_2)
        self.line_c_cur_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_c_cur_path.setObjectName("line_c_cur_path")
        self.verticalLayout_11.addWidget(self.line_c_cur_path)
        self.gridLayout_2.addLayout(self.verticalLayout_11, 1, 0, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.push_c_back = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_back.setMaximumSize(QtCore.QSize(50, 16777215))
        self.push_c_back.setObjectName("push_c_back")
        self.horizontalLayout_6.addWidget(self.push_c_back)
        self.push_c_foward = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_foward.setMaximumSize(QtCore.QSize(50, 16777215))
        self.push_c_foward.setObjectName("push_c_foward")
        self.horizontalLayout_6.addWidget(self.push_c_foward)
        self.push_c_new = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_new.setObjectName("push_c_new")
        self.horizontalLayout_6.addWidget(self.push_c_new)
        self.push_c_del = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_del.setObjectName("push_c_del")
        self.horizontalLayout_6.addWidget(self.push_c_del)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 2)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.list_c_drive = QtWidgets.QListWidget(self.groupBox_2)
        self.list_c_drive.setMaximumSize(QtCore.QSize(100, 16777215))
        self.list_c_drive.setObjectName("list_c_drive")
        self.verticalLayout_10.addWidget(self.list_c_drive)
        self.gridLayout_2.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.label_free = QtWidgets.QLabel(self.groupBox_2)
        self.label_free.setAlignment(QtCore.Qt.AlignCenter)
        self.label_free.setObjectName("label_free")
        self.gridLayout_2.addWidget(self.label_free, 0, 1, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setRowStretch(3, 13)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 4)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1249, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "EQP_Local"))
        self.groupBox.setTitle(_translate("mainWindow", "EQP "))
        self.label_9.setText(_translate("mainWindow", "Path5"))
        self.push_e_back.setText(_translate("mainWindow", "◀"))
        self.push_e_foward.setText(_translate("mainWindow", "▶"))
        self.push_e_new.setText(_translate("mainWindow", "새폴더(ctrl+n)"))
        self.push_e_del.setText(_translate("mainWindow", "삭제(ctrl+d)"))
        self.label_7.setText(_translate("mainWindow", "Path3"))
        self.label_8.setText(_translate("mainWindow", "Path4"))
        self.label_10.setText(_translate("mainWindow", "현재 경로"))
        self.label.setText(_translate("mainWindow", "Line"))
        self.label_12.setText(_translate("mainWindow", "EQP"))
        self.label_2.setText(_translate("mainWindow", "Drive"))
        self.label_3.setText(_translate("mainWindow", "확장자"))
        self.push_eqp_info.setText(_translate("mainWindow", "EQP 등록"))
        self.push_ext_info.setText(_translate("mainWindow", "확장자 등록"))
        self.label_5.setText(_translate("mainWindow", "Path1"))
        self.label_6.setText(_translate("mainWindow", "Path2"))
        self.push_manual.setText(_translate("mainWindow", "사용법"))
        self.push_hotkey.setText(_translate("mainWindow", "단축키"))
        self.groupBox_3.setTitle(_translate("mainWindow", "Load Status"))
        self.label_status.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">IDLE</span></p></body></html>"))
        self.label_image.setText(_translate("mainWindow", "image"))
        self.groupBox_2.setTitle(_translate("mainWindow", "Local"))
        self.label_11.setText(_translate("mainWindow", "현재 경로"))
        self.push_c_back.setText(_translate("mainWindow", "◀"))
        self.push_c_foward.setText(_translate("mainWindow", "▶"))
        self.push_c_new.setText(_translate("mainWindow", "새폴더(n)"))
        self.push_c_del.setText(_translate("mainWindow", "삭제(del.)"))
        self.label_4.setText(_translate("mainWindow", "Drive"))
        self.label_free.setText(_translate("mainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

