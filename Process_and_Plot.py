# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 23:16:30 2025

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
    PixelLength = 460 - 20  # scale bar length in pixels
    nm_per_pixel = 1000 / PixelLength  # conversion factor (1 µm = 1000 nm)
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
        diameters_nm = []

        for region in props:
            if region.area > min_pixels:
                diameter_nm = region.equivalent_diameter * nm_per_pixel
                diameters_nm.append(diameter_nm)

        diameters_nm.sort(reverse=True)  # optional: largest to smallest

        if diameters_nm:
            row_data = {"Frame_number": i}
            for j, d in enumerate(diameters_nm, start=1):
                row_data[f"Particle_{j}"] = d
            all_rows.append(row_data)
            print(f"  -> {len(diameters_nm)} particles recorded")
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

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # registers 3D plotting

def plot_3d_histogram(subfolder, csv_name="droplet_diameters_by_frame.csv", bin_width=50):
    """
    Create a 3D surface plot showing droplet size distributions across frames.
    
    Parameters
    ----------
    subfolder : str
        Name of the folder (inside the same directory as this script) 
        where the CSV and images are located.
    csv_name : str
        Name of the CSV file to plot.
    bin_width : float
        Width of histogram bins in nanometers.
    """

    # === Build file path dynamically (same logic as main() ===
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, subfolder)
    csv_path = os.path.join(folder_path, csv_name)

    if not os.path.exists(csv_path):
        print(f"⚠️ CSV not found at: {csv_path}")
        return

    print(f"\n📊 Loading droplet data from:\n{csv_path}\n")

    # === Load data ===
    df = pd.read_csv(csv_path)

    # Extract numeric columns (ignore Frame_number)
    size_data = df.drop(columns=["Frame_number"]).values
    frame_numbers = df["Frame_number"].values

    # Flatten all non-NaN values to find global range
    all_sizes = size_data.flatten()
    all_sizes = all_sizes[~np.isnan(all_sizes)]
    min_d, max_d = np.min(all_sizes), np.max(all_sizes)

    # Create common histogram bins
    bins = np.arange(min_d, max_d + bin_width, bin_width)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Compute histogram for each frame
    hist_matrix = []
    for row in size_data:
        valid = row[~np.isnan(row)]
        counts, _ = np.histogram(valid, bins=bins)
        hist_matrix.append(counts)
    hist_matrix = np.array(hist_matrix)

    # Create coordinate grids
    X, Y = np.meshgrid(bin_centers, frame_numbers)

    # === Plot 3D surface ===
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, hist_matrix, cmap='viridis', edgecolor='none')
    ax.set_xlabel("Droplet Diameter (nm)")
    ax.set_ylabel("Frame Number")
    ax.set_zlabel("Count")
    ax.set_title("Droplet Size Distribution Across Frames")
    fig.colorbar(surf, shrink=0.6, label="Count")

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
    plot_3d_histogram(subfolder="Test6_frames_tif_8bit")
