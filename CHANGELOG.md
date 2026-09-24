# Project Changelog

All notable changes to this project will be documented in this file.

## [0.12.0] - Phase 16 Complete
### Added
- Created `perception/visual_degradation.py` implementing Gaussian Blur, Resolution Downsampling, and Illumination scaling.
- Updated `perception_node` and `visual_odometry_node` to process `/camera/image_degraded`.
- Added `launch/degradation_experiment.launch.py` supporting CLI args (`sensor_config`, `degradation_mode`, `severity_level`).

## [0.11.0] - Phase 14 & 15 Complete
### Added
- Created `navigation/waypoint_navigator.py` implementing classical proportional velocity control.
- Added `navigation/experiment_logger.py` logging ATE error metrics and trajectory data to CSV (`experiments/raw/`).
- Created `launch/baseline_navigation.launch.py`.