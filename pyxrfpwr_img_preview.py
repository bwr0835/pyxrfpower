# PyXRFPower: Image preview window
# File: pyxrfpower_img_preview.py
# Author: B. Roter

# This PyXRFPower window controls the display (i.e. contrast and orientation) of images when previewing them.

from PyQt6 import QtCore, QtWidgets
from pyqtgraph import PlotWidget

import numpy as np, pyqtgraph as pg

class Ui_Form(QtWidgets.QWidget):
    img_preview_window_closed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(837, 599)
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 511, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(parent=self.layoutWidget)
        self.toolButton.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.toolButton, 0, 2, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(parent=self.layoutWidget)
        self.toolButton_2.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout_2.addWidget(self.toolButton_2, 0, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_4.setGeometry(QtCore.QRect(550, 530, 111, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.widget = PlotWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(20, 80, 511, 514))
        self.widget.setObjectName("widget")
        self.pushButton_5 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_5.setGeometry(QtCore.QRect(550, 560, 281, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.layoutWidget_2 = QtWidgets.QWidget(parent=Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(550, 200, 190, 111))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox = QtWidgets.QCheckBox(parent=self.layoutWidget_2)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_3.addWidget(self.checkBox, 2, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 1, 0, 1, 2)
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.layoutWidget_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_3.addWidget(self.checkBox_2, 3, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 2)
        self.layoutWidget_3 = QtWidgets.QWidget(parent=Form)
        self.layoutWidget_3.setGeometry(QtCore.QRect(550, 360, 171, 85))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget_3)
        self.doubleSpinBox.setFrame(True)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMinimum(0.001)
        self.doubleSpinBox.setMaximum(10.0)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_4.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget_3)
        self.doubleSpinBox_2.setFrame(True)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMaximum(1.0)
        self.doubleSpinBox_2.setSingleStep(0.1)
        self.doubleSpinBox_2.setProperty("value", 0.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout_4.addWidget(self.doubleSpinBox_2, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 2, 0, 1, 1)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget_3)
        self.doubleSpinBox_3.setFrame(True)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMaximum(1.0)
        self.doubleSpinBox_3.setSingleStep(0.1)
        self.doubleSpinBox_3.setProperty("value", 1.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout_4.addWidget(self.doubleSpinBox_3, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(550, 170, 121, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(550, 330, 101, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 711, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 450, 111, 32))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.toolButton.setDisabled(True)

        self.gamma_char = "<i>\u03B3</i>"

    def update_img_contrast_values(self, gamma, lower_quantile, upper_quantile):
        self.doubleSpinBox.setValue(gamma)
        self.doubleSpinBox_2.setValue(lower_quantile)
        self.doubleSpinBox_3.setValue(upper_quantile)

        self.show()

        return

    def update_img_preview(self, element, img, gamma, lower_quantile, upper_quantile, dx, dy):
        corrected_img_data = img.T
        corrected_img_data = np.flip(corrected_img_data, axis = 1)

        self.widget.plotItem.clear()

        elemental_img = pg.ImageItem(corrected_img_data)
        
        color_map = pg.colormap.getFromMatplotlib('hot')
        
        elemental_img.setColorMap(colorMap = color_map)

        self.widget.plotItem.getViewBox().setAspectLocked(True, ratio = dx/dy)

        self.widget.addItem(elemental_img)

        if gamma == int(gamma):
            gamma = int(gamma)
        
        if lower_quantile == int(lower_quantile):
            lower_quantile = int(lower_quantile)
        
        if upper_quantile == int(upper_quantile):
            upper_quantile = int(upper_quantile)

        title = "Elemental Image of " + str(element, 'utf-8') + " (" + self.gamma_char + " = " + str(gamma) + ", LQ = " + str(lower_quantile) + ", UQ = " + str(upper_quantile) + ")"

        self.widget.plotItem.hideAxis('bottom')
        self.widget.plotItem.hideAxis('left')
        self.widget.plotItem.setTitle(title, color = 'w')

        return

    def compare_quantiles(self):
        lower_quantile = self.doubleSpinBox_2.value()
        upper_quantile = self.doubleSpinBox_3.value()

        if lower_quantile >= upper_quantile:
            self.pushButton_3.setDisabled(True)
            self.pushButton_5.setDisabled(True)
        
        else:
            self.pushButton_3.setDisabled(False)
            self.pushButton_5.setDisabled(False)

        return
    
    def compare_quantile_to_original(self, updated_quantile, orig_quantile):
        if updated_quantile == orig_quantile:
            self.pushButton_3.setDisabled(True)
            self.pushButton_5.setDisabled(False)
        
        else:
            self.pushButton_3.setDisabled(False)
            self.pushButton_5.setDisabled(True)

    def closeEvent(self, ev):
        self.img_preview_window_closed.emit()

        ev.accept()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Image Preview"))
        self.label_2.setText(_translate("Form", "Element:"))
        self.toolButton.setText(_translate("Form", "..."))
        self.toolButton_2.setText(_translate("Form", "..."))
        self.pushButton_4.setText(_translate("Form", "Cancel"))
        self.pushButton_5.setText(_translate("Form", "Calculate Power Spectral Density (PSD)"))
        self.checkBox.setText(_translate("Form", "Flip Horizontally"))
        self.pushButton_2.setText(_translate("Form", "Rotate Clockwise"))
        self.checkBox_2.setText(_translate("Form", "Flip Vertically"))
        self.pushButton.setText(_translate("Form", "Rotate Counterclockwise"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p align=\"right\">Lower Quantile:</p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p align=\"right\">Gamma:</p></body></html>"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p align=\"right\">Upper Quantile:</p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:700; text-decoration: underline;\">Image Orientation</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:700; text-decoration: underline;\">Image Contrast</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p>Preview images (NOTES: Only image orientation details are applied to calculations, and images do not show padding).</p></body></html>"))
        self.pushButton_3.setText(_translate("Form", "Apply"))