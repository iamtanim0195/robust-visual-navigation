# Research Hypotheses & Testability

## Primary Hypothesis ($H_1$)
Fusing visual features with wheel odometry and inertial measurements (EKF-based state estimation) significantly reduces localization error (ATE) and increases goal-reaching success rate under visual degradation compared to vision-only navigation.

## Null Hypothesis ($H_0$)
Multi-sensor fusion provides no statistically significant difference ($p \ge 0.05$) in localization error or goal completion success rate compared to vision-only navigation under visual degradation conditions.

## Sub-Hypotheses
- **$H_{sub1}$**: Wheel odometry + IMU fusion will bound state estimation drift during complete visual blackout, enabling partial goal recovery.
- **$H_{sub2}$**: Reinforcement Learning policies trained on mixed/degraded visual inputs will demonstrate higher success rates under unseen visual noise than classical planners relying on un-adapted visual features.

## Rejection & Verification Criteria
- $H_0$ will be rejected in favor of $H_1$ if a two-tailed paired t-test or Wilcoxon signed-rank test yields $p < 0.05$ across repeated evaluation trials under identical degradation levels.
- Negative or non-significant results will be explicitly documented without parameter manipulation.