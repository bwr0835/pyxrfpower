# PyXRFPower: Change pixel dimension window
# File: pyxrfpwr_change_pixel_dims.py
# Author: B. Roter

# This PyXRFPower window controls the display of pixel sizes when a user desires to modify them.

from PyQt6 import QtCore, QtWidgets
from pyxrfpwr_math_fxns import round_correct as rc

class Ui_Form(QtWidgets.QWidget):
    pixel_dim_window_closed = QtCore.pyqtSignal()
   
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(349, 143)
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 40, 269, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget)
        self.doubleSpinBox.setDecimals(7)
        self.doubleSpinBox.setMaximum(10000000.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget)
        self.doubleSpinBox_2.setDecimals(7)
        self.doubleSpinBox_2.setMaximum(10000000.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout_2.addWidget(self.doubleSpinBox_2, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 163, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 110, 163, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.ndec = self.doubleSpinBox.decimals()

    def update_pixel_dim(self, axis, length):
        if axis == 'x':
            self.doubleSpinBox.setValue(rc(length, ndec = self.ndec))
        
        elif axis == 'y':
            self.doubleSpinBox_2.setValue(rc(length, ndec = self.ndec))

    def closeEvent(self, ev):
        self.pixel_dim_window_closed.emit()

        ev.accept()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Pixel Dimensions"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"right\">Pixel Height (&mu;m):</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"right\">Pixel Width (&mu;m):</p></body></html>"))
        self.pushButton.setText(_translate("Form", "Cancel"))
        self.pushButton_2.setText(_translate("Form", "OK"))
        self.label.setText(_translate("Form", "Change pixel dimensions."))