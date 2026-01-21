#!/usr/bin/env python3
"""
SCRIPT DE VERIFICACIÓN v4.0 - DATASET MEGA
===========================================
Verifica la integridad del dataset v4.0 generado con 20,000 muestras.

Uso: python verify_dataset_v4.py [dataset_path]
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Usar archivo por defecto si no se especifica
if len(sys.argv) > 1:
    dataset_file = sys.argv[1]
else:
    dataset_file = "data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"

print("="*80)
print("VERIFICACIÓN DE DATASET v4.0 - MEGA EXPANSION")
print("="*80)

errors = []
warnings = []
passed = 0

# ============================================================================
# 1. VERIFICAR ARCHIVO DATASET
# ============================================================================
print(f"\n[1/5] Verificando archivo: {dataset_file}...")

if not os.path.exists(dataset_file):
    print(f"  ✗ Error: Archivo no encontrado: {dataset_file}")
    sys.exit(1)

file_size_mb = os.path.getsize(dataset_file) / (1024 * 1024)
print(f"  ✓ Archivo existe ({file_size_mb:.1f} MB)")
passed += 1

# ============================================================================
# 2. VERIFICAR ESTRUCTURA DEL CSV
# ============================================================================
print("\n[2/5] Verificando estructura del dataset...")

try:
    df = pd.read_csv(dataset_file)
    
    # Verificar dimensiones esperadas
    expected_rows = 20000  # v4.0 MEGA
    expected_cols_min = 35  # 35 canales
    
    print(f"  ✓ Dataset cargado exitosamente")
    print(f"  • Filas: {len(df):,}")
    print(f"  • Columnas: {len(df.columns)}")
    
    if len(df) >= expected_rows:
        print(f"  ✓ Muestras: {len(df):,} (correcto, ≥ {expected_rows:,})")
        passed += 1
    else:
        warnings.append(f"Número de muestras menor al esperado: {len(df)} (esperado: {expected_rows})")
        print(f"  ⚠ Muestras: {len(df):,} (esperado: ≥ {expected_rows:,})")
    
    if len(df.columns) >= expected_cols_min:
        print(f"  ✓ Canales: {len(df.columns)} (correcto, ≥ {expected_cols_min})")
        passed += 1
    else:
        errors.append(f"Número de canales insuficiente: {len(df.columns)} (esperado: ≥ {expected_cols_min})")
        print(f"  ✗ Canales: {len(df.columns)} (esperado: ≥ {expected_cols_min})")
    
    # Valores faltantes
    missing = df.isnull().sum().sum()
    if missing == 0:
        print(f"  ✓ Valores faltantes: 0")
        passed += 1
    else:
        warnings.append(f"Dataset contiene {missing} valores faltantes")
        print(f"  ⚠ Valores faltantes: {missing}")
    
    # Tipos de datos
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"  ✓ Columnas numéricas: {len(numeric_cols)}")
    
except Exception as e:
    print(f"  ✗ Error al cargar CSV: {str(e)}")
    errors.append(f"Error al cargar CSV: {str(e)}")
    sys.exit(1)

# ============================================================================
# 3. VERIFICAR RANGO DE VALORES
# ============================================================================
print("\n[3/5] Verificando rangos físicos...")

try:
    # Columnas esperadas en v4.0
    expected_cols = ['Engine_RPM', 'Throttle_pos', 'Wheel_Speed', 'Brake_Pressure',
                     'Lateral_Accel', 'Wheel_Slip_Ratio', 'Glicko_Rating', 'Glicko_Deviation']
    
    found_cols = [col for col in expected_cols if col in df.columns]
    print(f"  ✓ Columnas clave encontradas: {len(found_cols)}/{len(expected_cols)}")
    
    # Verificar rangos
    if 'Engine_RPM' in df.columns:
        rpm_min, rpm_max = df['Engine_RPM'].min(), df['Engine_RPM'].max()
        if 0 <= rpm_min < rpm_max <= 15000:
            print(f"  ✓ Engine_RPM: [{rpm_min:.0f}, {rpm_max:.0f}] (válido)")
            passed += 1
        else:
            warnings.append(f"Engine_RPM fuera de rango esperado: [{rpm_min}, {rpm_max}]")
            print(f"  ⚠ Engine_RPM: [{rpm_min:.0f}, {rpm_max:.0f}] (posible problema)")
    
    if 'Throttle_pos' in df.columns:
        thr_min, thr_max = df['Throttle_pos'].min(), df['Throttle_pos'].max()
        if 0 <= thr_min <= thr_max <= 100:
            print(f"  ✓ Throttle_pos: [{thr_min:.1f}, {thr_max:.1f}]% (válido)")
            passed += 1
        else:
            warnings.append(f"Throttle_pos fuera de [0, 100]: [{thr_min}, {thr_max}]")
            print(f"  ⚠ Throttle_pos: [{thr_min:.1f}, {thr_max:.1f}]% (inusual)")
    
    if 'Glicko_Deviation' in df.columns:
        gd_mean = df['Glicko_Deviation'].mean()
        gd_std = df['Glicko_Deviation'].std()
        if 0 < gd_mean < 200 and 0 < gd_std < 150:
            print(f"  ✓ Glicko_Deviation: μ={gd_mean:.1f}, σ={gd_std:.1f} (válido)")
            passed += 1
        else:
            warnings.append(f"Glicko_Deviation valores inusuales: μ={gd_mean}, σ={gd_std}")
            print(f"  ⚠ Glicko_Deviation: μ={gd_mean:.1f}, σ={gd_std:.1f}")
    
except Exception as e:
    print(f"  ✗ Error verificando rangos: {str(e)}")
    errors.append(f"Error en verificación de rangos: {str(e)}")

# ============================================================================
# 4. VERIFICAR ESTADÍSTICAS BÁSICAS
# ============================================================================
print("\n[4/5] Verificando estadísticas...")

try:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Estadísticas básicas
    print(f"  ✓ Columnas numéricas: {len(numeric_cols)}")
    print(f"  ✓ Media de valores: {df[numeric_cols].mean().mean():.2f}")
    print(f"  ✓ Desv. Est. promedio: {df[numeric_cols].std().mean():.2f}")
    
    # Verificar distribuciones
    if 'Glicko_Rating' in df.columns:
        gr_mean = df['Glicko_Rating'].mean()
        gr_std = df['Glicko_Rating'].std()
        print(f"  ✓ Glicko_Rating: μ={gr_mean:.1f} ± {gr_std:.1f}")
        passed += 1
    
except Exception as e:
    print(f"  ✗ Error en estadísticas: {str(e)}")
    errors.append(f"Error en estadísticas: {str(e)}")

# ============================================================================
# 5. VERIFICAR REPRODUCIBILIDAD
# ============================================================================
print("\n[5/5] Verificando reproducibilidad...")

# Buscar archivo generador
gen_scripts = ['scripts/generators/generate_case_study_data_v4.py',
               'generate_case_study_data_v4.py']

gen_found = False
for script_path in gen_scripts:
    if os.path.exists(script_path):
        print(f"  ✓ Script generador encontrado: {script_path}")
        gen_found = True
        passed += 1
        break

if not gen_found:
    warnings.append("Script generador no encontrado (reproducibilidad limitada)")
    print(f"  ⚠ Script generador no localizado")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN DE VERIFICACIÓN")
print("="*80)

total_checks = 15
print(f"\n✓ Verificaciones pasadas: {passed}/{total_checks}")

if len(errors) > 0:
    print(f"\n✗ ERRORES CRÍTICOS ({len(errors)}):")
    for i, err in enumerate(errors, 1):
        print(f"  {i}. {err}")

if len(warnings) > 0:
    print(f"\n⚠ ADVERTENCIAS ({len(warnings)}):")
    for i, warn in enumerate(warnings, 1):
        print(f"  {i}. {warn}")

print("\n" + "="*80)

if len(errors) == 0:
    print("✅ DATASET LISTO PARA ANÁLISIS")
    sys.exit(0)
else:
    print("⚠️  DATASET CON PROBLEMAS - REVISAR ERRORES")
    sys.exit(1)
