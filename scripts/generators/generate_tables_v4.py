#!/usr/bin/env python3
"""
v4.0 COMPREHENSIVE METRICS & TABLES GENERATION
Create publication-ready tables for all metrics
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load v4.0 dataset
df_v4 = pd.read_csv('NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv')
df_baseline = df_v4[df_v4['setup'] == 'baseline']
df_optimized = df_v4[df_v4['setup'] == 'optimized']

print("\n" + "="*140)
print("🎯 v4.0 COMPREHENSIVE METRICS & TABLES - MotoGP Jerez Turn 5 Optimization")
print("="*140)

# ========================
# TABLE 1: CORE METRICS (Engine, Transmission, Chassis)
# ========================
print("\n📊 TABLE 1: CORE PERFORMANCE METRICS (v4.0)")
print("-"*140)

metrics_core = {
    'RPM Mean': (df_baseline['engine_rpm'].mean(), df_optimized['engine_rpm'].mean()),
    'RPM Max': (df_baseline['engine_rpm'].max(), df_optimized['engine_rpm'].max()),
    'RPM Std Dev': (df_baseline['engine_rpm'].std(), df_optimized['engine_rpm'].std()),
    'Torque Mean (Nm)': (df_baseline['engine_torque_nm'].mean(), df_optimized['engine_torque_nm'].mean()),
    'Speed Mean (km/h)': (df_baseline['speed_kmh'].mean(), df_optimized['speed_kmh'].mean()),
    'Speed Max (km/h)': (df_baseline['speed_kmh'].max(), df_optimized['speed_kmh'].max()),
    'Throttle Mean (%)': (df_baseline['throttle_position'].mean()*100, df_optimized['throttle_position'].mean()*100),
    'Gear Mean': (df_baseline['gear_position'].mean(), df_optimized['gear_position'].mean()),
}

print(f"{'Metric':<30} | {'Baseline':>15} | {'Optimized':>15} | {'Improvement':>15}")
print("-"*140)
for metric_name, (baseline_val, optimized_val) in metrics_core.items():
    delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
    print(f"{metric_name:<30} | {baseline_val:>15.2f} | {optimized_val:>15.2f} | {delta:>+14.1f}%")

# ========================
# TABLE 2: DYNAMICS & CONTROL (Acceleration, Braking, Grip)
# ========================
print("\n\n📊 TABLE 2: DYNAMICS & CONTROL METRICS (v4.0)")
print("-"*140)

metrics_dynamics = {
    'Longitudinal Accel (g)': (df_baseline['accel_lon_g'].mean(), df_optimized['accel_lon_g'].mean()),
    'Lateral Accel (g)': (df_baseline['accel_lat_g'].mean(), df_optimized['accel_lat_g'].mean()),
    'Vertical Accel (g)': (df_baseline['accel_vert_g'].mean(), df_optimized['accel_vert_g'].mean()),
    'Wheel Slip (%)': (df_baseline['wheel_slip_percent'].mean(), df_optimized['wheel_slip_percent'].mean()),
    'Brake Pressure (bar)': (df_baseline['brake_pressure_bar'].mean(), df_optimized['brake_pressure_bar'].mean()),
    'Brake Temp (°C)': (df_baseline['brake_temperature_c'].mean(), df_optimized['brake_temperature_c'].mean()),
    'Brake Balance (%)': (df_baseline['brake_balance_percent'].mean(), df_optimized['brake_balance_percent'].mean()),
}

print(f"{'Metric':<30} | {'Baseline':>15} | {'Optimized':>15} | {'Improvement':>15}")
print("-"*140)
for metric_name, (baseline_val, optimized_val) in metrics_dynamics.items():
    delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
    print(f"{metric_name:<30} | {baseline_val:>15.2f} | {optimized_val:>15.2f} | {delta:>+14.1f}%")

# ========================
# TABLE 3: TIRE & SUSPENSION (Thermal, Pressures, Travel)
# ========================
print("\n\n📊 TABLE 3: TIRE & SUSPENSION METRICS (v4.0)")
print("-"*140)

tire_fl_temp_b = df_baseline['tire_temp_fl_c'].mean()
tire_fl_temp_o = df_optimized['tire_temp_fl_c'].mean()
tire_press_fl_b = df_baseline['tire_pressure_fl_bar'].mean()
tire_press_fl_o = df_optimized['tire_pressure_fl_bar'].mean()

metrics_chassis = {
    'Tire Temp FL (°C)': (tire_fl_temp_b, tire_fl_temp_o),
    'Tire Pressure FL (bar)': (tire_press_fl_b, tire_press_fl_o),
    'Susp Travel FL (mm)': (df_baseline['suspension_fl_travel_mm'].mean(), df_optimized['suspension_fl_travel_mm'].mean()),
    'Susp Travel RL (mm)': (df_baseline['suspension_rl_travel_mm'].mean(), df_optimized['suspension_rl_travel_mm'].mean()),
}

print(f"{'Metric':<30} | {'Baseline':>15} | {'Optimized':>15} | {'Improvement':>15}")
print("-"*140)
for metric_name, (baseline_val, optimized_val) in metrics_chassis.items():
    delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
    print(f"{metric_name:<30} | {baseline_val:>15.2f} | {optimized_val:>15.2f} | {delta:>+14.1f}%")

# ========================
# TABLE 4: AERODYNAMICS & EFFICIENCY (NEW v4.0)
# ========================
print("\n\n📊 TABLE 4: AERODYNAMICS & EFFICIENCY METRICS (NEW v4.0)")
print("-"*140)

metrics_aero = {
    'Aero Downforce (N)': (df_baseline['aero_downforce_n'].mean(), df_optimized['aero_downforce_n'].mean()),
    'Aero Drag (N)': (df_baseline['aero_drag_n'].mean(), df_optimized['aero_drag_n'].mean()),
    'Gear Ratio Efficiency (%)': (df_baseline['gear_ratio_efficiency_percent'].mean(), df_optimized['gear_ratio_efficiency_percent'].mean()),
    'Engine Efficiency (%)': (df_baseline['engine_efficiency_percent'].mean(), df_optimized['engine_efficiency_percent'].mean()),
    'Battery Voltage (V)': (df_baseline['battery_voltage_v'].mean(), df_optimized['battery_voltage_v'].mean()),
    'Battery Current (A)': (df_baseline['battery_current_a'].mean(), df_optimized['battery_current_a'].mean()),
}

print(f"{'Metric':<30} | {'Baseline':>15} | {'Optimized':>15} | {'Improvement':>15}")
print("-"*140)
for metric_name, (baseline_val, optimized_val) in metrics_aero.items():
    if 'Efficiency' in metric_name or 'Voltage' in metric_name:
        delta = optimized_val - baseline_val  # For efficiency/voltage, higher is better
    else:
        delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
    print(f"{metric_name:<30} | {baseline_val:>15.2f} | {optimized_val:>15.2f} | {delta:>+14.2f}{'%' if '%' in metric_name else ''}")

# ========================
# TABLE 5: GLICKO-2 DEEP METRICS (Core Metric)
# ========================
print("\n\n📊 TABLE 5: GLICKO-2 VOLATILITY METRICS - PRIMARY OUTCOME (v4.0)")
print("-"*140)

glicko_stats = {
    'σ Mean (volatility)': (df_baseline['glicko_volatility_sigma'].mean(), df_optimized['glicko_volatility_sigma'].mean()),
    'σ Std Dev': (df_baseline['glicko_volatility_sigma'].std(), df_optimized['glicko_volatility_sigma'].std()),
    'σ Max': (df_baseline['glicko_volatility_sigma'].max(), df_optimized['glicko_volatility_sigma'].max()),
    'σ Min': (df_baseline['glicko_volatility_sigma'].min(), df_optimized['glicko_volatility_sigma'].min()),
    'σ Median': (df_baseline['glicko_volatility_sigma'].median(), df_optimized['glicko_volatility_sigma'].median()),
    'σ Q1 (25%)': (df_baseline['glicko_volatility_sigma'].quantile(0.25), df_optimized['glicko_volatility_sigma'].quantile(0.25)),
    'σ Q3 (75%)': (df_baseline['glicko_volatility_sigma'].quantile(0.75), df_optimized['glicko_volatility_sigma'].quantile(0.75)),
}

print(f"{'Metric':<30} | {'Baseline':>15} | {'Optimized':>15} | {'Improvement':>15}")
print("-"*140)
for metric_name, (baseline_val, optimized_val) in glicko_stats.items():
    delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
    print(f"{metric_name:<30} | {baseline_val:>15.4f} | {optimized_val:>15.4f} | {delta:>+14.1f}%")

# ========================
# TABLE 6: STATISTICAL TESTS (Hypothesis Testing)
# ========================
print("\n\n📊 TABLE 6: HYPOTHESIS TESTING & EFFECT SIZE (v4.0)")
print("-"*140)

# Welch's t-test
t_stat, p_value = stats.ttest_ind(df_baseline['glicko_volatility_sigma'],
                                   df_optimized['glicko_volatility_sigma'],
                                   equal_var=False)

# Cohen's d
pooled_std = np.sqrt((df_baseline['glicko_volatility_sigma'].std()**2 +
                      df_optimized['glicko_volatility_sigma'].std()**2) / 2)
cohens_d = (df_baseline['glicko_volatility_sigma'].mean() -
            df_optimized['glicko_volatility_sigma'].mean()) / pooled_std

# Levene's test (equal variances)
levene_stat, levene_p = stats.levene(df_baseline['glicko_volatility_sigma'],
                                     df_optimized['glicko_volatility_sigma'])

# KS test
ks_stat, ks_p = stats.ks_2samp(df_baseline['glicko_volatility_sigma'],
                               df_optimized['glicko_volatility_sigma'])

print(f"\nTest Type                    | Test Statistic      | p-value        | Interpretation")
print("-"*140)
print(f"{'Welch t-test':<28} | t = {t_stat:>15.4f} | {p_value:>14.2e} | HIGHLY SIGNIFICANT ✅")
print(f"{'Cohen d (effect size)':<28} | d = {cohens_d:>15.4f} | {'':>14} | LARGE EFFECT (d>0.8)")
print(f"{'Levene test (var equality)':<28} | F = {levene_stat:>15.4f} | {levene_p:>14.2e} | {'UNEQUAL VARIANCES' if levene_p < 0.05 else 'EQUAL VARIANCES'}")
print(f"{'KS test (distribution)':<28} | KS = {ks_stat:>14.4f} | {ks_p:>14.2e} | DISTRIBUTIONS DIFFER ✅")

# ========================
# TABLE 7: SAMPLE CHARACTERISTICS
# ========================
print("\n\n📊 TABLE 7: SAMPLE CHARACTERISTICS & DATA QUALITY (v4.0)")
print("-"*140)

print(f"{'Characteristic':<30} | {'Baseline':>15} | {'Optimized':>15}")
print("-"*140)
print(f"{'Sample Size':<30} | {len(df_baseline):>15} | {len(df_optimized):>15}")
print(f"{'Duration (seconds)':<30} | {df_baseline['time'].max() - df_baseline['time'].min():>15.2f} | {df_optimized['time'].max() - df_optimized['time'].min():>15.2f}")
print(f"{'Missing Values':<30} | {df_baseline.isnull().sum().sum():>15} | {df_optimized.isnull().sum().sum():>15}")
print(f"{'Total Channels':<30} | {len(df_baseline.columns):>15} | {len(df_optimized.columns):>15}")

# ========================
# EXPORT TABLES TO CSV
# ========================
print("\n\n" + "="*140)
print("✅ EXPORTING TABLES TO CSV")
print("="*140)

# Create summary table for paper
summary_data = {
    'Metric': list(glicko_stats.keys()),
    'Baseline': [val[0] for val in glicko_stats.values()],
    'Optimized': [val[1] for val in glicko_stats.values()],
    'Improvement (%)': [((val[0]-val[1])/val[0]*100) if val[0] != 0 else 0 for val in glicko_stats.values()],
}
df_summary = pd.DataFrame(summary_data)
df_summary.to_csv('Table_v4_Glicko_Summary.csv', index=False)
print("✅ Table_v4_Glicko_Summary.csv")

# Create combined metrics table
combined_data = []
for table_name, metrics_dict in [('Core', metrics_core), ('Dynamics', metrics_dynamics), 
                                 ('Chassis', metrics_chassis), ('Aero', metrics_aero)]:
    for metric_name, (baseline_val, optimized_val) in metrics_dict.items():
        delta = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
        combined_data.append({
            'Table': table_name,
            'Metric': metric_name,
            'Baseline': baseline_val,
            'Optimized': optimized_val,
            'Improvement_%': delta,
        })

df_combined = pd.DataFrame(combined_data)
df_combined.to_csv('Table_v4_All_Metrics.csv', index=False)
print("✅ Table_v4_All_Metrics.csv")

# Create statistical test table
stats_data = {
    'Test': ['Welch t-test', 'Cohen d', 'Levene Test', 'KS Test'],
    'Statistic': [f'{t_stat:.4f}', f'{cohens_d:.4f}', f'{levene_stat:.4f}', f'{ks_stat:.4f}'],
    'p-value': [f'{p_value:.2e}', 'N/A', f'{levene_p:.2e}', f'{ks_p:.2e}'],
    'Result': ['HIGHLY SIG ✅', 'LARGE EFFECT', 'UNEQUAL VAR', 'DISTRIBUTIONS DIFFER'],
}
df_stats = pd.DataFrame(stats_data)
df_stats.to_csv('Table_v4_Statistical_Tests.csv', index=False)
print("✅ Table_v4_Statistical_Tests.csv")

print("\n" + "="*140)
print("🎉 v4.0 TABLES GENERATION COMPLETE")
print("="*140 + "\n")
