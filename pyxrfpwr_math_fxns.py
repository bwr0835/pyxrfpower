# File: pyxrfpower_math_fxns.py
# Author: B. Roter

# List of math functions external to Python and/or PyQt libraries and/or programs used for PyXRFPower

def round_correct(num, ndec): # CORRECTLY round a number (num) to chosen number of decimal places (ndec)

    if ndec == 0:
        return int(num + 0.5)
    
    else:
        digit_value = 10**ndec
        
        if num > 0:
            return int(num*digit_value + 0.5)/digit_value
        
        else:
            return int(num*digit_value - 0.5)/digit_value
        
class normalize: # A class of normalization functions
    def pwr_law_norm(array, min_threshold, max_threshold, gamma): # Power law normalization
        if (min_threshold > max_threshold) or (max_threshold == 0):
            print("\n Error: Minimum threshold must be less than maximum threshold \n")

            return
        
        else:
            array[array < min_threshold] = min_threshold
            array[array > max_threshold] = max_threshold
            
            array_norm = ((array - min_threshold)/(max_threshold - min_threshold))**gamma

            return array_norm