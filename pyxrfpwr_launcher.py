# PyXRFPower: Main control code
# File: pyxrfpower_launcher.py
# Author: B. Roter

# This is the main PyXRFPower control module.

# Note: Some of the functions associated with closing a window via their window "close" buttons, 
# as well as closing a window via "cancel" buttons, may mix, as PyQt cannot differentiate between the two.

import os, sys, platform
import pyxrfpwr_main_window, pyxrfpwr_change_pixel_dims, pyxrfpwr_img_preview, pyxrfpwr_img_2dpsd, pyxrfpwr_el_select, pyxrfpwr_psd_a, pyxrfpwr_res_params, pyxrfpwr_xy_res_params
import numpy as np, csv, copy

from PyQt6 import QtCore, QtWidgets
from pyxrfpwr_hdf5_data_extract import extracth5data as eh5
from pyxrfpwr_math_fxns import round_correct as rc, normalize
from edge_filter import edge_gauss_filter as egf
from psd_calc import psd
from pyxrfpwr_mat_extract import extractmat as em

class psd_launch(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        self.gui = pyxrfpwr_main_window.Ui_MainWindow()
        self.gui_pixel_dims = pyxrfpwr_change_pixel_dims.Ui_Form()
        self.gui_plots_2d = pyxrfpwr_img_2dpsd.Ui_Form()
        self.gui_psd_a = pyxrfpwr_psd_a.Ui_Form()
        self.gui_psd_a_el_select = pyxrfpwr_el_select.Ui_Form()
        self.gui_psd_a_res_params = pyxrfpwr_res_params.Ui_Form()
        self.gui_psd_a_res_params_xy = pyxrfpwr_xy_res_params.Ui_Form()
        self.gui_img_preview = pyxrfpwr_img_preview.Ui_Form()

        self.platform = platform.system()

        self.file_startup_flag = 1
        self.fitting_enabled = 0
        self.pixel_dims_changed = 0

        self.gui_directory_backup = None
        self.exp_backup = None
        self.n_ur_backup = None
        self.sigma = 5
        self.alpha = 10
        self.gamma = 1
        self.lower_quantile = 0
        self.upper_quantile = 1
        self.snr_cutoff = 5
        self.n_elements_max = 10
        self.synchrotron_index = 0
        self.cdot = "\u00B7"
        self.deg = "\u00B0"
        self.times = "\u00D7"
        self.delta = "\u03B4"
        self.mu = "\u03BC"
        self.sigma_char = "<i>\u03C3</i>"
        self.alpha_char = "<i>\u03B1</i>"

        self.gamma_orig = copy.copy(self.gamma)
        self.lower_quantile_orig = copy.copy(self.lower_quantile)
        self.upper_quantile_orig = copy.copy(self.upper_quantile)

        self.gui.actionElemental_Images_2D_PSD_Plots.triggered.connect(lambda: self.gui_plots_2d.show())
        self.gui.actionAzimuthal_PSD_Plot.triggered.connect(lambda: self.gui_psd_a.show())
        self.gui.actionCircular_X_ray_Beam.triggered.connect(lambda: self.gui_psd_a_res_params.show())
        self.gui.actionNon_Circular_X_ray_Beam.triggered.connect(lambda: self.gui_psd_a_res_params_xy.show())
        self.gui.checkBox.clicked.connect(self.change_pixel_dims_checkbox_clicked)
        self.gui.checkBox_2.clicked.connect(self.padding_enabled_button_clicked)
        self.gui.checkBox_4.clicked.connect(self.filter_checkbox_changed)
        self.gui.comboBox.currentIndexChanged.connect(self.file_combo_button_changed)
        self.gui.comboBox_2.currentIndexChanged.connect(self.synchro_combo_button_changed)
        self.gui.pushButton.clicked.connect(self.preview_img_button_clicked)
        self.gui.toolButton.clicked.connect(self.load_file_button_clicked)
        self.gui.toolButton_2.clicked.connect(self.left_file_arrow_clicked)
        self.gui.toolButton_3.clicked.connect(self.right_file_arrow_clicked)

        self.gui_pixel_dims.pixel_dim_window_closed.connect(self.change_pixel_dims_cancel_button_clicked)
        self.gui_pixel_dims.pushButton.clicked.connect(self.change_pixel_dims_cancel_button_clicked)
        self.gui_pixel_dims.pushButton_2.clicked.connect(self.change_pixel_dims_ok_button_clicked)
    
        self.gui_img_preview.checkBox.clicked.connect(self.flip_hor_button_checkbox_clicked)
        self.gui_img_preview.checkBox_2.clicked.connect(self.flip_vert_button_checkbox_clicked)
        self.gui_img_preview.comboBox.currentIndexChanged.connect(self.img_preview_element_combo_button_changed)
        self.gui_img_preview.doubleSpinBox.valueChanged.connect(self.gamma_changed)
        self.gui_img_preview.doubleSpinBox_2.valueChanged.connect(self.lower_quantile_changed)
        self.gui_img_preview.doubleSpinBox_3.valueChanged.connect(self.upper_quantile_changed)
        self.gui_img_preview.img_preview_window_closed.connect(self.img_preview_cancel_button_clicked)
        self.gui_img_preview.pushButton.clicked.connect(self.rotate_img_ccw_button_clicked)
        self.gui_img_preview.pushButton_2.clicked.connect(self.rotate_img_cw_button_clicked)
        self.gui_img_preview.pushButton_3.clicked.connect(self.img_preview_apply_button_clicked)
        self.gui_img_preview.pushButton_4.clicked.connect(self.img_preview_cancel_button_clicked)
        self.gui_img_preview.pushButton_5.clicked.connect(self.calculate_psd_button_clicked)
        self.gui_img_preview.toolButton.clicked.connect(self.left_img_preview_element_arrow_clicked)
        self.gui_img_preview.toolButton_2.clicked.connect(self.right_img_preview_element_arrow_clicked)

        self.gui_plots_2d.toolButton.clicked.connect(self.left_element_arrow_clicked)
        self.gui_plots_2d.toolButton_2.clicked.connect(self.right_element_arrow_clicked)
        self.gui_plots_2d.comboBox.currentIndexChanged.connect(self.element_combo_button_changed)
        self.gui_plots_2d.pushButton.clicked.connect(self.batch_export_img_button_clicked)

        self.gui_psd_a_el_select.el_select_window_closed.connect(self.el_select_cancel_button_clicked)
        self.gui_psd_a_el_select.listWidget.itemSelectionChanged.connect(self.item_selection_changed)
        self.gui_psd_a_el_select.pushButton.clicked.connect(self.el_select_cancel_button_clicked)
        self.gui_psd_a_el_select.pushButton_2.clicked.connect(self.el_select_ok_button_clicked)
        
        self.gui_psd_a.lr.sigRegionChanged.connect(self.gui_psd_a.adjust_pt_selection_box)
        self.gui_psd_a.lr.sigRegionChangeFinished.connect(self.pt_selection_region_change_finished)
        self.gui_psd_a.psd_a_window_closed.connect(self.create_fits_cancel_button_clicked)
        self.gui_psd_a.pushButton.clicked.connect(self.create_fits_cancel_button_clicked)
        self.gui_psd_a.pushButton_2.clicked.connect(self.apply_fit_button_clicked)
        self.gui_psd_a.pushButton_3.clicked.connect(self.next_fit_button_clicked)
        self.gui_psd_a.pushButton_4.clicked.connect(self.finish_button_clicked)
        self.gui_psd_a.pushButton_5.clicked.connect(self.select_elements_button_clicked)
        self.gui_psd_a.pushButton_6.clicked.connect(self.create_fits_button_clicked)
        self.gui_psd_a.pushButton_7.clicked.connect(self.calculate_res_button_clicked)
        self.gui_psd_a.pushButton_8.clicked.connect(self.export_psd_a_button_clicked)
        
        self.gui_psd_a_res_params.tableWidget.horizontalHeader().sectionResized.connect(self.gui_psd_a_res_params.tableWidget.resizeRowsToContents)
        self.gui_psd_a_res_params_xy.tableWidget.horizontalHeader().sectionResized.connect(self.gui_psd_a_res_params_xy.tableWidget.resizeRowsToContents)

        sys.exit(app.exec())

    def load_file_button_clicked(self):
        self.gui.setDisabled(True)
        self.gui_plots_2d.setDisabled(True)
        self.gui_psd_a.setDisabled(True)

        if self.gui_directory_backup is not None:
            default_directory = self.gui_directory_backup
        
        else:
            default_directory = os.path.join(os.path.expanduser("~"), "Documents")

        files = QtWidgets.QFileDialog.getOpenFileNames(self.gui, "Open XRF data file(s)", default_directory, "HDF5 (*.h5*);;MATLAB (*.mat*)")

        if files[0] == "" or files[0] == []:
            self.gui.setDisabled(False)
            self.gui_plots_2d.setDisabled(False)
            self.gui_psd_a.setDisabled(False)

            return
        
        self.file_list = files[0]

        if self.platform == "Darwin" or self.platform == "Linux": # If computer running the GUI runs Mac or Linux software
            self.name_list = [file.split("/")[-1] for file in self.file_list] #/home/file/path/to/file.h5 - > [home, file, path, to, file.h5] -> file.h5
        
        elif self.platform == "Windows": # If computer running the GUI runs Windows software
            self.name_list = [file.split("\\")[-1] for file in self.file_list]

        self.gui_directory = os.path.dirname(os.path.abspath(self.file_list[0]))

        self.gui_directory_backup = copy.copy(self.gui_directory)

        self.gui.setDisabled(False)
        self.gui_plots_2d.setDisabled(False)
        self.gui_psd_a.setDisabled(False)

        self.gui.toolButton_2.setDisabled(False)
        self.gui.toolButton_3.setDisabled(False)
        self.gui.comboBox.setDisabled(False)
        
        self.gui.update_file_info_startup(files = self.name_list, directory = self.gui_directory)

        if self.gui.comboBox.count() == 1:
            self.gui.toolButton_2.setDisabled(True)
            self.gui.toolButton_3.setDisabled(True)
        
        else:
            self.gui.toolButton_2.setDisabled(True)
            self.gui.toolButton_3.setDisabled(False)
        
        if self.file_list[0].endswith(".h5"):
            self.gui_plots_2d.file_ext = ".h5"

            if self.gui.comboBox_2.isEnabled():
                curr_synchro_index = self.gui.comboBox_2.currentIndex()
        
                if curr_synchro_index == 0:
                    if self.file_list[0].endswith(".h5"):
                        self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Select a synchrotron.</span></p></body></html>")
                        
                        self.gui.pushButton.setDisabled(True)

                        return
            
                    else:
                        return
            
                try:
                    self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = eh5(self.file_list[0], synchrotron = self.synchrotron)
                
                except:
                    self.gui.pushButton.setDisabled(True)
                    
                    self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Cannot read file <code>&#8212;</code> check synchrotron and/or file.</span></p></body></html>")

                    return
                
                self.nx_orig = copy.copy(self.nx)
                self.ny_orig = copy.copy(self.ny)

                if (self.nx % 2) or (self.ny % 2):
                    self.gui.checkBox_2.setChecked(True)
                    self.gui.checkBox_2.setDisabled(False)

                    self.nx_backup = copy.copy(self.nx)
                    self.ny_backup = copy.copy(self.ny)
                
                    if (self.nx % 2) and (self.ny % 2):
                        self.nx += 1
                        self.ny += 1
        
                    elif self.nx % 2:
                        self.nx += 1
                
                    else:
                        self.ny += 1
            
                else:
                    self.gui.checkBox_2.setChecked(False)
                    self.gui.checkBox_2.setDisabled(True)

                self.dx_um_orig = copy.copy(self.dx_um)
                self.dy_um_orig = copy.copy(self.dy_um)
                
                self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
                self.n_ur_orig = copy.copy(self.n_ur)

                self.gui.reset_pixel_dims_checkbox()
                
                self.gui.update_img_dims(nx = self.nx, ny = self.ny)
                self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
                self.gui.update_error_msg()
                
                self.gui.pushButton.setDisabled(False)
                self.gui.spinBox_2.setValue(self.n_ur)

            else:
                self.gui.comboBox_2.setDisabled(False)
                self.gui.checkBox_2.setDisabled(True)

        elif self.file_list[0].endswith(".mat"):
            self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = em(self.file_list[0])

            self.nx_orig = copy.copy(self.nx)
            self.ny_orig = copy.copy(self.ny)

            self.gui_plots_2d.file_ext = ".mat"

            if self.gui.comboBox.count() == 1:
                self.gui.toolButton_2.setDisabled(True)
                self.gui.toolButton_3.setDisabled(True)
        
            else:
                self.gui.toolButton_2.setDisabled(True)
                self.gui.toolButton_3.setDisabled(False)

            self.gui.comboBox_2.setCurrentIndex(0)
            self.gui.comboBox_2.setDisabled(True)
            self.gui.spinBox_2.setDisabled(False)

            if (self.nx % 2) or (self.ny % 2):
                self.gui.checkBox_2.setChecked(True)
                self.gui.checkBox_2.setDisabled(False)
                
                if (self.nx % 2) and (self.ny % 2):
                    self.nx_backup = copy.copy(self.nx)
                    self.ny_backup = copy.copy(self.ny)
                
                    self.nx += 1
                    self.ny += 1
        
                elif self.nx % 2:
                    self.nx_backup = copy.copy(self.nx)
                    self.ny_backup = self.ny

                    self.nx += 1
                
                else:
                    self.nx_backup = self.nx
                    self.ny_backup = copy.copy(self.ny)

                    self.ny += 1
            
            else:
                self.gui.checkBox_2.setChecked(False)
                self.gui.checkBox_2.setDisabled(True)

            self.dx_um_orig = copy.copy(self.dx_um)
            self.dy_um_orig = copy.copy(self.dy_um)

            self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2))) # Default n_ur = sqrt[(nx/2)^2 + (ny/2)^2]
            self.n_ur_orig = copy.copy(self.n_ur)

            self.gui.reset_pixel_dims_checkbox()
            self.gui.update_img_dims(nx = self.nx, ny = self.ny)
            self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
            self.gui.update_error_msg()
            
            if self.file_startup_flag:
                self.gui.further_initialization(sigma = self.sigma, alpha = self.alpha)
            
                self.file_startup_flag = 0

        self.normalized_intensity_array = []
        
        self.new_file = 1
        self.k = 0 # k image rotations (k < 0 = clockwise, k > 0 = counterclockwise)

        return
        
    def synchro_combo_button_changed(self): # VALID FOR HDF5 FILES ONLY
        curr_file_index = self.gui.comboBox.currentIndex()
        curr_synchro_index = self.gui.comboBox_2.currentIndex()
        
        if curr_synchro_index == 0:
            if self.file_list[curr_file_index].endswith(".h5"):
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Select a synchrotron.</span></p></body></html>")
                
                self.gui.pushButton.setDisabled(True)

                return
            
            else:
                self.gui.update_error_msg()
                
                return

        self.synchrotron = self.gui.comboBox_2.currentText()

        try:
            self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = eh5(self.file_list[curr_file_index], synchrotron = self.synchrotron)
        
        except:
            self.gui.pushButton.setDisabled(True)
            self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Cannot read file <code>&#8212;</code> check synchrotron and/or file.</span></p></body></html>")

            return

        self.normalized_intensity_array = []
        
        self.new_file = 1
        self.k = 0 # k image rotations (k < 0 = clockwise, k > 0 = counterclockwise)

        self.nx_orig = copy.copy(self.nx)
        self.ny_orig = copy.copy(self.ny)
        
        if (self.nx % 2) or (self.ny % 2):
            self.gui.checkBox_2.setChecked(True)
            self.gui.checkBox_2.setDisabled(False)

            self.nx_backup = copy.copy(self.nx)
            self.ny_backup = copy.copy(self.ny)
                
            if (self.nx % 2) and (self.ny % 2):
                self.nx += 1
                self.ny += 1
        
            elif self.nx % 2:
                self.nx += 1
                
            else:
                self.ny += 1
            
        else:
            self.gui.checkBox_2.setChecked(False)
            self.gui.checkBox_2.setDisabled(True)
            
        self.dx_um_orig = copy.copy(self.dx_um)
        self.dy_um_orig = copy.copy(self.dy_um)       
       
        self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
        self.n_ur_orig = copy.copy(self.n_ur)
    
        self.gui.reset_pixel_dims_checkbox()

        self.gui.update_error_msg()
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
        
        self.gui.pushButton.setDisabled(False)
    
        if self.file_startup_flag:
            self.gui.further_initialization(sigma = self.sigma, alpha = self.alpha)

            self.file_startup_flag = 0
        
        self.gui.spinBox_2.setValue(self.n_ur)

        return
            
    def file_combo_button_changed(self):
        current_file_index = self.gui.comboBox.currentIndex()
        
        current_file = self.file_list[current_file_index]

        if current_file_index == self.gui.comboBox.count() - 1:
            self.gui.toolButton_2.setDisabled(False)
            self.gui.toolButton_3.setDisabled(True)

        elif current_file_index == 0:
            self.gui.toolButton_2.setDisabled(True)
            self.gui.toolButton_3.setDisabled(False)
        
        else:
            self.gui.toolButton_2.setDisabled(False)
            self.gui.toolButton_3.setDisabled(False)
        
        if current_file.endswith(".h5"):
            synchrotron_index = self.gui.comboBox_2.currentIndex()
            
            self.synchrotron = self.gui.comboBox_2.currentText()
            
            if synchrotron_index == 0:
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Select a synchrotron.</span></p></body></html>")
                
                self.gui.pushButton.setDisabled(True)
                
                return

            try:
                self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = eh5(current_file, synchrotron = self.synchrotron)

            except:
                self.gui.pushButton.setDisabled(True)
                
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Cannot read file <code>&#8212;</code> check synchrotron and/or file.</span></p></body></html>")

                return
            
            self.gui.pushButton.setDisabled(False)
        
            if self.file_startup_flag:
                self.gui.further_initialization(sigma = self.sigma, alpha = self.alpha)

                self.file_startup_flag = 0

        elif current_file.endswith(".mat"):
            self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = em(current_file)

            self.gui.comboBox_2.setCurrentIndex(0)
            self.gui.comboBox_2.setDisabled(True)

        self.gui.update_error_msg()

        self.normalized_intensity_array = []

        self.new_file = 1
        self.k = 0 # k image rotations (k < 0 = clockwise, k > 0 = counterclockwise)

        self.nx_orig = np.copy(self.nx)
        self.ny_orig = np.copy(self.ny)
        
        if (self.nx % 2) or (self.ny % 2):
            self.gui.checkBox_2.setChecked(True)
            self.gui.checkBox_2.setDisabled(False)

            self.nx_backup = copy.copy(self.nx)
            self.ny_backup = copy.copy(self.ny)
                
            if (self.nx % 2) and (self.ny % 2):
                self.nx += 1
                self.ny += 1
        
            elif self.nx % 2:
                self.nx += 1
                
            else:
                self.ny += 1
            
        else:
            self.gui.checkBox_2.setChecked(False)
            self.gui.checkBox_2.setDisabled(True)
        
        self.dx_um_orig = copy.copy(self.dx_um)
        self.dy_um_orig = copy.copy(self.dy_um)
        
        self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
        self.n_ur_orig = copy.copy(self.n_ur)

        self.gui.reset_pixel_dims_checkbox()
    
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
    
        self.gui.spinBox_2.setValue(self.n_ur)

        return
        
    def left_file_arrow_clicked(self):
        current_file_index = self.gui.comboBox.currentIndex()
            
        self.gui.comboBox.setCurrentIndex(current_file_index - 1)
            
        current_file_index = self.gui.comboBox.currentIndex()

        current_file = self.file_list[current_file_index]

        if current_file_index == 0:
            self.gui.toolButton_2.setDisabled(True)
        
        if current_file_index != self.gui.comboBox.count() - 1:
            self.gui.toolButton_3.setDisabled(False)

        self.gui.comboBox.itemText(current_file_index)
            
        if current_file.endswith(".h5"):
            synchrotron_index = self.gui.comboBox_2.currentIndex()
            
            self.synchrotron = self.gui.comboBox_2.currentText()
            
            if synchrotron_index == 0:
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Select a synchrotron.</span></p></body></html>")
                
                self.gui.pushButton.setDisabled(True)
                
                return

            try:
                self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = eh5(current_file, synchrotron = self.synchrotron)

            except:
                self.gui.pushButton.setDisabled(True)
                
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Cannot read file <code>&#8212;</code> check synchrotron and/or file.</span></p></body></html>")

                return
            
            self.gui.update_error_msg()

            self.gui.pushButton.setDisabled(False)
        
            if self.file_startup_flag:
                self.gui.further_initialization(sigma = self.sigma, alpha = self.alpha)

                self.file_startup_flag = 0

        elif current_file.endswith(".mat"):
            self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = em(current_file)
        
        self.normalized_intensity_array = []

        self.new_file = 1
        self.k = 0 # k image rotations (k < 0 = clockwise, k > 0 = counterclockwise)

        self.nx_orig = copy.copy(self.nx)
        self.ny_orig = copy.copy(self.ny)
        
        if (self.nx % 2) or (self.ny % 2):
            self.gui.checkBox_2.setChecked(True)
            self.gui.checkBox_2.setDisabled(False)

            self.nx_backup = copy.copy(self.nx)
            self.ny_backup = copy.copy(self.ny)
                
            if (self.nx % 2) and (self.ny % 2):
                self.nx += 1
                self.ny += 1
        
            elif self.nx % 2:
                self.nx += 1
                
            else:
                self.ny += 1
            
        else:
            self.gui.checkBox_2.setChecked(False)
            self.gui.checkBox_2.setDisabled(True)

        self.dx_um_orig = copy.copy(self.dx_um)
        self.dy_um_orig = copy.copy(self.dy_um)
        
        self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
        self.n_ur_orig = copy.copy(self.n_ur)

        self.gui.reset_pixel_dims_checkbox()
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
        
        self.gui.spinBox_2.setValue(self.n_ur)

        return

    def right_file_arrow_clicked(self):
        current_file_index = self.gui.comboBox.currentIndex()
        
        self.gui.comboBox.setCurrentIndex(current_file_index + 1)

        current_file_index = self.gui.comboBox.currentIndex()

        current_file = self.file_list[current_file_index]

        if current_file_index != 0:
            self.gui.toolButton_2.setDisabled(False)

        if current_file_index == self.gui.comboBox.count() - 1:
            self.gui.toolButton_3.setDisabled(True)

        self.gui.comboBox.itemText(current_file_index)
            
        if current_file.endswith(".h5"):
            synchrotron_index = self.gui.comboBox_2.currentIndex()
            
            self.synchrotron = self.gui.comboBox_2.currentText()
            
            if synchrotron_index == 0:
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Select a synchrotron.</span></p></body></html>")
                
                self.gui.pushButton.setDisabled(True)
                
                return

            try:
                self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = eh5(current_file, synchrotron = self.synchrotron)

            except:
                self.gui.pushButton.setDisabled(True)
                
                self.gui.update_error_msg("<html><head/><body><p align=\"right\"><span style=\" font-weight:700; color:#ff2600;\">Cannot read file <code>&#8212;</code> check synchrotron and/or file.</span></p></body></html>")

                return
            
            self.gui.update_error_msg()
            
            self.gui.pushButton.setDisabled(False)
        
            if self.file_startup_flag:
                self.gui.further_initialization(sigma = self.sigma, alpha = self.alpha)

                self.file_startup_flag = 0

        elif current_file.endswith(".mat"):
            self.elements, self.intensity, self.nx, self.ny, self.dx_um, self.dy_um = em(current_file)
        
        self.normalized_intensity_array = []

        self.new_file = 1
        self.k = 0 # k image rotations (k < 0 = clockwise, k > 0 = counterclockwise)

        self.nx_orig = copy.copy(self.nx)
        self.ny_orig = copy.copy(self.ny)
        
        if (self.nx % 2) or (self.ny % 2):
            self.gui.checkBox_2.setChecked(True)
            self.gui.checkBox_2.setDisabled(False)

            self.nx_backup = copy.copy(self.nx)
            self.ny_backup = copy.copy(self.ny)
                
            if (self.nx % 2) and (self.ny % 2):
                self.nx += 1
                self.ny += 1
        
            elif self.nx % 2:
                self.nx += 1
                
            else:
                self.ny += 1
            
        else:
            self.gui.checkBox_2.setChecked(False)
            self.gui.checkBox_2.setDisabled(True)
        
        self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
        self.n_ur_orig = copy.copy(self.n_ur)

        self.dx_um_orig = copy.copy(self.dx_um)
        self.dy_um_orig = copy.copy(self.dy_um)

        self.gui.reset_pixel_dims_checkbox()
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)
    
        self.gui.spinBox_2.setValue(self.n_ur)

        return

    def change_pixel_dims_checkbox_clicked(self):
        if self.gui.checkBox.isChecked():
            self.gui.setDisabled(True)
            self.gui_plots_2d.setDisabled(True)
            self.gui_psd_a.setDisabled(True)
            
            if self.gui_psd_a_res_params.isVisible():
                self.gui_psd_a_res_params.setDisabled(True)
            
            elif self.gui_psd_a_res_params_xy.isVisible():
                self.gui_psd_a_res_params_xy.setDisabled(True)

            self.gui_pixel_dims.update_pixel_dim('x', self.dx_um)
            self.gui_pixel_dims.update_pixel_dim('y', self.dy_um)

            self.gui_pixel_dims.show()
        
        else:
            self.dx_um = self.dx_um_orig
            self.dy_um = self.dy_um_orig

            self.pixel_dims_changed = 1

            self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)

    def change_pixel_dims_cancel_button_clicked(self):
        self.gui_pixel_dims.close()
        
        self.gui.setDisabled(False)
        self.gui_plots_2d.setDisabled(False)
        self.gui_psd_a.setDisabled(False)

        if self.pixel_dims_changed: # To bypass competing "Cancel" and "OK" "close" signals
            self.gui.checkBox.setChecked(True)
        
        else:
            self.gui.checkBox.setChecked(False)
            
        if self.gui_psd_a_res_params.isVisible():
            self.gui_psd_a_res_params.setDisabled(False)
            
        elif self.gui_psd_a_res_params_xy.isVisible():
            self.gui_psd_a_res_params_xy.setDisabled(False)

        self.gui_pixel_dims.update_pixel_dim(axis = 'x', length = self.dx_um)
        self.gui_pixel_dims.update_pixel_dim(axis = 'y', length = self.dy_um)

    def change_pixel_dims_ok_button_clicked(self):
        self.dx_um = self.gui_pixel_dims.doubleSpinBox.value()
        self.dy_um = self.gui_pixel_dims.doubleSpinBox_2.value()
       
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)

        self.pixel_dims_changed = 1
        
        self.gui_pixel_dims.close()
        
        self.gui.setDisabled(False)
        self.gui_plots_2d.setDisabled(False)
        self.gui_psd_a.setDisabled(False)
        
        if self.gui_psd_a_res_params.isVisible():
            self.gui_psd_a_res_params.setDisabled(False)
            
        elif self.gui_psd_a_res_params_xy.isVisible():
            self.gui_psd_a_res_params_xy.setDisabled(False)

    def padding_enabled_button_clicked(self):
        if self.gui.checkBox_2.isChecked():
            if self.nx % 2:
                self.nx_backup = copy.copy(self.nx)
                
                self.nx += 1
        
            if self.ny % 2:
                self.ny_backup = copy.copy(self.ny)
                
                self.ny += 1
        
        else:
            if self.nx_backup % 2:
                self.nx -= 1
            
            if self.ny_backup % 2:
                self.ny -= 1
        
        self.n_ur = int(0.5*(1 + np.sqrt(self.nx**2 + self.ny**2)))
        self.n_ur_orig = copy.copy(self.n_ur)

        self.gui.update_img_dims(nx = self.nx, ny = self.ny) # Note: If pixel spacings are averages, then they will be assumed to not change when adding an extra row and/or column
       
        self.gui.spinBox_2.setValue(self.n_ur)
        
        return
                                   
    def filter_checkbox_changed(self):
        if self.gui.checkBox_4.isChecked():
            self.gui.spinBox.setDisabled(False)
            self.gui.spinBox.setValue(int(self.sigma))
            self.gui.doubleSpinBox.setDisabled(False)
            self.gui.doubleSpinBox.setValue(self.alpha)
        
        else:
            self.sigma_backup = self.gui.spinBox.value()
            self.alpha_backup = self.gui.doubleSpinBox.value()
            
            self.gui.spinBox.clear()
            self.gui.spinBox.setDisabled(True)
            self.gui.doubleSpinBox.clear()
            self.gui.doubleSpinBox.setDisabled(True)

        return

    def preview_img_button_clicked(self):
        self.gui.setDisabled(True)
        
        self.gui_plots_2d.close()
        self.gui_psd_a.close()
        
        if self.gui.checkBox_3.isChecked():
            self.gui_psd_a_res_params.close()
        
        else:
            self.gui_psd_a_res_params_xy.close()
#        
        if self.normalized_intensity_array == []:
            self.elements_string = []
        
            self.elements_backup = copy.deepcopy(self.elements)
        
            self.elements_string_backup = copy.copy(self.elements_string)
            
            for element in self.elements:
                element_index = np.ndarray.item(np.where(self.elements == element)[0])

                element_string = str(element, 'utf-8')

                intensity = copy.copy(self.intensity[element_index])
                
                min_threshold, max_threshold = np.quantile(intensity, [self.lower_quantile, self.upper_quantile])

                normalized_intensity = normalize.pwr_law_norm(intensity, min_threshold = min_threshold, max_threshold = max_threshold, gamma = self.gamma)

                self.normalized_intensity_array.append(normalized_intensity)
                self.elements_string.append(element_string)

            self.gui_img_preview.checkBox.setChecked(False)
            self.gui_img_preview.checkBox_2.setChecked(False)

            self.gui_img_preview.update_img_preview(self.elements[0], self.normalized_intensity_array[0], 
                                                    self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um) # Display preview of first elemental intensity map

            self.gui_img_preview.comboBox.clear()
            self.gui_img_preview.comboBox.addItems(self.elements_string)

            self.gui_img_preview.update_img_contrast_values(gamma = self.gamma, lower_quantile = self.lower_quantile, upper_quantile = self.upper_quantile)

            self.gui_img_preview.pushButton_3.setDisabled(False)
            self.gui_img_preview.pushButton_5.setDisabled(False)

            if len(self.elements) == 0:
                self.gui_img_preview.toolButton_2.setDisabled(True)
        
            else:
                self.gui_img_preview.toolButton_2.setDisabled(False)

        else:
            self.gui_img_preview.doubleSpinBox.setValue(self.gamma_orig)
            self.gui_img_preview.doubleSpinBox_2.setValue(self.lower_quantile_orig)
            self.gui_img_preview.doubleSpinBox_3.setValue(self.upper_quantile_orig)

            self.gui_img_preview.update_img_preview(self.elements[self.current_element_index], self.normalized_intensity_array[self.current_element_index], 
                                                    self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um) # Display preview of first elemental intensity map
       
        self.gui_img_preview.show()

        self.additional_contrast_calculations = 0

        return
    
    def img_preview_element_combo_button_changed(self):
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        element = self.elements_backup[current_element_index]

        self.gui_img_preview.update_img_preview(element, self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if current_element_index == 0:
            self.gui_img_preview.toolButton.setDisabled(True)
        
        else:
            self.gui_img_preview.toolButton.setDisabled(False)
        
        if current_element_index == self.gui_img_preview.comboBox.count() - 1:
            self.gui_img_preview.toolButton_2.setDisabled(True)
        
        else:
            self.gui_img_preview.toolButton_2.setDisabled(False)
        
        return
    
    def left_img_preview_element_arrow_clicked(self):
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        
        self.gui_img_preview.comboBox.setCurrentIndex(current_element_index - 1)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        element = self.elements[current_element_index]
        
        self.gui_img_preview.comboBox.itemText(current_element_index)

        self.gui_img_preview.update_img_preview(element, self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if current_element_index == 0:
            self.gui_img_preview.toolButton.setDisabled(True)
        
        if current_element_index != self.gui_img_preview.comboBox.count() - 1:
            self.gui_img_preview.toolButton_2.setDisabled(False)
        
        return
    
    def right_img_preview_element_arrow_clicked(self):
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        
        self.gui_img_preview.comboBox.setCurrentIndex(current_element_index + 1)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        element = self.elements[current_element_index]

        self.gui_img_preview.comboBox.itemText(current_element_index)

        self.gui_img_preview.update_img_preview(element, self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if current_element_index != 0:
            self.gui_img_preview.toolButton.setDisabled(False)

        if current_element_index == self.gui_img_preview.comboBox.count() - 1:
            self.gui_img_preview.toolButton_2.setDisabled(True)
        
        return

    def gamma_changed(self):
        self.additional_contrast_calculations = 1

        return

    def lower_quantile_changed(self):
        self.gui_img_preview.compare_quantiles()

        self.additional_contrast_calculations = 1 

        return

    def upper_quantile_changed(self):
        self.gui_img_preview.compare_quantiles()

        self.additional_contrast_calculations = 1 

        return

    def img_preview_cancel_button_clicked(self):
        self.gui_img_preview.close()
        
        self.current_element_index = self.gui_img_preview.comboBox.currentIndex()

        self.gui.setDisabled(False)

        return

    def rotate_img_ccw_button_clicked(self):
        for element in self.elements:
            element_index = np.ndarray.item(np.where(self.elements == element)[0])

            normalized_intensity = self.normalized_intensity_array[element_index]

            self.normalized_intensity_array[element_index] = np.rot90(normalized_intensity, k = 1)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()

        self.nx, self.ny = self.ny, self.nx
        self.nx_backup, self.ny_backup = self.ny_backup, self.nx_backup
        self.dx_um, self.dy_um = self.dy_um, self.dx_um
        self.dx_um_orig, self.dy_um_orig = self.dy_um_orig, self.dx_um_orig

        self.gui_img_preview.update_img_preview(self.elements[current_element_index], self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)
        
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)

        self.gui_img_preview.pushButton_2.setDisabled(False)

        self.k += 1

        if self.k >= 2:
            self.gui_img_preview.pushButton.setDisabled(True)
        
        else:
            self.gui_img_preview.pushButton.setDisabled(False)

        return
    
    def rotate_img_cw_button_clicked(self):
        for element in self.elements:
            element_index = np.ndarray.item(np.where(self.elements == element)[0])

            normalized_intensity = self.normalized_intensity_array[element_index]

            self.normalized_intensity_array[element_index] = np.rot90(normalized_intensity, k = -1)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()

        self.nx, self.ny = self.ny, self.nx
        self.nx_backup, self.ny_backup = self.ny_backup, self.nx_backup
        self.dx_um, self.dy_um = self.dy_um, self.dx_um
        self.dx_um_orig, self.dy_um_orig = self.dy_um_orig, self.dx_um_orig

        self.gui_img_preview.update_img_preview(self.elements[current_element_index], self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)
        
        self.gui.update_img_dims(nx = self.nx, ny = self.ny)
        self.gui.update_pixel_dims(dx = self.dx_um, dy = self.dy_um)

        self.gui_img_preview.pushButton.setDisabled(False)

        self.k -= 1

        if self.k <= -2:
            self.gui_img_preview.pushButton_2.setDisabled(True)
        
        else:
            self.gui_img_preview.pushButton_2.setDisabled(False)

        return
    
    def flip_hor_button_checkbox_clicked(self):
        for element in self.elements:
            element_index = np.ndarray.item(np.where(self.elements == element)[0])

            normalized_intensity = self.normalized_intensity_array[element_index]

            self.normalized_intensity_array[element_index] = np.flip(normalized_intensity, axis = 1)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        
        self.gui_img_preview.update_img_preview(self.elements[current_element_index], self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        return

    def flip_vert_button_checkbox_clicked(self):
        for element in self.elements:
            element_index = np.ndarray.item(np.where(self.elements == element)[0])

            normalized_intensity = self.normalized_intensity_array[element_index]

            self.normalized_intensity_array[element_index] = np.flip(normalized_intensity, axis = 0)
        
        current_element_index = self.gui_img_preview.comboBox.currentIndex()
        
        self.gui_img_preview.update_img_preview(self.elements[current_element_index], self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        return

    def img_preview_apply_button_clicked(self):
        self.gamma = self.gui_img_preview.doubleSpinBox.value()
        self.lower_quantile = self.gui_img_preview.doubleSpinBox_2.value()
        self.upper_quantile = self.gui_img_preview.doubleSpinBox_3.value()

        self.gamma_orig = copy.copy(self.gamma)
        self.lower_quantile_orig = copy.copy(self.lower_quantile)
        self.upper_quantile_orig = copy.copy(self.upper_quantile)

        if (self.k != 0) or (self.gui_img_preview.checkBox.isChecked()) or (self.gui_img_preview.checkBox_2.isChecked()):
            for element in self.elements:
                element_index = np.ndarray.item(np.where(self.elements == element)[0])

                intensity = copy.copy(self.intensity[element_index]) # For some reason, not copying will cause self.intensity to change each time "Apply" is clicked

                min_threshold, max_threshold = np.quantile(intensity, [self.lower_quantile, self.upper_quantile])

                self.normalized_intensity_array[element_index] = normalize.pwr_law_norm(intensity, min_threshold = min_threshold, max_threshold = max_threshold, gamma = self.gamma)

                if self.k != 0:
                    self.normalized_intensity_array[element_index] = np.rot90(self.normalized_intensity_array[element_index], k = self.k)
                
                if self.gui_img_preview.checkBox.isChecked():
                    self.normalized_intensity_array[element_index] = np.flip(self.normalized_intensity_array[element_index], axis = 1)

                if self.gui_img_preview.checkBox_2.isChecked():
                    self.normalized_intensity_array[element_index] = np.flip(self.normalized_intensity_array[element_index], axis = 0)
        
        else:
            for element in self.elements:
                element_index = np.ndarray.item(np.where(self.elements == element)[0])

                intensity = copy.copy(self.intensity[element_index]) # For some reason, not copying will cause self.intensity to change each time "Apply" is clicked

                min_threshold, max_threshold = np.quantile(intensity, [self.lower_quantile, self.upper_quantile])

                self.normalized_intensity_array[element_index] = normalize.pwr_law_norm(intensity, min_threshold = min_threshold, max_threshold = max_threshold, gamma = self.gamma)

        current_element_index = self.gui_img_preview.comboBox.currentIndex()

        self.gui_img_preview.update_img_preview(self.elements[current_element_index], self.normalized_intensity_array[current_element_index], 
                                                self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        self.additional_contrast_calculations = 0

    def calculate_psd_button_clicked(self):    
        self.gui_img_preview.close()
        
        self.snr_enabled_start = 0
        self.new_calculation = 1

        padding_checked = self.gui.checkBox_2.isChecked()
        circular_beam_checked = self.gui.checkBox_3.isChecked()
        smoothing_checked = self.gui.checkBox_4.isChecked()
        
        hor_flip_checked = self.gui_img_preview.checkBox.isChecked()
        vert_flip_checked = self.gui_img_preview.checkBox_2.isChecked()
        
        self.current_element_index = self.gui_img_preview.comboBox.currentIndex()

        self.padding_checked = copy.copy(padding_checked)
        self.circular_beam_checked = copy.copy(circular_beam_checked)
        self.smoothing_checked = copy.copy(smoothing_checked)
        self.gamma_orig = copy.copy(self.gamma)
        self.lower_quantile_orig = copy.copy(self.lower_quantile)
        self.upper_quantile_orig = copy.copy(self.upper_quantile)

        self.gui_psd_a.circular_beam_checked = self.circular_beam_checked
        self.gui_plots_2d.circular_beam_checked = self.circular_beam_checked
        
        self.n_ur = self.gui.spinBox_2.value()

        self.gui.spinBox_2.setValue(self.n_ur)

        self.gui_plots_2d.pushButton.setDisabled(True)

        self.n_ur_backup = copy.copy(self.n_ur)

        self.gui_psd_a.n_ur = self.n_ur_backup
        
        self.psd_dict = {}
        self.im = {}
        self.im_orig = {}

        self.intensity_backup = copy.deepcopy(self.intensity)
        
        if circular_beam_checked:
            self.lin_fit_dict = {} 
            self.lin_fit_dict_backup = {}
            self.hor_fit_dict = {}
            self.hor_fit_dict_backup = {}
            self.res_params = {}
            self.res_params_backup = {}

        else:
            self.lin_fit_dict_x = {}
            self.lin_fit_dict_x_backup = {}
            self.lin_fit_dict_y = {}
            self.lin_fit_dict_y_backup = {}
            self.hor_fit_dict_x = {}
            self.hor_fit_dict_x_backup = {}
            self.hor_fit_dict_y = {}
            self.hor_fit_dict_y_backup = {}
            self.res_params_x = {}
            self.res_params_x_backup = {}
            self.res_params_y = {}
            self.res_params_y_backup = {}
        
        if self.additional_contrast_calculations:
            self.gamma = self.gui_img_preview.doubleSpinBox.value()
            self.lower_quantile = self.gui_img_preview.doubleSpinBox_2.value()
            self.upper_quantile = self.gui_img_preview.doubleSpinBox_3.value()

            self.gamma_orig = copy.copy(self.gamma)
            self.lower_quantile_orig = copy.copy(self.lower_quantile)
            self.upper_quantile_orig = copy.copy(self.upper_quantile)
        
        for element in self.elements:
            element_index = np.ndarray.item(np.where(self.elements == element)[0])

            intensity_indiv = self.intensity_backup[element_index]
            
            intensity_indiv_backup = copy.copy(self.intensity[element_index])

            self.im[element] = self.normalized_intensity_array[element_index]
            self.im_orig[element] = self.intensity[element_index]

            if self.additional_contrast_calculations:
                min_threshold, max_threshold = np.quantile(intensity_indiv_backup, [self.lower_quantile, self.upper_quantile])
                
                self.im[element] = normalize.pwr_law_norm(intensity_indiv_backup, min_threshold, max_threshold, self.gamma)

            idx = np.where(intensity_indiv < 0)

            if np.size(idx) != 0:
                intensity_indiv += np.abs(np.min(intensity_indiv))

                intensity_indiv = np.sqrt(intensity_indiv)
            
            else:
                intensity_indiv = np.sqrt(intensity_indiv)
            
            if (self.k != 0) or hor_flip_checked or vert_flip_checked:
                if self.k != 0:
                    intensity_indiv = np.rot90(intensity_indiv, k = self.k)
                    
                    self.im_orig[element] = np.rot90(self.im_orig[element], k = self.k)

                    if self.additional_contrast_calculations:
                        self.im[element] = np.rot90(self.im[element], k = self.k)
                
                if hor_flip_checked:
                    intensity_indiv = np.flip(intensity_indiv, axis = 1)

                    self.im_orig[element] = np.flip(self.im_orig[element], axis = 1)

                    if self.additional_contrast_calculations:
                        self.im[element] = np.flip(self.im[element], axis = 1)
                
                if vert_flip_checked:
                    intensity_indiv = np.flip(intensity_indiv, axis = 0)

                    self.im_orig[element] = np.flip(self.im_orig[element], axis = 0)

                    if self.additional_contrast_calculations:
                        self.im[element] = np.flip(self.im[element], axis = 0)
        
            if padding_checked:
                intensity_indiv_avg = np.mean(intensity_indiv)

                if (self.nx_backup % 2) and (self.ny_backup % 2):
                    intensity_indiv = np.vstack((intensity_indiv, intensity_indiv_avg*np.ones(self.nx_backup))) # Pad x-dxn
                    intensity_indiv = np.hstack((intensity_indiv, intensity_indiv_avg*np.ones(((self.ny_backup + 1), 1)))) # Pad y-dxn (when padding x-dxn as well)

                elif self.nx_backup % 2:
                    intensity_indiv = np.hstack((intensity_indiv, intensity_indiv_avg*np.ones((self.ny_backup, 1)))) # Pad x-dxn only
                
                else:
                    intensity_indiv = np.vstack((intensity_indiv, intensity_indiv_avg*np.ones(self.nx_backup))) # Pad y-dxn only

            if smoothing_checked:
                self.alpha = self.gui.doubleSpinBox.value()
                self.sigma = self.gui.spinBox.value()
                
                self.sigma_backup = copy.copy(self.sigma)
                self.alpha_backup = copy.copy(self.alpha)

                self.gui.doubleSpinBox.setValue(self.alpha)
                self.gui.spinBox.setValue(self.sigma)

                intensity_indiv_filtered = egf(intensity_indiv, self.sigma, self.alpha, self.nx, self.ny)

                if circular_beam_checked:
                    self.ur, self.psd, self.psd_a = psd(intensity_indiv_filtered, 
                                                        self.dx_um, self.dy_um, self.nx, self.ny, self.n_ur, circular_beam_checked)

                    self.psd_dict[element] = [self.ur, self.psd, self.psd_a]
            
                else:
                    self.ur_x, self.ur_y, self.psd, self.psd_a_x, self.psd_a_y = psd(intensity_indiv_filtered, 
                                                        self.dx_um, self.dy_um, self.nx, self.ny, self.n_ur, circular_beam_checked)
                    
                    self.psd_dict[element] = [self.ur_x, self.ur_y, self.psd, self.psd_a_x, self.psd_a_y]
                
            else:
                if circular_beam_checked:
                    self.ur, self.psd, self.psd_a = psd(intensity_indiv, 
                                                    self.dx_um, self.dy_um, self.nx, self.ny, self.n_ur, 
                                                    circular_beam_checked)
                    
                    self.psd_dict[element] = [self.ur, self.psd, self.psd_a]
                
                else:
                    self.ur_x, self.ur_y, self.psd, self.psd_a_x, self.psd_a_y = psd(intensity_indiv, 
                                                        self.dx_um, self.dy_um, self.nx, self.ny, self.n_ur, circular_beam_checked)
                    
                    self.psd_dict[element] = [self.ur_x, self.ur_y, self.psd, self.psd_a_x, self.psd_a_y]

        if smoothing_checked:
            if self.new_file:
                self.gui_plots_2d.update_2d_plots(self.elements[0], self.im, self.psd_dict, 
                                                  self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                                  self.sigma, self.alpha)
            
            else:
                self.gui_plots_2d.update_2d_plots(self.elements[self.current_element_index], self.im, self.psd_dict, 
                                                  self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                                  self.sigma, self.alpha)
        
        else:
            if self.new_file:
                self.gui_plots_2d.update_2d_plots(self.elements[0], self.im, self.psd_dict, 
                                                  self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)
            
            else: self.gui_plots_2d.update_2d_plots(self.elements[self.current_element_index], self.im, self.psd_dict, 
                                                  self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        self.elements_string_backup = copy.copy(self.elements_string)
        self.elements_backup = copy.deepcopy(self.elements)

        if self.new_file:
            self.gui_plots_2d.comboBox.clear()
            self.gui_plots_2d.comboBox.addItems(self.elements_string)

            self.gui_psd_a_el_select.listWidget.clear()
            self.gui_psd_a_el_select.listWidget.addItems(self.elements_string)
            self.gui_psd_a_el_select.pushButton_2.setDisabled(True)

            self.new_file = 0
        
        else:
            selected_elements = self.gui_psd_a_el_select.listWidget.selectedItems()

            if len(selected_elements) > 0:
                self.gui_psd_a_el_select.pushButton_2.setDisabled(False)
            
            else:
                self.gui_psd_a_el_select.pushButton_2.setDisabled(True)
        
        self.gui_plots_2d.comboBox.setCurrentIndex(self.current_element_index)

        self.gui_psd_a_el_select.show()
        
        return

    def element_combo_button_changed(self):
        element_index = self.gui_plots_2d.comboBox.currentIndex()
        element = self.elements_backup[element_index]
        
        if self.smoothing_checked:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                              self.sigma_backup, self.alpha_backup)
        
        else:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if element_index == 0:
            self.gui_plots_2d.toolButton.setDisabled(True)
        
        else:
            self.gui_plots_2d.toolButton.setDisabled(False)
        
        if element_index == self.gui_plots_2d.comboBox.count() - 1:
            self.gui_plots_2d.toolButton_2.setDisabled(True)
        
        else:
            self.gui_plots_2d.toolButton_2.setDisabled(False)
        
        return

    def left_element_arrow_clicked(self): 
        current_element_index = self.gui_plots_2d.comboBox.currentIndex()
        
        self.gui_plots_2d.comboBox.setCurrentIndex(current_element_index - 1)
        
        current_element_index = self.gui_plots_2d.comboBox.currentIndex()
        element = self.elements_backup[current_element_index]
        
        self.gui_plots_2d.comboBox.itemText(current_element_index)
        
        if self.smoothing_checked:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                              self.sigma_backup, self.alpha_backup)
        
        else:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if current_element_index == 0:
            self.gui_plots_2d.toolButton.setDisabled(True)

        if current_element_index != self.gui_plots_2d.comboBox.count() - 1:
            self.gui_plots_2d.toolButton_2.setDisabled(False)

        return
    
    def right_element_arrow_clicked(self):
        current_element_index = self.gui_plots_2d.comboBox.currentIndex()
        
        self.gui_plots_2d.comboBox.setCurrentIndex(current_element_index + 1)
        
        current_element_index = self.gui_plots_2d.comboBox.currentIndex()
        element = self.elements_backup[current_element_index]

        self.gui_plots_2d.comboBox.itemText(current_element_index)
        
        if self.smoothing_checked:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                              self.sigma_backup, self.alpha_backup)
        
        else:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        if current_element_index != 0:
            self.gui_plots_2d.toolButton.setDisabled(False)

        if current_element_index == self.gui_plots_2d.comboBox.count() - 1:
            self.gui_plots_2d.toolButton_2.setDisabled(True)

        return

    def select_elements_button_clicked(self):
        if self.new_calculation:
            self.gui_psd_a_el_select.listWidget.clearSelection()

        self.gui.setDisabled(True)
        self.gui_plots_2d.pushButton.setDisabled(True)
        self.gui_psd_a.setDisabled(True)

        if self.selected_element_strings_backup is not None:
            for element in self.selected_element_strings_backup:
                selected_element_index = self.gui_psd_a_el_select.listWidget.findItems(element, QtCore.Qt.MatchFlag.MatchExactly)     
                
                [element_index.setSelected(True) for element_index in selected_element_index]

        self.gui_psd_a_el_select.show()

    def item_selection_changed(self):
        selected_elements = self.gui_psd_a_el_select.listWidget.selectedItems()

        if len(selected_elements) == 0:
            self.gui_psd_a_el_select.pushButton_2.setDisabled(True)
        
        else:
            self.gui_psd_a_el_select.pushButton_2.setDisabled(False)
        
        if len(selected_elements) > self.n_elements_max:
            selected_elements[self.n_elements_max].setSelected(False)

    def el_select_cancel_button_clicked(self):
        self.gui_psd_a_el_select.close()
        self.gui.setDisabled(False)
        self.gui_psd_a.setDisabled(False)

        self.gui_psd_a.pushButton_5.setDisabled(False)

        if self.gui_psd_a.isVisible():
            if self.new_calculation:
                self.gui_psd_a.widget.plotItem.clear()
                
                if self.selected_element_strings_backup is None:
                    self.gui_psd_a.pushButton_6.setDisabled(True)
                    self.gui_psd_a.pushButton_8.setDisabled(True)
            
            else:
                self.gui.menuResolution_Parameter_Summary.setDisabled(False)
                
                self.gui_psd_a.pushButton_6.setDisabled(False)
                self.gui_psd_a.pushButton_8.setDisabled(False)
        
        else:
            if self.new_calculation:
                self.gui_psd_a.clear_plot_widget_completely()

                self.selected_element_strings_backup = None

                self.gui.menuView.setDisabled(False)
                self.gui.menuResolution_Parameter_Summary.setDisabled(True)

                self.gui_psd_a.doubleSpinBox.clear()
                self.gui_psd_a.doubleSpinBox.setDisabled(True)
                self.gui_psd_a.pushButton.setDisabled(True)
                self.gui_psd_a.pushButton_2.setDisabled(True)
                self.gui_psd_a.pushButton_3.setDisabled(True)
                self.gui_psd_a.pushButton_4.setDisabled(True)
                self.gui_psd_a.pushButton_6.setDisabled(True)
                self.gui_psd_a.pushButton_7.setDisabled(True)
                self.gui_psd_a.pushButton_8.setDisabled(True)
            
            else:
                if self.circular_beam_checked:
                    if len(self.res_params) > 0:
                        self.gui.menuResolution_Parameter_Summary.setDisabled(False)
                        self.gui.actionNon_Circular_X_ray_Beam.setDisabled(True)
            
                    else:
                        self.gui.menuResolution_Parameter_Summary.setDisabled(True)
        
                else:
                    if len(self.res_params_x) > 0:
                        self.gui.menuResolution_Parameter_Summary.setDisabled(False)
                        self.gui.actionCircular_X_ray_Beam.setDisabled(True)
            
                    else:
                        self.gui.menuResolution_Parameter_Summary.setDisabled(True)
                

                self.gui_psd_a.pushButton_8.setDisabled(False)

            self.gui_psd_a.show()

        return

    def el_select_ok_button_clicked(self):
        snr_disabled = 1
        
        self.new_calculation = 0
        
        selected_element_addresses = self.gui_psd_a_el_select.listWidget.selectedItems()
        
        self.selected_element_strings = [selected_element_addresses[element].text() for element in range(len(selected_element_addresses))] 

        self.selected_element_strings_backup = copy.copy(self.selected_element_strings)
        self.selected_elements = [bytes(element, 'utf-8') for element in self.selected_element_strings]

        self.gui_psd_a.plot_both_fits_enabled = 1 # Flag for making sure no fits are plotted for an element if only one fit exists
                                                  # resulting from cancellations in the middle of fitting

        if self.circular_beam_checked:
            if len(self.res_params) > 0:
                self.gui.menuResolution_Parameter_Summary.setDisabled(False)
                self.gui.actionNon_Circular_X_ray_Beam.setDisabled(True)
            
            else:
                self.gui.menuResolution_Parameter_Summary.setDisabled(True)
        
        else:
            if len(self.res_params_x) > 0:
                self.gui.menuResolution_Parameter_Summary.setDisabled(False)
                self.gui.actionCircular_X_ray_Beam.setDisabled(True)
            
            else:
                self.gui.menuResolution_Parameter_Summary.setDisabled(True)

        self.gui.setDisabled(False)
        self.gui_psd_a.setDisabled(False)
        self.gui_plots_2d.pushButton.setDisabled(False)

        self.gui.menuView.setDisabled(False)
        self.gui.pushButton.setDisabled(False)

        self.gui_psd_a.pushButton.setDisabled(True)
        self.gui_psd_a.pushButton_2.setDisabled(True)
        self.gui_psd_a.pushButton_3.setDisabled(True)
        self.gui_psd_a.pushButton_4.setDisabled(True)
        self.gui_psd_a.pushButton_6.setDisabled(False)

        if self.circular_beam_checked:
            for element in self.selected_elements:
                if self.lin_fit_dict_backup.get(element) is not None:
                    self.gui_psd_a.doubleSpinBox.setDisabled(False)
                    self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)
                    self.gui_psd_a.pushButton_7.setDisabled(False)

                    snr_disabled = 0

                    break
            
            if snr_disabled:
                self.gui_psd_a.doubleSpinBox.clear()
                self.gui_psd_a.doubleSpinBox.setDisabled(True)
                self.gui_psd_a.pushButton_7.setDisabled(True)
            
            self.gui_psd_a.update_psd_a_plot(self.selected_elements, self.psd_dict, self.n_ur_backup, 
                                             self.lin_fit_dict_backup, self.hor_fit_dict_backup, self.res_params_backup)

            first_element_index = bytes(self.selected_element_strings_backup[0], 'utf-8')
            
            n_ur_good = len(self.psd_dict[first_element_index][0])

            print(n_ur_good)

            if n_ur_good != self.n_ur_backup: # Warning if there are radial spatial frequency bins without contributing pixels (these frequencies are thrown out when plotting)
                self.gui_psd_a.update_msg_box(f"""<html><head/><body><p align=\"left\"><span style=\" font-weight:700; color:#ff2600;\"> Warning: Only <b>{n_ur_good}</b> radial spatial frequency bins are contributing to <i>S</i>(<i>u<sub>r</sub></i>). </span></p></body></html>""")
            
            else:
                self.gui_psd_a.update_msg_box()

        else:
            self.gui_psd_a.plot_both_x_and_y_enabled = 1

            for element in self.selected_elements:
                if self.lin_fit_dict_x_backup.get(element) is not None:
                    self.gui_psd_a.doubleSpinBox.setDisabled(False)
                    self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)
                    self.gui_psd_a.pushButton_7.setDisabled(False)

                    snr_disabled = 0

                    break
            
            if snr_disabled:
                self.gui_psd_a.doubleSpinBox.clear()
                self.gui_psd_a.doubleSpinBox.setDisabled(True)
                self.gui_psd_a.pushButton_7.setDisabled(True)
            
            self.gui_psd_a.update_psd_a_plot_xy(self.selected_elements, self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, 
                                                self.lin_fit_dict_x_backup, self.lin_fit_dict_y_backup, 
                                                self.hor_fit_dict_x_backup, self.hor_fit_dict_y_backup,
                                                self.res_params_x_backup, self.res_params_y_backup)

            self.gui_psd_a.update_msg_box()
        
        self.gui.update_error_msg()
        
        self.gui_psd_a.vb.setMouseEnabled(x = False, y = False)

        self.gui_psd_a_el_select.close()

        return

    def pt_selection_region_change_finished(self):
        if np.shape(self.gui_psd_a.idx)[0] < 1:
            self.gui_psd_a.pushButton_2.setDisabled(True)
        
        else:
            self.gui_psd_a.pushButton_2.setDisabled(False)

        return

    def create_fits_button_clicked(self):    
        self.fitting_enabled = 1
        self.enable_point_selection = 1
        self.gui_psd_a.pushButton_8.setDisabled(False)
        
        self.gui.setDisabled(True)
        self.gui_plots_2d.pushButton.setDisabled(True)

        first_element = self.selected_elements[0]        

        self.gui_psd_a.doubleSpinBox.setDisabled(True)
        self.gui_psd_a.pushButton.setDisabled(False)
        self.gui_psd_a.pushButton_2.setDisabled(True)
        self.gui_psd_a.pushButton_3.setDisabled(True)
        self.gui_psd_a.pushButton_4.setDisabled(True)
        self.gui_psd_a.pushButton_5.setDisabled(True)
        self.gui_psd_a.pushButton_6.setDisabled(True)
        self.gui_psd_a.pushButton_7.setDisabled(True)

        self.idx = 0

        self.gui_psd_a.enable_point_selection = 1
        self.gui_psd_a.plot_both_fits_enabled = 0

        if self.circular_beam_checked:
            self.gui_psd_a.ur_element = self.psd_dict[first_element][0]
            self.gui_psd_a.psd_a_element = self.psd_dict[first_element][2]

            self.gui_psd_a.update_psd_a_plot([first_element], self.psd_dict, self.n_ur_backup) # Brackets are needed since update_psd_a_plot expects an element array to sweep through
            
            self.gui_psd_a.label.setText("Select points for the data trend fitting of " + self.selected_element_strings[0] + ".")
            self.gui_psd_a.pushButton_3.setText("Select Noise Floor Points")

        else:
            self.gui_psd_a.plot_both_x_and_y_enabled = 0
            self.gui_psd_a.x_enabled = 1
            
            self.gui_psd_a.ur_x_element = self.psd_dict[first_element][0]
            self.gui_psd_a.ur_y_element = self.psd_dict[first_element][1]
            self.gui_psd_a.psd_a_x_element = self.psd_dict[first_element][3]
            self.gui_psd_a.psd_a_y_element = self.psd_dict[first_element][4]

            self.gui_psd_a.update_psd_a_plot_xy([first_element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled) # Brackets are needed since update_psd_a_plot expects an element array to sweep through

            self.gui_psd_a.label.setText("Select points for the data trend fitting of " + self.selected_element_strings[0] + " for <i>x</i>.")
            self.gui_psd_a.pushButton_3.setText("Select y Data Trend Points")

        self.gui_psd_a.pushButton_2.setText("Fit Data Trend Points")
        self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)

        self.gui_psd_a.lr.hide()

        self.gui_psd_a.widget.plotItem.vb.mouseDragEvent = self.gui_psd_a.create_pt_selection_box

        return

    def create_fits_cancel_button_clicked(self):
        if self.fitting_enabled:
            snr_disabled = 1

            self.gui_psd_a.enable_point_selection = 0
            self.gui_psd_a.plot_both_fits_enabled = 1

            self.gui.setDisabled(False)
            self.gui_plots_2d.pushButton.setDisabled(False)
        
            self.gui_psd_a.label.clear()
            self.gui_psd_a.label_4.clear()
            self.gui_psd_a.label_5.clear()
            self.gui_psd_a.pushButton.setDisabled(True)
            self.gui_psd_a.pushButton_2.setDisabled(True)
            self.gui_psd_a.pushButton_2.setText("")
            self.gui_psd_a.pushButton_3.setDisabled(True)
            self.gui_psd_a.pushButton_3.setText("")
            self.gui_psd_a.pushButton_4.setDisabled(True)
            self.gui_psd_a.pushButton_5.setDisabled(False)
            self.gui_psd_a.pushButton_6.setDisabled(False)
            self.gui_psd_a.pushButton_8.setDisabled(False)
        
            if self.circular_beam_checked:
                self.gui_psd_a.update_psd_a_plot(self.selected_elements, self.psd_dict, self.n_ur_backup, self.lin_fit_dict_backup, self.hor_fit_dict_backup, self.res_params_backup)

                for element in self.selected_elements:
                    if self.lin_fit_dict_backup.get(element) is not None:
                        self.gui_psd_a.doubleSpinBox.setDisabled(False)
                        self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)
                        self.gui_psd_a.pushButton_7.setDisabled(False)

                        snr_disabled = 0

                        break
            
                if snr_disabled:
                    self.gui_psd_a.doubleSpinBox.clear()
                    self.gui_psd_a.doubleSpinBox.setDisabled(True)
                    self.gui_psd_a.pushButton_7.setDisabled(True)
        
            else:
                self.gui_psd_a.x_enabled = 1
                self.gui_psd_a.plot_both_x_and_y_enabled = 1

                for element in self.selected_elements:
                    if self.lin_fit_dict_x_backup.get(element) is not None:
                        self.gui_psd_a.doubleSpinBox.setDisabled(False)
                        self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)
                        self.gui_psd_a.pushButton_7.setDisabled(False)

                        snr_disabled = 0

                        break
            
                if snr_disabled:
                    self.gui_psd_a.doubleSpinBox.clear()
                    self.gui_psd_a.doubleSpinBox.setDisabled(True)
                    self.gui_psd_a.pushButton_7.setDisabled(True)
            
                self.gui_psd_a.update_psd_a_plot_xy(self.selected_elements, self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, 
                                                    self.lin_fit_dict_x_backup, self.lin_fit_dict_y_backup, 
                                                    self.hor_fit_dict_x_backup, self.hor_fit_dict_y_backup, 
                                                    self.res_params_x_backup, self.res_params_y_backup)
                
                self.fitting_enabled = 0

        return

    def apply_fit_button_clicked(self):
        self.gui_psd_a.plot_both_fits_enabled = 0

        element = self.selected_elements[self.idx]
        
        text = self.gui_psd_a.label.text()

        if self.circular_beam_checked:
            ur_element = self.psd_dict[element][0]
            psd_a_element = self.psd_dict[element][2]
            
            ur_element_shaded = ur_element[self.gui_psd_a.idx]
            psd_a_element_shaded = psd_a_element[self.gui_psd_a.idx]
            
            if "data trend" in text:
                m, b_lin = np.polyfit(np.log10(ur_element_shaded), np.log10(psd_a_element_shaded), deg = 1)

                psd_a_lin_fit = 10**(m*np.log10(ur_element[1:]) + b_lin)

                self.lin_fit_dict[element] = [psd_a_lin_fit, m, b_lin]

                self.gui_psd_a.update_psd_a_plot([element], self.psd_dict, self.n_ur_backup, self.lin_fit_dict)
                self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                self.gui_psd_a.lr.hide()

                self.gui_psd_a.label_4.clear()
                self.gui_psd_a.label_4.setText(str(rc(m, ndec = 7)))
                self.gui_psd_a.label_5.clear()
                self.gui_psd_a.label_5.setText(str(rc(10**b_lin, ndec = 7)))
                self.gui_psd_a.pushButton_2.setDisabled(True)
                self.gui_psd_a.pushButton_3.setDisabled(False)
             
            elif "noise floor" in text:
                b_hor = np.mean(np.log10(psd_a_element_shaded))
                psd_a_hor_fit = 10**(b_hor*np.ones(len(ur_element) - 1))

                self.hor_fit_dict[element] = [psd_a_hor_fit, b_hor]

                self.gui_psd_a.update_psd_a_plot([element], self.psd_dict, self.n_ur_backup, self.hor_fit_dict)
                self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                self.gui_psd_a.lr.hide()

                self.gui_psd_a.pushButton_2.setDisabled(True)
                self.gui_psd_a.label_5.clear()
                self.gui_psd_a.label_5.setText(str(rc(10**b_hor, ndec = 7)))

                if self.idx == len(self.selected_elements) - 1:
                    self.gui_psd_a.pushButton_4.setDisabled(False)

                else:
                    self.gui_psd_a.pushButton_3.setDisabled(False)
       
        else:
            if "data trend" in text:
                if self.gui_psd_a.x_enabled:
                    ur_x_element = self.psd_dict[element][0]
                    psd_a_x_element = self.psd_dict[element][3]              
                    
                    ur_x_element_shaded = ur_x_element[self.gui_psd_a.idx]
                    psd_a_x_element_shaded = psd_a_x_element[self.gui_psd_a.idx]
                    
                    m_x, b_lin_x = np.polyfit(np.log10(ur_x_element_shaded), np.log10(psd_a_x_element_shaded), deg = 1)
                    psd_a_x_lin_fit = 10**(m_x*np.log10(ur_x_element[1:]) + b_lin_x)

                    self.lin_fit_dict_x[element] = [psd_a_x_lin_fit, m_x, b_lin_x]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, self.lin_fit_dict_x)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label_4.clear()
                    self.gui_psd_a.label_4.setText(str(rc(m_x, ndec = 7)))
                    self.gui_psd_a.label_5.clear()
                    self.gui_psd_a.label_5.setText(str(rc(10**b_lin_x, ndec = 7)))
                
                else:
                    ur_y_element = self.psd_dict[element][1]
                    psd_a_y_element = self.psd_dict[element][4]

                    ur_y_element_shaded = ur_y_element[self.gui_psd_a.idx]
                    psd_a_y_element_shaded = psd_a_y_element[self.gui_psd_a.idx]
                    
                    m_y, b_lin_y = np.polyfit(np.log10(ur_y_element_shaded), np.log10(psd_a_y_element_shaded), deg = 1)
                    psd_a_y_lin_fit = 10**(m_y*np.log10(ur_y_element[1:]) + b_lin_y)

                    self.lin_fit_dict_y[element] = [psd_a_y_lin_fit, m_y, b_lin_y]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, None, self.lin_fit_dict_y)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label_4.clear()
                    self.gui_psd_a.label_4.setText(str(rc(m_y, ndec = 7)))
                    self.gui_psd_a.label_5.clear()
                    self.gui_psd_a.label_5.setText(str(rc(10**b_lin_y, ndec = 7)))
                
                self.gui_psd_a.pushButton_2.setDisabled(True)
                self.gui_psd_a.pushButton_3.setDisabled(False)

            elif "noise floor" in text:
                if self.gui_psd_a.x_enabled:
                    ur_x_element = self.psd_dict[element][0]
                    psd_a_x_element = self.psd_dict[element][3]              
                    
                    ur_x_element_shaded = ur_x_element[self.gui_psd_a.idx]
                    psd_a_x_element_shaded = psd_a_x_element[self.gui_psd_a.idx]

                    b_hor_x = np.mean(np.log10(psd_a_x_element_shaded))
                    psd_a_x_hor_fit = 10**(b_hor_x*np.ones(len(ur_x_element) - 1))

                    self.hor_fit_dict_x[element] = [psd_a_x_hor_fit, b_hor_x]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, self.hor_fit_dict_x)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.pushButton_2.setDisabled(True)
                    self.gui_psd_a.pushButton_3.setDisabled(False)
                    self.gui_psd_a.label_5.clear()
                    self.gui_psd_a.label_5.setText(str(rc(10**b_hor_x, ndec = 7)))
                
                else:
                    ur_y_element = self.psd_dict[element][1]
                    psd_a_y_element = self.psd_dict[element][4]              
                    
                    ur_y_element_shaded = ur_y_element[self.gui_psd_a.idx]
                    psd_a_y_element_shaded = psd_a_y_element[self.gui_psd_a.idx]
                    
                    b_hor_y = np.mean(np.log10(psd_a_y_element_shaded))
                    psd_a_y_hor_fit = 10**(b_hor_y*np.ones(len(ur_y_element) - 1))

                    self.hor_fit_dict_y[element] = [psd_a_y_hor_fit, b_hor_y]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, None, self.hor_fit_dict_y)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.pushButton_2.setDisabled(True)
                    self.gui_psd_a.label_5.clear()
                    self.gui_psd_a.label_5.setText(str(rc(10**b_hor_y, ndec = 7)))

                    if self.idx == len(self.selected_elements) - 1:
                        self.gui_psd_a.pushButton_4.setDisabled(False)

                    else:
                        self.gui_psd_a.pushButton_3.setDisabled(False)

        return
    
    def next_fit_button_clicked(self):
        text = self.gui_psd_a.label.text()

        self.gui_psd_a.label_4.clear()
        self.gui_psd_a.label_5.clear()
        self.gui_psd_a.pushButton_2.setDisabled(True)
        self.gui_psd_a.pushButton_3.setDisabled(True)
        
        if self.circular_beam_checked:
            if "data trend" in text:
                element = self.selected_elements[self.idx]

                self.gui_psd_a.ur_element = self.psd_dict[element][0]
                self.gui_psd_a.psd_a_element = self.psd_dict[element][2]

                self.gui_psd_a.update_psd_a_plot([element], self.psd_dict, self.n_ur_backup)
                self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                self.gui_psd_a.lr.hide()

                self.gui_psd_a.label.setText("Select points for the noise floor fitting of " + self.selected_element_strings[self.idx] + ".")
                self.gui_psd_a.pushButton_2.setText("Fit Noise Floor Points")
            
                if self.idx == len(self.selected_elements) - 1:
                    self.gui_psd_a.pushButton_3.setText("")
                    self.gui_psd_a.pushButton_3.setDisabled(True)
            
                else:
                     self.gui_psd_a.pushButton_3.setText("Select Data Trend Points")

            elif "noise floor" in text:
                self.idx += 1

                element = self.selected_elements[self.idx]

                self.gui_psd_a.ur_element = self.psd_dict[element][0]
                self.gui_psd_a.psd_a_element = self.psd_dict[element][2]

                self.gui_psd_a.update_psd_a_plot([element], self.psd_dict, self.n_ur_backup)
                self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                self.gui_psd_a.lr.hide()

                self.gui_psd_a.label.setText("Select points for the data trend fitting of " + self.selected_element_strings[self.idx] + ".")
                self.gui_psd_a.pushButton_2.setText("Fit Data Trend Points")
                self.gui_psd_a.pushButton_3.setText("Select Noise Floor Points")
        
        else:
            if "data trend" in text:
                if self.gui_psd_a.x_enabled:
                    self.gui_psd_a.x_enabled = 0

                    element = self.selected_elements[self.idx]

                    self.gui_psd_a.ur_y_element = self.psd_dict[element][1]
                    self.gui_psd_a.psd_a_y_element = self.psd_dict[element][4]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label.setText("Select points for the data trend fitting of " + self.selected_element_strings[self.idx] + " for <i>y</i>.")
                    self.gui_psd_a.pushButton_3.setText("Select x Noise Floor Points")

                else:
                    self.gui_psd_a.x_enabled = 1

                    element = self.selected_elements[self.idx]

                    self.gui_psd_a.ur_x_element = self.psd_dict[element][0]
                    self.gui_psd_a.psd_a_x_element = self.psd_dict[element][3]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label.setText("Select points for the noise floor fitting of " + self.selected_element_strings[self.idx] + " for <i>x</i>.")
                    self.gui_psd_a.pushButton_2.setText("Fit Noise Floor Points")
                    self.gui_psd_a.pushButton_3.setText("Select y Noise Floor Points")

            elif "noise floor" in text:
                if self.gui_psd_a.x_enabled:
                    self.gui_psd_a.x_enabled = 0

                    element = self.selected_elements[self.idx]

                    self.gui_psd_a.ur_x_element = self.psd_dict[element][0]
                    self.gui_psd_a.psd_a_x_element = self.psd_dict[element][3]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label.setText("Select points for the noise floor fitting of " + self.selected_element_strings[self.idx] + " in <i>y</i>.")

                    if self.idx == len(self.selected_elements) - 1:
                        self.gui_psd_a.pushButton_3.setText("")
                        self.gui_psd_a.pushButton_3.setDisabled(True)
            
                    else:
                        self.gui_psd_a.pushButton_3.setText("Select x Data Trend Points")
                
                else:
                    self.idx += 1
                    
                    self.gui_psd_a.x_enabled = 1
                    
                    element = self.selected_elements[self.idx]

                    self.gui_psd_a.ur_x_element = self.psd_dict[element][0]
                    self.gui_psd_a.psd_a_x_element = self.psd_dict[element][3]

                    self.gui_psd_a.update_psd_a_plot_xy([element], self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled)
                    self.gui_psd_a.widget.addItem(self.gui_psd_a.lr)
                    self.gui_psd_a.lr.hide()

                    self.gui_psd_a.label.setText("Select points for the data trend fitting of " + self.selected_element_strings[self.idx] + " in <i>x</i>.")
                    self.gui_psd_a.pushButton_2.setText("Fit Data Trend Points")
                    self.gui_psd_a.pushButton_3.setText("Select y Data Trend Points")

    def finish_button_clicked(self):
        self.gui_psd_a.enable_point_selection = 0
        self.gui_psd_a.plot_both_fits_enabled = 1
        
        self.gui.setDisabled(False)
        self.gui_plots_2d.pushButton.setDisabled(False)

        self.gui_psd_a.label.clear()
        self.gui_psd_a.label_4.clear()
        self.gui_psd_a.label_5.clear()
        self.gui_psd_a.pushButton.setDisabled(True)
        self.gui_psd_a.pushButton_2.setDisabled(True)
        self.gui_psd_a.pushButton_2.setText("")
        self.gui_psd_a.pushButton_3.setDisabled(True)
        self.gui_psd_a.pushButton_3.setText("")
        self.gui_psd_a.pushButton_4.setDisabled(True)
        self.gui_psd_a.pushButton_5.setDisabled(False)
        self.gui_psd_a.pushButton_6.setDisabled(False)
        self.gui_psd_a.pushButton_7.setDisabled(False)
        self.gui_psd_a.pushButton_8.setDisabled(False)

        if self.circular_beam_checked:
            self.lin_fit_dict_backup = copy.deepcopy(self.lin_fit_dict)
            self.hor_fit_dict_backup = copy.deepcopy(self.hor_fit_dict)

            self.gui_psd_a.update_psd_a_plot(self.selected_elements, self.psd_dict, self.n_ur_backup, self.lin_fit_dict, self.hor_fit_dict)
        
        else:
            self.gui_psd_a.x_enabled = 1
            self.gui_psd_a.plot_both_x_and_y_enabled = 1

            self.lin_fit_dict_x_backup = copy.deepcopy(self.lin_fit_dict_x)
            self.lin_fit_dict_y_backup = copy.deepcopy(self.lin_fit_dict_y)
            self.hor_fit_dict_x_backup = copy.deepcopy(self.hor_fit_dict_x)
            self.hor_fit_dict_y_backup = copy.deepcopy(self.hor_fit_dict_y)

            self.gui_psd_a.update_psd_a_plot_xy(self.selected_elements, self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, 
                                                self.lin_fit_dict_x, self.lin_fit_dict_y, 
                                                self.hor_fit_dict_x, self.hor_fit_dict_y)

        self.gui_psd_a.doubleSpinBox.setDisabled(False)
        self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)
        
        return

    def calculate_res_button_clicked(self):
        self.snr_cutoff = self.gui_psd_a.doubleSpinBox.value()
        
        self.gui_psd_a.doubleSpinBox.setValue(self.snr_cutoff)

        self.gui.menuResolution_Parameter_Summary.setDisabled(False)
        
        if self.circular_beam_checked:
            for element in self.selected_elements:
                if self.lin_fit_dict.get(element) is not None:
                    m = self.lin_fit_dict[element][1]
                    b_lin = self.lin_fit_dict[element][2]
                    b_hor = self.hor_fit_dict[element][1]

                    psd_a_cutoff = self.snr_cutoff*(10**b_hor)
                    ur_cutoff_inv_um = (psd_a_cutoff*10**-b_lin)**(1/m)
                    dr_hp_um = 0.5/ur_cutoff_inv_um

                    self.res_params[element] = [psd_a_cutoff, ur_cutoff_inv_um, dr_hp_um]

            self.res_params_backup = copy.deepcopy(self.res_params)

            self.gui_psd_a_res_params.update_res_params(self.elements_backup, self.lin_fit_dict, self.res_params)

            self.gui_psd_a.update_psd_a_plot(self.selected_elements, self.psd_dict, self.n_ur_backup, self.lin_fit_dict, self.hor_fit_dict, self.res_params)

            self.gui.actionNon_Circular_X_ray_Beam.setDisabled(True)
            self.gui.actionCircular_X_ray_Beam.setDisabled(False)
            
        else:
            for element in self.selected_elements:
                if self.lin_fit_dict_x.get(element) is not None:
                    m_x = self.lin_fit_dict_x[element][1]
                    m_y = self.lin_fit_dict_y[element][1]
                    b_lin_x = self.lin_fit_dict_x[element][2]
                    b_lin_y = self.lin_fit_dict_y[element][2]
                    b_hor_x = self.hor_fit_dict_x[element][1]
                    b_hor_y = self.hor_fit_dict_y[element][1]

                    psd_a_x_cutoff = self.snr_cutoff*(10**b_hor_x)
                    psd_a_y_cutoff = self.snr_cutoff*(10**b_hor_y)
                    ur_x_cutoff_inv_um = (psd_a_x_cutoff*10**-b_lin_x)**(1/m_x)
                    ur_y_cutoff_inv_um = (psd_a_y_cutoff*10**-b_lin_y)**(1/m_y)
                    dr_hp_x_um = 0.5/ur_x_cutoff_inv_um
                    dr_hp_y_um = 0.5/ur_y_cutoff_inv_um

                    self.res_params_x[element] = [psd_a_x_cutoff, ur_x_cutoff_inv_um, dr_hp_x_um]
                    self.res_params_y[element] = [psd_a_y_cutoff, ur_y_cutoff_inv_um, dr_hp_y_um]

            self.res_params_x_backup = copy.deepcopy(self.res_params_x)
            self.res_params_y_backup = copy.deepcopy(self.res_params_y)

            self.gui_psd_a_res_params_xy.update_res_params_xy(self.elements_backup, self.lin_fit_dict_x, self.lin_fit_dict_y, self.res_params_x, self.res_params_y)

            self.gui_psd_a.update_psd_a_plot_xy(self.selected_elements, self.psd_dict, self.n_ur_backup, self.gui_psd_a.x_enabled, self.lin_fit_dict_x, 
                                                self.lin_fit_dict_y, self.hor_fit_dict_x, self.hor_fit_dict_y, 
                                                self.res_params_x, self.res_params_y)
            
            self.gui.actionCircular_X_ray_Beam.setDisabled(True)
            self.gui.actionNon_Circular_X_ray_Beam.setDisabled(False)

    def batch_export_img_button_clicked(self):
        self.gui.setDisabled(True)
        self.gui_plots_2d.setDisabled(True)
        self.gui_psd_a.setDisabled(True)

        current_element_index = self.gui_plots_2d.comboBox.currentIndex()
        
        export_path = []
        file_name = []

        if self.exp_backup is not None:
            exp_path = self.exp_backup
        
        else:
            exp_path = self.gui_directory

        loaded_file_index = self.gui.comboBox.currentIndex()
        default_filename = self.name_list[loaded_file_index].split(".")[0]
        default_file_path = os.path.join(exp_path, default_filename)

        file_name = QtWidgets.QFileDialog.getSaveFileName(self.gui, "Select elemental image/2D PSD file root name", default_file_path, "SVG Files (*.svg)")[0]

        if file_name == "" or file_name == []:
            self.gui.setDisabled(False)
            self.gui_plots_2d.setDisabled(False)
            self.gui_psd_a.setDisabled(False)

            return
        
        exp_path = os.path.dirname(file_name)

        self.exp_backup = copy.copy(exp_path)

        if self.platform == "Darwin" or self.platform == "Linux":
            file_name = file_name.split("/")[-1]
        
        elif self.platform == "Windows":
            file_name = file_name.split("\\")[-1]

        file_name = file_name.split(".")[0]

        subdir_name = ["elemental_images", "2d_psd_plots"]
        
        if self.circular_beam_checked:
            for j in range(len(self.elements_string_backup)):
                element = self.elements_backup[j]
                element_string = self.elements_string_backup[j]
            
                if self.smoothing_checked:
                    self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                                      self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                                      self.sigma_backup, self.alpha_backup)
        
                else:
                    self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                                      self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

                for i in range(2):
                    export_path.append(os.path.join(exp_path, subdir_name[i]))
        
                    os.makedirs(export_path[i], exist_ok = True)

                    if i == 0:
                        elemental_img = self.im_orig[element]

                        filename = "el_img_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".svg"

                        QtWidgets.QApplication.processEvents()
                    
                        self.gui_plots_2d.widget.plotItem.writeSvg(filepath)
                    
                        filename = "el_img_data_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".csv"

                        with open(filepath, 'w') as f:
                            writer = csv.writer(f)
                        
                            writer.writerows(elemental_img)
                
                    if i == 1:
                        psd_2d = self.psd_dict[element][1]

                        filename = "psd_2d" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".svg"
            
                        QtWidgets.QApplication.processEvents()
                    
                        self.gui_plots_2d.widget_2.plotItem.writeSvg(filepath)

                        filename = "psd_2d_data_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".csv"

                        with open(filepath, 'w') as f:
                            writer = csv.writer(f)
                        
                            writer.writerows(psd_2d)
        
        else:
            for j in range(len(self.elements_string_backup)):
                element = self.elements_backup[j]
                element_string = self.elements_string_backup[j]
            
                if self.smoothing_checked:
                    self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                                      self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                                      self.sigma_backup, self.alpha_backup)
        
                else:
                    self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                                      self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

                for i in range(2):
                    export_path.append(os.path.join(exp_path, subdir_name[i]))
        
                    os.makedirs(export_path[i], exist_ok = True)

                    if i == 0:
                        elemental_img = self.im_orig[element]

                        filename = "el_img_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".svg"

                        QtWidgets.QApplication.processEvents()
                    
                        self.gui_plots_2d.widget.plotItem.writeSvg(filepath)
                    
                        filename = "el_img_data_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".csv"

                        with open(filepath, 'w') as f:
                            writer = csv.writer(f)
                        
                            writer.writerows(elemental_img)
                
                    if i == 1:
                        psd_2d = self.psd_dict[element][2]

                        filename = "psd_2d" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".svg"
            
                        QtWidgets.QApplication.processEvents()
                    
                        self.gui_plots_2d.widget_2.plotItem.writeSvg(filepath)

                        filename = "psd_2d_data_" + file_name + "_" + element_string
                        filepath = os.path.join(export_path[i], filename) + ".csv"

                        with open(filepath, 'w') as f:
                            writer = csv.writer(f)
                        
                            writer.writerows(psd_2d)

        element = self.elements_backup[current_element_index]

        self.gui.setDisabled(False)
        self.gui_plots_2d.setDisabled(False)
        self.gui_psd_a.setDisabled(False)

        if self.smoothing_checked:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um, 
                                              self.sigma_backup, self.alpha_backup)
        
        else:
            self.gui_plots_2d.update_2d_plots(element, self.im, self.psd_dict, 
                                              self.gamma, self.lower_quantile, self.upper_quantile, self.dx_um, self.dy_um)

        return

    def export_psd_a_button_clicked(self):
        self.gui.setDisabled(True)
        self.gui_plots_2d.setDisabled(True)
        self.gui_psd_a.setDisabled(True)
        
        file_name = []
        
        if self.exp_backup is not None:
            exp_path = self.exp_backup
        
        else:
            exp_path = self.gui_directory

        loaded_file_index = self.gui.comboBox.currentIndex()
        default_filename = self.name_list[loaded_file_index].split(".")[0]
        default_file_path = os.path.join(exp_path, default_filename)

        file_name = QtWidgets.QFileDialog.getSaveFileName(self.gui, "Select azimuthal PSD file root name", default_file_path, "SVG Files (*.svg)")[0]

        if file_name == "" or file_name == []:
            self.gui.setDisabled(False)
            self.gui_plots_2d.setDisabled(False)
            self.gui_psd_a.setDisabled(False)

            return

        exp_path = os.path.dirname(file_name)

        self.exp_backup = exp_path
        
        if self.platform == "Darwin" or self.platform == "Linux":
            file_name = file_name.split("/")[-1]
        
        elif self.platform == "Windows":
            file_name = file_name.split("\\")[-1]
        
        file_name = file_name.split(".")[0]

        subdir_name = "psd_a"

        export_path = os.path.join(exp_path, subdir_name)
        os.makedirs(export_path, exist_ok = True)

        if self.circular_beam_checked:
            filename = "psd_a_" + file_name
            filepath = os.path.join(export_path, filename) + ".svg"

            QtWidgets.QApplication.processEvents()
            QtWidgets.QApplication.processEvents()
                    
            self.gui_psd_a.widget.plotItem.writeSvg(filepath)
 
            for j in range(len(self.selected_elements)):
                headings_1 = ["nx", "ny", "dx (" + self.mu + "m)", "dy (" + self.mu + "m)", "n_ur"]
                headings_2 = ["u_r (" + self.mu + "m^-1)", "S(u_r)"]

                element = self.selected_elements[j]
                element_string = self.selected_element_strings[j]

                filename = "psd_a_data_" + file_name + "_" + element_string
                filepath = os.path.join(export_path, filename) + ".csv"
                    
                ur = self.psd_dict[element][0]
                psd_a = self.psd_dict[element][2]
            
                if self.res_params.get(element) is not None:
                    psd_a_lin_fit = self.lin_fit_dict[element][0]
                    psd_a_hor_fit = self.hor_fit_dict[element][0]
                    m = self.lin_fit_dict[element][1]
                    b_lin = self.lin_fit_dict[element][2]
                    b_hor = self.hor_fit_dict[element][1]
                    ur_cutoff_inv_um = self.res_params[element][1]
                    dr_hp_um = self.res_params[element][2]

                    headings_1.extend(["m_lin (" + self.mu + "m)", "b_lin", "b_hor", "u_res (" + self.mu + "m^-1)", 
                                       self.delta + "_res (" + self.mu + "m)"])
                    headings_2.extend(["S_dtf(u_r)", "S_nff(u_r)"])

                    data_headings1 = [self.nx_backup, self.ny_orig, self.dx_um_orig, self.dy_um_orig, 
                                      self.n_ur_backup, m, 10**b_lin, 10**b_hor, ur_cutoff_inv_um, dr_hp_um]
                    
                    data_headings2_line1 = [ur[0], psd_a[0]]
                    data_headings2_rest = np.column_stack((ur[1:], psd_a[1:], psd_a_lin_fit, psd_a_hor_fit))

                    with open(filepath, 'w', newline = "", encoding = 'utf-8-sig') as f:
                        writer = csv.writer(f)
                        
                        writer.writerow(headings_1)
                        writer.writerow(data_headings1)
                        writer.writerow("\n")
                        writer.writerow(headings_2)
                        writer.writerow(data_headings2_line1)
                        writer.writerows(data_headings2_rest)

                else:
                    data_headings1 = [self.nx_backup, self.ny_orig, self.dx_um_orig, self.dy_um_orig, self.n_ur_backup]
                    data_headings2 = np.column_stack((ur, psd_a))

                    with open(filepath, 'w', newline = "", encoding = 'utf-8') as f:
                        writer = csv.writer(f)

                        writer.writerow(headings_1)
                        writer.writerow(data_headings1)
                        writer.writerow("\n")
                        writer.writerow(headings_2)
                        writer.writerows(data_headings2)

            if len(self.res_params) > 0:
                filename = "psd_a_slope_res_outputs_" + file_name
                filepath = os.path.join(export_path, filename) + ".csv"

                headings_3 = ["Element", "m (" + self.mu + "m)", "u_res (" + self.mu + "m^-1)", self.delta + "_res (" + self.mu + "m)"]

                with open(filepath, 'w', newline = "", encoding = 'utf-8-sig') as f:
                    writer = csv.writer(f)

                    writer.writerow(headings_3)
                
                    for j in range(len(self.elements_backup)):
                        element = self.elements_backup[j]
                        element_string = self.elements_string[j]

                        if self.res_params.get(element) is not None:
                            m = self.lin_fit_dict[element][1]
                            ur_cutoff_inv_um = self.res_params[element][1]
                            dr_hp_um = self.res_params[element][2]
                    
                            writer.writerow([element_string, m, ur_cutoff_inv_um, dr_hp_um])
        
        else:
            filename = "psd_a_xy_" + file_name
            filepath = os.path.join(export_path, filename) + ".svg"

            QtWidgets.QApplication.processEvents()
            QtWidgets.QApplication.processEvents()
                    
            self.gui_psd_a.widget.plotItem.writeSvg(filepath)

            for j in range(len(self.selected_elements)):
                headings_1 = ["nx", "ny", "dx (" + self.mu + "m)", "dy (" + self.mu + "m)" ,"n_ur"]
                headings_2 = ["u_r,x (" + self.mu + "m^-1)", "S_x(u_r)"]
                headings_3 = ["u_r,y (" + self.mu + "m^-1)", "S_y(u_r)"]

                element = self.selected_elements[j]
                element_string = self.selected_element_strings[j]

                filename = "psd_a_xy_data_" + file_name + "_" + element_string
                filepath = os.path.join(export_path, filename) + ".csv"

                ur_x = self.psd_dict[element][0]
                ur_y = self.psd_dict[element][1]
                psd_a_x = self.psd_dict[element][3]
                psd_a_y = self.psd_dict[element][4]

                if self.res_params_x.get(element) is not None:
                    psd_a_x_lin_fit = self.lin_fit_dict_x[element][0]
                    psd_a_y_lin_fit = self.lin_fit_dict_y[element][0]
                    psd_a_x_hor_fit = self.hor_fit_dict_x[element][0]
                    psd_a_y_hor_fit = self.hor_fit_dict_y[element][0]

                    m_x = self.lin_fit_dict_x[element][1]
                    m_y = self.lin_fit_dict_y[element][1]
                    
                    b_lin_x = self.lin_fit_dict_x[element][2]
                    b_lin_y = self.lin_fit_dict_y[element][2]
                    b_hor_x = self.hor_fit_dict_x[element][1]
                    b_hor_y = self.hor_fit_dict_y[element][1]
                    
                    ur_x_cutoff_inv_um = self.res_params_x[element][1]
                    ur_y_cutoff_inv_um = self.res_params_y[element][1]
                    
                    dr_x_hp_um = self.res_params_x[element][2]
                    dr_y_hp_um = self.res_params_y[element][2]

                    headings_1.extend(["m_lin,x (" + self.mu + "m)", "m_lin,y (" + self.mu + "m)", 
                                       "b_lin,x", "b_lin,y", "b_hor,x", "b_hor,y", "u_res,x (" + self.mu + "m^-1)",
                                       "u_res,y (" + self.mu + "m^-1)", self.delta + "_res,x (" + self.mu + "m)", self.delta + "_res,y (" + self.mu + "m)"])
                    headings_2.extend(["S_x,dtf(u_r)", "S_x,nff"])
                    headings_3.extend(["S_y,dtf(u_r)", "S_y,nff"])

                    data_headings1 = [self.nx_backup, self.ny_backup, self.dx_um_orig, self.dy_um_orig, 
                                      self.n_ur_backup, m_x, m_y, 10**b_lin_x, 10**b_lin_y, 10**b_hor_x, 10**b_hor_y, ur_x_cutoff_inv_um, ur_y_cutoff_inv_um, 
                                      dr_x_hp_um, dr_y_hp_um]
                    
                    data_headings2_line1 = [ur_x[0], psd_a_x[0]]
                    data_headings2_rest = np.column_stack((ur_x[1:], psd_a_x[1:], psd_a_x_lin_fit, psd_a_x_hor_fit))

                    data_headings3_line1 = [ur_y[0], psd_a_y[0]]
                    data_headings3_rest = np.column_stack((ur_y[1:], psd_a_y[1:], psd_a_y_lin_fit, psd_a_y_hor_fit))

                    with open(filepath, 'w', newline = "", encoding = 'utf-8-sig') as f:
                        writer = csv.writer(f)
                        
                        writer.writerow(headings_1)
                        writer.writerow(data_headings1)
                        writer.writerow("\n")
                        writer.writerow(headings_2)
                        writer.writerow(data_headings2_line1)
                        writer.writerows(data_headings2_rest)
                        writer.writerow("\n")
                        writer.writerow(headings_3)
                        writer.writerow(data_headings3_line1)
                        writer.writerows(data_headings3_rest)
                
                else:
                    data_headings1 = [self.nx_backup, self.ny_backup, self.dx_um_backup, self.dy_um_orig, self.n_ur_backup]
                    data_headings2 = np.column_stack((ur_x, psd_a_x))
                    data_headings3 = np.column_stack((ur_y, psd_a_y))

                    with open(filepath, 'w', newline = "", encoding = 'utf-8') as f:
                        writer = csv.writer(f)

                        writer.writerow(headings_1)
                        writer.writerow(data_headings1)
                        writer.writerow("\n")
                        writer.writerow(headings_2)
                        writer.writerows(data_headings2)
                        writer.writerow("\n")
                        writer.writerow(headings_3)
                        writer.writerows(data_headings3)

            if len(self.res_params_x) > 0:
                filename = "psd_a_slope_res_xy_outputs_" + file_name
                filepath = os.path.join(export_path, filename) + ".csv"

                headings_4 = ["Element", "m_x (" + self.mu + "m)", "m_y (" + self.mu + "m)",
                              "u_res,x (" + self.mu + "m^-1)", "u_res,y (" + self.mu + "m^-1)", 
                              self.delta + "_res,x (" + self.mu + "m)", self.delta + "_res,y (" + self.mu + "m)"]
                
                with open(filepath, 'w', newline = "", encoding = 'utf-8-sig') as f:
                    writer = csv.writer(f)

                    writer.writerow(headings_4)
                
                    for j in range(len(self.elements_backup)):
                        element = self.elements_backup[j]
                        element_string = self.elements_string[j]

                        if self.res_params_x.get(element) is not None:
                            m_x = self.lin_fit_dict_x[element][1]
                            m_y = self.lin_fit_dict_y[element][1]
                            
                            ur_x_cutoff_inv_um = self.res_params_x[element][1]
                            ur_y_cutoff_inv_um = self.res_params_y[element][1]
                            
                            dr_x_hp_um = self.res_params_x[element][2]
                            dr_y_hp_um = self.res_params_y[element][2]
                    
                            writer.writerow([element_string, m_x, m_y, ur_x_cutoff_inv_um, ur_y_cutoff_inv_um, dr_x_hp_um, dr_y_hp_um])

        self.gui.setDisabled(False)
        self.gui_plots_2d.setDisabled(False)
        self.gui_psd_a.setDisabled(False)

        return

if __name__ == "__main__":
    psd_launch()