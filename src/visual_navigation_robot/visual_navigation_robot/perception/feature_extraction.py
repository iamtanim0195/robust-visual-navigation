import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self, max_corners=200, quality_level=0.01, min_distance=10):
        self.max_corners = max_corners
        self.quality_level = quality_level
        self.min_distance = min_distance

    def extract_corners(self, gray_img: np.ndarray) -> np.ndarray:
        """Extracts strong corner features using Shi-Tomasi method."""
        corners = cv2.goodFeaturesToTrack(
            gray_img,
            maxCorners=self.max_corners,
            qualityLevel=self.quality_level,
            minDistance=self.min_distance
        )
        return corners