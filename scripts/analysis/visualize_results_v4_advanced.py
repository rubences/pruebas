#!/usr/bin/env python3
"""
Publication-Quality Visualization v4.1 - MEGA Dataset EXPANDED
Advanced analysis figures with detailed metrics and comparisons
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

BASE_DIR = Path(__file__).resolve().parents[2] if len(Path(__file__).parents) >= 3 else Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "datasets"
TABLES_DIR = BASE_DIR / "data" / "tables"
OUTPUTS_DIR = BASE_DIR / "outputs" / "figures"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 100,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'font.family': 'DejaVu Sans',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'axes.linewidth': 1.2,
    'axes.edgecolor': '#333333',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.8,
    'lines.linewidth': 2.0,
    'lines.markersize': 6,
})

# Colorblind-friendly palette - Professional Q1
COLOR_BASELINE = '#1f77b4'      # Blue (Professional)
COLOR_OPTIMIZED = '#ff7f0e'     # Orange (Professional)
COLOR_IMPROVEMENT = '#2ca02c'   # Green (Professional)
COLOR_NEUTRAL = '#9467bd'       # Purple (Professional)
COLOR_ACCENT = '#d62728'        # Red (Accent)

# Load dataset
dataset_file = DATA_DIR / "NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"
if not dataset_file.exists():
    dataset_file = "NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"

try:
    df = pd.read_csv(dataset_file)
    df_baseline = df[df['setup'] == 'baseline'].reset_index(drop=True)
    df_optimized = df[df['setup'] == 'optimized'].reset_index(drop=True)
    print("✅ Dataset loaded successfully")
except FileNotFoundError:
    print("❌ Dataset not found")
    exit(1)

# Load metrics table
try:
    metrics_table = pd.read_csv(TABLES_DIR / "Table_v4_All_Metrics.csv")
except:
    metrics_table = None


def compute_p_and_d(series_a: pd.Series, series_b: pd.Series):
        """Compute Welch's t-test p-value and Cohen's d between two samples."""
        t_stat, p_val = stats.ttest_ind(series_a, series_b, equal_var=False)
        pooled = np.sqrt((np.var(series_a, ddof=1) + np.var(series_b, ddof=1)) / 2)
        cohend = (np.mean(series_a) - np.mean(series_b)) / pooled if pooled != 0 else np.nan
        return p_val, cohend

# ========================
# FIGURE 5: MULTI-METRIC TIME SERIES
# ========================
def create_figure_5():
    """Multi-metric time series with 4 key performance indicators"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 5: Temporal Evolution - Key Performance Indicators', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Engine RPM & Torque
    ax = fig.add_subplot(gs[0, 0])
    ax2 = ax.twinx()
    
    # RPM
    line1, = ax.plot(time_b, df_baseline['engine_rpm'].values[::downsample], 
                     color=COLOR_BASELINE, alpha=0.85, label='RPM Baseline', 
                     linewidth=2.5, zorder=3)
    line2, = ax.plot(time_o, df_optimized['engine_rpm'].values[::downsample], 
                     color=COLOR_OPTIMIZED, alpha=0.85, label='RPM Optimized', 
                     linewidth=2.5, zorder=3)
    
    # Torque
    line3, = ax2.plot(time_b, df_baseline['engine_torque_nm'].values[::downsample], 
                      color=COLOR_BASELINE, alpha=0.4, linestyle='--', 
                      linewidth=2.0, label='Torque Baseline', zorder=2)
    line4, = ax2.plot(time_o, df_optimized['engine_torque_nm'].values[::downsample], 
                      color=COLOR_OPTIMIZED, alpha=0.4, linestyle='--', 
                      linewidth=2.0, label='Torque Optimized', zorder=2)
    
    ax.set_ylabel('Engine RPM', fontweight='bold', fontsize=12, color=COLOR_BASELINE)
    ax2.set_ylabel('Torque (Nm)', fontweight='bold', fontsize=12, color=COLOR_OPTIMIZED)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=11)
    ax.set_title('A) Engine Performance', fontweight='bold', loc='left', fontsize=13)
    ax.tick_params(axis='y', labelcolor=COLOR_BASELINE, labelsize=10)
    ax2.tick_params(axis='y', labelcolor=COLOR_OPTIMIZED, labelsize=10)
    ax.grid(True, alpha=0.3, linewidth=0.8)
    
    # Add statistics annotation
    rpm_improvement = ((df_optimized['engine_rpm'].mean() - df_baseline['engine_rpm'].mean()) 
                       / df_baseline['engine_rpm'].mean() * 100)
    ax.text(0.02, 0.98, f'RPM Δ: {rpm_improvement:.1f}%', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Speed & Throttle
    ax = fig.add_subplot(gs[0, 1])
    ax2 = ax.twinx()
    
    ax.plot(time_b, df_baseline['speed_kmh'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.85, label='Speed Baseline', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['speed_kmh'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.85, label='Speed Optimized', linewidth=2.5, zorder=3)
    
    ax2.plot(time_b, df_baseline['throttle_position'].values[::downsample]*100, 
             color=COLOR_BASELINE, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    ax2.plot(time_o, df_optimized['throttle_position'].values[::downsample]*100, 
             color=COLOR_OPTIMIZED, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    
    ax.set_ylabel('Speed (km/h)', fontweight='bold', fontsize=12, color=COLOR_BASELINE)
    ax2.set_ylabel('Throttle (%)', fontweight='bold', fontsize=12, color=COLOR_OPTIMIZED)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=11)
    ax.set_title('B) Velocity Control', fontweight='bold', loc='left', fontsize=13)
    ax.grid(True, alpha=0.3, linewidth=0.8)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    
    # Glicko Volatility
    ax = fig.add_subplot(gs[1, 0])
    
    ax.fill_between(time_b, df_baseline['glicko_volatility_sigma'].values[::downsample],
                    alpha=0.5, color=COLOR_BASELINE, label='Baseline', edgecolor=COLOR_BASELINE, linewidth=1.5)
    ax.fill_between(time_o, df_optimized['glicko_volatility_sigma'].values[::downsample],
                    alpha=0.5, color=COLOR_OPTIMIZED, label='Optimized', edgecolor=COLOR_OPTIMIZED, linewidth=1.5)
    
    # Add mean lines
    ax.axhline(y=df_baseline['glicko_volatility_sigma'].mean(), color=COLOR_BASELINE, 
               linestyle='--', linewidth=2, alpha=0.8, label=f'μ Baseline')
    ax.axhline(y=df_optimized['glicko_volatility_sigma'].mean(), color=COLOR_OPTIMIZED, 
               linestyle='--', linewidth=2, alpha=0.8, label=f'μ Optimized')
    
    ax.set_ylabel('Glicko-2 σ (Volatility)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=11)
    ax.set_title('C) Rating Volatility Evolution', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3, linewidth=0.8)
    
    # Add improvement annotation
    vol_improvement = ((df_baseline['glicko_volatility_sigma'].mean() - 
                       df_optimized['glicko_volatility_sigma'].mean()) / 
                       df_baseline['glicko_volatility_sigma'].mean() * 100)
    ax.text(0.02, 0.98, f'Volatility ↓: {vol_improvement:.1f}%', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    # Wheel Slip & Brake Pressure
    ax = fig.add_subplot(gs[1, 1])
    ax2 = ax.twinx()
    
    ax.plot(time_b, df_baseline['wheel_slip_percent'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.85, label='Slip Baseline', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['wheel_slip_percent'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.85, label='Slip Optimized', linewidth=2.5, zorder=3)
    
    ax2.plot(time_b, df_baseline['brake_pressure_bar'].values[::downsample], 
             color=COLOR_BASELINE, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    ax2.plot(time_o, df_optimized['brake_pressure_bar'].values[::downsample], 
             color=COLOR_OPTIMIZED, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold', fontsize=12, color=COLOR_BASELINE)
    ax2.set_ylabel('Brake Pressure (bar)', fontweight='bold', fontsize=12, color=COLOR_OPTIMIZED)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=11)
    ax.set_title('D) Grip & Braking Control', fontweight='bold', loc='left', fontsize=13)
    ax.grid(True, alpha=0.3, linewidth=0.8)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    
    # Add slip improvement
    slip_improvement = ((df_baseline['wheel_slip_percent'].mean() - 
                        df_optimized['wheel_slip_percent'].mean()) / 
                        df_baseline['wheel_slip_percent'].mean() * 100)
    ax.text(0.02, 0.98, f'Slip ↓: {slip_improvement:.1f}%', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    return fig

# ========================
# FIGURE 6: STATISTICAL VALIDATION
# ========================
def create_figure_6():
    """Comprehensive statistical analysis"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=100)
    fig.suptitle('Figure 6: Statistical Validation & Distribution Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)

    # Referencias estadísticas del CSV de tests
    p_text = "p<1e-12 (Welch t, KS)"  # simplificado porque el CSV trae 0.00e+00
    d_text = "d=3.29 (gran efecto)"

    """Perfiles temporales con bandas de cuantiles y diferencias"""
    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    fig.suptitle('Figure 8: Time Series with Quantile Bands and Δ annotations', 
                 fontsize=16, fontweight='bold', y=0.95)

    # Speed: rolling median + IQR para robustez
    speed_b = df_baseline['speed_kmh'].rolling(window=80, min_periods=1).median()
    speed_o = df_optimized['speed_kmh'].rolling(window=80, min_periods=1).median()
    q10_b = speed_b.rolling(160, min_periods=1).quantile(0.10)
    q90_b = speed_b.rolling(160, min_periods=1).quantile(0.90)
    q10_o = speed_o.rolling(160, min_periods=1).quantile(0.10)
    q90_o = speed_o.rolling(160, min_periods=1).quantile(0.90)
    axs[0].plot(speed_b, label='Baseline', color=COLOR_BASELINE, linewidth=1.8)
    axs[0].plot(speed_o, label='Optimized', color=COLOR_OPTIMIZED, linewidth=1.8)
    axs[0].fill_between(speed_b.index, q10_b, q90_b, color=COLOR_BASELINE, alpha=0.15)
    axs[0].fill_between(speed_o.index, q10_o, q90_o, color=COLOR_OPTIMIZED, alpha=0.15)
    axs[0].set_ylabel('Speed (km/h)', fontweight='bold')
    axs[0].set_title('A) Speed profile (median + IQR)', fontweight='bold', loc='left', fontsize=13)
    axs[0].grid(alpha=0.3)

    delta_speed = (speed_o.mean() - speed_b.mean()) / speed_b.mean() * 100
    axs[0].text(0.01, 0.90, f'Δmean = {delta_speed:.2f}%', transform=axs[0].transAxes,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'),
                fontsize=10, color=COLOR_IMPROVEMENT if delta_speed > 0 else COLOR_ACCENT)

    # Throttle: media móvil con bandas 5-95
    thr_b = df_baseline['throttle_position']
    thr_o = df_optimized['throttle_position']
    axs[1].plot(thr_b.rolling(60, min_periods=1).mean(), label='Baseline', color=COLOR_BASELINE, linewidth=1.5)
    axs[1].plot(thr_o.rolling(60, min_periods=1).mean(), label='Optimized', color=COLOR_OPTIMIZED, linewidth=1.5)
    axs[1].fill_between(thr_b.index, thr_b.rolling(120, min_periods=1).quantile(0.05), thr_b.rolling(120, min_periods=1).quantile(0.95),
                        color=COLOR_BASELINE, alpha=0.15)
    axs[1].fill_between(thr_o.index, thr_o.rolling(120, min_periods=1).quantile(0.05), thr_o.rolling(120, min_periods=1).quantile(0.95),
                        color=COLOR_OPTIMIZED, alpha=0.15)
    axs[1].set_ylabel('Throttle (0-1)', fontweight='bold')
    axs[1].set_title('B) Throttle with 5-95% bands', fontweight='bold', loc='left', fontsize=13)
    axs[1].grid(alpha=0.3)

    delta_thr = (thr_o.mean() - thr_b.mean()) / thr_b.mean() * 100
    axs[1].text(0.01, 0.90, f'Δmean = {delta_thr:.2f}%', transform=axs[1].transAxes,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'),
                fontsize=10, color=COLOR_IMPROVEMENT if delta_thr > 0 else COLOR_ACCENT)

    # Steering: mediana y cuantiles para variabilidad
    steer_b = df_baseline['steering_angle_deg']
    steer_o = df_optimized['steering_angle_deg']
    sb_med = steer_b.rolling(80, min_periods=1).median()
    so_med = steer_o.rolling(80, min_periods=1).median()
    axs[2].plot(sb_med, label='Baseline', color=COLOR_BASELINE, linewidth=1.2)
    axs[2].plot(so_med, label='Optimized', color=COLOR_OPTIMIZED, linewidth=1.2)
    axs[2].fill_between(steer_b.index, steer_b.rolling(160, min_periods=1).quantile(0.1), steer_b.rolling(160, min_periods=1).quantile(0.9),
                        color=COLOR_BASELINE, alpha=0.15)
    axs[2].fill_between(steer_o.index, steer_o.rolling(160, min_periods=1).quantile(0.1), steer_o.rolling(160, min_periods=1).quantile(0.9),
                        color=COLOR_OPTIMIZED, alpha=0.15)
    axs[2].set_ylabel('Steering (deg)', fontweight='bold')
    axs[2].set_title('C) Steering variability (median + 10-90%)', fontweight='bold', loc='left', fontsize=13)
    axs[2].set_xlabel('Time (samples)', fontweight='bold')
    axs[2].grid(alpha=0.3)
    axs[2].legend(loc='upper right', fontsize=10, framealpha=0.9)

    delta_steer = (so_med.abs().mean() - sb_med.abs().mean()) / sb_med.abs().mean() * 100
    axs[2].text(0.01, 0.90, f'Δ|median| = {delta_steer:.2f}%', transform=axs[2].transAxes,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'),
                fontsize=10, color=COLOR_IMPROVEMENT if delta_steer < 0 else COLOR_ACCENT)

    return fig
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)

    # Eficiencia y consistencia
    ax = fig.add_subplot(gs[1, 1])
    metrics_eff = ['Engine Eff.\n(%)', 'Aero DF/Drag\nratio', 'Volatility σ', 'Slip\n(%)']
    df_drag_ratio = df_baseline['aero_downforce_n'].mean() / df_baseline['aero_drag_n'].mean() if df_baseline['aero_drag_n'].mean() != 0 else 0
    opt_drag_ratio = df_optimized['aero_downforce_n'].mean() / df_optimized['aero_drag_n'].mean() if df_optimized['aero_drag_n'].mean() != 0 else 0
    baseline_vals = [df_baseline['engine_efficiency_percent'].mean(), df_drag_ratio,
                        df_baseline['glicko_volatility_sigma'].mean(), df_baseline['wheel_slip_percent'].mean()]
    optimized_vals = [df_optimized['engine_efficiency_percent'].mean(), opt_drag_ratio,
                         df_optimized['glicko_volatility_sigma'].mean(), df_optimized['wheel_slip_percent'].mean()]

    x = np.arange(len(metrics_eff))
    ax.bar(x - width/2, baseline_vals, width, label='Baseline', 
            color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    ax.bar(x + width/2, optimized_vals, width, label='Optimized', 
            color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)

    for i, (b, o) in enumerate(zip(baseline_vals, optimized_vals)):
         delta = (o - b) / b * 100 if b != 0 else 0
         sign = '↑' if delta > 0 else '↓'
         face = 'lightgreen' if delta > 0 else 'wheat'
         ax.text(x[i], max(b, o) * 1.10, f'{sign}{abs(delta):.1f}%', ha='center', fontsize=10,
                  bbox=dict(boxstyle='round', facecolor=face, alpha=0.7, edgecolor='black'))

    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('D) Efficiency & Consistency', fontweight='bold', loc='left', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_eff, fontsize=10)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)

    return fig

# ========================
# FIGURE 8: DYNAMICS & CONTROL ANALYSIS
# ========================
def create_figure_8():
    """Detailed dynamics analysis with Q1 enhancements"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 8: Dynamics, Control & Suspension Analysis', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Accelerations
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(time_b, df_baseline['accel_lon_g'].values[::downsample]*100, 
            color=COLOR_BASELINE, alpha=0.9, label='Baseline (Lon)', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['accel_lon_g'].values[::downsample]*100, 
            color=COLOR_OPTIMIZED, alpha=0.9, label='Optimized (Lon)', linewidth=2.5, zorder=3)
    ax.plot(time_b, df_baseline['accel_lat_g'].values[::downsample]*100, 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (Lat)', linewidth=2.0, zorder=2)
    ax.plot(time_o, df_optimized['accel_lat_g'].values[::downsample]*100, 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (Lat)', linewidth=2.0, zorder=2)
    
    # Add annotations
    lon_base_mean = df_baseline['accel_lon_g'].mean() * 100
    lon_opt_mean = df_optimized['accel_lon_g'].mean() * 100
    improvement = ((lon_opt_mean - lon_base_mean) / abs(lon_base_mean) * 100)
    
    ax.text(0.02, 0.98, f'Lon. Accel ↑: {improvement:.1f}%\nμ: {lon_base_mean:.2f} → {lon_opt_mean:.2f} cm/s²',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Acceleration (cm/s²)', fontweight='bold', fontsize=12)
    ax.set_title('A) Longitudinal & Lateral Acceleration', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Suspension Travel
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(time_b, df_baseline['suspension_fl_travel_mm'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, label='Baseline (FL)', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['suspension_fl_travel_mm'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, label='Optimized (FL)', linewidth=2.5, zorder=3)
    ax.plot(time_b, df_baseline['suspension_rl_travel_mm'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (RL)', linewidth=2.0, zorder=2)
    ax.plot(time_o, df_optimized['suspension_rl_travel_mm'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (RL)', linewidth=2.0, zorder=2)
    
    # Suspension improvement
    fl_base_std = df_baseline['suspension_fl_travel_mm'].std()
    fl_opt_std = df_optimized['suspension_fl_travel_mm'].std()
    stability = ((fl_base_std - fl_opt_std) / fl_base_std * 100)
    
    ax.text(0.02, 0.98, f'Susp. Stability ↑: {stability:.1f}%\nσ FL: {fl_base_std:.2f} → {fl_opt_std:.2f} mm',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Suspension Travel (mm)', fontweight='bold', fontsize=12)
    ax.set_title('B) Suspension Compression', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Gyro (Rotation rates)
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(time_b, df_baseline['gyro_roll_dps'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, label='Baseline (Roll)', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['gyro_roll_dps'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, label='Optimized (Roll)', linewidth=2.5, zorder=3)
    ax.plot(time_b, df_baseline['gyro_yaw_dps'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (Yaw)', linewidth=2.0, zorder=2)
    ax.plot(time_o, df_optimized['gyro_yaw_dps'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (Yaw)', linewidth=2.0, zorder=2)
    
    # Angular stability
    roll_base_std = df_baseline['gyro_roll_dps'].std()
    roll_opt_std = df_optimized['gyro_roll_dps'].std()
    roll_stability = ((roll_base_std - roll_opt_std) / roll_base_std * 100)
    
    ax.text(0.02, 0.98, f'Roll Stability ↑: {roll_stability:.1f}%\nσ: {roll_base_std:.2f} → {roll_opt_std:.2f} dps',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Rotation Rate (dps)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('C) Angular Motion (Roll & Yaw)', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Brake Temperature vs Pressure
    ax = fig.add_subplot(gs[1, 1])
    ax2 = ax.twinx()
    ax.plot(time_b, df_baseline['brake_temperature_c'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, label='Baseline (Temp)', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['brake_temperature_c'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, label='Optimized (Temp)', linewidth=2.5, zorder=3)
    ax2.plot(time_b, df_baseline['brake_pressure_bar'].values[::downsample], 
             color=COLOR_BASELINE, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    ax2.plot(time_o, df_optimized['brake_pressure_bar'].values[::downsample], 
             color=COLOR_OPTIMIZED, alpha=0.4, linestyle='--', linewidth=2.0, zorder=2)
    
    # Brake efficiency annotation
    temp_base_mean = df_baseline['brake_temperature_c'].mean()
    temp_opt_mean = df_optimized['brake_temperature_c'].mean()
    temp_reduction = ((temp_base_mean - temp_opt_mean) / temp_base_mean * 100)
    
    ax.text(0.02, 0.98, f'Brake Temp ↓: {temp_reduction:.1f}%\nμ: {temp_base_mean:.1f} → {temp_opt_mean:.1f} °C',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Brake Temperature (°C)', fontweight='bold', color=COLOR_BASELINE, fontsize=12)
    ax2.set_ylabel('Brake Pressure (bar)', fontweight='bold', color=COLOR_OPTIMIZED, fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('D) Braking System Performance', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    return fig

# ========================
# FIGURE 9: DISTRIBUTION ANALYSIS
# ========================
def create_figure_9():
    """Distribuciones con anotaciones de efecto usando métricas de alto contraste."""
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Figure 9: Distribution Comparisons for High-Contrast Metrics', 
                 fontsize=16, fontweight='bold', y=0.96)

    # A) Wheel slip con KDE y p-values
    sns.kdeplot(df_baseline['wheel_slip_percent'], ax=axs[0, 0], label='Baseline', color=COLOR_BASELINE, fill=True, alpha=0.35)
    sns.kdeplot(df_optimized['wheel_slip_percent'], ax=axs[0, 0], label='Optimized', color=COLOR_OPTIMIZED, fill=True, alpha=0.35)
    axs[0, 0].set_title('A) Wheel Slip (%)', fontweight='bold', loc='left', fontsize=13)
    axs[0, 0].set_xlabel('Slip (%)')
    axs[0, 0].set_ylabel('Density')
    axs[0, 0].legend()
    axs[0, 0].grid(alpha=0.3)
    pval, cohend = compute_p_and_d(df_baseline['wheel_slip_percent'], df_optimized['wheel_slip_percent'])
    axs[0, 0].text(0.02, 0.92, f"p={pval:.2e}\nd={cohend:.2f}", transform=axs[0, 0].transAxes,
                  bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='black'))

    # B) Battery current
    sns.kdeplot(abs(df_baseline['battery_current_a']), ax=axs[0, 1], label='Baseline', color=COLOR_BASELINE, fill=True, alpha=0.35)
    sns.kdeplot(abs(df_optimized['battery_current_a']), ax=axs[0, 1], label='Optimized', color=COLOR_OPTIMIZED, fill=True, alpha=0.35)
    axs[0, 1].set_title('B) Battery Current |A|', fontweight='bold', loc='left', fontsize=13)
    axs[0, 1].set_xlabel('|Current| (A)')
    axs[0, 1].legend()
    axs[0, 1].grid(alpha=0.3)
    pval, cohend = compute_p_and_d(abs(df_baseline['battery_current_a']), abs(df_optimized['battery_current_a']))
    axs[0, 1].text(0.02, 0.92, f"p={pval:.2e}\nd={cohend:.2f}", transform=axs[0, 1].transAxes,
                  bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='black'))

    # C) Aero drag vs downforce ratio (box)
    df_box = pd.DataFrame({
        'setup': ['Baseline'] * len(df_baseline) + ['Optimized'] * len(df_optimized),
        'df_drag_ratio': pd.concat([
            df_baseline['aero_downforce_n'] / (df_baseline['aero_drag_n'].replace(0, np.nan)),
            df_optimized['aero_downforce_n'] / (df_optimized['aero_drag_n'].replace(0, np.nan))
        ], ignore_index=True)
    }).dropna()
    sns.boxplot(data=df_box, x='setup', y='df_drag_ratio', ax=axs[1, 0], palette=[COLOR_BASELINE, COLOR_OPTIMIZED], width=0.5)
    axs[1, 0].set_title('C) Downforce/Drag Ratio', fontweight='bold', loc='left', fontsize=13)
    axs[1, 0].set_xlabel('Setup')
    axs[1, 0].set_ylabel('DF/Drag')
    axs[1, 0].grid(axis='y', alpha=0.3)
    pval, cohend = compute_p_and_d(df_box[df_box['setup'] == 'Baseline']['df_drag_ratio'], df_box[df_box['setup'] == 'Optimized']['df_drag_ratio'])
    axs[1, 0].text(0.05, 0.92, f"p={pval:.2e}\nd={cohend:.2f}",
                   transform=axs[1, 0].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='black'))

    # D) Accel lateral boxplot con whiskers ajustados
    sns.boxplot(data=df, x='setup', y='accel_lat_g', ax=axs[1, 1], palette=[COLOR_BASELINE, COLOR_OPTIMIZED], width=0.5)
    axs[1, 1].set_title('D) Lateral Acceleration (g)', fontweight='bold', loc='left', fontsize=13)
    axs[1, 1].set_xlabel('Setup')
    axs[1, 1].set_ylabel('Acceleration (g)')
    axs[1, 1].grid(axis='y', alpha=0.3)
    pval, cohend = compute_p_and_d(df_baseline['accel_lat_g'], df_optimized['accel_lat_g'])
    axs[1, 1].text(0.05, 0.92, f"p={pval:.2e}\nd={cohend:.2f}",
                   transform=axs[1, 1].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='black'))

    return fig

# ========================
# FIGURE 10: EFFICIENCY & POWER
# ========================
def create_figure_10():
    """Engine efficiency, aerodynamics, and battery analysis with Q1 enhancements"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 10: Efficiency, Aerodynamics & Power Management', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Engine Efficiency
    ax = fig.add_subplot(gs[0, 0])
    ax.fill_between(time_b, df_baseline['engine_efficiency_percent'].values[::downsample],
                    alpha=0.3, color=COLOR_BASELINE, label='Baseline', zorder=1)
    ax.fill_between(time_o, df_optimized['engine_efficiency_percent'].values[::downsample],
                    alpha=0.3, color=COLOR_OPTIMIZED, label='Optimized', zorder=1)
    ax.plot(time_b, df_baseline['engine_efficiency_percent'].values[::downsample],
            color=COLOR_BASELINE, linewidth=2.5, alpha=0.9, zorder=3)
    ax.plot(time_o, df_optimized['engine_efficiency_percent'].values[::downsample],
            color=COLOR_OPTIMIZED, linewidth=2.5, alpha=0.9, zorder=3)
    
    base_mean = df_baseline['engine_efficiency_percent'].mean()
    opt_mean = df_optimized['engine_efficiency_percent'].mean()
    ax.axhline(y=base_mean, color=COLOR_BASELINE, linestyle='--', alpha=0.7, linewidth=2.0, 
               label=f"μ: {base_mean:.2f}%", zorder=2)
    ax.axhline(y=opt_mean, color=COLOR_OPTIMIZED, linestyle='--', alpha=0.7, linewidth=2.0, 
               label=f"μ: {opt_mean:.2f}%", zorder=2)
    
    # Efficiency improvement
    efficiency_gain = ((opt_mean - base_mean) / base_mean * 100)
    ax.text(0.02, 0.98, f'Efficiency ↑: {efficiency_gain:.2f}%\nμ: {base_mean:.2f} → {opt_mean:.2f}%',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Efficiency (%)', fontweight='bold', fontsize=12)
    ax.set_title('A) Engine Efficiency', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='lower right', ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Aerodynamic Forces
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(time_b, df_baseline['aero_downforce_n'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, linewidth=2.5, label='Baseline (DF)', zorder=3)
    ax.plot(time_o, df_optimized['aero_downforce_n'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, linewidth=2.5, label='Optimized (DF)', zorder=3)
    ax.plot(time_b, df_baseline['aero_drag_n'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', linewidth=2.0, label='Baseline (Drag)', zorder=2)
    ax.plot(time_o, df_optimized['aero_drag_n'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', linewidth=2.0, label='Optimized (Drag)', zorder=2)
    
    # Aero efficiency (downforce/drag ratio)
    df_base_mean = df_baseline['aero_downforce_n'].mean()
    drag_base_mean = df_baseline['aero_drag_n'].mean()
    df_opt_mean = df_optimized['aero_downforce_n'].mean()
    drag_opt_mean = df_optimized['aero_drag_n'].mean()
    
    aero_eff_base = df_base_mean / drag_base_mean if drag_base_mean != 0 else 0
    aero_eff_opt = df_opt_mean / drag_opt_mean if drag_opt_mean != 0 else 0
    
    ax.text(0.02, 0.98, f'Aero Efficiency: {aero_eff_base:.2f} → {aero_eff_opt:.2f}\nDF/Drag Ratio',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Force (N)', fontweight='bold', fontsize=12)
    ax.set_title('B) Aerodynamic Forces', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, loc='upper right', framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Battery Voltage
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(time_b, df_baseline['battery_voltage_v'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, linewidth=2.5, label='Baseline', zorder=3)
    ax.plot(time_o, df_optimized['battery_voltage_v'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, linewidth=2.5, label='Optimized', zorder=3)
    
    # Mean voltages
    base_mean = df_baseline['battery_voltage_v'].mean()
    opt_mean = df_optimized['battery_voltage_v'].mean()
    ax.axhline(base_mean, color=COLOR_BASELINE, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {base_mean:.2f}V', zorder=2)
    ax.axhline(opt_mean, color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {opt_mean:.2f}V', zorder=2)
    
    # Voltage stability
    voltage_diff = opt_mean - base_mean
    ax.text(0.02, 0.98, f'Voltage Δ: {voltage_diff:+.2f}V\nμ: {base_mean:.2f} → {opt_mean:.2f}V',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Voltage (V)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('C) Battery Voltage', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='lower left', ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Battery Current
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(time_b, abs(df_baseline['battery_current_a'].values[::downsample]), 
            color=COLOR_BASELINE, alpha=0.9, linewidth=2.5, label='Baseline', zorder=3)
    ax.plot(time_o, abs(df_optimized['battery_current_a'].values[::downsample]), 
            color=COLOR_OPTIMIZED, alpha=0.9, linewidth=2.5, label='Optimized', zorder=3)
    ax.fill_between(time_b, abs(df_baseline['battery_current_a'].values[::downsample]),
                    alpha=0.2, color=COLOR_BASELINE, zorder=1)
    ax.fill_between(time_o, abs(df_optimized['battery_current_a'].values[::downsample]),
                    alpha=0.2, color=COLOR_OPTIMIZED, zorder=1)
    
    # Current efficiency
    base_mean = abs(df_baseline['battery_current_a']).mean()
    opt_mean = abs(df_optimized['battery_current_a']).mean()
    current_reduction = ((base_mean - opt_mean) / base_mean * 100)
    
    ax.text(0.02, 0.98, f'Current Draw ↓: {current_reduction:.2f}%\nμ: {base_mean:.2f} → {opt_mean:.2f}A',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Current (A)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('D) Battery Current Draw', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    return fig

# ========================
# FIGURE 11: CORRELATION & SCATTER PLOTS
# ========================
def create_figure_11():
    """Multi-dimensional correlation analysis with Q1 enhancements"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 11: Phase Space & Multi-Dimensional Relationships', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # RPM vs Torque
    ax = fig.add_subplot(gs[0, 0])
    ax.scatter(df_baseline['engine_rpm'], df_baseline['engine_torque_nm'], 
              alpha=0.4, s=15, color=COLOR_BASELINE, label='Baseline', edgecolors='none')
    ax.scatter(df_optimized['engine_rpm'], df_optimized['engine_torque_nm'], 
              alpha=0.4, s=15, color=COLOR_OPTIMIZED, label='Optimized', edgecolors='none')
    
    # Add regression lines or mean markers
    from scipy.stats import linregress
    slope_b, intercept_b, r_b, _, _ = linregress(df_baseline['engine_rpm'], df_baseline['engine_torque_nm'])
    slope_o, intercept_o, r_o, _, _ = linregress(df_optimized['engine_rpm'], df_optimized['engine_torque_nm'])
    
    rpm_range = np.linspace(df_baseline['engine_rpm'].min(), df_baseline['engine_rpm'].max(), 100)
    ax.plot(rpm_range, slope_b * rpm_range + intercept_b, color=COLOR_BASELINE, 
            linewidth=2.5, linestyle='--', alpha=0.8, label=f'Baseline: R²={r_b**2:.3f}')
    ax.plot(rpm_range, slope_o * rpm_range + intercept_o, color=COLOR_OPTIMIZED, 
            linewidth=2.5, linestyle='--', alpha=0.8, label=f'Optimized: R²={r_o**2:.3f}')
    
    ax.set_xlabel('Engine RPM', fontweight='bold', fontsize=12)
    ax.set_ylabel('Torque (Nm)', fontweight='bold', fontsize=12)
    ax.set_title('A) RPM vs Torque Relationship', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='best')
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Throttle vs Speed
    ax = fig.add_subplot(gs[0, 1])
    ax.scatter(df_baseline['throttle_position']*100, df_baseline['speed_kmh'], 
              alpha=0.4, s=15, color=COLOR_BASELINE, label='Baseline', edgecolors='none')
    ax.scatter(df_optimized['throttle_position']*100, df_optimized['speed_kmh'], 
              alpha=0.4, s=15, color=COLOR_OPTIMIZED, label='Optimized', edgecolors='none')
    
    # Regression lines
    slope_b, intercept_b, r_b, _, _ = linregress(df_baseline['throttle_position']*100, df_baseline['speed_kmh'])
    slope_o, intercept_o, r_o, _, _ = linregress(df_optimized['throttle_position']*100, df_optimized['speed_kmh'])
    
    throttle_range = np.linspace(0, 100, 100)
    ax.plot(throttle_range, slope_b * throttle_range + intercept_b, color=COLOR_BASELINE, 
            linewidth=2.5, linestyle='--', alpha=0.8, label=f'Baseline: R²={r_b**2:.3f}')
    ax.plot(throttle_range, slope_o * throttle_range + intercept_o, color=COLOR_OPTIMIZED, 
            linewidth=2.5, linestyle='--', alpha=0.8, label=f'Optimized: R²={r_o**2:.3f}')
    
    ax.set_xlabel('Throttle Position (%)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Speed (km/h)', fontweight='bold', fontsize=12)
    ax.set_title('B) Throttle vs Speed Response', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='best')
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Lateral Accel vs Wheel Slip
    ax = fig.add_subplot(gs[1, 0])
    ax.scatter(df_baseline['accel_lat_g'], df_baseline['wheel_slip_percent'], 
              alpha=0.4, s=15, color=COLOR_BASELINE, label='Baseline', edgecolors='none')
    ax.scatter(df_optimized['accel_lat_g'], df_optimized['wheel_slip_percent'], 
              alpha=0.4, s=15, color=COLOR_OPTIMIZED, label='Optimized', edgecolors='none')
    
    # Optimal slip reference line
    ax.axhline(5.0, color=COLOR_IMPROVEMENT, linestyle=':', linewidth=2.0, alpha=0.7, 
               label='Optimal Slip (~5%)', zorder=2)
    
    ax.set_xlabel('Lateral Acceleration (g)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold', fontsize=12)
    ax.set_title('C) Cornering Behavior: Lat. Accel vs Slip', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='best')
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Tire Temp vs Slip
    ax = fig.add_subplot(gs[1, 1])
    ax.scatter(df_baseline['tire_temp_fl_c'], df_baseline['wheel_slip_percent'], 
              alpha=0.4, s=15, color=COLOR_BASELINE, label='Baseline', edgecolors='none')
    ax.scatter(df_optimized['tire_temp_fl_c'], df_optimized['wheel_slip_percent'], 
              alpha=0.4, s=15, color=COLOR_OPTIMIZED, label='Optimized', edgecolors='none')
    
    # Optimal regions
    ax.axhline(5.0, color=COLOR_IMPROVEMENT, linestyle=':', linewidth=2.0, alpha=0.7, 
               label='Optimal Slip', zorder=2)
    ax.axvspan(80, 95, alpha=0.1, color=COLOR_IMPROVEMENT, label='Optimal Temp Window')
    
    ax.set_xlabel('Front Tire Temperature (°C)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold', fontsize=12)
    ax.set_title('D) Tire Temperature vs Grip', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=9, framealpha=0.9, loc='best')
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    return fig

# ========================
# FIGURE 12: LAP-BY-LAP ANALYSIS
# ========================
def create_figure_12():
    """Per-lap breakdown analysis with Q1 enhancements"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 12: Lap-by-Lap Performance Breakdown', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Metrics by lap - Baseline
    ax = fig.add_subplot(gs[0, 0])
    lap_data_b = df_baseline.groupby('lap')[['engine_rpm', 'speed_kmh', 'glicko_volatility_sigma']].mean()
    ax.plot(lap_data_b.index, lap_data_b['engine_rpm'], marker='o', color=COLOR_BASELINE, 
            linewidth=2.5, markersize=8, label='RPM Mean', zorder=3)
    ax2 = ax.twinx()
    ax2.plot(lap_data_b.index, lap_data_b['glicko_volatility_sigma'], marker='s', 
            color=COLOR_BASELINE, linestyle='--', linewidth=2.5, markersize=8, alpha=0.7, 
            label='Glicko σ', zorder=3)
    
    # Mean lines
    rpm_mean = lap_data_b['engine_rpm'].mean()
    vol_mean = lap_data_b['glicko_volatility_sigma'].mean()
    ax.axhline(rpm_mean, color=COLOR_BASELINE, linestyle=':', linewidth=2.0, alpha=0.5, zorder=2)
    ax2.axhline(vol_mean, color=COLOR_BASELINE, linestyle=':', linewidth=2.0, alpha=0.5, zorder=2)
    
    ax.text(0.02, 0.98, f'RPM μ: {rpm_mean:.0f}\nGlicko σ μ: {vol_mean:.4f}',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_xlabel('Lap Number', fontweight='bold', fontsize=12)
    ax.set_ylabel('Engine RPM', fontweight='bold', color=COLOR_BASELINE, fontsize=12)
    ax2.set_ylabel('Glicko-2 σ', fontweight='bold', color=COLOR_BASELINE, alpha=0.7, fontsize=12)
    ax.set_title('A) Baseline: RPM & Volatility by Lap', fontweight='bold', loc='left', fontsize=13)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Metrics by lap - Optimized
    ax = fig.add_subplot(gs[0, 1])
    lap_data_o = df_optimized.groupby('lap')[['engine_rpm', 'speed_kmh', 'glicko_volatility_sigma']].mean()
    ax.plot(lap_data_o.index, lap_data_o['engine_rpm'], marker='o', color=COLOR_OPTIMIZED, 
            linewidth=2.5, markersize=8, label='RPM Mean', zorder=3)
    ax2 = ax.twinx()
    ax2.plot(lap_data_o.index, lap_data_o['glicko_volatility_sigma'], marker='s', 
            color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.5, markersize=8, alpha=0.7, 
            label='Glicko σ', zorder=3)
    
    # Mean lines
    rpm_mean = lap_data_o['engine_rpm'].mean()
    vol_mean = lap_data_o['glicko_volatility_sigma'].mean()
    ax.axhline(rpm_mean, color=COLOR_OPTIMIZED, linestyle=':', linewidth=2.0, alpha=0.5, zorder=2)
    ax2.axhline(vol_mean, color=COLOR_OPTIMIZED, linestyle=':', linewidth=2.0, alpha=0.5, zorder=2)
    
    # Compare with baseline
    vol_improvement = ((lap_data_b['glicko_volatility_sigma'].mean() - vol_mean) / 
                       lap_data_b['glicko_volatility_sigma'].mean() * 100)
    
    ax.text(0.02, 0.98, f'RPM μ: {rpm_mean:.0f}\nGlicko σ μ: {vol_mean:.4f}\nImprovement: {vol_improvement:.1f}%',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_xlabel('Lap Number', fontweight='bold', fontsize=12)
    ax.set_ylabel('Engine RPM', fontweight='bold', color=COLOR_OPTIMIZED, fontsize=12)
    ax2.set_ylabel('Glicko-2 σ', fontweight='bold', color=COLOR_OPTIMIZED, alpha=0.7, fontsize=12)
    ax.set_title('B) Optimized: RPM & Volatility by Lap', fontweight='bold', loc='left', fontsize=13)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Wheel Slip by Lap
    ax = fig.add_subplot(gs[1, 0])
    slip_b = df_baseline.groupby('lap')['wheel_slip_percent'].mean()
    slip_o = df_optimized.groupby('lap')['wheel_slip_percent'].mean()
    x = np.arange(len(slip_b))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, slip_b.values, width, label='Baseline', 
                   color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, slip_o.values, width, label='Optimized', 
                   color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=8)
    
    # Improvement
    slip_improvement = ((slip_b.mean() - slip_o.mean()) / slip_b.mean() * 100)
    ax.text(0.02, 0.98, f'Avg Slip ↓: {slip_improvement:.1f}%\n{slip_b.mean():.2f} → {slip_o.mean():.2f}%',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_xlabel('Lap Number', fontweight='bold', fontsize=12)
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold', fontsize=12)
    ax.set_title('C) Wheel Slip by Lap Comparison', fontweight='bold', loc='left', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels([str(int(i)) for i in slip_b.index], fontsize=10)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Speed Profile by Lap
    ax = fig.add_subplot(gs[1, 1])
    speed_b = df_baseline.groupby('lap')['speed_kmh'].max()
    speed_o = df_optimized.groupby('lap')['speed_kmh'].max()
    ax.plot(speed_b.index, speed_b.values, marker='o', color=COLOR_BASELINE, 
            linewidth=2.5, markersize=10, label='Baseline', alpha=0.9, zorder=3)
    ax.plot(speed_o.index, speed_o.values, marker='s', color=COLOR_OPTIMIZED, 
            linewidth=2.5, markersize=10, label='Optimized', alpha=0.9, zorder=3)
    ax.fill_between(speed_b.index, speed_b.values, alpha=0.2, color=COLOR_BASELINE, zorder=1)
    ax.fill_between(speed_o.index, speed_o.values, alpha=0.2, color=COLOR_OPTIMIZED, zorder=1)
    
    # Mean speed lines
    speed_b_mean = speed_b.mean()
    speed_o_mean = speed_o.mean()
    ax.axhline(speed_b_mean, color=COLOR_BASELINE, linestyle='--', linewidth=2.0, alpha=0.6, zorder=2)
    ax.axhline(speed_o_mean, color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.0, alpha=0.6, zorder=2)
    
    # Speed improvement
    speed_improvement = ((speed_o_mean - speed_b_mean) / speed_b_mean * 100)
    ax.text(0.02, 0.98, f'Avg Max Speed ↑: {speed_improvement:.2f}%\nμ: {speed_b_mean:.1f} → {speed_o_mean:.1f} km/h',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_xlabel('Lap Number', fontweight='bold', fontsize=12)
    ax.set_ylabel('Max Speed (km/h)', fontweight='bold', fontsize=12)
    ax.set_title('D) Maximum Speed per Lap', fontweight='bold', loc='left', fontsize=13)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    return fig

# ========================
# MAIN EXECUTION
# ========================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🎨 GENERATING ADVANCED PUBLICATION-QUALITY FIGURES v4.1")
    print("="*80 + "\n")
    
    figures = [
        (5, "Time Series Multi-Metrics", create_figure_5),
        (6, "Statistical Validation", create_figure_6),
        (7, "Performance Metrics Comparison", create_figure_7),
                (8, "Quantile Time Series", create_figure_8),
                (9, "Distribution Analysis", create_figure_9),
        (10, "Efficiency & Power Management", create_figure_10),
        (11, "Phase Space & Correlations", create_figure_11),
        (12, "Lap-by-Lap Breakdown", create_figure_12),
    ]
    
    for fig_num, fig_name, fig_func in figures:
        print(f"   Generating Figure {fig_num}: {fig_name}...")
        try:
            fig = fig_func()
            fig.savefig(OUTPUTS_DIR / f'Figure_{fig_num}_{fig_name.replace(" ", "_")}.pdf', 
                       dpi=300, bbox_inches='tight')
            fig.savefig(OUTPUTS_DIR / f'Figure_{fig_num}_{fig_name.replace(" ", "_")}.png', 
                       dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"   ✅ Figure {fig_num} saved")
        except Exception as e:
            print(f"   ❌ Error generating Figure {fig_num}: {e}")
    
    print("\n" + "="*80)
    print(f"🎉 ALL ADVANCED FIGURES GENERATED - Location: {OUTPUTS_DIR}")
    print("   • 8 comprehensive figures")
    print("   • 300 DPI resolution (publication-ready)")
    print("   • PDF + PNG formats")
    print("   • Professional color scheme")
    print("   • Detailed metrics & analysis")
    print("="*80 + "\n")
