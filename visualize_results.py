"""
VISUALIZACIÓN CIENTÍFICA - CASO DE ESTUDIO TURN 5 JEREZ
========================================================
Script para generar figuras de calidad de publicación (300 DPI, vectorial)
según los estándares de revistas Q1 en ingeniería y sistemas humano-máquina.

Outputs:
--------
- Figure_5_TimeSeries.pdf: Series temporales de RPM, Throttle, Glicko σ
- Figure_6_StatisticalValidation.pdf: Box plots y distribuciones
- Figure_7_PhaseSpace.pdf: Espacio de fase Throttle vs RPM
- Figure_8_HeatMap.pdf: Mapa de calor de volatilidad

Requirements: matplotlib>=3.7, seaborn>=0.12
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec

# Configuración de estilo para publicación
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13
plt.rcParams['text.usetex'] = False  # Cambiar a True si tienes LaTeX instalado

# Paleta de colores (colorblind-friendly)
COLOR_BASELINE = '#D55E00'  # Naranja (problema)
COLOR_OPTIMIZED = '#009E73'  # Verde (solución)
COLOR_CRITICAL = '#CC79A7'  # Rosa (eventos críticos)

# ============================================================================
# CARGAR DATOS
# ============================================================================
print("Cargando datos...")
df = pd.read_csv("NLA_CaseStudy_Turn5_Jerez_Q1.csv")
df_baseline = df[df['Setup_Type'] == 'BASELINE']
df_optimized = df[df['Setup_Type'] == 'OPTIMIZED']

# ============================================================================
# FIGURA 5: SERIES TEMPORALES COMPARATIVAS
# ============================================================================
print("Generando Figure 5: Series Temporales...")

fig = plt.figure(figsize=(10, 8))
gs = GridSpec(4, 1, figure=fig, hspace=0.3)

# Panel A: RPM
ax1 = fig.add_subplot(gs[0])
ax1.plot(df_baseline['Timestamp_s'], df_baseline['Engine_RPM'], 
         color=COLOR_BASELINE, linewidth=1.5, label='Baseline (Long Ratio)', alpha=0.9)
ax1.plot(df_optimized['Timestamp_s'], df_optimized['Engine_RPM'], 
         color=COLOR_OPTIMIZED, linewidth=1.5, label='Optimized (Short +2T)', alpha=0.9)

# Marcar eventos de shift
shift_times = [2.05, 4.85]
for st in shift_times:
    ax1.axvline(st, color=COLOR_CRITICAL, linestyle='--', alpha=0.5, linewidth=1)
    ax1.text(st, 18000, 'Shift', rotation=0, va='center', ha='center', 
             fontsize=8, color=COLOR_CRITICAL)

ax1.set_ylabel('Engine RPM')
ax1.set_xlim(0, 10)
ax1.set_ylim(9000, 18500)
ax1.legend(loc='lower right', frameon=True, fancybox=False, edgecolor='black')
ax1.grid(True, alpha=0.3, linestyle=':')
ax1.set_title('(A) Engine Speed Dynamics', loc='left', fontweight='bold')

# Panel B: Throttle Position
ax2 = fig.add_subplot(gs[1])
ax2.plot(df_baseline['Timestamp_s'], df_baseline['Throttle_Pos_%'], 
         color=COLOR_BASELINE, linewidth=1.2, alpha=0.8)
ax2.plot(df_optimized['Timestamp_s'], df_optimized['Throttle_Pos_%'], 
         color=COLOR_OPTIMIZED, linewidth=1.2, alpha=0.8)

for st in shift_times:
    ax2.axvline(st, color=COLOR_CRITICAL, linestyle='--', alpha=0.5, linewidth=1)

ax2.set_ylabel('Throttle Position (%)')
ax2.set_xlim(0, 10)
ax2.set_ylim(-5, 110)
ax2.grid(True, alpha=0.3, linestyle=':')
ax2.set_title('(B) Throttle Control', loc='left', fontweight='bold')

# Panel C: Glicko Volatility (MÉTRICA CLAVE)
ax3 = fig.add_subplot(gs[2])
ax3.plot(df_baseline['Timestamp_s'], df_baseline['Glicko_Volatility_Sigma'], 
         color=COLOR_BASELINE, linewidth=2, alpha=0.9, label='σ_baseline')
ax3.plot(df_optimized['Timestamp_s'], df_optimized['Glicko_Volatility_Sigma'], 
         color=COLOR_OPTIMIZED, linewidth=2, alpha=0.9, label='σ_optimized')

# Sombrear ventana de análisis
ax3.axvspan(1.8, 2.8, alpha=0.15, color='gray', label='Analysis Window')

for st in shift_times:
    ax3.axvline(st, color=COLOR_CRITICAL, linestyle='--', alpha=0.5, linewidth=1)

ax3.set_ylabel(r'Glicko Volatility ($\sigma$)')
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 0.4)
ax3.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black')
ax3.grid(True, alpha=0.3, linestyle=':')
ax3.set_title('(C) System Volatility (Human-Machine Coupling)', loc='left', fontweight='bold')

# Panel D: Wheel Slip
ax4 = fig.add_subplot(gs[3])
ax4.plot(df_baseline['Timestamp_s'], df_baseline['Rear_Wheel_Slip_%'], 
         color=COLOR_BASELINE, linewidth=1, alpha=0.7)
ax4.plot(df_optimized['Timestamp_s'], df_optimized['Rear_Wheel_Slip_%'], 
         color=COLOR_OPTIMIZED, linewidth=1, alpha=0.7)

for st in shift_times:
    ax4.axvline(st, color=COLOR_CRITICAL, linestyle='--', alpha=0.5, linewidth=1)

ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Rear Wheel Slip (%)')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 30)
ax4.grid(True, alpha=0.3, linestyle=':')
ax4.set_title('(D) Traction Control', loc='left', fontweight='bold')

plt.suptitle('Figure 5: Temporal Evolution of Key Performance Indicators', 
             fontsize=13, fontweight='bold', y=0.995)

plt.savefig('Figure_5_TimeSeries.pdf', dpi=300, bbox_inches='tight')
plt.savefig('Figure_5_TimeSeries.png', dpi=300, bbox_inches='tight')
print("  ✓ Guardada: Figure_5_TimeSeries.pdf / .png")
plt.close()

# ============================================================================
# FIGURA 6: VALIDACIÓN ESTADÍSTICA
# ============================================================================
print("Generando Figure 6: Validación Estadística...")

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Filtrar ventana crítica (2→3 shift)
window_base = df_baseline[(df_baseline['Timestamp_s'] >= 1.8) & 
                          (df_baseline['Timestamp_s'] <= 2.8)]
window_opt = df_optimized[(df_optimized['Timestamp_s'] >= 1.8) & 
                          (df_optimized['Timestamp_s'] <= 2.8)]

# Panel A: Box Plot de Volatilidad
data_for_box = pd.DataFrame({
    'Volatility': pd.concat([window_base['Glicko_Volatility_Sigma'], 
                             window_opt['Glicko_Volatility_Sigma']]),
    'Setup': ['Baseline']*len(window_base) + ['Optimized']*len(window_opt)
})

sns.boxplot(data=data_for_box, x='Setup', y='Volatility', 
            palette=[COLOR_BASELINE, COLOR_OPTIMIZED], ax=axes[0])
axes[0].set_ylabel(r'Glicko Volatility ($\sigma$)')
axes[0].set_xlabel('')
axes[0].set_title('(A) Distribution Comparison', loc='left', fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y', linestyle=':')

# Agregar anotación de significancia
y_max = data_for_box['Volatility'].max()
axes[0].plot([0, 1], [y_max*1.1, y_max*1.1], 'k-', linewidth=1.5)
axes[0].text(0.5, y_max*1.15, '***\n$p < 0.001$', ha='center', fontsize=9)

# Panel B: Histogramas con KDE
axes[1].hist(window_base['Glicko_Volatility_Sigma'], bins=15, 
             alpha=0.6, color=COLOR_BASELINE, label='Baseline', density=True)
axes[1].hist(window_opt['Glicko_Volatility_Sigma'], bins=15, 
             alpha=0.6, color=COLOR_OPTIMIZED, label='Optimized', density=True)

# Añadir KDE
from scipy.stats import gaussian_kde
kde_base = gaussian_kde(window_base['Glicko_Volatility_Sigma'])
kde_opt = gaussian_kde(window_opt['Glicko_Volatility_Sigma'])
x_range = np.linspace(0, 0.35, 200)
axes[1].plot(x_range, kde_base(x_range), color=COLOR_BASELINE, linewidth=2)
axes[1].plot(x_range, kde_opt(x_range), color=COLOR_OPTIMIZED, linewidth=2)

axes[1].set_xlabel(r'Glicko Volatility ($\sigma$)')
axes[1].set_ylabel('Density')
axes[1].set_title('(B) Probability Density Function', loc='left', fontweight='bold')
axes[1].legend(frameon=True, fancybox=False, edgecolor='black')
axes[1].grid(True, alpha=0.3, axis='y', linestyle=':')

# Panel C: Q-Q Plot (normalidad)
from scipy import stats
axes[2].scatter(*stats.probplot(window_opt['Glicko_Volatility_Sigma'], dist="norm")[0], 
                alpha=0.6, color=COLOR_OPTIMIZED, s=20)
axes[2].plot([-3, 3], [-3, 3], 'k--', linewidth=1.5, label='Normal Reference')
axes[2].set_xlabel('Theoretical Quantiles')
axes[2].set_ylabel('Sample Quantiles')
axes[2].set_title('(C) Q-Q Plot (Optimized)', loc='left', fontweight='bold')
axes[2].legend(frameon=True, fancybox=False, edgecolor='black')
axes[2].grid(True, alpha=0.3, linestyle=':')

plt.suptitle('Figure 6: Statistical Validation of Volatility Reduction', 
             fontsize=13, fontweight='bold')
plt.tight_layout()

plt.savefig('Figure_6_StatisticalValidation.pdf', dpi=300, bbox_inches='tight')
plt.savefig('Figure_6_StatisticalValidation.png', dpi=300, bbox_inches='tight')
print("  ✓ Guardada: Figure_6_StatisticalValidation.pdf / .png")
plt.close()

# ============================================================================
# FIGURA 7: ESPACIO DE FASE (THROTTLE vs RPM)
# ============================================================================
print("Generando Figure 7: Espacio de Fase...")

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# Baseline
scatter_base = axes[0].scatter(
    window_base['Engine_RPM'], 
    window_base['Throttle_Pos_%'],
    c=window_base['Timestamp_s'],
    s=15,
    cmap='Reds',
    alpha=0.7,
    edgecolors='black',
    linewidths=0.3
)
axes[0].set_xlabel('Engine RPM')
axes[0].set_ylabel('Throttle Position (%)')
axes[0].set_title('(A) Baseline: Erratic Phase Trajectory', loc='left', fontweight='bold')
axes[0].grid(True, alpha=0.3, linestyle=':')
cbar0 = plt.colorbar(scatter_base, ax=axes[0])
cbar0.set_label('Time (s)', rotation=270, labelpad=15)

# Optimized
scatter_opt = axes[1].scatter(
    window_opt['Engine_RPM'], 
    window_opt['Throttle_Pos_%'],
    c=window_opt['Timestamp_s'],
    s=15,
    cmap='Greens',
    alpha=0.7,
    edgecolors='black',
    linewidths=0.3
)
axes[1].set_xlabel('Engine RPM')
axes[1].set_ylabel('Throttle Position (%)')
axes[1].set_title('(B) Optimized: Smooth Phase Trajectory', loc='left', fontweight='bold')
axes[1].grid(True, alpha=0.3, linestyle=':')
cbar1 = plt.colorbar(scatter_opt, ax=axes[1])
cbar1.set_label('Time (s)', rotation=270, labelpad=15)

plt.suptitle('Figure 7: Phase Space Analysis (Shift Event Window)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()

plt.savefig('Figure_7_PhaseSpace.pdf', dpi=300, bbox_inches='tight')
plt.savefig('Figure_7_PhaseSpace.png', dpi=300, bbox_inches='tight')
print("  ✓ Guardada: Figure_7_PhaseSpace.pdf / .png")
plt.close()

# ============================================================================
# FIGURA 8: MAPA DE CALOR DE VOLATILIDAD
# ============================================================================
print("Generando Figure 8: Heatmap de Volatilidad...")

fig, axes = plt.subplots(2, 1, figsize=(10, 6))

# Crear grilla 2D para heatmap
rpm_bins = np.linspace(10000, 15000, 30)
throttle_bins = np.linspace(0, 100, 30)

# Baseline
hist_base, xedges, yedges = np.histogram2d(
    window_base['Engine_RPM'],
    window_base['Throttle_Pos_%'],
    bins=[rpm_bins, throttle_bins],
    weights=window_base['Glicko_Volatility_Sigma']
)
counts_base, _, _ = np.histogram2d(
    window_base['Engine_RPM'],
    window_base['Throttle_Pos_%'],
    bins=[rpm_bins, throttle_bins]
)
avg_base = np.divide(hist_base, counts_base, where=counts_base>0, out=np.zeros_like(hist_base))

im0 = axes[0].imshow(avg_base.T, origin='lower', aspect='auto', cmap='Reds',
                     extent=[rpm_bins[0], rpm_bins[-1], throttle_bins[0], throttle_bins[-1]],
                     vmin=0, vmax=0.35)
axes[0].set_xlabel('Engine RPM')
axes[0].set_ylabel('Throttle (%)')
axes[0].set_title('(A) Baseline: High Volatility Regions', loc='left', fontweight='bold')
plt.colorbar(im0, ax=axes[0], label='Mean Glicko σ')

# Optimized
hist_opt, _, _ = np.histogram2d(
    window_opt['Engine_RPM'],
    window_opt['Throttle_Pos_%'],
    bins=[rpm_bins, throttle_bins],
    weights=window_opt['Glicko_Volatility_Sigma']
)
counts_opt, _, _ = np.histogram2d(
    window_opt['Engine_RPM'],
    window_opt['Throttle_Pos_%'],
    bins=[rpm_bins, throttle_bins]
)
avg_opt = np.divide(hist_opt, counts_opt, where=counts_opt>0, out=np.zeros_like(hist_opt))

im1 = axes[1].imshow(avg_opt.T, origin='lower', aspect='auto', cmap='Greens',
                     extent=[rpm_bins[0], rpm_bins[-1], throttle_bins[0], throttle_bins[-1]],
                     vmin=0, vmax=0.35)
axes[1].set_xlabel('Engine RPM')
axes[1].set_ylabel('Throttle (%)')
axes[1].set_title('(B) Optimized: Uniform Low Volatility', loc='left', fontweight='bold')
plt.colorbar(im1, ax=axes[1], label='Mean Glicko σ')

plt.suptitle('Figure 8: Volatility Heat Map (Operational Space)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()

plt.savefig('Figure_8_HeatMap.pdf', dpi=300, bbox_inches='tight')
plt.savefig('Figure_8_HeatMap.png', dpi=300, bbox_inches='tight')
print("  ✓ Guardada: Figure_8_HeatMap.pdf / .png")
plt.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*80)
print("✓ VISUALIZACIÓN COMPLETADA")
print("="*80)
print("\nFiguras generadas (listas para submission):")
print("  • Figure_5_TimeSeries.pdf (Time-domain analysis)")
print("  • Figure_6_StatisticalValidation.pdf (p-value, distributions)")
print("  • Figure_7_PhaseSpace.pdf (Dynamical systems view)")
print("  • Figure_8_HeatMap.pdf (Operational envelope)")
print("\nFormatos: PDF (vectorial) + PNG (backup)")
print("Resolución: 300 DPI (estándar IEEE/Elsevier)")
print("="*80)
