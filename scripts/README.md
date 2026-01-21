# 🐍 Carpeta Scripts

Scripts Python para generación, análisis y visualización de datos.

## Estructura

### `generators/`
Scripts que generan nuevos datos o exportan a diferentes formatos:

- **generate_case_study_data.py** - v1.0 Generador base (2K muestras, Turn 5)
- **generate_case_study_data_v3.py** - v3.0 Multi-turn (5K muestras, 28 canales)
- **generate_case_study_data_v4.py** ⭐ - v4.0 MEGA (20K muestras, 35 canales, 6 turns)
- **generate_mdf4_binary.py** - Exportador MDF4 v1.0
- **generate_mdf4_binary_v3.py** - Exportador MDF4 v3.0 industrial
- **generate_tables_v4.py** ⭐ - Generador 7 tablas métricas v4.0

### `analysis/`
Scripts para análisis, verificación y visualización:

- **verify_dataset.py** - Valida integridad de datos (missing values, stats)
- **visualize_results.py** - Crea figuras v1-v3 (matplotlib)
- **visualize_results_v3.py** - Figuras mejoradas v3.0 (300 DPI)

### `utils/`
Código reutilizable y funciones auxiliares:

- **motor_glicko_simulator.py** - Core: motor MotoGP + Glicko-2 rating system

## Cómo Ejecutar

### Generar Nuevo Dataset v4.0
```bash
python scripts/generators/generate_case_study_data_v4.py

# Output:
# - data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv (20K rows)
# - outputs/tables/Turns_Analysis_v4.csv
```

### Generar Tablas Métricas
```bash
python scripts/generators/generate_tables_v4.py

# Output:
# - outputs/tables/Table_v4_Glicko_Summary.csv
# - outputs/tables/Table_v4_All_Metrics.csv
# - outputs/tables/Table_v4_Statistical_Tests.csv
```

### Verificar Dataset
```bash
python scripts/analysis/verify_dataset.py data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv

# Muestra: filas, columnas, missing values, estadísticas
```

### Generar Figuras
```bash
python scripts/analysis/visualize_results_v3.py

# Output:
# - outputs/figures/Figure_5_*.pdf
# - outputs/figures/Figure_6_*.pdf
# - outputs/figures/Figure_7_*.pdf
# - outputs/figures/Figure_8_*.pdf
```

## Dependencias

```
numpy>=2.4.1
pandas>=2.3.3
scipy>=1.10
matplotlib>=3.7
seaborn>=0.12
asammdf>=7.3
```

Ver `requirements.txt` en raíz.

## Flujo Típico

```
1. Generar datos
   python scripts/generators/generate_case_study_data_v4.py

2. Crear tablas
   python scripts/generators/generate_tables_v4.py

3. Verificar integridad
   python scripts/analysis/verify_dataset.py <dataset.csv>

4. Generar figuras
   python scripts/analysis/visualize_results_v3.py

5. Ver resultados
   cat outputs/tables/Table_v4_Glicko_Summary.csv
```

---

**Para más detalles:** Ver [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
