import cv2
import numpy as np

class FeatureTracker:
    def __init__(self, win_size=(15, 15), max_level=2):
        self.lk_params = dict(
            winSize=win_size,
            maxLevel=max_level,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )

    def track(self, prev_gray: np.ndarray, curr_gray: np.ndarray, prev_pts: np.ndarray):
        """Tracks feature points from prev_gray to curr_gray using LK Optical Flow."""
        if prev_pts is None or len(prev_pts) == 0:
            return None, None

        curr_pts, status, err = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, prev_pts, None, **self.lk_params
        )

        good_new = curr_pts[status == 1]
        good_old = prev_pts[status == 1]

        return good_new, good_old