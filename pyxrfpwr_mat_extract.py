# PyXRFPower: Matlab file handler
# File: pyxrfpower_mat_extract.py
# Author: B. Roter

# This XRF program converts a complex nest of Matlab structures into a dictionary to mimic an HDF5 file format
# and returns the following variables:
    # element_byte_new = Element peaks (exluding escape and scattering peaks) as bytes (bytes instead of strings as to mimic the HDF5 file format)
    # intensity_ug_cm2_ordered_array OR intensity_cts_ordered_array = Dictionary of 2D elemental image arrays (in ug/cm^2, if available, or cts/s, if not)
    # nx = # of pixels in x (see mote!)
    # ny = # of pixels in y (see mote!)
    # dx_um = Length of each pixel in x in units of microns (see note!)
    # dy_um = Length of each pixel in y in units of microns (see note!)

# Note: The images were scanned in one direction, and the data was processed using the same indexing
# scheme, but the data returned from this function is in the direction TRANSVERSE to 
# the scan direction
    # In other words:
        # The pixel numbers were flipped, the x and y coordinates were flipped, and the
        # resulting image arrays were transposed
        # The resulting images will differ from their HDF5 counterparts by a reflection about the horizontal axis, and then by 90 degrees counterclockwise
        # For the remainder of the code, images and variables associated with x and y are going to be referring to the
        # new indexing scheme

# To include a different Matlab file structure, please contact benjaminroter2026@u.northwestern.edu

from pymatreader import read_mat as rm

import numpy as np

def extractmat(file_name):
    mu = "\u03BC"
    
    matlab_data = {}
    
    matlab_data = rm(file_name) # Convert Matlab file structure to Python-like dictionary

    handles = matlab_data["handles"]

    xrf = handles["XRF"]
    fit_struct = handles["fit_struct"][-1] # The index of -1 refers to the final position of handles["fit_struct"], 
                                           # which contains data related to average values over all detector elements
    elements = fit_struct["names"]
    units = fit_struct["units"]

    elements_byte = np.array([bytes(element, 'utf-8') for element in elements])
    units_byte = np.array([bytes(unit, 'utf-8') for unit in units])
    
    elements_byte_new = []
    units_byte_new = []

    ny = int(xrf["num_x"])
    nx = int(xrf["num_y"])
    x = xrf["Y"]
    y = xrf["X"]
    length_scale = xrf["X_units"] # Length scale of the motors used during scanning

    elements_entries_to_ignore = [b'Compton', b'Elastic']
    
    for element in elements_byte:
        if b'escape' in element:
            elements_entries_to_ignore.append(element)
        
        if element not in elements_entries_to_ignore:
            elements_byte_new.append(element)
            
            element_index = np.ndarray.item(np.where(np.array(elements_byte_new) == element)[0])
            
            units_byte_new.append(units_byte[element_index])

    n_elements = len(elements_byte_new)
    
    no_mass_calibration = np.where(np.array(units_byte_new) == b'cts/ic')[0]

    if len(no_mass_calibration) == 0:
        intensity_ug_cm2 = fit_struct["calibrated"][:n_elements]

        intensity_ug_cm2_new = np.reshape(intensity_ug_cm2, [n_elements, ny, nx], order = 'F') # 'F' = Fortran-like indexing scheme

    else:
        intensity_cts_per_ion_chamber = fit_struct["c"][:n_elements] # Normalized counts (cts/upstream ion chamber reading)
        t_live = xrf["LTime"]

        scalars = fit_struct["scalars"]
        ic_label = fit_struct["ic_label"]

        if ic_label == "US_IC":
            I = scalars["US_IC"]
        
        elif ic_label == "DS_IC":
            I = scalars["DS_IC"]
        
        intensity_cts_per_ion_chamber = np.reshape(intensity_cts_per_ion_chamber, [n_elements, ny, nx], order = 'F')
        I = np.reshape(I, [ny, nx], order = 'F')
        t_live = np.reshape(t_live, [ny, nx], order = 'F')

        I_nan_idx = np.where(np.isnan(I)) # Find dead pixel locations in normalized intensity array

        I[I_nan_idx] = 0 # Set dead pixel values to zero

        intensity_cts = np.empty((n_elements, ny, nx))
        
        for j in range(n_elements):
            intensity_cts[j] = intensity_cts_per_ion_chamber[j]*np.mean(I) # Convert from ug/cm^2 to cts for each element (use average ion chamber readings to reduce noise)
    
    x = np.reshape(x, [ny, nx], order = 'F') # Reshape x coordinate array into an ny x nx array
    y = np.reshape(y, [ny, nx], order = 'F') # Reshape y coordinate array into an ny by nx array

    x1 = x[0][0]
    x2 = x[0][-1]

    y1 = y[0][0]
    y2 = y[-1][0]

    dx = np.abs(x2 - x1)/(nx - 1)
    dy = np.abs(y2 - y1)/(ny - 1)
    
    if length_scale == "um" or length_scale == (mu + "m") or length_scale == "micron" or length_scale == "microns" or length_scale == "micrometer" or length_scale == "micrometers" or length_scale == "micrometre" or length_scale == "micrometres":
        dx_um = dx
        dy_um = dy

    elif length_scale == "mm" or length_scale == "millimeter" or length_scale == "millimeters" or length_scale == "millimetre" or length_scale == "millimetres":
        dx_um = dx*1e3
        dy_um = dy*1e3

    elif length_scale == "cm" or length_scale == "centimeter" or length_scale == "centimeters" or length_scale == "centimetre" or length_scale == "centimetres":
        dx_um = dx*1e4
        dy_um = dy*1e4

    elif length_scale == "m" or length_scale == "meter" or length_scale == "meters" or length_scale == "metre" or length_scale == "metres":
        dx_um = dx*1e6
        dy_um = dy*1e6

    if len(no_mass_calibration) == 0:
        intensity_ug_cm2_ordered_array = []
        
        for j in range(n_elements):
            intensity_ug_cm2_ordered = np.rot90(intensity_ug_cm2_new[j], k = 1)
            intensity_ug_cm2_ordered = np.flip(intensity_ug_cm2_ordered, axis = 0)

            intensity_ug_cm2_ordered_array.append(intensity_ug_cm2_ordered)
        
        nx, ny = ny, nx
        dx_um, dy_um = dy_um, dx_um

        return np.array(elements_byte_new), intensity_ug_cm2_ordered_array, nx, ny, dx_um, dy_um
    
    else:
        intensity_cts_ordered_array = []
        
        for j in range(n_elements):
            intensity_cts_ordered = np.rot90(intensity_ug_cm2_new[j], k = 1)
            intensity_cts_ordered = np.flip(intensity_cts_ordered, axis = 0)

            intensity_cts_ordered_array.append(intensity_cts_ordered)
        
        nx, ny = ny, nx
        dx_um, dy_um = dy_um, dx_um

        return np.array(elements_byte_new), intensity_cts_ordered_array, nx, ny, dx_um, dy_um