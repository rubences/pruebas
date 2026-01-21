# MotoGP Nonlinear Lumping Analysis (NLA) - Jerez Circuit Study

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research: Q1](https://img.shields.io/badge/Research-Q1%20Ready-brightgreen.svg)](docs/)

## 📋 Descripción

Análisis avanzado de telemetría MotoGP aplicando la metodología Nonlinear Lumping Analysis (NLA) al Circuito de Jerez - Ángel Nieto. Este proyecto genera y analiza datasets sintéticos de alta fidelidad que replican condiciones reales de carrera, comparando configuraciones baseline y optimizadas con **validación estadística rigurosa**.

### 🎯 Características Principales

- **20,000 muestras** a 100Hz (estándar FIM)
- **37 canales telemetría**: motor, suspensión, aerodinámica, neumáticos, Glicko-2
- **6 curvas** del circuito de Jerez analizadas
- **Validación estadística**: Welch t-test, Cohen's d, Kolmogorov-Smirnov
- **Figuras Q1**: 8 visualizaciones publication-ready (PDF/PNG 300dpi)
- **Física Grade A+**: fuerzas reales, cargas laterales, interacciones complejas

---

## 📁 Estructura del Proyecto

```
pruebas/
├── 📂 bin/                          # Scripts ejecutables
│   ├── run_all.py                   # Ejecutar pipeline completo
│   ├── run_all.sh                   # Wrapper bash
│   ├── print_summary.py             # Resumen de resultados
│   └── show_structure.sh            # Mostrar estructura
│
├── 📂 data/                         # Datos y resultados
│   ├── datasets/                    # Datasets CSV
│   │   ├── NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv (20k muestras)
│   │   └── NLA_CaseStudy_Jerez_Industrial_AllChannels.csv
│   ├── tables/                      # Tablas de métricas
│   │   ├── Table_v4_All_Metrics.csv
│   │   ├── Table_v4_Glicko_Summary.csv
│   │   ├── Table_v4_Statistical_Tests.csv
│   │   └── Turns_Analysis_v4.csv
│   ├── mdf4/                        # Archivos MDF4
│   │   └── NLA_CaseStudy_Jerez_v3_Industrial.mf4
│   ├── raw/                         # Datos sin procesar
│   ├── processed/                   # Datos procesados
│   └── versioned/                   # Versiones anteriores
│
├── 📂 docs/                         # Documentación completa
│   ├── guides/                      # Guías de uso
│   │   ├── PROJECT_STRUCTURE.md     # Estructura detallada
│   │   ├── QUICK_START.md           # Inicio rápido
│   │   └── RUN_SCRIPTS_GUIDE.md     # Guía de ejecución
│   ├── methodology/                 # Metodología científica
│   │   └── DATASET_METHODOLOGY.md   # Metodología del dataset
│   ├── INDEX.md                     # Índice general
│   ├── MASTER_SCRIPTS_STATUS.md     # Estado de scripts
│   ├── README_DATASET.md            # Documentación dataset
│   └── README_MASTER_SCRIPTS.md     # Documentación scripts
│
├── 📂 outputs/                      # Resultados generados
│   ├── figures/                     # Figuras Q1 (PDF/PNG)
│   │   ├── Figure_5_Time_Series_Multi-Metrics.pdf
│   │   ├── Figure_6_Statistical_Validation.pdf
│   │   ├── Figure_7_Performance_Metrics_Comparison.pdf
│   │   ├── Figure_8_Quantile_Time_Series.pdf
│   │   ├── Figure_9_Distribution_Analysis.pdf
│   │   ├── Figure_10_Efficiency_&_Power_Management.pdf
│   │   ├── Figure_11_Phase_Space_&_Correlations.pdf
│   │   └── Figure_12_Lap-by-Lap_Breakdown.pdf
│   ├── tables/                      # Tablas adicionales
│   ├── mdf4/                        # MDF4 generados
│   ├── reports/                     # Informes
│   ├── documentation/               # Docs de outputs
│   │   ├── FIGURES_EXPLANATION_v4.1.md
│   │   ├── FIGURES_SUMMARY.txt
│   │   └── README_FIGURAS.md
│   ├── index.html                   # Visualización web
│   └── README.md                    # Documentación outputs
│
├── 📂 scripts/                      # Código fuente
│   ├── generators/                  # Generadores de datos
│   │   ├── generate_case_study_data_v4.py
│   │   ├── generate_tables_v4.py
│   │   └── generate_mdf4_v4.py
│   ├── analysis/                    # Análisis y visualización
│   │   └── visualize_results_v4_advanced.py
│   ├── utils/                       # Utilidades
│   └── README.md                    # Docs de scripts
│
├── requirements.txt                 # Dependencias Python
├── Makefile                         # Automatización
├── .gitignore                       # Archivos ignorados
└── README.md                        # Este archivo
```

---

## 🚀 Inicio Rápido

### 1️⃣ Instalación

```bash
# Clonar repositorio
git clone https://github.com/rubences/pruebas.git
cd pruebas

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Generar Todo el Pipeline

```bash
# Opción 1: Script Python (recomendado)
python bin/run_all.py

# Opción 2: Script Bash
bash bin/run_all.sh

# Opción 3: Makefile
make all
```

### 3️⃣ Generar Componentes Individuales

```bash
# Solo dataset
python scripts/generators/generate_case_study_data_v4.py

# Solo tablas
python scripts/generators/generate_tables_v4.py

# Solo figuras
python scripts/analysis/visualize_results_v4_advanced.py

# Resumen
python bin/print_summary.py
```

---

## 📊 Resultados Clave

### Mejoras Estadísticamente Significativas (p < 1e-12)

| Métrica | Baseline | Optimized | Mejora | Cohen's d |
|---------|----------|-----------|--------|-----------|
| **Glicko-2 Volatility σ** | 0.05966 | 0.03918 | **↓ 34.3%** | 3.29 |
| **Wheel Slip (%)** | 7.51 | 7.00 | **↓ 6.8%** | 0.52 |
| **Engine Efficiency (%)** | 88.1 | 89.4 | **↑ 1.5%** | 0.31 |
| **Battery Current (A)** | 47.2 | 45.8 | **↓ 3.0%** | 0.18 |

**Validación Estadística:**
- Welch t-test: p = 0.00e+00 (altamente significativo)
- Cohen's d = 3.29 (efecto muy grande)
- Kolmogorov-Smirnov: distribuciones diferentes confirmadas

---

## 📖 Documentación

### Guías Principales

- **[Quick Start](docs/guides/QUICK_START.md)**: Inicio rápido
- **[Project Structure](docs/guides/PROJECT_STRUCTURE.md)**: Estructura detallada
- **[Dataset Methodology](docs/methodology/DATASET_METHODOLOGY.md)**: Metodología científica
- **[Run Scripts Guide](docs/guides/RUN_SCRIPTS_GUIDE.md)**: Guía de ejecución

### Documentación Adicional

- **Figuras**: Ver [outputs/documentation/FIGURES_EXPLANATION_v4.1.md](outputs/documentation/FIGURES_EXPLANATION_v4.1.md)
- **Datasets**: Ver [docs/README_DATASET.md](docs/README_DATASET.md)
- **Scripts**: Ver [docs/README_MASTER_SCRIPTS.md](docs/README_MASTER_SCRIPTS.md)

---

## 🔬 Metodología Científica

### Dataset v4.0 MEGA

- **Muestras**: 20,000 (10,000 por setup)
- **Frecuencia**: 100 Hz (FIM estándar)
- **Duración**: 10 segundos efectivos por setup
- **Curvas**: 6 turns del circuito de Jerez
- **Física**: Grade A+ con validación experto MotoGP
- **Reproducibilidad**: Seed fijo (1854652912)

### Canales Telemetría (37)

**Motor & Transmisión** (7): RPM, torque, eficiencia, potencia, temperatura, gear, ratio  
**Suspensión** (4): Travel FL/RL, velocidad FL/RL  
**Neumáticos** (8): Temperatura y presión FL/FR/RL/RR  
**Frenos** (2): Temperatura, presión  
**Aerodinámica** (2): Downforce, drag  
**Dinámica** (8): Aceleración lon/lat, velocidad, throttle, steering, gyro roll/pitch/yaw  
**Control** (2): Slip, battery current/voltage  
**Glicko-2** (3): Rating μ, deviation RD, volatility σ  
**Meta** (1): Setup (baseline/optimized)

### Validación Estadística

- **Welch t-test**: Para diferencias de medias sin asumir varianzas iguales
- **Cohen's d**: Tamaño del efecto (0.2=pequeño, 0.5=medio, 0.8=grande)
- **Kolmogorov-Smirnov**: Comparación de distribuciones completas
- **Levene test**: Homogeneidad de varianzas

---

## 🛠️ Tecnologías

- **Python 3.8+**: Lenguaje principal
- **NumPy/Pandas**: Procesamiento de datos
- **SciPy**: Análisis estadístico
- **Matplotlib/Seaborn**: Visualización Q1
- **asammdf**: Generación MDF4 (opcional)

---

## 📝 Citación

Si utilizas este trabajo en tu investigación, por favor cita:

```bibtex
@article{nla_motogp_2024,
  title={Nonlinear Lumping Analysis for MotoGP Performance Optimization},
  author={[Tu Nombre]},
  journal={IEEE Transactions on Human-Machine Systems},
  year={2024},
  note={Q1 Journal - Under Review}
}
```

---

## 📧 Contacto

- **Autor**: [Tu Nombre]
- **Email**: tu.email@example.com
- **GitHub**: [@rubences](https://github.com/rubences)

---

## 📄 Licencia

MIT License - Ver LICENSE para más detalles.

---

## 🎯 Estado del Proyecto

✅ **Dataset v4.0**: Completo (20k muestras, 37 canales)  
✅ **Tablas Métricas**: Completas (4 tablas CSV)  
✅ **Figuras Q1**: Completas (8 figuras PDF/PNG 300dpi)  
✅ **Validación Estadística**: Completa (p<1e-12, d=3.29)  
✅ **Documentación**: Completa  
🔄 **MDF4 Generation**: En progreso  
🔄 **Publicación**: Preparando para Q1 journal  

---

**Última actualización**: Enero 2026  
**Versión**: 4.1  
**Target**: IEEE THMS / ACM TIST / Nature Scientific Data
