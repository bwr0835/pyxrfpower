# PyXRFPower: x and y resolution parameters (anisotropic/non-circular X-ray beam)
# File: pyxrfpwr_xy_res_params.py
# Author: B. Roter

# This PyXRFPower window controls the output parameters displayed when x and y resolutions are calculated.

# The output parameters include:
    # Element
    # x and y data trend slopes
    # SNR-defining x and y radial spatial frequencies (µm^-1)
    # x and y spatial resolutions (µm)

from PyQt6 import QtCore, QtGui, QtWidgets
from pyxrfpwr_math_fxns import round_correct as rc

class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(931, 300)
        self.tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 911, 271))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setWordWrap(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.init_delegate = AlignDelegate()
        
        self.cell = QtWidgets.QTableWidgetItem

        self.mu = "\u03BC"
        self.superscript_minus = "\u207B"
        self.superscript_1 = "\u00B9"
        self.cdot = "\u00B7"

        heading_1 = "Element"
        heading_2 = "Data Trend Fit Slope (x)"
        heading_3 = "Data Trend Fit Slope (y)"
        heading_4 = "Cutoff Spatial Frequency (x)\n" + "(" + self.mu + "m" + self.superscript_minus + self.superscript_1 + ")"
        heading_5 = "Cutoff Spatial Frequency (y)\n" + "(" + self.mu + "m" + self.superscript_minus + self.superscript_1 + ")"
        heading_6 = "Image Resolution (x)\n" + "(" + self.mu + "m)"
        heading_7 = "Image Resolution (y)\n" + "(" + self.mu + "m)"

        self.psd_a_param_headings_non_circular = [heading_1, heading_2, heading_3, heading_4, heading_5, heading_6, heading_7]

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_res_params_xy(self, selected_elements, lin_fit_x_output, lin_fit_y_output, res_x_output, res_y_output):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(selected_elements) + 1)

        font = QtGui.QFont()
        font.setBold(True)

        len_param_headings = len(self.psd_a_param_headings_non_circular)
        
        self.tableWidget.setItemDelegate(self.init_delegate)
        self.tableWidget.setColumnCount(len_param_headings)

        for i in range(len_param_headings):
            self.tableWidget.setItem(0, i, self.cell(self.psd_a_param_headings_non_circular[i]))
            self.tableWidget.item(0, i).setFont(font)

        j = 1 # Start writing elements and resolution parameters in the second row of the table
        
        for element in selected_elements:
            if res_x_output.get(element) is not None:
                for i in range(len_param_headings):
                    element_str = str(element, 'utf-8')
                    
                    if i == 0:
                        self.tableWidget.setItem(j, i, self.cell(element_str)) # Element
                    
                    elif i == 1:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(lin_fit_x_output[element][i], ndec = 7)))) # m_x

                    elif i == 2:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(lin_fit_y_output[element][i - 1], ndec = 7)))) # m_y

                    elif i == 3:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(res_x_output[element][i - 2], ndec = 7)))) # ur_cutoff,x
                    
                    elif i == 4:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(res_y_output[element][i - 3], ndec = 7)))) # ur_cutoff,y and dr_hp,x

                    elif i == 5:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(res_x_output[element][i - 3], ndec = 7))))

                    else:
                        self.tableWidget.setItem(j, i, self.cell(str(rc(res_y_output[element][i - 4], ndec = 7)))) # dr_hp,y

                j += 1

        self.show()

        return

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyXRFPower: Resolution Parameter Summary (Non-Circular X-ray Beam)"))

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter