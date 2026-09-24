# Project Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - Phase 4 Complete
### Added
- Created Gazebo Sim plugins for differential drive (`robot_gazebo.xacro`).
- Designed indoor test arena SDF world (`worlds/research_world.sdf`).
- Created Gazebo launch script (`launch/gazebo.launch.py`) with ROS-Gazebo topic bridges.

## [0.4.1] - Phase 3 Refinement
### Changed
- Updated `urdf/robot_core.xacro` to a rectangular 2WD chassis (0.20m x 0.15m x 0.06m) with 2 rear drive wheels and 1 front caster wheel.
- Updated `rviz/robot_view.rviz` panel classes (`rviz_common`) for ROS 2 Kilted compatibility.

## [0.4.0] - Phase 3 Complete
### Added
- Created URDF/Xacro robot model (`robot_core.xacro`, `materials.xacro`, `robot.urdf.xacro`).
- Created RViz2 visualization setup (`robot_view.rviz`) and launch file (`display_robot.launch.py`).

## [0.3.0] - Phase 2 Complete
### Added
- Created primary ROS 2 package `visual_navigation_robot` (`ament_python`).
- Added package layout directories: `launch/`, `urdf/`, `worlds/`, `config/`, `rviz/`, `meshes/`.

## [0.2.0] - Phase 1 Complete
### Added
- Formulated academic research docs in `docs/`: `research_problem.md`, `research_questions.md`, `hypothesis.md`, `system_architecture.md`, `experiment_plan.md`, and `evaluation_metrics.md`.
- Established experimental test matrix ($400$ systematic trial protocol) and REP-105 coordinate frame conventions.

## [0.1.0] - Phase 0 Complete
### Added
- Environment verification for Ubuntu 24.04 LTS, ROS 2 Kilted Kaiju, and Gazebo Sim 9.5.0.
- Primary workspace directory structure `~/visual_navigation_ws/src`.
- System specification documentation in `docs/project_overview.md`.