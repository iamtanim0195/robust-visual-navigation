# Research Problem Statement

## Problem Context
Autonomous mobile robot navigation in GPS-denied indoor environments relies heavily on visual sensors (RGB/Depth cameras) for perception and state estimation. However, vision-only navigation systems exhibit severe vulnerability to environmental visual degradation—such as low illumination, motion blur, reduced sensor resolution, and lens occlusion. These degradations lead to feature tracking failure, visual odometry drift, and unrecoverable localization loss.

While high-cost mobile platforms mitigate these issues using expensive multi-line LiDARs or industrial-grade IMUs, low-cost educational/commercial mobile robots are constrained by low-cost hardware (e.g., ESP32-CAM, MPU6050, low-resolution wheel encoders). 

## Research Gap
1. **Low-Cost Sensor Fusion Resilience**: Existing literature extensively studies sensor fusion on high-precision sensors, but quantitative evaluations of multi-sensor fusion under controlled visual degradation using ultra-low-cost hardware remain sparse.
2. **Degradation-Aware Navigation Policy**: Limited empirical data exists comparing how classical navigation (e.g., EKF + Nav2) versus Reinforcement Learning (RL) navigation policies gracefully degrade under structured, multi-level visual noise when constrained to identical sensor configurations.

## Scope of Investigation
This research investigates the navigation accuracy, trajectory drift, success rate, and computational efficiency of a differential-drive mobile robot operating under controlled levels of visual degradation across four distinct sensor configurations:
1. Vision Only
2. Vision + Wheel Odometry
3. Vision + IMU
4. Vision + Wheel Odometry + IMU (Full Fusion)