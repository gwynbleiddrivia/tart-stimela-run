#!/usr/bin/env python3
import os
import glob
import subprocess
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# ------------------------
# Config
# ------------------------
fits_dir = "img"         # folder with your FITS files
png_dir = "img_png"      # folder to store PNGs
movie_file = "tart_movie.mp4"
framerate = 10           # frames per second

os.makedirs(png_dir, exist_ok=True)

# ------------------------
# Select only main image FITS files
# ------------------------
fits_files = sorted(glob.glob(os.path.join(fits_dir, "*-image.fits")))
if not fits_files:
    raise FileNotFoundError("No image FITS files found matching '*-image.fits'")

# ------------------------
# Convert FITS -> PNG
# ------------------------
print("Converting FITS to PNG...")
for f in fits_files:
    base = os.path.basename(f).replace(".fits", "")
    png_path = os.path.join(png_dir, f"{base}.png")
    
    # Skip if PNG already exists
    if os.path.exists(png_path):
        continue

    # Load FITS
    h = np.squeeze(fits.getdata(f))
    
    # Normalize for display
    h = h - np.min(h)
    if np.max(h) > 0:
        h = h / np.max(h)
    
    # Plot & save
    plt.imshow(h, origin='lower', cmap='inferno')
    plt.axis('off')
    plt.savefig(png_path, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()

print(f"Converted {len(fits_files)} FITS files to PNGs in '{png_dir}'.")

# ------------------------
# Make movie using ffmpeg
# ------------------------
print("Making movie...")
subprocess.run([
    "ffmpeg",
    "-y",  # overwrite output
    "-framerate", str(framerate),
    "-i", os.path.join(png_dir, "%*-image.png"),  # match your PNGs
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    movie_file
], check=True)

print(f"Movie created: {movie_file}")
