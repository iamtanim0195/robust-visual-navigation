#!/bin/bash

echo "=================================================="
echo " Saving Live SLAM Map..."
echo "=================================================="

source /opt/ros/kilted/setup.bash
source ~/robust-visual-navigation/install/setup.bash

CONFIG_DIR="$HOME/robust-visual-navigation/src/visual_navigation_robot/config"
MAP_PATH="$CONFIG_DIR/building_map"

# 1. Save Map image (.pgm & .yaml) via slam_toolbox service
RESPONSE=$(ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: {data: '$MAP_PATH'}}")

echo "$RESPONSE"

if echo "$RESPONSE" | grep -q "result=1"; then
    echo "=================================================="
    echo " SUCCESS! Map saved successfully via slam_toolbox."
    echo " Files located at: $MAP_PATH"
    echo "=================================================="
    exit 0
fi

# 2. Fallback to nav2_map_server CLI if service fails
echo "Attempting fallback via nav2_map_server..."
ros2 run nav2_map_server map_saver_cli -f "$MAP_PATH" --ros-args \
  -p use_sim_time:=true \
  -p map_subscribe_transient_local:=true \
  -p save_map_timeout:=10.0

if [ -f "${MAP_PATH}.yaml" ]; then
    echo "=================================================="
    echo " SUCCESS! Map saved via map_saver_cli."
    echo "=================================================="
else
    echo "=================================================="
    echo " FAIL: Could not save map files."
    echo "=================================================="
fi