# Project Changelog

All notable changes to this project will be documented in this file.

## [0.8.0] - Phase 10 Complete
### Added
- Created `localization/visual_odometry_node.py` implementing Essential Matrix pose recovery (`findEssentialMat` / `recoverPose`).
- Added `/visual_odometry/odom` output topic.
- Registered `visual_odometry_node` executable and created `launch/visual_odometry.launch.py`.

## [0.7.0] - Phase 8 & 9 Complete
### Added
- Created modular perception sub-package (`perception/image_preprocessing.py`, `feature_extraction.py`, `feature_tracking.py`).
- Added `perception_node.py` implementing Lucas-Kanade optical flow tracking over `/camera/image_raw`.
- Registered `perception_node` executable in `setup.py` and created `launch/perception.launch.py`.