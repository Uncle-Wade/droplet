# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 19:25:17 2025

@author: LEHBERGCT22
"""

import os
import numpy as np
import pandas as pd
from skimage import io, measure
from skimage.filters import threshold_otsu

def main():
    # === USER SETTINGS ===
    folder_path = "./Test6_frames_tif_8bit"
    start = 410
    end = 420
    min_pixels = 200  # minimum region area (in pixels)
    PixelLength = 460 - 20  # scale bar length in pixels, change the 460 to whatever it needs to be
    mm_per_pixel = 10 / PixelLength  # conversion factor (1 cm = 10 mm)
    output_csv = os.path.join(folder_path, "all_diameters.csv")
    # ======================

    print(f"\nProcessing frames {start}–{end} from:\n{folder_path}\n")

    # Store all results across all frames
    all_results = []

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
        frame_results = []

        for n, region in enumerate(props):
            if region.area > min_pixels:
                diameter_nm = region.equivalent_diameter * nm_per_pixel
                frame_results.append((i, n, diameter_nm))

        if frame_results:
            frame_df = pd.DataFrame(frame_results, columns=["frame_number", "particle_number", "diameter_nm"])
            all_results.append(frame_df)
            print(f"  -> {len(frame_df)} particles > {min_pixels}px")
        else:
            print(f"  -> No regions found > {min_pixels}px")

    # === Combine and export all results ===
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        final_df.to_csv(output_csv, index=False)
        print(f"\n✅ Combined results saved to:\n{output_csv}")
        print(f"Total rows: {len(final_df)}")
    else:
        print("\n⚠️ No valid particle data found for any frames.")

if __name__ == "__main__":
    main()
