# PyXRFPower: Resolution parameters (isotropic/circular X-ray beam)
# File: pyxrfpwr_res_params.py
# Author: B. Roter

# This PyXRFPower window controls the output parameters displayed when isotropic resolution is calculated.

# The output parameters include:
    # Element
    # Data trend slope
    # SNR-defining radial spatial frequency (µm^-1)
    # Spatial resolutions (µm)

from PyQt6 import QtCore, QtGui, QtWidgets
from pyxrfpwr_math_fxns import round_correct as rc

class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        Form = self
        Form.setObjectName("Form")
        Form.resize(508, 300)
        self.tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 481, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(0)

        self.init_delegate = AlignDelegate()
        
        self.cell = QtWidgets.QTableWidgetItem

        self.cdot = "\u00B7"
        self.mu = "\u03BC"
        self.superscript_minus = "\u207B"
        self.superscript_1 = "\u00B9"
        
        heading_1 = "Element"
        heading_2 = "Data Trend Fit Slope"
        heading_3 = "Cutoff Spatial Frequency\n" + "(" + self.mu + "m" + self.superscript_minus + self.superscript_1 + ")"
        heading_4 = "Image Resolution\n(" + self.mu + "m)"

        self.psd_a_param_headings_circular = [heading_1, heading_2, heading_3, heading_4]

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_res_params(self, selected_elements, lin_fit_output, res_params):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(selected_elements) + 1)
        self.tableWidget.setColumnCount(len(self.psd_a_param_headings_circular))

        font = QtGui.QFont()
        font.setBold(True)

        len_param_headings = len(self.psd_a_param_headings_circular)
        
        self.tableWidget.setItemDelegate(self.init_delegate)
        self.tableWidget.setColumnCount(len_param_headings)

        for j in range(len_param_headings):
            self.tableWidget.setItem(0, j, self.cell(self.psd_a_param_headings_circular[j]))
            self.tableWidget.item(0, j).setFont(font)

        i = 1 # Start writing elements and resolution parameters in the second row of the table
    
        for element in selected_elements:
            if res_params.get(element) is not None:
                for j in range(len_param_headings):
                    element_str = str(element, 'utf-8')

                    if j == 0:
                        self.tableWidget.setItem(i, j, self.cell(element_str))
                
                    elif j == 1:
                        self.tableWidget.setItem(i, j, self.cell(str(rc(lin_fit_output[element][1], ndec = 7))))
                
                    else:
                        self.tableWidget.setItem(i, j, self.cell(str(rc(res_params[element][j - 1], ndec = 7)))) # Similar reasoning as above comment

                i += 1
        
        self.show()

        return

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Resolution Parameter Summary (Circular X-ray Beam)"))

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter