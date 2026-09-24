# Quantitative Evaluation Metrics

## 1. Absolute Trajectory Error (ATE)
Measures overall trajectory consistency against ground-truth pose $P^{gt}$ over total time steps $T$:

$$\text{ATE}_{RMSE} = \sqrt{ \frac{1}{T} \sum_{t=1}^{T} || \mathbf{p}_{t}^{gt} - \mathbf{p}_{t}^{est} ||^2 }$$

## 2. Navigation Success Rate (SR)
Ratio of successful goal arrivals ($d_{goal} \le 0.2 \text{ m}$ without collision) to total attempts $N_{total}$:

$$\text{SR} = \frac{N_{success}}{N_{total}} \times 100\%$$

## 3. Path Length Efficiency (PLE)
Ratio of optimal trajectory length $L_{opt}$ to executed path length $L_{exec}$:

$$\text{PLE} = \frac{L_{opt}}{L_{exec}}$$

## 4. Mean Computational Cost (CPU / Latency)
Average node processing time $\Delta t_{proc}$ (ms) per control cycle and CPU/RAM usage percentage.