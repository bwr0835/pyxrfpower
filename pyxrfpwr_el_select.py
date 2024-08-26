# PyXRFPower: Element selection window for azimuthally averaged PSD
# File: pyxrfpower_el_select.py
# Author: B. Roter

# This PyXRFPower window controls the display of elements a user can select when viewing and/or fitting
# azimuthally averaged power spectral densities.

from PyQt6 import QtCore, QtWidgets

class Ui_Form(QtWidgets.QWidget):
    el_select_window_closed = QtCore.pyqtSignal()

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(519, 312)
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 501, 211))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 311, 20))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 270, 501, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def closeEvent(self, ev):
        self.el_select_window_closed.emit()
        
        ev.accept()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Element Selection"))
        self.label.setText(_translate("Form", "Select element(s) for azimuthal PSD viewing and fitting:"))
        self.pushButton.setText(_translate("Form", "Cancel"))
        self.pushButton_2.setText(_translate("Form", "OK"))