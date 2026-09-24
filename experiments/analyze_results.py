import os
import glob
import pandas as pd
import numpy as np

def compute_trial_stats(csv_path):
    df = pd.read_csv(csv_path)
    if df.empty or 'error_m' not in df.columns:
        return None

    ate_rmse = np.sqrt(np.mean(df['error_m']**2))
    ate_max = df['error_m'].max()
    ate_std = df['error_m'].std()
    
    # Calculate total trajectory length
    dx = np.diff(df['gt_x'])
    dy = np.diff(df['gt_y'])
    path_len = np.sum(np.sqrt(dx**2 + dy**2))

    filename = os.path.basename(csv_path).replace('.csv', '')
    parts = filename.split('_')
    
    config = parts[1] if len(parts) > 1 else 'unknown'
    deg_mode = parts[2] if len(parts) > 2 else 'clean'

    return {
        'Trial': filename,
        'Config': config.upper(),
        'Degradation': deg_mode.capitalize(),
        'ATE_RMSE_m': round(ate_rmse, 4),
        'ATE_Max_m': round(ate_max, 4),
        'ATE_Std_m': round(ate_std, 4),
        'Path_Length_m': round(path_len, 2)
    }

def main():
    raw_dir = 'experiments/raw'
    csv_files = glob.glob(os.path.join(raw_dir, '*.csv'))

    if not csv_files:
        print(f"No CSV trial logs found in {raw_dir}. Run evaluation trials to generate logs.")
        return

    results = []
    for f in csv_files:
        stats = compute_trial_stats(f)
        if stats:
            results.append(stats)

    res_df = pd.DataFrame(results)
    
    output_table_path = 'experiments/tables/ate_benchmark_summary.csv'
    os.makedirs('experiments/tables', exist_ok=True)
    res_df.to_csv(output_table_path, index=False)

    print("\n=======================================================")
    print("      EXPERIMENTAL BENCHMARK EVALUATION SUMMARY        ")
    print("=======================================================\n")
    print(res_df.to_string(index=False))
    print(f"\nSummary table saved to: {output_table_path}\n")

if __name__ == '__main__':
    main()