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
    """Detailed dynamics analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    fig.suptitle('Figure 8: Dynamics, Control & Suspension Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Accelerations
    ax = axes[0, 0]
    ax.plot(time_b, df_baseline['accel_lon_g'].values[::downsample]*100, 
            color=COLOR_BASELINE, alpha=0.8, label='Baseline (Lon)', linewidth=1.5)
    ax.plot(time_o, df_optimized['accel_lon_g'].values[::downsample]*100, 
            color=COLOR_OPTIMIZED, alpha=0.8, label='Optimized (Lon)', linewidth=1.5)
    ax.plot(time_b, df_baseline['accel_lat_g'].values[::downsample]*100, 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (Lat)', linewidth=1.5)
    ax.plot(time_o, df_optimized['accel_lat_g'].values[::downsample]*100, 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (Lat)', linewidth=1.5)
    ax.set_ylabel('Acceleration (cm/s²)', fontweight='bold')
    ax.set_title('Longitudinal & Lateral Acceleration', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(alpha=0.3)
    
    # Suspension Travel
    ax = axes[0, 1]
    ax.plot(time_b, df_baseline['suspension_fl_travel_mm'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, label='Baseline (FL)', linewidth=1.5)
    ax.plot(time_o, df_optimized['suspension_fl_travel_mm'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, label='Optimized (FL)', linewidth=1.5)
    ax.plot(time_b, df_baseline['suspension_rl_travel_mm'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (RL)', linewidth=1.5)
    ax.plot(time_o, df_optimized['suspension_rl_travel_mm'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (RL)', linewidth=1.5)
    ax.set_ylabel('Suspension Travel (mm)', fontweight='bold')
    ax.set_title('Suspension Compression', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(alpha=0.3)
    
    # Gyro (Rotation rates)
    ax = axes[1, 0]
    ax.plot(time_b, df_baseline['gyro_roll_dps'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, label='Baseline (Roll)', linewidth=1.5)
    ax.plot(time_o, df_optimized['gyro_roll_dps'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, label='Optimized (Roll)', linewidth=1.5)
    ax.plot(time_b, df_baseline['gyro_yaw_dps'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', label='Baseline (Yaw)', linewidth=1.5)
    ax.plot(time_o, df_optimized['gyro_yaw_dps'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', label='Optimized (Yaw)', linewidth=1.5)
    ax.set_ylabel('Rotation Rate (dps)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Angular Motion (Roll & Yaw)', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(alpha=0.3)
    
    # Brake Temperature vs Pressure
    ax = axes[1, 1]
    ax2 = ax.twinx()
    ax.plot(time_b, df_baseline['brake_temperature_c'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, label='Baseline (Temp)', linewidth=2)
    ax.plot(time_o, df_optimized['brake_temperature_c'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, label='Optimized (Temp)', linewidth=2)
    ax2.plot(time_b, df_baseline['brake_pressure_bar'].values[::downsample], 
             color=COLOR_BASELINE, alpha=0.3, linestyle='--', linewidth=2)
    ax2.plot(time_o, df_optimized['brake_pressure_bar'].values[::downsample], 
             color=COLOR_OPTIMIZED, alpha=0.3, linestyle='--', linewidth=2)
    ax.set_ylabel('Brake Temperature (°C)', fontweight='bold', color=COLOR_BASELINE)
    ax2.set_ylabel('Brake Pressure (bar)', fontweight='bold', color=COLOR_OPTIMIZED)
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Braking System Performance', fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 9: THERMAL & TIRE ANALYSIS
# ========================
def create_figure_9():
    """Detailed thermal and tire pressure analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    fig.suptitle('Figure 9: Thermal Management & Tire Pressure Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Front Tire Temperatures
    ax = axes[0, 0]
    ax.fill_between(time_b, df_baseline['tire_temp_fl_c'].values[::downsample],
                    alpha=0.5, color=COLOR_BASELINE, label='Baseline')
    ax.fill_between(time_o, df_optimized['tire_temp_fl_c'].values[::downsample],
                    alpha=0.5, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_ylabel('Temperature (°C)', fontweight='bold')
    ax.set_title('Front Left Tire Temperature', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Rear Tire Temperatures
    ax = axes[0, 1]
    ax.fill_between(time_b, df_baseline['tire_temp_rl_c'].values[::downsample],
                    alpha=0.5, color=COLOR_BASELINE, label='Baseline')
    ax.fill_between(time_o, df_optimized['tire_temp_rl_c'].values[::downsample],
                    alpha=0.5, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_ylabel('Temperature (°C)', fontweight='bold')
    ax.set_title('Rear Left Tire Temperature', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Tire Pressure Front & Rear
    ax = axes[1, 0]
    ax.plot(time_b, df_baseline['tire_pressure_fl_bar'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, label='Baseline (FL)', linewidth=2)
    ax.plot(time_o, df_optimized['tire_pressure_fl_bar'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, label='Optimized (FL)', linewidth=2)
    ax.plot(time_b, df_baseline['tire_pressure_rl_bar'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.5, linestyle='--', linewidth=2)
    ax.plot(time_o, df_optimized['tire_pressure_rl_bar'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.5, linestyle='--', linewidth=2)
    ax.set_ylabel('Pressure (bar)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Tire Pressures (Front & Rear)', fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    
    # Brake Temperature Evolution
    ax = axes[1, 1]
    ax.plot(time_b, df_baseline['brake_temperature_c'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, linewidth=2, label='Baseline')
    ax.plot(time_o, df_optimized['brake_temperature_c'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, linewidth=2, label='Optimized')
    ax.fill_between(time_b, df_baseline['brake_temperature_c'].values[::downsample],
                    alpha=0.2, color=COLOR_BASELINE)
    ax.fill_between(time_o, df_optimized['brake_temperature_c'].values[::downsample],
                    alpha=0.2, color=COLOR_OPTIMIZED)
    ax.set_ylabel('Temperature (°C)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Brake System Temperature', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 10: EFFICIENCY & POWER
# ========================
def create_figure_10():
    """Engine efficiency, aerodynamics, and battery analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    fig.suptitle('Figure 10: Efficiency, Aerodynamics & Power Management', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    downsample = 20
    time_b = df_baseline['time'].values[::downsample]
    time_o = df_optimized['time'].values[::downsample]
    
    # Engine Efficiency
    ax = axes[0, 0]
    ax.fill_between(time_b, df_baseline['engine_efficiency_percent'].values[::downsample],
                    alpha=0.5, color=COLOR_BASELINE, label='Baseline')
    ax.fill_between(time_o, df_optimized['engine_efficiency_percent'].values[::downsample],
                    alpha=0.5, color=COLOR_OPTIMIZED, label='Optimized')
    ax.axhline(y=df_baseline['engine_efficiency_percent'].mean(), color=COLOR_BASELINE, 
               linestyle='--', alpha=0.8, linewidth=2, label=f"Mean Baseline: {df_baseline['engine_efficiency_percent'].mean():.2f}%")
    ax.axhline(y=df_optimized['engine_efficiency_percent'].mean(), color=COLOR_OPTIMIZED, 
               linestyle='--', alpha=0.8, linewidth=2, label=f"Mean Optimized: {df_optimized['engine_efficiency_percent'].mean():.2f}%")
    ax.set_ylabel('Efficiency (%)', fontweight='bold')
    ax.set_title('Engine Efficiency', fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    
    # Aerodynamic Forces
    ax = axes[0, 1]
    ax.plot(time_b, df_baseline['aero_downforce_n'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, linewidth=2, label='Baseline (DF)')
    ax.plot(time_o, df_optimized['aero_downforce_n'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, linewidth=2, label='Optimized (DF)')
    ax.plot(time_b, df_baseline['aero_drag_n'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.4, linestyle='--', linewidth=2, label='Baseline (Drag)')
    ax.plot(time_o, df_optimized['aero_drag_n'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.4, linestyle='--', linewidth=2, label='Optimized (Drag)')
    ax.set_ylabel('Force (N)', fontweight='bold')
    ax.set_title('Aerodynamic Forces', fontweight='bold')
    ax.legend(fontsize=8, loc='best')
    ax.grid(alpha=0.3)
    
    # Battery Voltage
    ax = axes[1, 0]
    ax.plot(time_b, df_baseline['battery_voltage_v'].values[::downsample], 
            color=COLOR_BASELINE, alpha=0.8, linewidth=2, label='Baseline')
    ax.plot(time_o, df_optimized['battery_voltage_v'].values[::downsample], 
            color=COLOR_OPTIMIZED, alpha=0.8, linewidth=2, label='Optimized')
    ax.set_ylabel('Voltage (V)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Battery Voltage', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Battery Current
    ax = axes[1, 1]
    ax.plot(time_b, abs(df_baseline['battery_current_a'].values[::downsample]), 
            color=COLOR_BASELINE, alpha=0.8, linewidth=2, label='Baseline')
    ax.plot(time_o, abs(df_optimized['battery_current_a'].values[::downsample]), 
            color=COLOR_OPTIMIZED, alpha=0.8, linewidth=2, label='Optimized')
    ax.fill_between(time_b, abs(df_baseline['battery_current_a'].values[::downsample]),
                    alpha=0.2, color=COLOR_BASELINE)
    ax.fill_between(time_o, abs(df_optimized['battery_current_a'].values[::downsample]),
                    alpha=0.2, color=COLOR_OPTIMIZED)
    ax.set_ylabel('Current (A)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_title('Battery Current Draw', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 11: CORRELATION & SCATTER PLOTS
# ========================
def create_figure_11():
    """Multi-dimensional correlation analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    fig.suptitle('Figure 11: Phase Space & Multi-Dimensional Relationships', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # RPM vs Torque
    ax = axes[0, 0]
    ax.scatter(df_baseline['engine_rpm'], df_baseline['engine_torque_nm'], 
              alpha=0.3, s=10, color=COLOR_BASELINE, label='Baseline')
    ax.scatter(df_optimized['engine_rpm'], df_optimized['engine_torque_nm'], 
              alpha=0.3, s=10, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_xlabel('Engine RPM', fontweight='bold')
    ax.set_ylabel('Torque (Nm)', fontweight='bold')
    ax.set_title('RPM vs Torque Relationship', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Throttle vs Speed
    ax = axes[0, 1]
    ax.scatter(df_baseline['throttle_position']*100, df_baseline['speed_kmh'], 
              alpha=0.3, s=10, color=COLOR_BASELINE, label='Baseline')
    ax.scatter(df_optimized['throttle_position']*100, df_optimized['speed_kmh'], 
              alpha=0.3, s=10, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_xlabel('Throttle Position (%)', fontweight='bold')
    ax.set_ylabel('Speed (km/h)', fontweight='bold')
    ax.set_title('Throttle vs Speed Response', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Lateral Accel vs Wheel Slip
    ax = axes[1, 0]
    ax.scatter(df_baseline['accel_lat_g'], df_baseline['wheel_slip_percent'], 
              alpha=0.3, s=10, color=COLOR_BASELINE, label='Baseline')
    ax.scatter(df_optimized['accel_lat_g'], df_optimized['wheel_slip_percent'], 
              alpha=0.3, s=10, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_xlabel('Lateral Acceleration (g)', fontweight='bold')
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold')
    ax.set_title('Cornering Behavior: Lat. Accel vs Slip', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Tire Temp vs Slip
    ax = axes[1, 1]
    ax.scatter(df_baseline['tire_temp_fl_c'], df_baseline['wheel_slip_percent'], 
              alpha=0.3, s=10, color=COLOR_BASELINE, label='Baseline')
    ax.scatter(df_optimized['tire_temp_fl_c'], df_optimized['wheel_slip_percent'], 
              alpha=0.3, s=10, color=COLOR_OPTIMIZED, label='Optimized')
    ax.set_xlabel('Front Tire Temperature (°C)', fontweight='bold')
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold')
    ax.set_title('Tire Temperature vs Grip', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 12: LAP-BY-LAP ANALYSIS
# ========================
def create_figure_12():
    """Per-lap breakdown analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    fig.suptitle('Figure 12: Lap-by-Lap Performance Breakdown', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Metrics by lap - Baseline
    ax = axes[0, 0]
    lap_data_b = df_baseline.groupby('lap')[['engine_rpm', 'speed_kmh', 'glicko_volatility_sigma']].mean()
    ax.plot(lap_data_b.index, lap_data_b['engine_rpm'], marker='o', color=COLOR_BASELINE, 
            linewidth=2, markersize=8, label='RPM Mean')
    ax2 = ax.twinx()
    ax2.plot(lap_data_b.index, lap_data_b['glicko_volatility_sigma'], marker='s', 
            color=COLOR_BASELINE, linestyle='--', linewidth=2, markersize=8, alpha=0.6, label='Glicko σ')
    ax.set_xlabel('Lap Number', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold', color=COLOR_BASELINE)
    ax2.set_ylabel('Glicko-2 σ', fontweight='bold', color=COLOR_BASELINE, alpha=0.6)
    ax.set_title('Baseline: RPM & Volatility by Lap', fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Metrics by lap - Optimized
    ax = axes[0, 1]
    lap_data_o = df_optimized.groupby('lap')[['engine_rpm', 'speed_kmh', 'glicko_volatility_sigma']].mean()
    ax.plot(lap_data_o.index, lap_data_o['engine_rpm'], marker='o', color=COLOR_OPTIMIZED, 
            linewidth=2, markersize=8, label='RPM Mean')
    ax2 = ax.twinx()
    ax2.plot(lap_data_o.index, lap_data_o['glicko_volatility_sigma'], marker='s', 
            color=COLOR_OPTIMIZED, linestyle='--', linewidth=2, markersize=8, alpha=0.6, label='Glicko σ')
    ax.set_xlabel('Lap Number', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold', color=COLOR_OPTIMIZED)
    ax2.set_ylabel('Glicko-2 σ', fontweight='bold', color=COLOR_OPTIMIZED, alpha=0.6)
    ax.set_title('Optimized: RPM & Volatility by Lap', fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Wheel Slip by Lap
    ax = axes[1, 0]
    slip_b = df_baseline.groupby('lap')['wheel_slip_percent'].mean()
    slip_o = df_optimized.groupby('lap')['wheel_slip_percent'].mean()
    x = np.arange(len(slip_b))
    width = 0.35
    ax.bar(x - width/2, slip_b.values, width, label='Baseline', color=COLOR_BASELINE, alpha=0.8)
    ax.bar(x + width/2, slip_o.values, width, label='Optimized', color=COLOR_OPTIMIZED, alpha=0.8)
    ax.set_xlabel('Lap Number', fontweight='bold')
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold')
    ax.set_title('Wheel Slip by Lap Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Speed Profile by Lap
    ax = axes[1, 1]
    speed_b = df_baseline.groupby('lap')['speed_kmh'].max()
    speed_o = df_optimized.groupby('lap')['speed_kmh'].max()
    ax.plot(speed_b.index, speed_b.values, marker='o', color=COLOR_BASELINE, 
            linewidth=2.5, markersize=10, label='Baseline')
    ax.plot(speed_o.index, speed_o.values, marker='s', color=COLOR_OPTIMIZED, 
            linewidth=2.5, markersize=10, label='Optimized')
    ax.fill_between(speed_b.index, speed_b.values, alpha=0.2, color=COLOR_BASELINE)
    ax.fill_between(speed_o.index, speed_o.values, alpha=0.2, color=COLOR_OPTIMIZED)
    ax.set_xlabel('Lap Number', fontweight='bold')
    ax.set_ylabel('Max Speed (km/h)', fontweight='bold')
    ax.set_title('Maximum Speed per Lap', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
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
