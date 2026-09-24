import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def process(self, frame_bgr: np.ndarray) -> np.ndarray:
        """Converts frame to grayscale and applies Contrast Limited Adaptive Histogram Equalization."""
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        enhanced_gray = self.clahe.apply(gray)
        return enhanced_gray