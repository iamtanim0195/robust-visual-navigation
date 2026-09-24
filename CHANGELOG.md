# Project Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - Phase 8 & 9 Complete
### Added
- Created modular perception sub-package (`perception/image_preprocessing.py`, `feature_extraction.py`, `feature_tracking.py`).
- Added `perception_node.py` implementing Lucas-Kanade optical flow tracking over `/camera/image_raw`.
- Registered `perception_node` executable in `setup.py` and created `launch/perception.launch.py`.

## [0.6.1] - Phase 6 & 7 Fix
### Fixed
- Mapped Gazebo Sim IMU scoped topic (`/world/research_world/model/visual_navigation_robot/link/imu_link/sensor/imu_sensor/imu`) to ROS 2 `/imu/data` topic in `launch/gazebo.launch.py`.