# File: psd_calc.py
# Author: Ben Roter
# Adapted from C. Jacobsen and B. Hoernberger (1998)

# This program calculates the 2D power spectral density of a 2D array, as well as the 1D, azimuthally averaged power spectral density of the same 2D array


# Inputs to function: 2D array (array)
#           `         Pixel spacing in x-dxn (dx)
#                     Pixel spacing in y-dxn (dy)
#                     Number of pixels in x-dxn (nx)
#                     Number of pixels in y-dxn (ny)
#                     Number of radial frequency bins (n_ur) 
#                     A flag indicating whether or not an isotropic beam is used (if not, separate x and y PSDs will be calculated)

# CAUTION: ALL LENGTH AND SPATIAL FREQUENCY SCALES ARE IN MICROMETERS AND MICROMETERS^-1, RESPECTIVELY

def psd(array, dx_um, dy_um, nx, ny, n_ur, circular_beam):
    import numpy as np
    
    from numpy.fft import fft2, fftshift

    # Take 2D FFT

    normsq = nx*ny # Normalization prefactor squared (fft2 fxn does NOT obey Parseval's theorem)

    array_fft = fftshift(fft2(fftshift(array))) # Take 2D spatial FFT of array and shift
                                      # <-----pos. freq.-----><-----neg. freq.-----> originally
    
    # Compute spatial Nyquist frequencies

    ux_nyq = 0.5/dx_um # Spatial Nyquist frequency in x-dxn
    uy_nyq = 0.5/dy_um # Spatial Nyquist frequency in y-dxn

    # Take max. frequency, go from -max to zero at N/2 (the center), and then to just shy of +max
    ux = 2*ux_nyq*(np.arange(nx) - 0.5*nx)/nx # Range of frequencies in x-dxn rel. to ux_nyq [2/nx = 1/(nx/2)] --> Go from FULLY -ux_nyq to ALMOST +ux_nyq 
                                              # In even-length 1D array, zero-freq. is at N/2
    uy = 2*uy_nyq*(np.arange(ny) - 0.5*ny)/ny # Range of frequencies in y-dxn rel. to uy_nyq [2/ny = 1/(ny/2)] --> Go from FULLY -uy_nyq to ALMOST +uy_nyq
                                              # In even-length 1D array, zero-freq. is at N/2

    ur_max = np.sqrt(np.min(ux)**2 + np.min(uy)**2) # Maximum radial frequency (in meters^-1) 
                                                    # Want FULLY +/- ux_nyq, uy_nyq

    # We're now going to consider two 1D arrays which will be plotted. The first is "ur" which is the
    # array of radial spatial frequencies, and the second is "psd_a" which is the
    # array of power values at each of these spatial frequencies. We could create these two arrays
    # together with 50 "bins" in radius (n_ur = 50), or 100 bins, or some other number.
    # We don't have to necessarily make "n_ur" equal to the square root of (nx/2)^2 plus (ny/2)^2
    
    ur = ur_max*np.arange(n_ur)/(n_ur - 1)
    
    # And then to calculate the power spectral density, we're going to need both an array
    # for adding up the net power at each of n_ur "bins", and also the net number of times we
    # added something into this bin. Thus, in the end, we'll divide each value of psd_a by each
    # value of psd_a_count to now make psd_a represent the average power from all pixels in
    # this radial "bin".

    
    # We now want to create an array "ur_ind" which is a 2D array where each pixel in the array
    # contains the radial spatial frequency of the pixel.  First we create it with the square
    # in each pixel.
    
    ur_ind = np.zeros((ny, nx))
    theta = np.zeros_like(ur_ind)
    
    for idy in range(ny):
        ur_ind[idy, 0:nx] = ux**2 + uy[idy]**2
        theta[idy, 0:nx] = np.arctan2(uy[idy], ux)
    
    # And now we take the square root to get the radial spatial frequency of the pixel,
    # at each pixel position (this is computationally faster than including the square root in the above line)
    
    ur_ind = np.sqrt(ur_ind)

    # Now we convert the 2D array of radial spatial frequency per pixel into a
    # 2D array, where every element of the array is
    # the pixel index in the 1D arrays "ur" and "psd_a".  Since those 1D arrays go from a spatial
    # frequency of 0 to a spatial frequency of "ur_max", and the 2D array "ur_ind" also has values
    # that go from 0 to "ur_max", all we have to do is find the nearest integer to
    # n_ur*ur_ind/ur_max)
    
    ur_ind = (0.5 + n_ur*ur_ind/ur_max).astype(int)

    # To do: create for loop that includes psd_a, psd_a_count for x and y dxns between different angles
    # Now calculate the 2D power array by squaring the Fourier transform of the image.
    
    psd = (np.abs(array_fft)**2)/normsq

    if circular_beam:
        psd_a = np.array([np.sum(psd[ur_ind == j]) for j in range(1, n_ur + 1)])
        psd_a_count = np.array([np.sum(ur_ind == j) for j in range(1, n_ur + 1)])

        ur_ind_good = np.where(psd_a_count > 0)

        if len(ur_ind_good) > 0:
            psd_a[ur_ind_good] /= psd_a_count[ur_ind_good]

        # Remove azimuthal PSD contributions of zero (due to contributing pixels being outside mask region)
        
        nonzero_psd_a_idx = np.where(psd_a > 0)

        ur_good = ur[nonzero_psd_a_idx]
        psd_a_nonzero = psd_a[nonzero_psd_a_idx]

        return ur_good, psd, psd_a_nonzero
    
    else: # If azimuthal PSD not assumed to be isotropic,
          # assume azimuthal PSD contains x and y components

        # Set angle boundaries

        theta_1 = np.pi/6
        theta_2 = np.pi/3
        theta_3 = 2*np.pi/3
        theta_4 = 5*np.pi/6

        # Create masks/boolean arrays that separate x and y radial spatial frequencies according to their phases.

        psd_a_x_mask = (np.abs(theta) <= theta_1) | (np.abs(theta) >= theta_4)
        psd_a_y_mask = (np.abs(theta) >= theta_2) & (np.abs(theta) <= theta_3)

        # Sum up all x and y azimuthal PSD values for a given radial spatial frequency while obeying the above phase constraints

        psd_a_x = np.array([np.sum(psd[(ur_ind == j) & psd_a_x_mask]) 
                            for j in range(1, n_ur + 1)])
        
        psd_a_y = np.array([np.sum(psd[(ur_ind == j) & psd_a_y_mask]) 
                            for j in range(1, n_ur + 1)])
        
        # Sum up all pixels contributing to a given radial frequency bin while obeying the above phase constraints

        psd_a_x_count = np.array([np.sum((ur_ind == j) & psd_a_x_mask) 
                                  for j in range(1, n_ur + 1)])
        
        psd_a_y_count = np.array([np.sum((ur_ind == j) & psd_a_y_mask) 
                                  for j in range(1, n_ur + 1)])
        
        # Check to see if there are no radial frequency bins with zero pixel contributions, and,
        # for each radial frequency index, scale the total x and y azimuthal PSDs in each radial frequency bin by the total number of pixels
        # contributing to each of those bins while adhering to the above phase constraints
        
        ur_ind_x_good = np.where(psd_a_x_count > 0)
        ur_ind_y_good = np.where(psd_a_y_count > 0)

        if len(ur_ind_x_good) > 0:
            psd_a_x[ur_ind_x_good] /= psd_a_x_count[ur_ind_x_good]
            
        if len(ur_ind_y_good) > 0:
            psd_a_y[ur_ind_y_good] /= psd_a_y_count[ur_ind_y_good]
        
        # Remove azimuthal PSD contributions of zero (due to contributing pixels being outside mask region)

        nonzero_psd_a_x_idx = np.where(psd_a_x > 0)
        nonzero_psd_a_y_idx = np.where(psd_a_y > 0)

        ur_x = ur[nonzero_psd_a_x_idx]
        ur_y = ur[nonzero_psd_a_y_idx]

        psd_a_x_nonzero = psd_a_x[nonzero_psd_a_x_idx]
        psd_a_y_nonzero = psd_a_y[nonzero_psd_a_y_idx]
            
        return ur_x, ur_y, psd, psd_a_x_nonzero, psd_a_y_nonzero