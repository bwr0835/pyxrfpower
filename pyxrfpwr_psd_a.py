# PyXRFPower: Azimuthal PSD window
# File: pyxrfpower_psd_a.py
# Author: B. Roter

# This PyXRFPower window controls the display of azimuthally averaged power spectral densities for both iso- and anisotropic X-ray beams

from PyQt6 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
from pyxrfpwr_math_fxns import round_correct as rc

import numpy as np, pyqtgraph as pg

class Ui_Form(QtWidgets.QWidget):
    psd_a_window_closed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(847, 722)
        
        pg.setConfigOption('foreground', 'k')
        
        self.widget = PlotWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(10, 50, 821, 481))
        self.widget.setObjectName("widget")
        self.widget.setBackground('w')
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 391, 41))
        self.label.setText("")
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 540, 821, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.legend = self.widget.plotItem.addLegend()
        self.legend.setParentItem(p = self.widget.plotItem)
        self.legend.setOffset((0, -350))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.layoutWidget_2 = QtWidgets.QWidget(parent=Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(460, 580, 371, 61))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.pushButton_8 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_8.setGeometry(QtCore.QRect(730, 680, 100, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.layoutWidget1 = QtWidgets.QWidget(parent=Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 610, 441, 32))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.layoutWidget2 = QtWidgets.QWidget(parent=Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 680, 551, 33))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.layoutWidget2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMinimum(1)
        self.doubleSpinBox.setMaximum(100000)
        self.gridLayout.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=Form)
        self.label_7.setGeometry(QtCore.QRect(450, 10, 381, 41))
        self.label_7.setText("")
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")

        self.x_enabled = 0
        
        self.delta = "<i>\u03B4</i>"
        self.mu = "\u03BC"
        
        r = [255, 0, 0] # Red
        o = [255, 128, 0] # Orange
        g = [0, 200, 0] # Green
        b = [0, 0, 255] # Blue
        ind = [75, 0, 130] # Indigo
        v = [143, 0, 255] # Violet
        br = [102, 51, 0] # Brown
        p = [255, 0, 127] # Pink
        t = [0, 204, 204] # Turquoise
        k = [0, 0, 0] # Black

        brightness_amplification = 75

        self.color_array = np.array([r, o, g, b, ind, v, br, p, t, k])
        self.color_array_lighter = np.array([r, o, g, b, ind, v, br, p, t, k])
        
        for color_index in range(len(self.color_array_lighter)):
            self.color_array_lighter[color_index] += brightness_amplification

            above_8_bit_color_index = np.where(self.color_array_lighter[color_index] > 255)

            self.color_array_lighter[color_index][above_8_bit_color_index] = 255

        self.linear = "Linear"

        self.lr = pg.LinearRegionItem()
        self.vb = self.widget.plotItem.getViewBox()
        
        self.psd_a_loglog_shaded = None
        self.psd_a_x_loglog_shaded = None
        self.psd_a_y_loglog_shaded = None
    
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_psd_a_plot(self, selected_elements, psd_output, n_ur, lin_fit_output = None, hor_fit_output = None, 
                          res_output = None): # Note: Can only plot up to seven UNIQUELY-COLORED curves
        
        self.widget.plotItem.clear()
        self.legend.clear()
       
        psd_a_min_array = np.zeros((len(selected_elements)))
        psd_a_max_array = np.zeros((len(selected_elements)))

        element_index = 0
        ur_element_index = 1
        legend_flag = 1
        offset = 0.04
        
        for j in range(len(selected_elements)):
            element = selected_elements[j]
            
            psd_a_element = psd_output[element][2]

            psd_a_min_array[j] = np.min(psd_a_element)
            psd_a_max_array[j] = np.max(psd_a_element[1:])
        
        psd_a_min = np.min(psd_a_min_array)
        psd_a_max = np.max(psd_a_max_array)

        psd_a_min_log = np.log10(psd_a_min)
        psd_a_max_log = np.log10(psd_a_max)

        if np.abs(psd_a_min_log) == np.Inf: # Dead pixels
            psd_a_min_log = -1e8
        
        if np.abs(psd_a_max_log) == np.Inf: # Dead pixels
            psd_a_max_log = -1e8

        for element in selected_elements:
            color_index = element_index % len(self.color_array)
            
            selected_color = self.color_array[int(color_index)]

            ur_element = psd_output[element][0]
            psd_a_element = psd_output[element][2]

            pen = pg.mkPen(selected_color, width = 3)

            psd_a_loglog = pg.PlotDataItem(ur_element[1:], psd_a_element[1:], pen = pen)

            if ~self.plot_both_fits_enabled:
                if lin_fit_output is not None and lin_fit_output.get(element) is not None:
                    pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashLine)
                    
                    psd_a_lin_fit = lin_fit_output[element][0]

                    psd_a_lin_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_lin_fit, pen = pen)

                    self.widget.addItem(psd_a_lin_fit_loglog)

                if hor_fit_output is not None and hor_fit_output.get(element) is not None:
                    pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                    
                    psd_a_hor_fit = hor_fit_output[element][0]
                    
                    psd_a_hor_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_hor_fit, pen = pen)

                    self.widget.addItem(psd_a_hor_fit_loglog)
            
            else:
                psd_a_lin_fit = lin_fit_output[element][0]
                psd_a_hor_fit = hor_fit_output[element][0]

                pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashLine)
                psd_a_lin_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_lin_fit, pen = pen)

                pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                psd_a_hor_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_hor_fit, pen = pen)

                self.widget.addItem(psd_a_lin_fit_loglog)
                self.widget.addItem(psd_a_hor_fit_loglog)

            element_text = pg.TextItem("", **{'color': selected_color})

            element_text.setHtml(str(element, 'utf-8'))

            self.widget.addItem(psd_a_loglog)
            self.widget.addItem(element_text)

            element_text.setPos(offset + np.log10(ur_element[ur_element_index]), offset + np.log10(psd_a_element[ur_element_index + 1]))

            if res_output is not None and res_output.get(element) is not None and self.plot_both_fits_enabled:
                psd_a_cutoff = res_output[element][0]
                ur_cutoff = res_output[element][1]
                dr_hp = res_output[element][2]
                
                pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashLine)
                psd_a_lin_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_lin_fit, pen = pen)

                pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                psd_a_hor_fit_loglog = pg.PlotDataItem(ur_element[1:], psd_a_hor_fit, pen = pen)

                self.widget.addItem(psd_a_lin_fit_loglog)
                self.widget.addItem(psd_a_hor_fit_loglog)
                
                symbolPen = pg.mkPen(selected_color)
                symbolBrush = pg.mkBrush(selected_color)

                psd_a_cutoff_point_loglog = pg.PlotDataItem([ur_cutoff], [psd_a_cutoff], pen = None, symbol = 'o', symbolPen = symbolPen, 
                                                          symbolBrush = symbolBrush)
                
                pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashDotLine)

                ur_cutoff_vert_line = pg.PlotDataItem([ur_cutoff, ur_cutoff], [10**psd_a_min_log, psd_a_cutoff], pen = pen)

                res_param_text = pg.TextItem("", **{'color': selected_color})
                res_param_text.setHtml(str(rc(ur_cutoff, ndec = 7)) + " " + self.mu + "m<sup>-1</sup> (" 
                                        + str(rc(dr_hp, ndec = 7)) + " " + self.mu + "m)")

                self.widget.addItem(psd_a_cutoff_point_loglog)
                self.widget.addItem(ur_cutoff_vert_line)
                self.widget.addItem(res_param_text)

                res_param_text.setPos(offset + np.log10(ur_cutoff), offset + np.log10(psd_a_cutoff))

                if legend_flag:
                    self.legend.addItem(psd_a_loglog, "Measured Data")
                    self.legend.addItem(psd_a_lin_fit_loglog, "Data Trend Fit")
                    self.legend.addItem(psd_a_hor_fit_loglog, "Noise Floor Fit")
                    self.legend.addItem(psd_a_cutoff_point_loglog, "<i>u</i><sub>cutoff</sub> (" + self.delta + "<sub>hp</sub>)")

                    legend_flag = 0
            
            ur_element_index += 1
            element_index += 1

        self.widget.setLogMode(True, True)
        self.widget.setXRange(np.log10(ur_element[1]), np.log10(ur_element[-1]), padding = 0)
        self.widget.setYRange(psd_a_min_log, 0.05 + psd_a_max_log, padding = 0)
        self.widget.plotItem.setTitle("<i>S</i>(<i>u<sub>r</sub></i>) v. <i>u<sub>r</sub></i> (<i>n</i><sub><i>u<sub>r</sub></i></sub> = " + str(n_ur) + ")")
        self.widget.plotItem.setLabel('left', "<i>S</i>(<i>u<sub>r</sub></i>)")
        self.widget.plotItem.setLabel('bottom', "<i>u<sub>r</sub></i> (" + self.mu + "m<sup>-1</sup>)")
        self.widget.plotItem.showGrid(True, True, alpha = 1)
        
        self.show()

        return

    def update_psd_a_plot_xy(self, selected_elements, psd_output, n_ur, x_enabled, lin_fit_x_output = None, lin_fit_y_output = None, hor_fit_x_output = None, hor_fit_y_output = None, 
                             res_x_output = None, res_y_output = None): # Note: Can only plot up to seven UNIQUELY-COLORED curves
        
        self.widget.plotItem.clear()
        self.legend.clear()

        ur_x_min_array = np.zeros((len(selected_elements)))
        ur_y_min_array = np.zeros((len(selected_elements)))

        ur_x_max_array = np.zeros((len(selected_elements)))
        ur_y_max_array = np.zeros((len(selected_elements)))

        psd_a_x_min_array = np.zeros((len(selected_elements)))
        psd_a_x_max_array = np.zeros((len(selected_elements)))
        psd_a_y_min_array = np.zeros((len(selected_elements)))
        psd_a_y_max_array = np.zeros((len(selected_elements)))

        element_index = 0
        ur_element_index = 1
        legend_flag = 1
        offset = 0.04
        
        for j in range(len(selected_elements)):
            element = selected_elements[j]
            
            ur_x_element = psd_output[element][0]
            ur_y_element = psd_output[element][1]

            psd_a_x_element = psd_output[element][3]
            psd_a_y_element = psd_output[element][4]

            ur_x_min_array[j] = ur_x_element[1]
            ur_y_min_array[j] = ur_y_element[1]
            
            ur_x_max_array[j] = np.max(ur_x_element[1:])
            ur_y_max_array[j] = np.max(ur_y_element[1:])
            
            psd_a_x_min_array[j] = np.min(psd_a_x_element)
            psd_a_y_min_array[j] = np.min(psd_a_y_element[1:])
            
            psd_a_x_max_array[j] = np.max(psd_a_x_element[1:])
            psd_a_y_max_array[j] = np.max(psd_a_y_element[1:])
    
        ur_x_min = np.min(ur_x_min_array)
        ur_y_min = np.min(ur_y_min_array)
        
        ur_x_max = np.max(ur_x_max_array)
        ur_y_max = np.max(ur_y_max_array)

        psd_a_x_min = np.min(psd_a_x_min_array)
        psd_a_y_min = np.min(psd_a_y_min_array)
        
        psd_a_x_max = np.max(psd_a_x_max_array)
        psd_a_y_max = np.max(psd_a_y_max_array)

        ur_min = np.min([ur_x_min, ur_y_min])
        ur_max = np.max([ur_x_max, ur_y_max])
        
        psd_a_min = np.min([psd_a_x_min, psd_a_y_min])
        
        psd_a_max = np.max([psd_a_x_max, psd_a_y_max])

        psd_a_min_log = np.log10(psd_a_min)
        psd_a_max_log = np.log10(psd_a_max)

        for element in selected_elements:
            color_index = element_index % len(self.color_array)
            
            selected_color = self.color_array[int(color_index)]
            selected_color_tinted = self.color_array_lighter[color_index]

            ur_x_element = psd_output[element][0]
            ur_y_element = psd_output[element][1]
            psd_a_x_element = psd_output[element][3]
            psd_a_y_element = psd_output[element][4]

            pen_x = pg.mkPen(selected_color, width = 3)
            pen_y = pg.mkPen(selected_color_tinted, width = 3)

            psd_a_x_loglog = pg.PlotDataItem(ur_x_element[1:], psd_a_x_element[1:], pen = pen_x)
            psd_a_y_loglog = pg.PlotDataItem(ur_y_element[1:], psd_a_y_element[1:], pen = pen_y)

            if ~self.plot_both_fits_enabled:
                if (lin_fit_x_output is not None and lin_fit_x_output.get(element) is not None) or (lin_fit_y_output is not None and lin_fit_y_output.get(element) is not None):
                    pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashLine)
                    
                    if x_enabled:
                        psd_a_x_lin_fit = lin_fit_x_output[element][0]

                        psd_a_x_lin_fit_loglog = pg.PlotDataItem(ur_x_element[1:], psd_a_x_lin_fit, pen = pen)

                        self.widget.addItem(psd_a_x_lin_fit_loglog)
                    
                    else:
                        psd_a_y_lin_fit = lin_fit_y_output[element][0]

                        psd_a_y_lin_fit_loglog = pg.PlotDataItem(ur_y_element[1:], psd_a_y_lin_fit, pen = pen)

                        self.widget.addItem(psd_a_y_lin_fit_loglog)

                if (hor_fit_x_output is not None and hor_fit_x_output.get(element) is not None) or (hor_fit_y_output is not None and hor_fit_y_output.get(element) is not None):
                    pen = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                    
                    if x_enabled:
                        psd_a_x_hor_fit = hor_fit_x_output[element][0]
                    
                        psd_a_x_hor_fit_loglog = pg.PlotDataItem(ur_x_element[1:], psd_a_x_hor_fit, pen = pen)

                        self.widget.addItem(psd_a_x_hor_fit_loglog)

                    else:
                        psd_a_y_hor_fit = hor_fit_y_output[element][0]
                    
                        psd_a_y_hor_fit_loglog = pg.PlotDataItem(ur_y_element[1:], psd_a_y_hor_fit, pen = pen)

                        self.widget.addItem(psd_a_y_hor_fit_loglog)
                
            element_text = pg.TextItem("", **{'color': selected_color})

            element_text.setHtml(str(element, 'utf-8'))
            
            self.widget.addItem(element_text)

            if self.plot_both_x_and_y_enabled:
                self.widget.addItem(psd_a_x_loglog)
                self.widget.addItem(psd_a_y_loglog)

                if self.plot_both_fits_enabled and (lin_fit_x_output is not None and lin_fit_x_output.get(element) is not None) and (lin_fit_y_output is not None and lin_fit_y_output.get(element) is not None):
                    if (hor_fit_x_output is not None and hor_fit_x_output.get(element) is not None) and (hor_fit_y_output is not None and hor_fit_y_output.get(element) is not None):
                        psd_a_x_lin_fit = lin_fit_x_output[element][0]
                        psd_a_y_lin_fit = lin_fit_y_output[element][0]
                        psd_a_x_hor_fit = hor_fit_x_output[element][0]
                        psd_a_y_hor_fit = hor_fit_y_output[element][0]

                        pen_x = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashLine)
                        pen_y = pg.mkPen(selected_color_tinted, width = 3, style = QtCore.Qt.PenStyle.DotLine)

                        psd_a_x_lin_fit_loglog = pg.PlotDataItem(ur_x_element[1:], psd_a_x_lin_fit, pen = pen_x)
                        psd_a_y_lin_fit_loglog = pg.PlotDataItem(ur_y_element[1:], psd_a_y_lin_fit, pen = pen_y)
                        psd_a_x_hor_fit_loglog = pg.PlotDataItem(ur_x_element[1:], psd_a_x_hor_fit, pen = pen_x)
                        psd_a_y_hor_fit_loglog = pg.PlotDataItem(ur_y_element[1:], psd_a_y_hor_fit, pen = pen_y)

                        self.widget.addItem(psd_a_x_lin_fit_loglog)
                        self.widget.addItem(psd_a_y_lin_fit_loglog)
                        self.widget.addItem(psd_a_x_hor_fit_loglog)
                        self.widget.addItem(psd_a_y_hor_fit_loglog)
                
                if ur_x_element[ur_element_index] < ur_y_element[ur_element_index]:
                    element_text.setPos(offset + np.log10(ur_x_element[ur_element_index]), 
                                        offset + np.log10(psd_a_x_element[ur_element_index + 1]))
                
                else:
                    element_text.setPos(offset + np.log10(ur_y_element[ur_element_index]), 
                                        offset + np.log10(psd_a_y_element[ur_element_index + 1]))

                self.widget.setXRange(np.log10(ur_min), np.log10(ur_max), padding = 0)
                self.widget.setYRange(psd_a_min_log, psd_a_max_log, padding = 0)
            
            else:
                pen = pg.mkPen(selected_color, width = 3)

                if x_enabled:
                    psd_a_x_loglog.setPen(pen)
                    
                    self.widget.addItem(psd_a_x_loglog)

                    element_text.setPos(offset + np.log10(ur_x_element[ur_element_index]), 
                                        offset + np.log10(psd_a_x_element[ur_element_index + 1]))

                    self.widget.setXRange(np.log10(ur_x_element[1]), np.log10(ur_x_max), padding = 0)
                    self.widget.setYRange(np.log10(psd_a_x_min), np.log10(psd_a_x_max), padding = 0)
                
                else:
                    psd_a_y_loglog.setPen(pen)
                    
                    self.widget.addItem(psd_a_y_loglog)

                    element_text.setPos(offset + np.log10(ur_y_element[ur_element_index]), 
                                        offset + np.log10(psd_a_y_element[ur_element_index + 1]))
                    
                    self.widget.setXRange(np.log10(ur_y_element[1]), np.log10(ur_y_max), padding = 0)
                    self.widget.setYRange(np.log10(psd_a_y_min), np.log10(psd_a_y_max), padding = 0)
            
            if (res_x_output is not None and res_x_output.get(element) is not None) and (res_y_output is not None and res_y_output.get(element) is not None) and self.plot_both_x_and_y_enabled:
                psd_a_x_cutoff = res_x_output[element][0]
                psd_a_y_cutoff = res_y_output[element][0]
                ur_x_cutoff = res_x_output[element][1]
                ur_y_cutoff = res_y_output[element][1]
                dr_x_hp = res_x_output[element][2]
                dr_y_hp = res_y_output[element][2]

                pen_x = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                pen_y = pg.mkPen(selected_color_tinted, width = 3, style = QtCore.Qt.PenStyle.DotLine)
                
                symbolPen_x = pg.mkPen(selected_color)
                symbolPen_y = pg.mkPen(selected_color_tinted)

                symbolBrush_x = pg.mkBrush(selected_color)
                symbolBrush_y = pg.mkBrush(selected_color_tinted)

                psd_a_x_cutoff_point_loglog = pg.PlotDataItem([ur_x_cutoff], [psd_a_x_cutoff], pen = None, symbol = 'o', 
                                                              symbolPen = symbolPen_x, symbolBrush = symbolBrush_x)
                psd_a_y_cutoff_point_loglog = pg.PlotDataItem([ur_y_cutoff], [psd_a_y_cutoff], pen = None, symbol = 'o', 
                                                              symbolPen = symbolPen_y, symbolBrush = symbolBrush_y)
                

                pen_x = pg.mkPen(selected_color, width = 3, style = QtCore.Qt.PenStyle.DashDotLine)
                pen_y = pg.mkPen(selected_color_tinted, width = 3, style = QtCore.Qt.PenStyle.DashDotLine)

                ur_x_cutoff_vert_line = pg.PlotDataItem([ur_x_cutoff, ur_x_cutoff], [10**psd_a_min_log, psd_a_x_cutoff], pen = pen_x)
                ur_y_cutoff_vert_line = pg.PlotDataItem([ur_y_cutoff, ur_y_cutoff], [10**psd_a_min_log, psd_a_y_cutoff], pen = pen_y)

                res_x_param_text = pg.TextItem("", **{'color': selected_color})
                res_x_param_text.setHtml(str(rc(ur_x_cutoff, ndec = 7)) + " " + self.mu + "m<sup>-1</sup> (" 
                                        + str(rc(dr_x_hp, ndec = 7)) + " " + self.mu + "m)")

                res_y_param_text = pg.TextItem("", **{'color': selected_color_tinted})
                res_y_param_text.setHtml(str(rc(ur_y_cutoff, ndec = 7)) + " " + self.mu + "m<sup>-1</sup> (" 
                                        + str(rc(dr_y_hp, ndec = 7)) + " " + self.mu + "m)")

                self.widget.addItem(psd_a_x_cutoff_point_loglog)
                self.widget.addItem(psd_a_y_cutoff_point_loglog)
                self.widget.addItem(ur_x_cutoff_vert_line)
                self.widget.addItem(ur_y_cutoff_vert_line)
                self.widget.addItem(res_x_param_text)
                self.widget.addItem(res_y_param_text)
                
                res_x_param_text.setPos(offset + np.log10(ur_x_cutoff), offset + np.log10(psd_a_x_cutoff))
                res_y_param_text.setPos(offset + np.log10(ur_y_cutoff), offset + np.log10(psd_a_y_cutoff))

                if legend_flag:
                    self.legend.addItem(psd_a_x_loglog, "Measured Data (<i>x</i>)")
                    self.legend.addItem(psd_a_y_loglog, "Measured Data (<i>y</i>)")
                    self.legend.addItem(psd_a_x_lin_fit_loglog, "Data Trend Fit (<i>x</i>)")
                    self.legend.addItem(psd_a_y_lin_fit_loglog, "Data Trend Fit (<i>y</i>)")
                    self.legend.addItem(psd_a_x_hor_fit_loglog, "Noise Floor Fit (<i>x</i>)")
                    self.legend.addItem(psd_a_y_hor_fit_loglog, "Noise Floor Fit (<i>y</i>)")
                    self.legend.addItem(psd_a_x_cutoff_point_loglog, 
                                        "<i>u</i><sub>cutoff</sub> (" + self.delta + "<sub>hp,<i>x</i></sub>)")
                    self.legend.addItem(psd_a_y_cutoff_point_loglog, 
                                        "<i>u</i><sub>cutoff</sub> (" + self.delta + "<sub>hp,<i>y</i></sub>)")

                    legend_flag = 0
            
            elif legend_flag and self.plot_both_fits_enabled:
                self.legend.addItem(psd_a_x_loglog, "Measured Data (<i>x</i>)")
                self.legend.addItem(psd_a_y_loglog, "Measured Data (<i>y</i>)")

                legend_flag = 0

            ur_element_index += 1
            element_index += 1

        self.widget.setLogMode(True, True)
        
        if self.plot_both_x_and_y_enabled:
            self.widget.setXRange(np.log10(ur_min), np.log10(ur_max), padding = 0)
            self.widget.setYRange(psd_a_min_log, psd_a_max_log, padding = 0)
        
        else:
            if x_enabled:
                self.widget.setXRange(np.log10(ur_x_element[1]), np.log10(ur_x_max), padding = 0)
                self.widget.setYRange(np.log10(psd_a_x_min), np.log10(psd_a_x_max), padding = 0)
            
            else:
                self.widget.setXRange(np.log10(ur_y_element[1]), np.log10(ur_y_max), padding = 0)
                self.widget.setYRange(np.log10(psd_a_y_min), np.log10(psd_a_y_max), padding = 0)
            
        self.widget.plotItem.setTitle("<i>S</i>(<i>u<sub>r</sub></i>) v. <i>u<sub>r</sub></i> (<i>n</i><sub><i>u<sub>r</sub></i></sub> = " + str(n_ur) + ")")
        self.widget.plotItem.setLabel('left', "<i>S</i>(<i>u<sub>r</sub></i>)")
        self.widget.plotItem.setLabel('bottom', "<i>u<sub>r</sub></i> (" + self.mu + "m<sup>-1</sup>)")
        self.widget.plotItem.showGrid(True, True)
        
        self.show()

        return

    def create_pt_selection_box(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.enable_point_selection:
                self.lr.setRegion([self.vb.mapToView(ev.buttonDownPos()).x(), self.vb.mapToView(ev.pos()).x()])
            
                ev.accept()
            
                log_x_min, log_x_max = self.lr.getRegion()      
            
                self.widget.removeItem(self.psd_a_loglog_shaded)

                if self.circular_beam_checked:
                    self.idx = np.array(np.where((self.ur_element >= 10**log_x_min) & (self.ur_element <= 10**log_x_max)))[0]

                    self.psd_a_loglog_shaded = pg.PlotDataItem((self.ur_element[self.idx]), (self.psd_a_element[self.idx]), pen = None, symbol = 'o')

                    self.widget.addItem(self.psd_a_loglog_shaded)

                    self.lr.setBounds((np.log10(self.ur_element[1]), np.log10(self.ur_element[-1])))
                
                else:
                    if self.x_enabled:
                        self.widget.removeItem(self.psd_a_x_loglog_shaded)
                        
                        self.idx = np.array(np.where((self.ur_x_element >= 10**log_x_min) & (self.ur_x_element <= 10**log_x_max)))[0]

                        self.psd_a_x_loglog_shaded = pg.PlotDataItem((self.ur_x_element[self.idx]), (self.psd_a_x_element[self.idx]), 
                                                                 pen = None, symbol = 'o')
                        
                        self.widget.addItem(self.psd_a_x_loglog_shaded)

                        self.lr.setBounds((np.log10(self.ur_x_element[1]), np.log10(self.ur_x_element[-1])))
                
                    else:
                        self.widget.removeItem(self.psd_a_y_loglog_shaded)
                        
                        self.idx = np.array(np.where((self.ur_y_element >= 10**log_x_min) & (self.ur_y_element <= 10**log_x_max)))[0]

                        self.psd_a_y_loglog_shaded = pg.PlotDataItem((self.ur_y_element[self.idx]), (self.psd_a_y_element[self.idx]), pen = None, symbol = 'o')

                        self.widget.addItem(self.psd_a_y_loglog_shaded)

                        self.lr.setBounds((np.log10(self.ur_y_element[1]), np.log10(self.ur_y_element[-1])))
               
                self.lr.show()
                
                return
            
        else:
            self.pg.ViewBox.mouseDragEvent(self.vb, ev)

    def adjust_pt_selection_box(self):
        if self.enable_point_selection:
            log_x_min, log_x_max = self.lr.getRegion()

            if self.circular_beam_checked:
                self.idx = np.array(np.where((self.ur_element >= 10**log_x_min) & 
                                     (self.ur_element <= 10**log_x_max)))[0]

                self.widget.removeItem(self.psd_a_loglog_shaded)

                self.psd_a_loglog_shaded = pg.PlotDataItem(self.ur_element[self.idx], self.psd_a_element[self.idx], 
                                                   pen = None, symbol = 'o')
        
                self.widget.addItem(self.psd_a_loglog_shaded)

            else:
                if self.x_enabled:
                    self.widget.removeItem(self.psd_a_x_loglog_shaded)
                    
                    self.idx = np.array(np.where((self.ur_x_element >= 10**log_x_min) & 
                                     (self.ur_x_element <= 10**log_x_max)))[0]
    
                    self.psd_a_x_loglog_shaded = pg.PlotDataItem(self.ur_x_element[self.idx], self.psd_a_x_element[self.idx], 
                                                   pen = None, symbol = 'o')
        
                    self.widget.addItem(self.psd_a_x_loglog_shaded)
            
                else:
                    self.widget.removeItem(self.psd_a_y_loglog_shaded)

                    self.idx = np.array(np.where((self.ur_y_element >= 10**log_x_min) & 
                                     (self.ur_y_element <= 10**log_x_max)))[0]

                    self.psd_a_y_loglog_shaded = pg.PlotDataItem(self.ur_y_element[self.idx], self.psd_a_y_element[self.idx], 
                                                   pen = None, symbol = 'o')
        
                    self.widget.addItem(self.psd_a_y_loglog_shaded)
            
            return

    def clear_plot_widget_completely(self):
        self.widget.plotItem.clear()
        self.widget.plotItem.setTitle("")
        self.widget.plotItem.setLabel('left', "")
        self.widget.plotItem.setLabel('bottom', "")
        self.widget.plotItem.setLogMode(x = False, y = False)
        self.widget.plotItem.showGrid(x = False, y = False)
        
        self.widget.setXRange(0, 1)
        self.widget.setYRange(0, 1)

    def update_msg_box(self, msg = None):
        if msg is not None:
            self.label_7.setText(msg)
        
        else:
            self.label_7.clear()
        
        return

    def closeEvent(self, ev):
        self.psd_a_window_closed.emit()

        ev.accept()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Azimuthal PSD Plot"))
        self.pushButton.setText(_translate("Form", "Cancel"))
        self.pushButton_4.setText(_translate("Form", "Finish"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"right\">Slope:</p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"right\">Intercept:</p></body></html>"))
        self.pushButton_8.setText(_translate("Form", "Export"))
        self.pushButton_5.setText(_translate("Form", "Select Element(s)"))
        self.pushButton_6.setText(_translate("Form", "Create Data Trend and Noise Floor Fits"))
        self.label_6.setText(_translate("Form", "Resolution-Determining SNR Cutoff:"))
        self.pushButton_7.setText(_translate("Form", "Calculate Image Resolution"))