#!/usr/bin/env python3
"""
Publication-Quality Visualization v4.0 - MEGA Dataset
Generate 4 advanced figures (300 DPI, colorblind-friendly) for v4.0 dataset

Figures:
- Figure 5: Time Series Analysis (RPM, Throttle, Glicko σ, Wheel Slip)
- Figure 6: Statistical Validation (Distribution analysis + Q-Q plots)
- Figure 7: Phase Space Analysis (Throttle vs RPM dynamics)
- Figure 8: Volatility Heatmaps (Temporal evolution)
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
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ========================
# SETUP & STYLE
# ========================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Colorblind-friendly palette
COLORS_BASELINE = '#0173B2'   # Blue
COLORS_OPTIMIZED = '#DE8F05'  # Orange
COLORS_DIFF = '#CC78BC'        # Purple

# Load dataset
dataset_file = DATA_DIR / "NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"
if not dataset_file.exists():
    dataset_file = "NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"

try:
    df = pd.read_csv(dataset_file)
    df_baseline = df[df['setup'] == 'baseline'].reset_index(drop=True)
    df_optimized = df[df['setup'] == 'optimized'].reset_index(drop=True)
    print("✅ Data loaded successfully")
except FileNotFoundError:
    print("❌ Dataset not found. Run generate_case_study_data_v4.py first")
    exit(1)

# ========================
# FIGURE 5: TIME SERIES
# ========================
def create_figure_5():
    """4-panel time series: RPM, Throttle, Glicko σ, Wheel Slip"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)
    fig.suptitle('Figure 5: Temporal Evolution - Jerez v4.0 MEGA Dataset', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    # Subsample for clarity
    downsample = 10
    time_baseline = df_baseline['time'].values[::downsample]
    time_optimized = df_optimized['time'].values[::downsample]
    
    # RPM
    ax = axes[0, 0]
    ax.plot(time_baseline, df_baseline['engine_rpm'].values[::downsample], 
            color=COLORS_BASELINE, alpha=0.7, label='Baseline', linewidth=1.5)
    ax.plot(time_optimized, df_optimized['engine_rpm'].values[::downsample], 
            color=COLORS_OPTIMIZED, alpha=0.7, label='Optimized', linewidth=1.5)
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    # Throttle Position
    ax = axes[0, 1]
    ax.plot(time_baseline, df_baseline['throttle_position'].values[::downsample]*100, 
            color=COLORS_BASELINE, alpha=0.7, label='Baseline', linewidth=1.5)
    ax.plot(time_optimized, df_optimized['throttle_position'].values[::downsample]*100, 
            color=COLORS_OPTIMIZED, alpha=0.7, label='Optimized', linewidth=1.5)
    ax.set_ylabel('Throttle Position (%)', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    # Glicko Volatility Sigma
    ax = axes[1, 0]
    ax.plot(time_baseline, df_baseline['glicko_volatility_sigma'].values[::downsample], 
            color=COLORS_BASELINE, alpha=0.7, label='Baseline', linewidth=1.5)
    ax.plot(time_optimized, df_optimized['glicko_volatility_sigma'].values[::downsample], 
            color=COLORS_OPTIMIZED, alpha=0.7, label='Optimized', linewidth=1.5)
    ax.set_ylabel('Glicko-2 σ (Volatility)', fontweight='bold')
    ax.set_xlabel('Time (seconds)', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    # Wheel Slip Ratio
    ax = axes[1, 1]
    ax.plot(time_baseline, df_baseline['wheel_slip_percent'].values[::downsample], 
            color=COLORS_BASELINE, alpha=0.7, label='Baseline', linewidth=1.5)
    ax.plot(time_optimized, df_optimized['wheel_slip_percent'].values[::downsample], 
            color=COLORS_OPTIMIZED, alpha=0.7, label='Optimized', linewidth=1.5)
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold')
    ax.set_xlabel('Time (seconds)', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 6: STATISTICAL VALIDATION
# ========================
def create_figure_6():
    """Distribution analysis + Q-Q plots"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)
    fig.suptitle('Figure 6: Statistical Validation - Glicko-2 Volatility Distribution', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    # Histogram with KDE
    ax = axes[0, 0]
    ax.hist(df_baseline['glicko_volatility_sigma'], bins=50, alpha=0.6, 
            color=COLORS_BASELINE, label='Baseline', density=True, edgecolor='black')
    ax.hist(df_optimized['glicko_volatility_sigma'], bins=50, alpha=0.6, 
            color=COLORS_OPTIMIZED, label='Optimized', density=True, edgecolor='black')
    ax.set_xlabel('Glicko-2 σ', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    ax.set_title('Distribution Comparison')
    
    # Box plot
    ax = axes[0, 1]
    data_box = [df_baseline['glicko_volatility_sigma'], df_optimized['glicko_volatility_sigma']]
    bp = ax.boxplot(data_box, labels=['Baseline', 'Optimized'], patch_artist=True,
                    widths=0.6)
    bp['boxes'][0].set_facecolor(COLORS_BASELINE)
    bp['boxes'][1].set_facecolor(COLORS_OPTIMIZED)
    ax.set_ylabel('Glicko-2 σ', fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    ax.set_title('Box Plot Comparison')
    
    # Q-Q Plot Baseline
    ax = axes[1, 0]
    stats.probplot(df_baseline['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(COLORS_BASELINE)
    ax.get_lines()[1].set_color('red')
    ax.set_title('Q-Q Plot: Baseline', fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Q-Q Plot Optimized
    ax = axes[1, 1]
    stats.probplot(df_optimized['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(COLORS_OPTIMIZED)
    ax.get_lines()[1].set_color('red')
    ax.set_title('Q-Q Plot: Optimized', fontweight='bold')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 7: PHASE SPACE
# ========================
def create_figure_7():
    """Throttle vs RPM dynamics"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=100)
    fig.suptitle('Figure 7: Phase Space Analysis - Throttle vs RPM', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    # Baseline phase space
    ax = axes[0]
    ax.scatter(df_baseline['throttle_position']*100, df_baseline['engine_rpm'], 
              alpha=0.3, s=10, color=COLORS_BASELINE, edgecolors='none')
    ax.set_xlabel('Throttle Position (%)', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.set_title('Baseline Setup', fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Optimized phase space
    ax = axes[1]
    ax.scatter(df_optimized['throttle_position']*100, df_optimized['engine_rpm'], 
              alpha=0.3, s=10, color=COLORS_OPTIMIZED, edgecolors='none')
    ax.set_xlabel('Throttle Position (%)', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.set_title('Optimized Setup', fontweight='bold')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

# ========================
# FIGURE 8: HEATMAP
# ========================
def create_figure_8():
    """Volatility heatmaps"""
    
    # Create time-binned data
    n_bins = 50
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
    fig.suptitle('Figure 8: Temporal Volatility Evolution - Heatmap Analysis', 
                 fontsize=14, fontweight='bold', y=1.00)
    
    # Baseline heatmap
    ax = axes[0]
    time_bins = np.linspace(df_baseline['time'].min(), df_baseline['time'].max(), n_bins)
    sigma_baseline = []
    for i in range(len(time_bins)-1):
        mask = (df_baseline['time'] >= time_bins[i]) & (df_baseline['time'] < time_bins[i+1])
        sigma_baseline.append(df_baseline[mask]['glicko_volatility_sigma'].mean())
    
    im1 = ax.imshow([sigma_baseline], aspect='auto', cmap='Blues', interpolation='nearest')
    ax.set_ylabel('Baseline', fontweight='bold')
    ax.set_xlabel('Time Window', fontweight='bold')
    ax.set_yticks([])
    ax.set_title('Baseline Volatility', fontweight='bold')
    plt.colorbar(im1, ax=ax, label='Glicko-2 σ')
    
    # Optimized heatmap
    ax = axes[1]
    time_bins = np.linspace(df_optimized['time'].min(), df_optimized['time'].max(), n_bins)
    sigma_optimized = []
    for i in range(len(time_bins)-1):
        mask = (df_optimized['time'] >= time_bins[i]) & (df_optimized['time'] < time_bins[i+1])
        sigma_optimized.append(df_optimized[mask]['glicko_volatility_sigma'].mean())
    
    im2 = ax.imshow([sigma_optimized], aspect='auto', cmap='Oranges', interpolation='nearest')
    ax.set_ylabel('Optimized', fontweight='bold')
    ax.set_xlabel('Time Window', fontweight='bold')
    ax.set_yticks([])
    ax.set_title('Optimized Volatility', fontweight='bold')
    plt.colorbar(im2, ax=ax, label='Glicko-2 σ')
    
    plt.tight_layout()
    return fig

# ========================
# MAIN EXECUTION
# ========================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🎨 GENERATING PUBLICATION-QUALITY FIGURES v4.0")
    print("="*80 + "\n")
    
    # Figure 5: Time Series
    print("   Generating Figure 5: Time Series Analysis...")
    fig5 = create_figure_5()
    fig5.savefig(FIGURES_DIR / 'Figure_5_TimeSeries.pdf', dpi=300, bbox_inches='tight')
    fig5.savefig(FIGURES_DIR / 'Figure_5_TimeSeries.png', dpi=300, bbox_inches='tight')
    plt.close(fig5)
    print("   ✅ Figure 5 saved")
    
    # Figure 6: Statistical Validation
    print("   Generating Figure 6: Statistical Validation...")
    fig6 = create_figure_6()
    fig6.savefig(FIGURES_DIR / 'Figure_6_StatisticalValidation.pdf', dpi=300, bbox_inches='tight')
    fig6.savefig(FIGURES_DIR / 'Figure_6_StatisticalValidation.png', dpi=300, bbox_inches='tight')
    plt.close(fig6)
    print("   ✅ Figure 6 saved")
    
    # Figure 7: Phase Space
    print("   Generating Figure 7: Phase Space Analysis...")
    fig7 = create_figure_7()
    fig7.savefig(FIGURES_DIR / 'Figure_7_PhaseSpace.pdf', dpi=300, bbox_inches='tight')
    fig7.savefig(FIGURES_DIR / 'Figure_7_PhaseSpace.png', dpi=300, bbox_inches='tight')
    plt.close(fig7)
    print("   ✅ Figure 7 saved")
    
    # Figure 8: Heatmap
    print("   Generating Figure 8: Volatility Heatmap...")
    fig8 = create_figure_8()
    fig8.savefig(FIGURES_DIR / 'Figure_8_HeatMap.pdf', dpi=300, bbox_inches='tight')
    fig8.savefig(FIGURES_DIR / 'Figure_8_HeatMap.png', dpi=300, bbox_inches='tight')
    plt.close(fig8)
    print("   ✅ Figure 8 saved")
    
    print("\n" + "="*80)
    print(f"🎉 ALL FIGURES GENERATED - Location: {FIGURES_DIR}")
    print("="*80 + "\n")
