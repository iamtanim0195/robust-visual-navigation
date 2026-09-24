# Project Changelog

All notable changes to this project will be documented in this file.

## [0.9.0] - Phase 11 Complete
### Added
- Integrated `robot_localization` EKF filter configurations for $S_1, S_2, S_3, S_4$ modes (`config/ekf_s*.yaml`).
- Created `launch/sensor_fusion.launch.py` with runtime configuration argument `sensor_config:=s1|s2|s3|s4`.
- Enabled filtered odometry output over `/odometry/filtered`.

## [0.8.0] - Phase 10 Complete
### Added
- Created `localization/visual_odometry_node.py` implementing Essential Matrix pose recovery (`findEssentialMat` / `recoverPose`).
- Added `/visual_odometry/odom` output topic.
- Registered `visual_odometry_node` executable and created `launch/visual_odometry.launch.py`.