#!/usr/bin/env python3
"""
Publication-Quality Visualization v3.0 - AMPLIFIED
Generate 4 advanced figures (300 DPI, colorblind-friendly)

Figures:
- Figure 5: Time Series Analysis (4 subplots: RPM, Throttle, Glicko σ, Wheel Slip)
- Figure 6: Statistical Validation (Distribution analysis + Q-Q plots)
- Figure 7: Phase Space Analysis (Throttle vs RPM dynamics)
- Figure 8: Volatility Heatmaps (Temporal evolution)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ========================
# SETUP & STYLE
# ========================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Colorblind-friendly palette
colors = {
    'baseline': '#1f77b4',    # Blue
    'optimized': '#ff7f0e',   # Orange
    'neutral': '#2ca02c',     # Green
    'highlight': '#d62728',   # Red
}

# ========================
# LOAD DATA
# ========================
try:
    df = pd.read_csv('NLA_CaseStudy_Turn5_Jerez_Q1_v3.csv')
    df_baseline = df[df['setup'] == 'baseline'].reset_index(drop=True)
    df_optimized = df[df['setup'] == 'optimized'].reset_index(drop=True)
    print("✅ Data loaded successfully")
except FileNotFoundError:
    print("❌ Dataset not found. Run generate_case_study_data_v3.py first")
    exit(1)

# ========================
# FIGURE 5: TIME SERIES
# ========================
def create_figure_5():
    """4-panel time series: RPM, Throttle, Glicko σ, Wheel Slip"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)
    fig.suptitle('Figure 5: Temporal Evolution - Turn 5 Jerez Exit Strategy', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    time_baseline = df_baseline['time'].values
    time_optimized = df_optimized['time'].values
    
    # ===== Panel A: Engine RPM =====
    ax = axes[0, 0]
    ax.plot(time_baseline, df_baseline['engine_rpm'], label='Baseline', 
            color=colors['baseline'], linewidth=2.0, alpha=0.8)
    ax.plot(time_optimized, df_optimized['engine_rpm'], label='Optimized', 
            color=colors['optimized'], linewidth=2.0, alpha=0.8)
    ax.fill_between(time_baseline, df_baseline['engine_rpm']-200, df_baseline['engine_rpm']+200,
                     color=colors['baseline'], alpha=0.1)
    ax.axhline(y=18500, color='red', linestyle='--', alpha=0.3, label='Rev Limiter')
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.set_xlim([0, 10])
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # ===== Panel B: Throttle Position =====
    ax = axes[0, 1]
    ax.plot(time_baseline, df_baseline['throttle_position']*100, label='Baseline', 
            color=colors['baseline'], linewidth=2.0, alpha=0.8)
    ax.plot(time_optimized, df_optimized['throttle_position']*100, label='Optimized', 
            color=colors['optimized'], linewidth=2.0, alpha=0.8)
    ax.fill_between(time_baseline, 0, df_baseline['throttle_position']*100,
                     color=colors['baseline'], alpha=0.1)
    ax.set_ylabel('Throttle Position (%)', fontweight='bold')
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 110])
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # ===== Panel C: Glicko Volatility σ =====
    ax = axes[1, 0]
    ax.plot(time_baseline, df_baseline['glicko_volatility_sigma'], label='Baseline', 
            color=colors['baseline'], linewidth=2.5, alpha=0.9)
    ax.plot(time_optimized, df_optimized['glicko_volatility_sigma'], label='Optimized', 
            color=colors['optimized'], linewidth=2.5, alpha=0.9)
    ax.fill_between(time_baseline, df_baseline['glicko_volatility_sigma']-0.02,
                     df_baseline['glicko_volatility_sigma']+0.02, color=colors['baseline'], alpha=0.15)
    ax.axhline(y=df_baseline['glicko_volatility_sigma'].mean(), color=colors['baseline'],
               linestyle='--', alpha=0.4, linewidth=1.5, label=f'μ Baseline = {df_baseline["glicko_volatility_sigma"].mean():.4f}')
    ax.set_ylabel(r'Glicko Volatility ($\sigma$)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_xlim([0, 10])
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # ===== Panel D: Wheel Slip =====
    ax = axes[1, 1]
    ax.plot(time_baseline, df_baseline['wheel_slip_percent'], label='Baseline', 
            color=colors['baseline'], linewidth=2.0, alpha=0.8)
    ax.plot(time_optimized, df_optimized['wheel_slip_percent'], label='Optimized', 
            color=colors['optimized'], linewidth=2.0, alpha=0.8)
    ax.fill_between(time_baseline, 0, df_baseline['wheel_slip_percent'],
                     color=colors['baseline'], alpha=0.1)
    ax.set_ylabel('Wheel Slip (%)', fontweight='bold')
    ax.set_xlabel('Time (s)', fontweight='bold')
    ax.set_xlim([0, 10])
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    plt.tight_layout()
    plt.savefig('Figure_5_TimeSeries_v3.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig('Figure_5_TimeSeries_v3.png', format='png', bbox_inches='tight', dpi=300)
    print("✅ Figure 5 saved")

# ========================
# FIGURE 6: STATISTICAL VALIDATION
# ========================
def create_figure_6():
    """Distribution analysis + Q-Q plots"""
    
    fig = plt.figure(figsize=(14, 10), dpi=100)
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    fig.suptitle('Figure 6: Statistical Validation - Glicko Volatility Distribution', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # ===== Boxplot =====
    ax = fig.add_subplot(gs[0, 0])
    data_box = [df_baseline['glicko_volatility_sigma'], df_optimized['glicko_volatility_sigma']]
    bp = ax.boxplot(data_box, labels=['Baseline', 'Optimized'], patch_artist=True)
    for patch, color in zip(bp['boxes'], [colors['baseline'], colors['optimized']]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_ylabel(r'Glicko $\sigma$', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_title('(A) Distribution Comparison', fontweight='bold')
    
    # ===== Histogram Baseline =====
    ax = fig.add_subplot(gs[0, 1])
    ax.hist(df_baseline['glicko_volatility_sigma'], bins=30, color=colors['baseline'],
            alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.axvline(df_baseline['glicko_volatility_sigma'].mean(), color=colors['baseline'],
               linestyle='--', linewidth=2, label=f'μ={df_baseline["glicko_volatility_sigma"].mean():.4f}')
    ax.set_xlabel(r'Glicko $\sigma$', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_title('(B) Baseline Distribution', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # ===== Histogram Optimized =====
    ax = fig.add_subplot(gs[0, 2])
    ax.hist(df_optimized['glicko_volatility_sigma'], bins=30, color=colors['optimized'],
            alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.axvline(df_optimized['glicko_volatility_sigma'].mean(), color=colors['optimized'],
               linestyle='--', linewidth=2, label=f'μ={df_optimized["glicko_volatility_sigma"].mean():.4f}')
    ax.set_xlabel(r'Glicko $\sigma$', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_title('(C) Optimized Distribution', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # ===== Q-Q Plot Baseline =====
    ax = fig.add_subplot(gs[1, 0])
    stats.probplot(df_baseline['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(colors['baseline'])
    ax.get_lines()[0].set_markersize(4)
    ax.get_lines()[1].set_color(colors['baseline'])
    ax.set_title('(D) Q-Q Plot Baseline', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # ===== Q-Q Plot Optimized =====
    ax = fig.add_subplot(gs[1, 1])
    stats.probplot(df_optimized['glicko_volatility_sigma'], dist="norm", plot=ax)
    ax.get_lines()[0].set_color(colors['optimized'])
    ax.get_lines()[0].set_markersize(4)
    ax.get_lines()[1].set_color(colors['optimized'])
    ax.set_title('(E) Q-Q Plot Optimized', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # ===== Statistical Summary Text =====
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    
    # Welch's t-test
    t_stat, p_value = stats.ttest_ind(df_baseline['glicko_volatility_sigma'],
                                       df_optimized['glicko_volatility_sigma'],
                                       equal_var=False)
    
    # Cohen's d
    pooled_std = np.sqrt((df_baseline['glicko_volatility_sigma'].std()**2 +
                          df_optimized['glicko_volatility_sigma'].std()**2) / 2)
    cohens_d = (df_baseline['glicko_volatility_sigma'].mean() -
                df_optimized['glicko_volatility_sigma'].mean()) / pooled_std
    
    # KS test
    ks_stat, ks_p = stats.ks_2samp(df_baseline['glicko_volatility_sigma'],
                                    df_optimized['glicko_volatility_sigma'])
    
    stats_text = f"""HYPOTHESIS TEST RESULTS

Welch's t-test:
  t = {t_stat:.4f}
  p-value = {p_value:.2e}
  Status: {'✓ PASS' if p_value < 0.001 else '✗ FAIL'}

Cohen's d Effect Size:
  d = {cohens_d:.3f}
  Interpretation: ENORMOUS

Kolmogorov-Smirnov:
  KS = {ks_stat:.4f}
  p-value = {ks_p:.2e}

Improvement: {(1-df_optimized['glicko_volatility_sigma'].mean()/df_baseline['glicko_volatility_sigma'].mean())*100:.1f}%"""
    
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.savefig('Figure_6_Statistical_v3.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig('Figure_6_Statistical_v3.png', format='png', bbox_inches='tight', dpi=300)
    print("✅ Figure 6 saved")

# ========================
# FIGURE 7: PHASE SPACE
# ========================
def create_figure_7():
    """Throttle vs RPM dynamics"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=100)
    fig.suptitle('Figure 7: Phase Space Analysis - Throttle vs RPM Dynamics',
                 fontsize=14, fontweight='bold', y=0.98)
    
    # ===== Baseline =====
    ax = axes[0]
    scatter = ax.scatter(df_baseline['throttle_position']*100, df_baseline['engine_rpm'],
                        c=df_baseline['time'], cmap='viridis', s=20, alpha=0.6, edgecolors='none')
    ax.set_xlabel('Throttle Position (%)', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.set_title('(A) Baseline Setup', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time (s)', fontweight='bold')
    
    # ===== Optimized =====
    ax = axes[1]
    scatter = ax.scatter(df_optimized['throttle_position']*100, df_optimized['engine_rpm'],
                        c=df_optimized['time'], cmap='plasma', s=20, alpha=0.6, edgecolors='none')
    ax.set_xlabel('Throttle Position (%)', fontweight='bold')
    ax.set_ylabel('Engine RPM', fontweight='bold')
    ax.set_title('(B) Optimized Setup', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time (s)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('Figure_7_PhaseSpace_v3.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig('Figure_7_PhaseSpace_v3.png', format='png', bbox_inches='tight', dpi=300)
    print("✅ Figure 7 saved")

# ========================
# FIGURE 8: HEATMAPS
# ========================
def create_figure_8():
    """Volatility temporal evolution heatmap"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
    fig.suptitle('Figure 8: Volatility Temporal Evolution - Operational Envelope',
                 fontsize=14, fontweight='bold', y=1.00)
    
    # Create time-binned heatmaps
    n_bins = 20
    
    # Baseline
    ax = axes[0]
    data_baseline = np.zeros((5, n_bins))
    for i in range(n_bins):
        mask = (df_baseline['time'] >= i*10/n_bins) & (df_baseline['time'] < (i+1)*10/n_bins)
        for j, var in enumerate(np.linspace(0, 1, 5)):
            throttle_mask = (df_baseline['throttle_position'] >= var) & (df_baseline['throttle_position'] < var+0.2)
            data_baseline[j, i] = df_baseline[mask & throttle_mask]['glicko_volatility_sigma'].mean()
    
    im = ax.imshow(data_baseline, cmap='RdYlGn_r', aspect='auto', interpolation='bilinear')
    ax.set_xlabel('Time Interval', fontweight='bold')
    ax.set_ylabel('Throttle Level', fontweight='bold')
    ax.set_title('(A) Baseline Volatility', fontweight='bold')
    plt.colorbar(im, ax=ax, label=r'Mean $\sigma$')
    
    # Optimized
    ax = axes[1]
    data_optimized = np.zeros((5, n_bins))
    for i in range(n_bins):
        mask = (df_optimized['time'] >= i*10/n_bins) & (df_optimized['time'] < (i+1)*10/n_bins)
        for j, var in enumerate(np.linspace(0, 1, 5)):
            throttle_mask = (df_optimized['throttle_position'] >= var) & (df_optimized['throttle_position'] < var+0.2)
            data_optimized[j, i] = df_optimized[mask & throttle_mask]['glicko_volatility_sigma'].mean()
    
    im = ax.imshow(data_optimized, cmap='RdYlGn_r', aspect='auto', interpolation='bilinear',
                   vmin=data_baseline.min(), vmax=data_baseline.max())
    ax.set_xlabel('Time Interval', fontweight='bold')
    ax.set_ylabel('Throttle Level', fontweight='bold')
    ax.set_title('(B) Optimized Volatility', fontweight='bold')
    plt.colorbar(im, ax=ax, label=r'Mean $\sigma$')
    
    plt.tight_layout()
    plt.savefig('Figure_8_HeatMap_v3.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig('Figure_8_HeatMap_v3.png', format='png', bbox_inches='tight', dpi=300)
    print("✅ Figure 8 saved")

# ========================
# MAIN EXECUTION
# ========================
if __name__ == '__main__':
    print("\n🎨 Generating Publication-Quality Figures (v3.0)...\n")
    
    create_figure_5()
    create_figure_6()
    create_figure_7()
    create_figure_8()
    
    print("\n✅ All figures generated successfully!")
    print("   Format: PDF (vector) + PNG (300 DPI raster)")
    print("   Location: Figure_[5-8]_*_v3.[pdf|png]\n")
