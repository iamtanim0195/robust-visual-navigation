# Robust Vision-Based Autonomous Navigation for Low-Cost Mobile Robots under Visual Degradation

**Author:** Md. Sahadat Hossen Tanim  
**Framework:** ROS 2 (Kilted) & Gazebo Harmonic  
**Repository:** https://github.com/iamtanim0195/robust-visual-navigation  

---

## Abstract
Autonomous mobile robot navigation relying primarily on monocular visual odometry suffers rapid localization drift when subjected to visual environmental degradation, such as motion blur, illumination drop, and resolution downsampling. This paper evaluates a multi-sensor sensor fusion architecture alongside a Reinforcement Learning (RL) continuous control policy to sustain navigation accuracy under severe visual noise. Using an Extended Kalman Filter (EKF) combining 5-point Essential Matrix Visual Odometry, Wheel Odometry, and a 6-DOF IMU across four configurations ($S_1-S_4$), we benchmark localization performance in a Gazebo simulation arena. Experimental results show that full multi-sensor fusion ($S_4$) reduces Absolute Trajectory Error (ATE) RMSE by **60.5%** under severe Gaussian blur compared to vision-only estimation ($S_1$), successfully bounding localization error to **0.1546 m**. Furthermore, Proximal Policy Optimization (PPO) reinforcement learning agents demonstrate superior trajectory recovery under high noise compared to classical proportional velocity baselines.

---

## I. Introduction
Visual Odometry (VO) provides cost-effective pose estimation for low-cost autonomous mobile robots. However, feature-based optical tracking methods (e.g., Lucas-Kanade optical flow, FAST feature detection) degrade severely under sudden lighting changes, fast turns causing motion blur, or low-resolution camera sensors.

This research addresses three central Research Questions (RQs):
1. **RQ1:** How significantly does multi-sensor fusion reduce localization drift compared to monocular visual odometry alone?
2. **RQ2:** To what threshold does visual degradation (blur, illumination drop, downsampling) disrupt classical waypoint navigation?
3. **RQ3:** Does a Proximal Policy Optimization (PPO) reinforcement learning controller achieve greater trajectory resilience under visual noise than classical controllers?

---

## II. System Architecture & Methodology

### A. Robot Kinematics & Perception Pipeline
The experimental platform is a 2WD differential drive chassis modeled in URDF/Xacro, equipped with an RGB camera ($640 \times 480$ @ 30 FPS) and an MPU6050 6-DOF IMU. The vision processing pipeline leverages OpenCV CLAHE histogram equalization, FAST corner detection, and Lucas-Kanade optical flow feature tracking.

### B. Visual Odometry & Multi-Sensor Fusion
Motion estimation extracts relative transformation matrices $(R, t)$ from tracked feature correspondences via the 5-point Essential Matrix algorithm with RANSAC outlier rejection:
$$E = K'^T F K$$
State estimation is fused via `robot_localization` EKF modules configured into four experimental profiles:
* **$S_1$:** Monocular Visual Odometry Only
* **$S_2$:** Visual Odometry + Differential Wheel Encoders
* **$S_3$:** Visual Odometry + IMU Accelerometer/Gyroscope
* **$S_4$:** Full Multi-Sensor Fusion ($VO + Wheel + IMU$)

### C. Visual Degradation Pipeline
A ROS 2 image interceptor node dynamically applies controlled visual noise to `/camera/image_raw` before processing:
1. **Gaussian Blur:** Kernel sizes $k \in \{7, 15, 27\}$ ($\sigma = 3, 7, 13$).
2. **Resolution Downsampling:** Spatial scaling down to $12.5\%$ ($80 \times 60$).
3. **Low Illumination:** Brightness attenuation factors down to $5\%$.

---

## III. Experimental Benchmarks & Results

### A. Absolute Trajectory Error (ATE) Benchmark Summary

| Configuration | Sensor Profile | Environmental Condition | ATE RMSE (m) | ATE Max (m) | ATE Std (m) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **$S_4$** | Full Fusion | Clean Baseline | **0.0202** | 0.0317 | 0.0049 |
| **$S_3$** | VO + IMU | Clean Baseline | 0.0287 | 0.0446 | 0.0066 |
| **$S_2$** | VO + Wheels | Clean Baseline | 0.0368 | 0.0604 | 0.0085 |
| **$S_1$** | Vision Only | Clean Baseline | 0.0524 | 0.0795 | 0.0132 |
| **$S_4$** | Full Fusion | Illumination Drop | **0.1024** | 0.1498 | 0.0202 |
| **$S_3$** | VO + IMU | Illumination Drop | 0.1460 | 0.2128 | 0.0278 |
| **$S_2$** | VO + Wheels | Illumination Drop | 0.1810 | 0.2694 | 0.0340 |
| **$S_1$** | Vision Only | Illumination Drop | 0.2565 | 0.3837 | 0.0504 |
| **$S_4$** | Full Fusion | Severe Gaussian Blur | **0.1546** | 0.2430 | 0.0284 |
| **$S_3$** | VO + IMU | Severe Gaussian Blur | 0.2133 | 0.3043 | 0.0412 |
| **$S_2$** | VO + Wheels | Severe Gaussian Blur | 0.2722 | 0.3908 | 0.0504 |
| **$S_1$** | Vision Only | Severe Gaussian Blur | **0.3911** | 0.6847 | 0.0786 |

---

## IV. Discussion & Conclusion

The quantitative evaluation demonstrates that monocular visual odometry alone ($S_1$) is fragile under environmental noise, exhibiting a **746% increase in ATE RMSE** when moving from clean conditions (0.0524 m) to severe visual blur (0.3911 m). 

By integrating IMU angular velocity and wheel encoder odometry into an EKF framework ($S_4$), localization drift is bounded to **0.1546 m**, preserving navigation accuracy. Furthermore, reinforcement learning control policies trained via PPO in Gym environments exhibit dynamic velocity throttling when confidence in estimated position degrades, mitigating aggressive divergence.

**Conclusion:** Multi-sensor fusion combining inertial and wheel feedback with visual odometry is essential for low-cost mobile robots operating in real-world environments prone to visual degradation.