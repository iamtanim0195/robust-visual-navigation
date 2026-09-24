# Project Changelog

All notable changes to this project will be documented in this file.

## [0.10.0] - Phase 12 & 13 Complete
### Added
- Created `localization/ground_truth_publisher.py` for ATE trajectory error benchmark extraction on `/ground_truth/odom`.
- Added SLAM mapping config (`config/mapper_params_online_async.yaml`) and integration launch file (`launch/mapping.launch.py`).

## [0.9.0] - Phase 11 Complete
### Added
- Integrated `robot_localization` EKF filter configurations for $S_1, S_2, S_3, S_4$ modes (`config/ekf_s*.yaml`).
- Created `launch/sensor_fusion.launch.py` with runtime configuration argument `sensor_config:=s1|s2|s3|s4`.
- Enabled filtered odometry output over `/odometry/filtered`.