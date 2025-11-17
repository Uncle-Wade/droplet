# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 19:15:37 2025

@author: LEHBERGCT22
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:54:52 2025

@author: LEHBERGCT22
"""

import imageio
from skimage import color, img_as_ubyte
import os

# --- Settings ---
video_path = 'Test6.mov'                 # Path to your .mov file
output_folder = 'Test6_frames_tif_8bit'  # Folder to save 8-bit .tif frames

# --- Create output folder ---
os.makedirs(output_folder, exist_ok=True)

# --- Initialize video reader (uses FFmpeg) ---
reader = imageio.get_reader(video_path, format='ffmpeg')

# --- Get video metadata ---
meta = reader.get_meta_data()
nframes = meta.get('nframes', None)
print(f"Video info: {meta}")
if nframes:
    print(f"Approx total frames: {nframes}")


# --- Extract and save all frames ---
for i, frame in enumerate(reader):
    gray = color.rgb2gray(frame)
    filename = os.path.join(output_folder, f'frame_{i:04d}.tif')
    imageio.imwrite(filename, img_as_ubyte(gray))

print(f"✅ Done! Saved all frames as 8-bit grayscale TIFFs in '{output_folder}'.")
reader.close()
