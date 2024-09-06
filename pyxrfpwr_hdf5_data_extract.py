# PyXRFPower: HDF5 file handler
# File: pyxrfpwr_hdf5_data_extract.py
# Author: B. Roter

# This program extracts relevant X-ray fluorescence data from synchrotron light source HDF5 files for the use with the XRFPower interface

# To include an HDF5 file structure from a different synchrotron, please contact benjaminroter2026@u.northwestern.edu.

# The following parameters are returned:
   # Element names
   # Intensity maps (in units of either µg/cm^2 or cts/s)
   # nx = # of pixels in x
   # ny = # of pixels in y
   # dx_um = Length of each pixel in x (µm)
   # dy_um = Length of each pixel in y (µm)

def extracth5data(h5file, synchrotron):
   import h5py, numpy as np

   h5 = h5py.File(h5file, 'r') # Store the file path
    
   if synchrotron == "Advanced Photon Source (APS)":
      if "MAPS/XRF_Analyzed/NNLS" in h5.keys():
         counts_h5 = h5['MAPS/XRF_Analyzed/NNLS/Counts_Per_Sec'] # Extract photon fluxes for each pixel
         elements_h5 = h5['MAPS/XRF_Analyzed/NNLS/Channel_Names'] # Extract element, parameter names
      
      elif "MAPS/XRF_Analyzed/Fitted" in h5.keys():
         counts_h5 = h5['MAPS/XRF_Analyzed/Fitted/Counts_Per_Sec']
         elements_h5 = h5['MAPS/XRF_Analyzed/Fitted/Channel_Names']

      nx_h5 = h5['MAPS/Scan/x_axis']
      ny_h5 = h5['MAPS/Scan/y_axis']
      
      elements = elements_h5[()]
      counts = counts_h5[()]
      nx_conv = ny_h5[()] # Width and height are reversed in the actual HDF5 data structure
      ny_conv = nx_h5[()] # Width and height are reversed in the actual HDF5 data structure

      nx = len(nx_conv)
      ny = len(ny_conv) - 2 # MAPS tacks on two extra values for whatever reason

      elements_entries_to_ignore = [b'Ar_Ar', b'COMPTON_AMPLITUDE', 
                                    b'COHERENT_SCT_AMPLITUDE', b'Num_Iter', 
                                    b'Fit_Residual', b'Total_Fluorescence_Yield',
                                    b'Sum_Elastic_Inelastic']

      if "MAPS/Quantification" in h5.keys():
         calib_curve_labels_h5 = h5['MAPS/Quantification/Calibration/NNLS/Calibration_Curve_Labels']
         calib_usic_h5 = h5['MAPS/Quantification/Calibration/NNLS/Calibration_Curve_US_IC']
         scaler_names_h5 = h5['MAPS/Scalers/Names']
         scaler_values_h5 = h5['MAPS/Scalers/Values']

         calib_curve_labels = calib_curve_labels_h5[()]
         calib_usic = calib_usic_h5[()] # Normalize by upstream ion chamber readings
         scaler_names = scaler_names_h5[()]
         scaler_values = scaler_values_h5[()]

         us_ic_scaler_values_idx = np.ndarray.item(np.where(scaler_names == b'US_IC')[0])
         
         us_ic_scaler_values = scaler_values[us_ic_scaler_values_idx][:, :-2]

         calib_curve_labels_k_shell = calib_curve_labels[0]
         calib_curve_labels_l_shell = calib_curve_labels[1]
         calib_curve_labels_m_shell = calib_curve_labels[2]

         calib_usic_k_shell = calib_usic[0]
         calib_usic_l_shell = calib_usic[1]
         calib_usic_m_shell = calib_usic[2]

         ug_cm2_ordered_array = []
         new_element_array = []
      
         for element in elements:
            if element not in elements_entries_to_ignore:
               element_index = np.ndarray.item(np.where(elements == element)[0])

               counts_new = counts[element_index][:, :-2] # MAPS tacks on two extra columns of zeroes post-scan for whatever reason

               if b'_L' in element:
                  element_index_2 = np.ndarray.item(np.where(calib_curve_labels_l_shell == element)[0])

                  ug_cm2 = counts_new/us_ic_scaler_values/calib_usic_l_shell[element_index_2]

               elif b'_M' in element:
                  element_index_2 = np.ndarray.item(np.where(calib_curve_labels_m_shell == element)[0])
   
                  ug_cm2 = counts_new/us_ic_scaler_values/calib_usic_m_shell[element_index_2]

               else:
                  element_index_2 = np.ndarray.item(np.where(calib_curve_labels_k_shell == element)[0])

                  ug_cm2 = counts_new/us_ic_scaler_values/calib_usic_k_shell[element_index_2]

               ug_cm2_ordered_array.append(ug_cm2)
               new_element_array.append(element)

      else:
         counts_ordered_array = []
         new_element_array = []

         scaler_names_h5 = h5['MAPS/Scalers/Names']
         scaler_values_h5 = h5['MAPS/Scalers/Values']

         scaler_values = scaler_values_h5[()]
         scaler_names = scaler_names_h5[()]

         us_ic_scaler_values_idx = np.ndarray.item(np.where(scaler_names == b'US_IC')[0])

         us_ic_scaler_values = scaler_values[us_ic_scaler_values_idx][:, :-2]
         
         for element in elements:
            if element not in elements_entries_to_ignore:
               element_index = np.ndarray.item(np.where(elements == element)[0])

               counts_ordered = counts[element_index][:, :-2] # MAPS tacks on two extra columns of zeroes post-scan for whatever reason

               counts_ordered_array.append(counts_ordered)
               new_element_array.append(element)
    
      # Get corresponding pixel spacings
      
      dx_um = 1e3*np.abs(nx_conv[-1] - nx_conv[0])/(nx - 1)
      dy_um = 1e3*np.abs(ny_conv[-3] - ny_conv[0])/(ny - 1)
      
      nx, ny = ny, nx
      dx_um, dy_um = dy_um, dx_um

    
      if "MAPS/Quantification" in h5.keys():
         return np.array(new_element_array), ug_cm2_ordered_array, nx, ny, dx_um, dy_um
      
      else:
         return np.array(new_element_array), counts_ordered_array, nx, ny, dx_um, dy_um
      
   elif synchrotron == "National Synchrotron Light Source II (NSLS-II)":         
      elements_h5 = h5["xrfmap/detsum/xrf_fit_name"]
      counts_h5 = h5["xrfmap/detsum/xrf_fit"]
      axis_coords_h5 = h5["xrfmap/positions/pos"]

      elements = elements_h5[()]
      counts = counts_h5[()]
      axis_coords = axis_coords_h5[()]

      x = axis_coords[0]
      y = axis_coords[1]

      nx = np.shape(x)[1]
      ny = np.shape(y)[0]

      dx_um = np.abs(x[0][-1] - x[0][0])/(nx - 1)
      dy_um = np.abs(y[-1][0] - y[0][0])/(ny - 1)
            
      return elements, counts, nx, ny, dx_um, dy_um