# Project Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Phase 18 & 19 Complete
### Added
- Implemented Gymnasium environment (`nav_gym_env.py`) and Stable-Baselines3 PPO training script (`train_ppo.py`).
- Added automated log analysis and statistical evaluation script (`experiments/analyze_results.py`).

## [0.12.0] - Phase 16 Complete
### Added
- Created `perception/visual_degradation.py` implementing Gaussian Blur, Resolution Downsampling, and Illumination scaling.
- Updated `perception_node` and `visual_odometry_node` to process `/camera/image_degraded`.
- Added `launch/degradation_experiment.launch.py` supporting CLI args (`sensor_config`, `degradation_mode`, `severity_level`).