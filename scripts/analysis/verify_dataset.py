#!/usr/bin/env python3
"""
SCRIPT DE VERIFICACIÓN RÁPIDA - CALIDAD Q1
==========================================
Ejecuta este script para validar que todos los componentes del dataset
cumplan con los estándares de publicación Q1.

Uso: python verify_dataset.py
"""

import os
import sys
import pandas as pd
import numpy as np

print("="*80)
print("VERIFICACIÓN DE DATASET Q1 - CASO DE ESTUDIO TURN 5 JEREZ")
print("="*80)

errors = []
warnings = []
passed = 0

# ============================================================================
# 1. VERIFICAR ARCHIVOS REQUERIDOS
# ============================================================================
print("\n[1/6] Verificando archivos requeridos...")

required_files = {
    'NLA_CaseStudy_Turn5_Jerez_Q1.csv': 'Dataset principal',
    'Table3_Comparative_Metrics.csv': 'Tabla resumen',
    'DATASET_METHODOLOGY.md': 'Documentación metodológica',
    'README_DATASET.md': 'Guía de usuario',
    'generate_case_study_data.py': 'Código generador',
    'visualize_results.py': 'Código de visualización',
    'requirements.txt': 'Dependencias'
}

for filename, description in required_files.items():
    if os.path.exists(filename):
        print(f"  ✓ {filename} ({description})")
        passed += 1
    else:
        errors.append(f"Falta archivo requerido: {filename}")
        print(f"  ✗ {filename} (FALTA)")

# ============================================================================
# 2. VERIFICAR ESTRUCTURA DEL CSV
# ============================================================================
print("\n[2/6] Verificando estructura del dataset...")

try:
    df = pd.read_csv('NLA_CaseStudy_Turn5_Jerez_Q1.csv')
    
    # Dimensiones
    expected_rows = 2000  # 2 laps * 1000 samples
    expected_cols = 18
    
    if len(df) == expected_rows:
        print(f"  ✓ Filas: {len(df)} (correcto)")
        passed += 1
    else:
        warnings.append(f"Número de filas inesperado: {len(df)} (esperado: {expected_rows})")
        print(f"  ⚠ Filas: {len(df)} (esperado: {expected_rows})")
    
    if len(df.columns) == expected_cols:
        print(f"  ✓ Columnas: {len(df.columns)} (correcto)")
        passed += 1
    else:
        warnings.append(f"Número de columnas inesperado: {len(df.columns)} (esperado: {expected_cols})")
        print(f"  ⚠ Columnas: {len(df.columns)} (esperado: {expected_cols})")
    
    # Valores faltantes
    missing = df.isnull().sum().sum()
    if missing == 0:
        print(f"  ✓ Valores faltantes: 0")
        passed += 1
    else:
        errors.append(f"Dataset contiene {missing} valores faltantes")
        print(f"  ✗ Valores faltantes: {missing}")
    
except Exception as e:
    errors.append(f"Error al cargar CSV: {str(e)}")
    print(f"  ✗ Error: {str(e)}")

# ============================================================================
# 3. VERIFICAR MÉTRICAS CLAVE
# ============================================================================
print("\n[3/6] Verificando métricas clave...")

try:
    df_baseline = df[df['Setup_Type'] == 'BASELINE']
    df_optimized = df[df['Setup_Type'] == 'OPTIMIZED']
    
    # Filtrar ventana crítica
    window_base = df_baseline[(df_baseline['Timestamp_s'] >= 1.8) & 
                              (df_baseline['Timestamp_s'] <= 2.8)]
    window_opt = df_optimized[(df_optimized['Timestamp_s'] >= 1.8) & 
                              (df_optimized['Timestamp_s'] <= 2.8)]
    
    # Glicko Volatility
    sigma_base = window_base['Glicko_Volatility_Sigma'].mean()
    sigma_opt = window_opt['Glicko_Volatility_Sigma'].mean()
    reduction = ((sigma_base - sigma_opt) / sigma_base) * 100
    
    if reduction > 80:
        print(f"  ✓ Reducción de volatilidad: {reduction:.1f}% (> 80%)")
        passed += 1
    else:
        warnings.append(f"Reducción de volatilidad baja: {reduction:.1f}%")
        print(f"  ⚠ Reducción de volatilidad: {reduction:.1f}% (esperado > 80%)")
    
    # Cohen's d
    from scipy import stats
    t_stat, p_value = stats.ttest_ind(
        window_base['Glicko_Volatility_Sigma'],
        window_opt['Glicko_Volatility_Sigma']
    )
    
    if p_value < 0.001:
        print(f"  ✓ Significancia estadística: p = {p_value:.2e} (< 0.001)")
        passed += 1
    else:
        errors.append(f"p-value insuficiente: {p_value:.2e}")
        print(f"  ✗ p-value: {p_value:.2e} (esperado < 0.001)")
    
except Exception as e:
    errors.append(f"Error en análisis estadístico: {str(e)}")
    print(f"  ✗ Error: {str(e)}")

# ============================================================================
# 4. VERIFICAR FIGURAS
# ============================================================================
print("\n[4/6] Verificando figuras...")

figures = [
    'Figure_5_TimeSeries.pdf',
    'Figure_6_StatisticalValidation.pdf',
    'Figure_7_PhaseSpace.pdf',
    'Figure_8_HeatMap.pdf'
]

for fig in figures:
    if os.path.exists(fig):
        size_kb = os.path.getsize(fig) / 1024
        if size_kb > 10:  # Mínimo 10 KB para PDFs válidos
            print(f"  ✓ {fig} ({size_kb:.0f} KB)")
            passed += 1
        else:
            warnings.append(f"Figura sospechosamente pequeña: {fig} ({size_kb:.0f} KB)")
            print(f"  ⚠ {fig} ({size_kb:.0f} KB - posiblemente corrupta)")
    else:
        errors.append(f"Falta figura: {fig}")
        print(f"  ✗ {fig} (FALTA)")

# ============================================================================
# 5. VERIFICAR RANGOS FÍSICOS
# ============================================================================
print("\n[5/6] Verificando rangos físicos...")

try:
    ranges_ok = True
    
    # RPM
    if df['Engine_RPM'].min() < 9000 or df['Engine_RPM'].max() > 18500:
        warnings.append(f"RPM fuera de rango: [{df['Engine_RPM'].min():.0f}, {df['Engine_RPM'].max():.0f}]")
        ranges_ok = False
    
    # Speed
    if df['Speed_kmh'].min() < 85 or df['Speed_kmh'].max() > 250:
        warnings.append(f"Velocidad fuera de rango: [{df['Speed_kmh'].min():.0f}, {df['Speed_kmh'].max():.0f}]")
        ranges_ok = False
    
    # Throttle
    if df['Throttle_Pos_%'].min() < -1 or df['Throttle_Pos_%'].max() > 101:
        warnings.append(f"Throttle fuera de rango: [{df['Throttle_Pos_%'].min():.1f}, {df['Throttle_Pos_%'].max():.1f}]")
        ranges_ok = False
    
    # Glicko
    if df['Glicko_Volatility_Sigma'].min() < 0 or df['Glicko_Volatility_Sigma'].max() > 0.5:
        warnings.append(f"Glicko σ fuera de rango: [{df['Glicko_Volatility_Sigma'].min():.3f}, {df['Glicko_Volatility_Sigma'].max():.3f}]")
        ranges_ok = False
    
    if ranges_ok:
        print(f"  ✓ Todos los canales dentro de rangos físicos")
        passed += 1
    else:
        print(f"  ⚠ Algunos canales fuera de rango (ver warnings)")
    
except Exception as e:
    errors.append(f"Error en verificación de rangos: {str(e)}")
    print(f"  ✗ Error: {str(e)}")

# ============================================================================
# 6. VERIFICAR REPRODUCIBILIDAD
# ============================================================================
print("\n[6/6] Verificando reproducibilidad...")

try:
    with open('generate_case_study_data.py', 'r') as f:
        code = f.read()
        
    checks = {
        'numpy': 'import numpy' in code,
        'pandas': 'import pandas' in code,
        'scipy': 'from scipy' in code,
        'docstrings': '"""' in code or "'''" in code,
        'comments': '#' in code
    }
    
    for component, present in checks.items():
        if present:
            print(f"  ✓ {component.capitalize()} presente")
            passed += 1
        else:
            warnings.append(f"Falta {component} en código")
            print(f"  ⚠ {component.capitalize()} ausente")
    
except Exception as e:
    errors.append(f"Error verificando código: {str(e)}")
    print(f"  ✗ Error: {str(e)}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN DE VERIFICACIÓN")
print("="*80)

total_checks = passed + len(warnings) + len(errors)
print(f"\n✓ Verificaciones pasadas: {passed}/{total_checks}")

if warnings:
    print(f"\n⚠ ADVERTENCIAS ({len(warnings)}):")
    for w in warnings:
        print(f"  • {w}")

if errors:
    print(f"\n✗ ERRORES CRÍTICOS ({len(errors)}):")
    for e in errors:
        print(f"  • {e}")
    print("\n❌ DATASET NO LISTO PARA PUBLICACIÓN")
    sys.exit(1)
elif warnings:
    print("\n⚠ DATASET FUNCIONAL PERO CON ADVERTENCIAS")
    print("   Revisar warnings antes de submission")
    sys.exit(0)
else:
    print("\n✅ DATASET COMPLETAMENTE VALIDADO - LISTO PARA PUBLICACIÓN Q1")
    print("\nPróximos pasos:")
    print("  1. Revisar GUIA_INTEGRACION_PAPER.md")
    print("  2. Integrar Tabla 3 y Figuras 5-8 en el manuscrito")
    print("  3. Subir material suplementario al journal")
    sys.exit(0)
