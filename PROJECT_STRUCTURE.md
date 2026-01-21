# 📁 Estructura del Proyecto - MotoGP Dataset & Glicko-2 Simulator

```
pruebas/
│
├── 📄 ROOT DOCUMENTATION
│   ├── README.md                          # Overview principal del proyecto
│   ├── INDEX.md                           # Índice de versiones y archivos
│   ├── README_DATASET.md                  # Documentación del dataset
│   ├── DATASET_METHODOLOGY.md             # Metodología de generación
│   ├── requirements.txt                   # Dependencias Python
│   └── PROJECT_STRUCTURE.md              # Este archivo
│
├── 📊 data/
│   │
│   ├── raw/                              # Datos crudos/originales (v1)
│   │   ├── sample_data.csv              # Dataset inicial de ejemplo
│   │   └── NLA_CaseStudy_Turn5_Jerez.csv # Turn 5 solamente (v1)
│   │
│   ├── processed/                        # Datos procesados/limpios
│   │   └── [Vacío - para futuros datos procesados]
│   │
│   └── versioned/                        # Versiones v1 - v4
│       ├── NLA_CaseStudy_Turn5_Jerez_Q1.csv          # v1 - 2,000 muestras, Turn 5
│       ├── NLA_CaseStudy_Turn5_Jerez_Q1_v3.csv      # v3 - 5,000 muestras
│       ├── NLA_CaseStudy_Jerez_Industrial.mf4       # v2 - formato MDF4 binario
│       ├── NLA_CaseStudy_Jerez_v3_Industrial.mf4    # v3 - MDF4 expandido (2.5 MB)
│       └── NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv       # v4 - 20,000 muestras ⭐
│
├── 🐍 scripts/
│   │
│   ├── generators/                       # Generadores de datos
│   │   ├── generate_case_study_data.py   # v1.0 - Generador base (2K muestras, Turn 5)
│   │   ├── generate_case_study_data_v3.py # v3.0 - Multi-turn (5K muestras)
│   │   ├── generate_case_study_data_v4.py # v4.0 - MEGA (10K muestras/setup) ⭐
│   │   ├── generate_mdf4_binary.py       # v1.0 - Exportador MDF4
│   │   ├── generate_mdf4_binary_v3.py    # v3.0 - MDF4 expandido
│   │   └── generate_tables_v4.py         # v4.0 - Generador de 7 tablas métricas
│   │
│   ├── analysis/                         # Scripts de análisis
│   │   ├── visualize_results.py          # Generador de figuras (v1-v3)
│   │   ├── visualize_results_v3.py       # Figuras v3.0 mejoradas
│   │   └── verify_dataset.py             # Validación y verificación de datos
│   │
│   └── utils/                            # Utilidades reutilizables
│       └── motor_glicko_simulator.py     # Core simulator: motor MotoGP + Glicko-2
│
├── 📈 outputs/
│   │
│   ├── tables/                           # Tablas CSV para publicación
│   │   ├── Table3_Comparative_Metrics.csv     # Comparativa v1-v3
│   │   ├── Table_v4_Glicko_Summary.csv        # ⭐ Glicko-2 volatility (σ)
│   │   ├── Table_v4_All_Metrics.csv           # ⭐ 24 métricas principales
│   │   ├── Table_v4_Statistical_Tests.csv     # ⭐ Tests estadísticos (t, d, KS)
│   │   └── Turns_Analysis_v4.csv              # ⭐ Análisis por 6 curvas Jerez
│   │
│   ├── figures/                          # Visualizaciones (PDF + PNG, 300 DPI)
│   │   ├── Figure_5_TimeSeries.pdf       # Series temporales (v1)
│   │   ├── Figure_5_TimeSeries_v3.pdf    # Series temporales (v3)
│   │   ├── Figure_6_Statistical_v3.pdf   # Validación estadística (v3)
│   │   ├── Figure_7_PhaseSpace_v3.pdf    # Espacio de fase (v3)
│   │   ├── Figure_8_HeatMap_v3.pdf       # Mapa de calor (v3)
│   │   └── [PNG equivalentes para web]
│   │
│   ├── mdf4/                             # Archivos binarios ASAM MDF4
│   │   └── [Vacío - para futuros MDF4 v4.0]
│   │
│   └── reports/                          # Reportes y resúmenes
│       └── v4.0_MEGA_EXPANDED_SUMMARY.md # ⭐ Resumen ejecutivo v4.0
│
├── 📚 docs/
│   │
│   ├── guides/                           # Guías y tutoriales
│   │   ├── GUIA_INTEGRACION_PAPER.md     # Cómo integrar en papel académico
│   │   └── MDF4_INDUSTRIAL_GUIDE.md      # Guía formato industrial MDF4
│   │
│   └── summaries/                        # Resúmenes ejecutivos
│       ├── RESUMEN_EJECUTIVO.md          # Resumen general del proyecto
│       └── AMPLIFIED_v3_RESUMEN_FINAL.md # Resumen v3.0 específico
│
└── .gitignore
```

---

## 🗂️ Organización por Versión

### v1.0 - Original (2,000 muestras)
- **Dataset:** `data/versioned/NLA_CaseStudy_Turn5_Jerez_Q1.csv`
- **Generador:** `scripts/generators/generate_case_study_data.py`
- **Circuito:** Turn 5 solamente (Ayrton)
- **Canales:** 18 básicos

### v2.0 - Ampliado con MDF4 (2,000 muestras)
- **Dataset:** `data/versioned/NLA_CaseStudy_Jerez_Industrial.mf4`
- **Generador MDF4:** `scripts/generators/generate_mdf4_binary.py`
- **Canales MDF4:** 43 (nivel industrial)
- **Formato:** ASAM MDF4 binario comprimido

### v3.0 - Industrial (5,000 muestras)
- **Dataset CSV:** `data/versioned/NLA_CaseStudy_Turn5_Jerez_Q1_v3.csv`
- **Dataset MDF4:** `data/versioned/NLA_CaseStudy_Jerez_v3_Industrial.mf4` (2.5 MB)
- **Generador:** `scripts/generators/generate_case_study_data_v3.py`
- **Figuras:** 4 gráficos publicables (v3)
- **Canales:** 28 CSV + 65 MDF4
- **Análisis:** Validación estadística completa

### v4.0 - MEGA Expansion (20,000 muestras) ⭐
- **Dataset:** `data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv` (3.2 MB)
- **Generador:** `scripts/generators/generate_case_study_data_v4.py`
- **Tablas:** 7 nuevas tablas métricas
- **Análisis:** 6 curvas completas Jerez (Senna, Dry Sack, Ciklon, Cartuja, Ayrton, Giro)
- **Canales:** 35 (7 nuevos: aero, eficiencia, batería)
- **Resultados:** p=0.00e+00, Cohen's d=3.290, Glicko σ ↓ 83.6%

---

## 📋 Casos de Uso por Carpeta

### `data/versioned/`
```bash
# Descargar dataset principal v4.0
cat data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv | head -5

# Examinar versión anterior (v3)
wc -l data/versioned/NLA_CaseStudy_Turn5_Jerez_Q1_v3.csv
```

### `scripts/generators/`
```bash
# Regenerar dataset v4.0 (10 segundos)
python scripts/generators/generate_case_study_data_v4.py

# Generar tablas métricas
python scripts/generators/generate_tables_v4.py

# Convertir a MDF4 industrial
python scripts/generators/generate_mdf4_binary_v3.py
```

### `outputs/tables/`
```bash
# Ver tabla de resumen Glicko-2 (para paper)
cat outputs/tables/Table_v4_Glicko_Summary.csv

# Análisis por curva (6 turns)
cat outputs/tables/Turns_Analysis_v4.csv
```

### `outputs/figures/`
```bash
# Abrir figura de validación estadística
open outputs/figures/Figure_6_Statistical_v3.pdf

# Convertir PNG a web
identify outputs/figures/Figure_*.png | head -5
```

---

## 🎯 Flujo de Trabajo Recomendado

```
1. EXPLORACIÓN
   └─ data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv
      └─ Leer primeras filas, entender estructura

2. ANÁLISIS
   ├─ scripts/generators/generate_case_study_data_v4.py (regen si necesario)
   └─ scripts/analysis/visualize_results_v3.py (crear gráficos)

3. VALIDACIÓN
   ├─ scripts/analysis/verify_dataset.py
   └─ outputs/tables/Table_v4_Statistical_Tests.csv

4. DOCUMENTACIÓN
   ├─ docs/guides/GUIA_INTEGRACION_PAPER.md (para paper)
   └─ outputs/reports/v4.0_MEGA_EXPANDED_SUMMARY.md

5. PUBLICACIÓN
   ├─ outputs/tables/Table_v4_*.csv (copiar a paper)
   └─ outputs/figures/Figure_*.pdf (300 DPI ready)
```

---

## 📊 Mapeo Rápido de Recursos

| Necesidad | Archivo |
|-----------|---------|
| **Dataset principal v4.0** | `data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv` |
| **Tabla de resultados** | `outputs/tables/Table_v4_Glicko_Summary.csv` |
| **Tests estadísticos** | `outputs/tables/Table_v4_Statistical_Tests.csv` |
| **Análisis por curva** | `outputs/tables/Turns_Analysis_v4.csv` |
| **Figuras publicables** | `outputs/figures/Figure_*_v3.pdf` |
| **Regenerar dataset** | `scripts/generators/generate_case_study_data_v4.py` |
| **Generar tablas** | `scripts/generators/generate_tables_v4.py` |
| **Guía paper** | `docs/guides/GUIA_INTEGRACION_PAPER.md` |
| **Resumen ejecutivo** | `outputs/reports/v4.0_MEGA_EXPANDED_SUMMARY.md` |

---

## 🔄 Versioning & Cambios

```
v1.0 → v2.0:  Agregado MDF4 (43 canales)
v2.0 → v3.0:  +3K muestras, 28 canales CSV, 65 MDF4, validación
v3.0 → v4.0:  +15K muestras (20K total), 7 canales nuevos, 6 curvas ⭐
```

**v4.0 Ready for Publication:**
- ✅ 20,000 muestras (10x v1.0)
- ✅ 35 canales multisistema
- ✅ 6 curvas completas Jerez
- ✅ p=0.00e+00 (estadísticamente significativo)
- ✅ Cohen's d=3.290 (efecto masivo)
- ✅ 7 tablas métricas
- ✅ Reproducible (seed determinista)

---

**Última actualización:** 21 Enero 2026
**Status:** Listo para envío Q1+ (IEEE THMS, ACM TIST, Nature Scientific Data)
