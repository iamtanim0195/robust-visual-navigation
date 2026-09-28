# Robust Vision-Based Autonomous Navigation for Low-Cost Mobile Robots

[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Kilted-blue)](https://docs.ros.org/)
[![Gazebo](https://img.shields.io/badge/Simulation-Gazebo-orange)](https://gazebosim.org/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Research](https://img.shields.io/badge/Project-Research--Oriented-purple)]()

> **A research-oriented ROS 2 framework for investigating robust autonomous navigation using visual perception, wheel odometry, inertial sensing, sensor fusion, and controlled visual degradation in indoor mobile-robot environments.**

---

## 1. Research Overview

Autonomous mobile robots operating in indoor environments often rely heavily on visual information for perception and localization. However, real-world visual conditions are rarely ideal. Motion blur, reduced illumination, image degradation, noise, and resolution loss can significantly affect visual perception and consequently navigation performance.

This project investigates whether **multi-sensor fusion of visual information, wheel odometry, and inertial measurements can improve localization and navigation robustness under degraded visual conditions**.

The project follows a **simulation-first, sim-to-real research methodology**, using ROS 2 and Gazebo as the primary experimental environment and a low-cost differential-drive robot as the eventual physical validation platform.

### Research Pipeline

```text
Visual Perception
       │
       ▼
Visual Odometry ─────┐
                     │
Wheel Odometry ──────┼──► Sensor Fusion ──► Localization
                     │
IMU ─────────────────┘
                                      │
                                      ▼
                              Navigation / Planning
                                      │
                                      ▼
                                   cmd_vel
                                      │
                                      ▼
                               Mobile Robot
```

---

# 2. Research Question

### Main Research Question

> **How does multi-sensor fusion of vision, wheel odometry, and inertial measurements affect the accuracy and robustness of autonomous navigation in a low-cost mobile robot under visual degradation?**

### Sub-Research Questions

**RQ1.** How does sensor fusion affect localization accuracy compared with vision-only navigation?

**RQ2.** How does visual degradation affect autonomous navigation performance?

**RQ3.** Does combining visual, wheel-odometry, and inertial measurements improve robustness?

**RQ4.** How does navigation performance change between simulation and a physical low-cost robot?

**RQ5.** What trade-offs exist between localization accuracy, navigation performance, and computational cost?

---

# 3. Research Hypothesis

> **H1:** Fusing visual information with wheel odometry and inertial measurements will reduce localization error and improve navigation robustness compared with vision-only navigation, particularly under degraded visual conditions.

The hypothesis is evaluated experimentally rather than assumed to be true.

Both positive and negative findings are retained as part of the research process.

---

# 4. Research Objectives

The project aims to:

* Develop a modular ROS 2 autonomous navigation framework.
* Build a realistic differential-drive mobile robot simulation.
* Integrate RGB vision, wheel odometry, and IMU sensing.
* Investigate visual odometry and state estimation.
* Implement multi-sensor fusion using an Extended Kalman Filter.
* Establish a classical autonomous-navigation baseline.
* Introduce controlled visual degradation.
* Quantitatively evaluate localization and navigation robustness.
* Investigate reinforcement-learning-based navigation as an extension.
* Transfer the architecture toward a physical low-cost robot.
* Evaluate the simulation-to-real performance gap.
* Produce a reproducible research repository and experimental dataset.

---

# 5. System Architecture

The project is designed around a modular architecture separating perception, localization, navigation, experimentation, and hardware abstraction.

```text
                         ┌──────────────────────────┐
                         │      Research / Web UI    │
                         │  Teleoperation & Monitor  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │    ROS 2      │
                              │ Communication │
                              └───────┬───────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
 ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
 │ RGB Camera      │        │ Wheel Odometry  │        │      IMU        │
 │ Visual Input    │        │ Encoder Data    │        │ 6-DOF Motion    │
 └────────┬────────┘        └────────┬────────┘        └────────┬────────┘
          │                          │                          │
          ▼                          ▼                          ▼
 ┌─────────────────┐        ┌─────────────────────────────────────────┐
 │ Visual          │        │        State Estimation                 │
 │ Odometry        │───────►│        Sensor Fusion / EKF             │
 └─────────────────┘        └───────────────────┬─────────────────────┘
                                               │
                                               ▼
                                     ┌──────────────────┐
                                     │ Localization     │
                                     │ /odometry/filtered│
                                     └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │ Mapping / SLAM   │
                                     └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │ Navigation       │
                                     │ & Planning       │
                                     └────────┬─────────┘
                                              │
                                           /cmd_vel
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │ Differential     │
                                     │ Drive Robot      │
                                     └──────────────────┘
```

---

# 6. Sensor Configuration Experiments

A central part of the research is the controlled comparison of sensor configurations.

| Configuration | Vision | Wheel Odometry | IMU |
| :-----------: | :----: | :------------: | :-: |
|     **S1**    |    ✓   |        —       |  —  |
|     **S2**    |    ✓   |        ✓       |  —  |
|     **S3**    |    ✓   |        —       |  ✓  |
|     **S4**    |    ✓   |        ✓       |  ✓  |

This allows the contribution of individual sensing modalities and their combination to be experimentally investigated.

---

# 7. Visual Degradation Framework

To evaluate robustness, the framework introduces controlled visual disturbances.

### Current / Planned Conditions

* Gaussian blur
* Reduced image resolution
* Low illumination
* Image noise
* Motion blur
* Compression artifacts
* Partial occlusion

Example degradation levels:

```text
Clean
   │
   ├── Blur
   │     ├── σ = 3
   │     ├── σ = 7
   │     └── σ = 13
   │
   ├── Resolution
   │     ├── 100%
   │     ├── 50%
   │     └── 12.5%
   │
   └── Illumination
         ├── 50%
         ├── 20%
         └── 5%
```

The purpose is to create a controlled experimental environment where navigation robustness can be measured quantitatively.

---

# 8. Evaluation Methodology

The experimental framework is designed around repeated and controlled trials.

For each experiment, the system records relevant information such as:

```text
experiment_id
sensor_configuration
environment
visual_condition
severity
random_seed
ground_truth_pose
estimated_pose
navigation_success
collision
time_to_goal
path_length
localization_error
```

### Primary Metrics

| Metric                      | Purpose                                         |
| --------------------------- | ----------------------------------------------- |
| **ATE RMSE**                | Measures trajectory/localization error          |
| **Navigation Success Rate** | Measures task completion                        |
| **Collision Rate**          | Measures safety/robustness                      |
| **Time to Goal**            | Measures efficiency                             |
| **Path Length**             | Measures navigation efficiency                  |
| **Path Efficiency**         | Compares travelled distance with reference path |
| **Orientation Error**       | Measures heading estimation                     |
| **Computational Cost**      | Measures system efficiency                      |

---

# 9. Ground-Truth Evaluation

Gazebo provides access to simulated ground-truth robot pose.

The framework uses this information during experiments to compare:

```text
Ground Truth Trajectory
          vs
Estimated Trajectory
```

A simplified trajectory error can be represented as:

```text
e(t) = √[(x_gt - x_est)² + (y_gt - y_est)²]
```

and aggregated over the trajectory to calculate an appropriate error metric such as ATE RMSE.

Ground truth is used **for evaluation**, not as an input to the navigation algorithm.

---

# 10. Navigation Architecture

The navigation pipeline is organized as:

```text
Goal
 │
 ▼
Global Planning
 │
 ▼
Waypoint / Path Generation
 │
 ▼
Localization
 │
 ▼
Local Control
 │
 ▼
/cmd_vel
 │
 ▼
Differential Drive Robot
```

The current waypoint navigation layer supports target-coordinate navigation and state-machine-based motion control.

Future extensions include integration with more advanced global/local planning and reinforcement-learning-based navigation.

---

# 11. Reinforcement Learning Extension

The project includes a Gymnasium-compatible navigation environment and Stable-Baselines3 PPO infrastructure.

The RL component is treated as an **extension to the classical navigation baseline**, rather than replacing the experimental baseline.

### Planned RL Pipeline

```text
Robot State + Visual Features + Goal
                │
                ▼
        Gymnasium Environment
                │
                ▼
              PPO
                │
                ▼
       Navigation Policy
                │
                ▼
             cmd_vel
```

Training and evaluation will measure:

* cumulative reward
* navigation success
* collision rate
* episode length
* time to goal
* path length
* robustness under visual degradation

The RL experiments will be evaluated independently from the classical navigation experiments.

---

# 12. Sim-to-Real Architecture

The long-term physical platform consists of:

### Hardware

* ESP32-CAM
* ESP32-S3
* 25GA370 encoder motors
* Motor driver
* MPU6050 IMU
* Differential-drive chassis

### Hardware Architecture

```text
                 ESP32-CAM
                    │
                 Camera
                    │
                  Wi-Fi
                    │
                    ▼
             ┌──────────────┐
             │ PC / ROS 2   │
             │              │
             │ Vision       │
             │ Localization │
             │ Navigation   │
             │ RL           │
             └──────┬───────┘
                    │
                 cmd_vel
                    │
                    ▼
             ┌──────────────┐
             │  ESP32-S3    │
             │              │
             │ Encoders     │
             │ MPU6050      │
             │ Motor PID    │
             └──────┬───────┘
                    │
                    ▼
              Motor Driver
                    │
                    ▼
             25GA370 Motors
```

The software architecture is intentionally designed around standard ROS 2 interfaces so that high-level components can eventually operate with physical hardware.

---

# 13. Simulation-to-Real Research

The physical robot is not simply a demonstration platform.

It will be used to investigate the gap between simulated and real-world performance.

The comparison will consider:

* localization error
* navigation success
* collision behavior
* trajectory length
* completion time
* visual degradation
* sensor noise
* communication latency
* wheel slip
* lighting variation

This allows the project to move from simulation-based evaluation toward real-world validation.

---

# 14. Repository Structure

```text
robust-visual-navigation/
│
├── README.md
├── LICENSE
├── CHANGELOG.md
│
├── start_demo.sh
├── save_map.sh
├── experiment_log.csv
│
├── src/
│   └── visual_navigation_robot/
│       │
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       │
│       ├── config/
│       │   ├── building_locations.yaml
│       │   ├── building_map.yaml
│       │   └── ...
│       │
│       ├── launch/
│       │   ├── gazebo.launch.py
│       │   ├── mapping.launch.py
│       │   └── slam.launch.py
│       │
│       ├── visual_navigation_robot/
│       │   │
│       │   ├── localization/
│       │   ├── navigation/
│       │   ├── perception/
│       │   └── reinforcement_learning/
│       │
│       └── web_ui/
│           ├── index.html
│           └── app.js
│
├── experiments/
│   ├── raw/
│   ├── processed/
│   ├── tables/
│   ├── figures/
│   ├── analyze_results.py
│   └── generate_mock_trials.py
│
├── docs/
│   ├── research_questions.md
│   ├── hypothesis.md
│   ├── experiment_plan.md
│   ├── methodology.md
│   └── research_paper_draft.md
│
└── models/
```

---

# 15. Installation

## Requirements

Recommended environment:

* Ubuntu 22.04 / 24.04
* ROS 2 Humble / Kilted
* Gazebo
* Python 3
* colcon
* RViz2

Additional ROS packages may include:

```bash
sudo apt update

sudo apt install -y \
  ros-${ROS_DISTRO}-slam-toolbox \
  ros-${ROS_DISTRO}-nav2-map-server \
  ros-${ROS_DISTRO}-rosbridge-server \
  ros-${ROS_DISTRO}-web-video-server
```

### Build

```bash
cd ~/robust-visual-navigation

colcon build --symlink-install

source install/setup.bash
```

---

# 16. Quick Start

### Launch the simulation

```bash
source ~/robust-visual-navigation/install/setup.bash

ros2 launch visual_navigation_robot gazebo.launch.py
```

### Start the sensor-fusion pipeline

```bash
source ~/robust-visual-navigation/install/setup.bash

ros2 launch visual_navigation_robot mapping.launch.py \
  sensor_config:=s4
```

### Start waypoint navigation

```bash
source ~/robust-visual-navigation/install/setup.bash

ros2 run visual_navigation_robot waypoint_navigator \
  --ros-args \
  -p goal_x:=5.0 \
  -p goal_y:=2.0 \
  -p use_sim_time:=true
```

---

# 17. Experimental Workflow

The recommended research workflow is:

```text
Environment Verification
          ↓
Robot Simulation
          ↓
Sensor Integration
          ↓
Localization
          ↓
Sensor Fusion
          ↓
Classical Navigation Baseline
          ↓
Controlled Experiments
          ↓
Visual Degradation
          ↓
Statistical Analysis
          ↓
Reinforcement Learning
          ↓
Physical Robot
          ↓
Sim-to-Real Evaluation
          ↓
Research Findings
```

---

# 18. Research Reproducibility

Reproducibility is a core design principle of this project.

Experiments should preserve:

* configuration parameters
* random seeds
* software version
* model version
* environment
* sensor configuration
* degradation settings
* raw measurements
* processed results

Raw experimental data should be separated from generated summaries and figures.

Example:

```text
experiments/
├── raw/
├── processed/
├── tables/
└── figures/
```

This allows results to be independently regenerated from the underlying data.

---

# 19. Current Research Status

### System Development

* [x] ROS 2 workspace
* [x] Gazebo simulation
* [x] Differential-drive robot
* [x] ROS 2 communication
* [x] Camera pipeline
* [x] IMU pipeline
* [x] Wheel odometry
* [x] Sensor-fusion architecture
* [x] Waypoint navigation
* [x] Experimental logging infrastructure
* [x] Visual degradation framework
* [x] PPO training infrastructure

### Research Validation

* [ ] Full repeated-trial benchmark
* [ ] Statistical analysis of real experimental trials
* [ ] Controlled sensor-ablation study
* [ ] Robustness evaluation
* [ ] RL evaluation
* [ ] Physical robot implementation
* [ ] Sim-to-real experiments
* [ ] Final research conclusions

> **Important:** Infrastructure completion does not imply experimental validation. Benchmark values should only be reported as research findings after they have been generated from reproducible experimental trials.

---

# 20. Academic Contribution

The project is designed around a research question rather than solely around system implementation.

The intended research contribution is to experimentally investigate:

1. The effect of sensor configuration on localization performance.
2. The effect of visual degradation on autonomous navigation.
3. The role of multi-sensor fusion in maintaining robustness.
4. The computational and performance trade-offs of different sensing configurations.
5. The transfer of navigation policies and state-estimation approaches from simulation to a low-cost physical platform.

The final contribution will be defined from the experimentally supported findings rather than predetermined results.

---

# 21. Future Research Directions

Potential extensions include:

* Robust visual odometry
* Learned visual representations
* Vision transformers
* Explainable navigation
* Uncertainty-aware sensor fusion
* Domain randomization
* Adversarial visual degradation
* Robust reinforcement learning
* Adaptive sensor selection
* Edge AI deployment
* Multi-robot navigation
* Dynamic obstacle avoidance
* Real-world long-duration experiments

---

# 22. Research Outputs

The project is intended to produce several research artifacts:

### Software

A modular ROS 2 autonomous-navigation framework.

### Experimental Dataset

Structured trajectory and navigation-performance measurements under controlled sensing conditions.

### Analysis Pipeline

Reproducible scripts for generating tables and figures from experimental data.

### Physical Prototype

A low-cost differential-drive robot for sim-to-real validation.

### Academic Manuscript

A research paper documenting:

* research motivation
* methodology
* experimental design
* results
* statistical analysis
* limitations
* conclusions

---

# 23. Academic Positioning

This project combines several areas of computer science and robotics:

```text
Computer Vision
       +
Robotics
       +
Sensor Fusion
       +
State Estimation
       +
Autonomous Navigation
       +
Reinforcement Learning
       +
Robust AI
       +
Sim-to-Real
```

It is intended as a research portfolio project demonstrating the complete research cycle:

```text
Research Question
      ↓
System Design
      ↓
Implementation
      ↓
Controlled Experiment
      ↓
Data Collection
      ↓
Statistical Analysis
      ↓
Interpretation
      ↓
Research Communication
```

---

# 24. Citation

If this repository contributes to academic work, please cite the associated publication once available.

```bibtex
@software{tanim_robust_visual_navigation,
  author  = {Md. Sahadat Hossen Tanim},
  title   = {Robust Vision-Based Autonomous Navigation for Low-Cost Mobile Robots},
  year    = {2026},
  url     = {https://github.com/iamtanim0195/robust-visual-navigation}
}
```

> **Note:** The citation metadata should be updated when a DOI, conference publication, or journal publication becomes available.

---

# 25. Author

**Md. Sahadat Hossen Tanim**

B.Sc. in Computer Science and Engineering
Hamdard University Bangladesh

Research interests:

* Computer Vision
* Robotics
* Autonomous Navigation
* Sensor Fusion
* Reinforcement Learning
* Explainable AI
* Robust AI
* Sim-to-Real Learning

GitHub:

https://github.com/iamtanim0195/robust-visual-navigation

---

## License

This project is released under the **Apache License 2.0**.

See [LICENSE](LICENSE) for details.
