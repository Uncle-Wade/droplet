# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 19:22:21 2025

@author: LEHBERGCT22
"""

import os
import numpy as np
import pandas as pd
from skimage import io, measure
from skimage.filters import threshold_otsu

def main():
    # === USER SETTINGS ===
        # Get the directory where this Python file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add your specific folder name here (inside the same directory as this script)
    subfolder = "Test6_frames_tif_8bit"  # <-- you can change this freely
    folder_path = os.path.join(base_dir, subfolder)
    
    start = 410
    end = 420
    min_pixels = 1  # minimum region area (in pixels)
    PixelLength = 460  
    # scale bar length in pixels. original code had 1um scalebar. we will go with 1cm physical scalebar
    # we will measure the pixel amount of the scalebar nad record it above
   
    mm_per_pixel = 10 / PixelLength  # conversion factor (1 cm = 10 mm)
    output_csv = os.path.join(folder_path, "droplet_diameters_by_frame.csv")
    # ======================

    print(f"\nProcessing frames {start}–{end} from:\n{folder_path}\n")

    all_rows = []  # will store one row per frame

    for i in range(start, end + 1):
        filename = f"frame_{i:04d}.TIF"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            print(f"⚠️ Skipping {filename} (file not found)")
            continue

        print(f"Processing {filename}...")

        # === Read and invert image ===
        image = io.imread(filepath)
        image = 255 - image  # invert grayscale

        # === Threshold using Otsu ===
        ots = threshold_otsu(image)
        binary = image < ots
        labeled = measure.label(binary)

        # === Measure labeled regions ===
        props = measure.regionprops(labeled)
        diameters_mm = []

        for region in props:
            if region.area > min_pixels:
                diameter_mm = region.equivalent_diameter * mm_per_pixel
                diameters_mm.append(diameter_mm)

        diameters_mm.sort(reverse=True)  # optional: largest to smallest

        if diameters_mm:
            row_data = {"Frame_number": i}
            for j, d in enumerate(diameters_mm, start=1):
                row_data[f"Particle_{j}"] = d
            all_rows.append(row_data)
            print(f"  -> {len(diameters_mm)} particles recorded")
        else:
            all_rows.append({"Frame_number": i})
            print(f"  -> No regions found > {min_pixels}px")

    # === Combine all rows and export ===
    if all_rows:
        final_df = pd.DataFrame(all_rows)
        final_df.to_csv(output_csv, index=False)
        print(f"\n✅ Droplet diameters saved to:\n{output_csv}")
        print(f"Total frames processed: {len(final_df)}")
    else:
        print("\n⚠️ No valid particle data found for any frames.")

if __name__ == "__main__":
    main()

