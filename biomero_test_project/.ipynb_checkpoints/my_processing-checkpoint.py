import numpy as np
from scipy.ndimage import gaussian_filter

def main(image):
    """
    Apply a Gaussian blur to the input image (a 200x200 NumPy array).
    Returns the blurred image.
    """
    sigma = 2.0  # adjust blur strength
    blurred = gaussian_filter(image, sigma=sigma)

    print(f"Processed image with Gaussian blur (σ={sigma})")
    return blurred