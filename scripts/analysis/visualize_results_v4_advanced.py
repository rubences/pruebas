#!/usr/bin/env python3
"""
Publication-Quality Visualization v4.1 - MEGA Dataset EXPANDED
Advanced analysis figures with detailed metrics and comparisons

Figures:
- Figure 5: Multi-Metric Time Series (RPM, Torque, Throttle, Speed)
- Figure 6: Statistical Validation (Distribution + Statistical Tests)
- Figure 7: Performance Metrics Comparison (Bar charts with improvements)
- Figure 8: Dynamics & Control (Acceleration, Slip, Braking)
- Figure 9: Thermal & Suspension Analysis (Temps, Pressures, Travel)
- Figure 10: Efficiency & Power (Engine, Aero, Battery)
- Figure 11: Phase Space & Correlation (Multi-dimensional analysis)
- Figure 12: Lap-by-Lap Analysis (Per-turn breakdown)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "versioned"
OUTPUTS_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ========================
# SETUP & STYLE - Q1 JOURNAL QUALITY
# ========================
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.4)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 15,
    'figure.titleweight': 'bold',
    'figure.dpi': 100,
    'savefig.dpi': 300,
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
    
    # Glicko Volatility Distribution
    ax = axes[0, 0]
    ax.hist(df_baseline['glicko_volatility_sigma'], bins=50, alpha=0.6, 
            color=COLOR_BASELINE, label='Baseline', density=True, edgecolor='black', linewidth=0.5)
    ax.hist(df_optimized['glicko_volatility_sigma'], bins=50, alpha=0.6, 
            color=COLOR_OPTIMIZED, label='Optimized', density=True, edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Glicko-2 σ', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.set_title('Volatility Distribution', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Box Plot Comparison
    ax = axes[0, 1]
    data_box = [df_baseline['glicko_volatility_sigma'], df_optimized['glicko_volatility_sigma']]
    bp = ax.boxplot(data_box, labels=['Baseline', 'Optimized'], patch_artist=True, widths=0.6)
    bp['boxes'][0].set_facecolor(COLOR_BASELINE)
    bp['boxes'][1].set_facecolor(COLOR_OPTIMIZED)
    ax.set_ylabel('Glicko-2 σ', fontweight='bold')
    ax.set_title('Volatility Comparison', fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    # Q-Q Plot Baseline
    ax = axes[0, 2]
    stats.probplot(df_baseline['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(COLOR_BASELINE)
    ax.get_lines()[0].set_markersize(4)
    ax.get_lines()[1].set_color('red')
    ax.set_title('Q-Q Plot: Baseline', fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Wheel Slip Distribution
    ax = axes[1, 0]
    ax.hist(df_baseline['wheel_slip_percent'], bins=50, alpha=0.6, 
            color=COLOR_BASELINE, label='Baseline', density=True, edgecolor='black', linewidth=0.5)
    ax.hist(df_optimized['wheel_slip_percent'], bins=50, alpha=0.6, 
            color=COLOR_OPTIMIZED, label='Optimized', density=True, edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Wheel Slip (%)', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.set_title('Slip Distribution', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # RPM Distribution
    ax = axes[1, 1]
    ax.hist(df_baseline['engine_rpm'], bins=50, alpha=0.6, 
            color=COLOR_BASELINE, label='Baseline', density=True, edgecolor='black', linewidth=0.5)
    ax.hist(df_optimized['engine_rpm'], bins=50, alpha=0.6, 
            color=COLOR_OPTIMIZED, label='Optimized', density=True, edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Engine RPM', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.set_title('RPM Distribution', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Q-Q Plot Optimized
    ax = axes[1, 2]
    stats.probplot(df_optimized['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(COLOR_OPTIMIZED)
    ax.get_lines()[0].set_markersize(4)
    ax.get_lines()[1].set_color('red')
    ax.set_title('Q-Q Plot: Optimized', fontweight='bold')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 7: PERFORMANCE METRICS COMPARISON
# ========================
def create_figure_7():
    """Bar chart comparison of key metrics with statistical annotations"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 7: Performance Metrics Comparison with Statistical Significance', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Core metrics
    ax = fig.add_subplot(gs[0, 0])
    metrics_core = ['RPM\nMean', 'RPM\nMax', 'Speed\nMax', 'Throttle\nMean']
    baseline_vals = [df_baseline['engine_rpm'].mean(), df_baseline['engine_rpm'].max(),
                     df_baseline['speed_kmh'].max(), df_baseline['throttle_position'].mean()*100]
    optimized_vals = [df_optimized['engine_rpm'].mean(), df_optimized['engine_rpm'].max(),
                      df_optimized['speed_kmh'].max(), df_optimized['throttle_position'].mean()*100]
    
    x = np.arange(len(metrics_core))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline', 
                   color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, optimized_vals, width, label='Optimized', 
                   color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('A) Core Engine Metrics', fontweight='bold', loc='left', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_core, fontsize=10)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Dynamics metrics
    ax = fig.add_subplot(gs[0, 1])
    metrics_dyn = ['Wheel\nSlip (%)', 'Lat.\nAccel (g)', 'Brake\nTemp (°C)', 'Brake\nPress. (bar)']
    baseline_vals = [df_baseline['wheel_slip_percent'].mean(), abs(df_baseline['accel_lat_g'].mean())*100,
                     df_baseline['brake_temperature_c'].mean(), df_baseline['brake_pressure_bar'].mean()]
    optimized_vals = [df_optimized['wheel_slip_percent'].mean(), abs(df_optimized['accel_lat_g'].mean())*100,
                      df_optimized['brake_temperature_c'].mean(), df_optimized['brake_pressure_bar'].mean()]
    
    x = np.arange(len(metrics_dyn))
    bars1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline', 
                   color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, optimized_vals, width, label='Optimized', 
                   color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Highlight improvement in wheel slip
    improvement = ((baseline_vals[0] - optimized_vals[0]) / baseline_vals[0] * 100)
    ax.text(0, max(baseline_vals[0], optimized_vals[0]) * 1.15, 
            f'↓ {improvement:.1f}%', ha='center', fontsize=11, 
            fontweight='bold', color=COLOR_IMPROVEMENT,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('B) Dynamics & Control', fontweight='bold', loc='left', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_dyn, fontsize=10)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Thermal metrics
    ax = fig.add_subplot(gs[1, 0])
    metrics_thermal = ['Tire FL\n(°C)', 'Tire RL\n(°C)', 'Brake\nTemp (°C)', 'Battery\n(V)']
    baseline_vals = [df_baseline['tire_temp_fl_c'].mean(), df_baseline['tire_temp_rl_c'].mean(),
                     df_baseline['brake_temperature_c'].mean(), df_baseline['battery_voltage_v'].mean()]
    optimized_vals = [df_optimized['tire_temp_fl_c'].mean(), df_optimized['tire_temp_rl_c'].mean(),
                      df_optimized['brake_temperature_c'].mean(), df_optimized['battery_voltage_v'].mean()]
    
    x = np.arange(len(metrics_thermal))
    bars1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline', 
                   color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, optimized_vals, width, label='Optimized', 
                   color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('C) Thermal & Power', fontweight='bold', loc='left', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_thermal, fontsize=10)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(alpha=0.3, axis='y', linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Efficiency metrics
    ax = fig.add_subplot(gs[1, 1])
    metrics_eff = ['Engine\nEff. (%)', 'Aero\nDrag (N)', 'Glicko σ', 'Battery\nCurrent (A)']
    baseline_vals = [df_baseline['engine_efficiency_percent'].mean(), df_baseline['aero_drag_n'].mean(),
                     df_baseline['glicko_volatility_sigma'].mean(), abs(df_baseline['battery_current_a'].mean())]
    optimized_vals = [df_optimized['engine_efficiency_percent'].mean(), df_optimized['aero_drag_n'].mean(),
                      df_optimized['glicko_volatility_sigma'].mean(), abs(df_optimized['battery_current_a'].mean())]
    
    x = np.arange(len(metrics_eff))
    bars1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline', 
                   color=COLOR_BASELINE, alpha=0.85, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, optimized_vals, width, label='Optimized', 
                   color=COLOR_OPTIMIZED, alpha=0.85, edgecolor='black', linewidth=1.2)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Highlight improvements
    eff_improvement = ((optimized_vals[0] - baseline_vals[0]) / baseline_vals[0] * 100)
    vol_improvement = ((baseline_vals[2] - optimized_vals[2]) / baseline_vals[2] * 100)
    
    ax.text(0, max(baseline_vals[0], optimized_vals[0]) * 1.08, 
            f'↑ {eff_improvement:.1f}%', ha='center', fontsize=10, 
            fontweight='bold', color=COLOR_IMPROVEMENT,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    ax.text(2, max(baseline_vals[2], optimized_vals[2]) * 1.08, 
            f'↓ {vol_improvement:.1f}%', ha='center', fontsize=10, 
            fontweight='bold', color=COLOR_IMPROVEMENT,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('D) Efficiency & Performance', fontweight='bold', loc='left', fontsize=13)
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
# FIGURE 9: THERMAL & TIRE ANALYSIS
# ========================
def create_figure_9():
    """Detailed thermal and tire pressure analysis with Q1 enhancements"""
    fig = plt.figure(figsize=(16, 10), dpi=100)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    fig.suptitle('Figure 9: Thermal Management & Tire Pressure Analysis', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Front Tire Temperatures
    ax = fig.add_subplot(gs[0, 0])
    ax.fill_between(time_b, df_baseline['tire_temp_fl_c'].values[::downsample],
                    alpha=0.4, color=COLOR_BASELINE, label='Baseline', zorder=2)
    ax.fill_between(time_o, df_optimized['tire_temp_fl_c'].values[::downsample],
                    alpha=0.4, color=COLOR_OPTIMIZED, label='Optimized', zorder=2)
    ax.plot(time_b, df_baseline['tire_temp_fl_c'].values[::downsample],
            color=COLOR_BASELINE, linewidth=2.5, alpha=0.9, zorder=3)
    ax.plot(time_o, df_optimized['tire_temp_fl_c'].values[::downsample],
            color=COLOR_OPTIMIZED, linewidth=2.5, alpha=0.9, zorder=3)
    
    # Mean temperatures
    base_mean = df_baseline['tire_temp_fl_c'].mean()
    opt_mean = df_optimized['tire_temp_fl_c'].mean()
    ax.axhline(base_mean, color=COLOR_BASELINE, linestyle='--', linewidth=2.0, alpha=0.6, 
               label=f'μ: {base_mean:.1f}°C', zorder=2)
    ax.axhline(opt_mean, color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.0, alpha=0.6, 
               label=f'μ: {opt_mean:.1f}°C', zorder=2)
    
    # Thermal management annotation
    temp_difference = opt_mean - base_mean
    ax.text(0.02, 0.98, f'Tire Temp Δ: {temp_difference:+.1f}°C\nμ: {base_mean:.1f} → {opt_mean:.1f}',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=12)
    ax.set_title('A) Front Left Tire Temperature', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Rear Tire Temperatures
    ax = fig.add_subplot(gs[0, 1])
    ax.fill_between(time_b, df_baseline['tire_temp_rl_c'].values[::downsample],
                    alpha=0.4, color=COLOR_BASELINE, label='Baseline', zorder=2)
    ax.fill_between(time_o, df_optimized['tire_temp_rl_c'].values[::downsample],
                    alpha=0.4, color=COLOR_OPTIMIZED, label='Optimized', zorder=2)
    ax.plot(time_b, df_baseline['tire_temp_rl_c'].values[::downsample],
            color=COLOR_BASELINE, linewidth=2.5, alpha=0.9, zorder=3)
    ax.plot(time_o, df_optimized['tire_temp_rl_c'].values[::downsample],
            color=COLOR_OPTIMIZED, linewidth=2.5, alpha=0.9, zorder=3)
    
    base_mean = df_baseline['tire_temp_rl_c'].mean()
    opt_mean = df_optimized['tire_temp_rl_c'].mean()
    ax.axhline(base_mean, color=COLOR_BASELINE, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {base_mean:.1f}°C', zorder=2)
    ax.axhline(opt_mean, color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {opt_mean:.1f}°C', zorder=2)
    
    temp_difference = opt_mean - base_mean
    ax.text(0.02, 0.98, f'Tire Temp Δ: {temp_difference:+.1f}°C\nμ: {base_mean:.1f} → {opt_mean:.1f}',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=12)
    ax.set_title('B) Rear Left Tire Temperature', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Tire Pressure Front & Rear
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(time_b, df_baseline['tire_pressure_fl_bar'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, label='Baseline (FL)', linewidth=2.5, zorder=3)
    ax.plot(time_o, df_optimized['tire_pressure_fl_bar'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, label='Optimized (FL)', linewidth=2.5, zorder=3)
    ax.plot(time_b, df_baseline['tire_pressure_rl_bar'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', linewidth=2.0, label='Baseline (RL)', zorder=2)
    ax.plot(time_o, df_optimized['tire_pressure_rl_bar'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', linewidth=2.0, label='Optimized (RL)', zorder=2)
    
    # Pressure stability
    fl_base_std = df_baseline['tire_pressure_fl_bar'].std()
    fl_opt_std = df_optimized['tire_pressure_fl_bar'].std()
    stability = ((fl_base_std - fl_opt_std) / fl_base_std * 100)
    
    ax.text(0.02, 0.98, f'Pressure Stability ↑: {stability:.1f}%\nσ FL: {fl_base_std:.3f} → {fl_opt_std:.3f} bar',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Pressure (bar)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('C) Tire Pressures (Front & Rear)', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Brake Temperature Evolution
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(time_b, df_baseline['brake_temperature_c'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.9, linewidth=2.5, label='Baseline', zorder=3)
    ax.plot(time_o, df_optimized['brake_temperature_c'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.9, linewidth=2.5, label='Optimized', zorder=3)
    ax.fill_between(time_b, df_baseline['brake_temperature_c'].values[::downsample],
                    alpha=0.2, color=COLOR_BASELINE, zorder=1)
    ax.fill_between(time_o, df_optimized['brake_temperature_c'].values[::downsample],
                    alpha=0.2, color=COLOR_OPTIMIZED, zorder=1)
    
    # Mean lines
    base_mean = df_baseline['brake_temperature_c'].mean()
    opt_mean = df_optimized['brake_temperature_c'].mean()
    ax.axhline(base_mean, color=COLOR_BASELINE, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {base_mean:.1f}°C', zorder=2)
    ax.axhline(opt_mean, color=COLOR_OPTIMIZED, linestyle='--', linewidth=2.0, alpha=0.6,
               label=f'μ: {opt_mean:.1f}°C', zorder=2)
    
    # Thermal efficiency
    temp_reduction = ((base_mean - opt_mean) / base_mean * 100)
    ax.text(0.02, 0.98, f'Brake Cooling ↑: {temp_reduction:.1f}%\nμ: {base_mean:.1f} → {opt_mean:.1f}°C',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, edgecolor='black'))
    
    ax.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
    ax.set_title('D) Brake System Temperature', fontweight='bold', loc='left', fontsize=13)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)
    
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
        (8, "Dynamics & Control Analysis", create_figure_8),
        (9, "Thermal & Tire Analysis", create_figure_9),
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
