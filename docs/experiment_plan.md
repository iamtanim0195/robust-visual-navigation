# Experimental Protocol & Evaluation Matrix

## Independent Variables
1. **Sensor Configurations ($S$)**:
   - $S_1$: Vision Only
   - $S_2$: Vision + Wheel Odometry
   - $S_3$: Vision + IMU
   - $S_4$: Vision + Wheel Odometry + IMU (Full Fusion)

2. **Visual Degradation Modes ($D$)**:
   - Clean (Nominal lighting, clear lens)
   - Gaussian Blur (Levels: Low $\sigma=1$, Med $\sigma=3$, High $\sigma=5$)
   - Resolution Reduction (Levels: 100%, 50%, 25% downsampling)
   - Low Illumination (Levels: 100%, 30%, 10% brightness reduction)

3. **Environments ($E$)**:
   - $E_1$: Corridor World (Gazebo Sim)
   - $E_2$: Obstacle World (Gazebo Sim)
   - $E_3$: Physical Test Arena (Real Hardware)

## Test Protocol
- Each condition $(S_i, D_j, E_k)$ will undergo **$N = 10$ repeated evaluation runs** with randomized start/goal configurations or fixed waypoint tracks.
- Total Simulation Trials: $4 \text{ configs} \times 10 \text{ degradation variants} \times 10 \text{ runs} = 400 \text{ runs}$.