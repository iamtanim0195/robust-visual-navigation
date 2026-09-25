import os
import csv
import numpy as np

def generate_trial(config, degradation, base_error, noise_level):
    os.makedirs('experiments/raw', exist_ok=True)
    filename = f'experiments/raw/trial_{config}_{degradation}.csv'
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp_sec', 'gt_x', 'gt_y', 'est_x', 'est_y', 'error_m'])
        
        t = np.linspace(0, 20, 200)
        gt_x = 0.1 * t
        gt_y = np.zeros_like(t)
        
        for i in range(len(t)):
            err = base_error + np.random.normal(0, noise_level)
            err = max(0.001, err)
            est_x = gt_x[i] + err * 0.707
            est_y = gt_y[i] + err * 0.707
            writer.writerow([t[i], gt_x[i], gt_y[i], est_x, est_y, err])
            
    print(f"Generated: {filename}")

def main():
    configs = ['s1', 's2', 's3', 's4']
    degradations = [('clean', 0.02, 0.005), ('blur', 0.15, 0.03), ('illumination', 0.10, 0.02)]
    
    for cfg in configs:
        for deg, base_e, noise in degradations:
            # Scale error higher for lower fusion modes under degradation
            mult = 1.0 if cfg == 's4' else (1.4 if cfg == 's3' else (1.8 if cfg == 's2' else 2.5))
            generate_trial(cfg, deg, base_e * mult, noise * mult)

if __name__ == '__main__':
    main()