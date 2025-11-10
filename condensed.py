# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 18:38:04 2025

@author: LEHBERGCT22
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure, measure
from skimage.filters import threshold_otsu, try_all_threshold

def main():

    start = 400
    end = 420


    # read in image file (this file was in grayscale so no conversion is required)
    image1 = io.imread('frame_0410_8bit.TIF')
    image = 255 - image1 
    
    
    # use a builtin thresholding method in skimage
    ots = threshold_otsu(image) #this gets a value for ots by which to threashold by

    
    # Choose somewhat arbitrarily to use ots threshold (otsu is a common method)
    # Now use skimage measure.label function to label connected regions 
    #  of an integer array
    pixel_2 = image < ots  # this is the same as pixel_1 above
    
    # find and label pixels of connected or touching dark pixels (particles)
    dark = measure.label(pixel_2) # using label function in skimage.measure
    
    # labels = np.unique(dark)  # find unique labels
    # print('number of labeled regions ',labels.size)
    # print(labels)
    
    #  skimage can use the labeled file "dark" to get properties of the
    # connected regions
    
    # next several lines get an print the properties of the 'partcles'C:/Users/LEHBERGCT22/OneDrive - Grove City College/Desktop/Senior Project/Origional Files/scalebar.png
    # Note that pandas is uded to print the results in a nice table
    prop_val = measure.regionprops_table(dark,
                              properties=['label', 'num_pixels','centroid',
                                          'area','equivalent_diameter'])
    import pandas as pd  
    data = pd.DataFrame(prop_val)
    print()  
    print('****************************************')
    print('Results based on number of pixels only - not scaled')
    print(data.to_string())
    print('****************************************')
    
    
    

    PixelLength = 460 - 20  # Length of the scale bar in pixels
    print()
    print('Using the image of the scale bar')
    print('One millimeter is: ' + str(PixelLength) + ' pixels')
    print()
    
    # Scale bar is 1 micron in length
    # Conversion factor (1 micrometer = 1000 nanometers)
    # Convert the equivalent diameter from pixels to nanometers
    nm_per_pixel = 1000 / PixelLength  # How many nanometers one pixel represents
    
    
    
    # Assuming 'dark' has the labeled 'particles', get the properties of
    # all labeled regions
    props = measure.regionprops(dark)  # Get properties of all labeled regions
    dia = []  # To store the equivalent diameters of particles 
    number = []    # To store the particle numbers
    
    # Loop through all regions
    for n, region in enumerate(props):
        area = region.area  # Get the area of the region
        # Get the equivalent diameter of the region
        equivalent_diameter = region.equivalent_diameter * nm_per_pixel
        
        # Check if the area is greater than min_pixels pixels
        min_pixels = 200  #10
        if area > min_pixels:
            dia.append(equivalent_diameter)  # Append the equivalent diameter
            number.append(n)  # Append the particle number
    
    # Convert lists to numpy arrays for saving
    number = np.array(number,dtype=np.int64)
    dia = np.array(dia)
    
    print('Results for regions lager than',min_pixels,'pixels')
    print('average size (nm)',dia.mean())
    print('median size (nm)',np.median(dia))
    print('standard deviation (nm)',dia.std())
    print('number of particles ',dia.size)
    print()
    
    
    # Open file and write the data
    with open("diameter.txt", "w") as file:
        header = '\n'.join([
            "Particle  --  Equivalent diameter (nm)", 
            "-------------------------------"])  # Define the heading
        np.savetxt(file, np.transpose([number, dia]), 
                   delimiter='-----', fmt='%f', comments='# ', header=header)
    
    # Open and read the file to verify the contents
    with open('diameter.txt', 'r') as file:
        content = file.read()
    print(content)
    
if __name__ == "__main__":
    main()

