# PyXRFPower: Elemental Image and 2D PSD Viewing Window
# File: pyxrfpwr_img_2dpsd.py
# Author: B. Roter

# This PyXRFPower window controls the display of elemental images and 2D power spectral densities after previewing the original images.

from PyQt6 import QtCore, QtWidgets
from pyqtgraph import PlotWidget

import numpy as np, pyqtgraph as pg

class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(1077, 590)
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 511, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
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
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(940, 20, 111, 32))
        self.pushButton.setObjectName("pushButton")
        self.widget = PlotWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(20, 60, 514, 514))
        self.widget.setObjectName("widget")
        self.widget_2 = PlotWidget(parent=Form)
        self.widget_2.setGeometry(QtCore.QRect(540, 60, 514, 514))
        self.widget_2.setObjectName("widget_2")
        
        self.sigma_char = "<i>\u03C3</i>"
        self.alpha_char = "<i>\u03B1</i>"
        self.gamma_char = "<i>\u03B3</i>"

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_2d_plots(self, element, image, psd_output, gamma, lower_quantile, upper_quantile, dx, dy, sigma = None, alpha = None):
        img = image[element]

        if self.circular_beam_checked:
            psd = psd_output[element][1]
        
        else:
            psd = psd_output[element][2]

        idx_nan = np.where(psd == 0) # Dead pixels
        psd[idx_nan] = float("nan")

        # Correct image, 2D PSD orientations since PyQtGraph displays them incorrectly
        
        corrected_img_data = img.T
        corrected_img_data = np.flip(corrected_img_data, axis = 1)
        
        corrected_2d_psd_data = psd.T
        corrected_2d_psd_data = np.flip(corrected_2d_psd_data, axis = 1)
        
        self.widget.plotItem.clear()
        self.widget_2.plotItem.clear()
        
        elemental_img = pg.ImageItem(corrected_img_data)
        psd_img = pg.ImageItem(10*np.log10(corrected_2d_psd_data))

        color_map = pg.colormap.getFromMatplotlib('hot')
        
        elemental_img.setColorMap(colorMap = color_map)
        psd_img.setColorMap(colorMap = color_map)
        
        # Fix aspect ratios so entire images are displayed

        self.widget.plotItem.getViewBox().setAspectLocked(True, ratio = dx/dy)
        self.widget_2.plotItem.getViewBox().setAspectLocked(True, ratio = dy/dx)

        self.widget.addItem(elemental_img)
        self.widget_2.addItem(psd_img)

        self.widget.plotItem.hideAxis('bottom')
        self.widget.plotItem.hideAxis('left')

        if gamma == int(gamma):
            gamma = int(gamma)
        
        if lower_quantile == int(lower_quantile):
            lower_quantile = int(lower_quantile)
        
        if upper_quantile == int(upper_quantile):
            upper_quantile = int(upper_quantile)

        self.widget.plotItem.setTitle("Elemental Image of " + str(element, 'utf-8') + " (" + self.gamma_char + " = " + str(gamma) + ", LQ = " + str(lower_quantile) + ", UQ = " + str(upper_quantile) + ")", color = 'w')

        if sigma is not None and alpha is not None:
            if alpha == int(alpha):
                alpha = int(alpha)
            
            self.widget_2.plotItem.setTitle("10 log(2D PSD): " + str(element, 'utf-8') + " (" + self.sigma_char + " = " + str(sigma) + ", " + self.alpha_char + " = " + str(alpha) + ")", color = 'w')
        
        else:
            self.widget_2.plotItem.setTitle("10 log(2D PSD): " + str(element, 'utf-8'))
        
        self.widget_2.plotItem.hideAxis('bottom')
        self.widget_2.plotItem.hideAxis('left')
        
        self.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Elemental Images and 2D PSD Plots"))
        self.label.setText(_translate("Form", "Element:"))
        self.toolButton.setText(_translate("Form", "..."))
        self.toolButton_2.setText(_translate("Form", "..."))
        self.pushButton.setText(_translate("Form", "Batch Export"))