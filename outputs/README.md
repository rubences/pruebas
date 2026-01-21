# 📈 Carpeta Outputs

Contiene todos los resultados, tablas, figuras y reportes generados.

## Estructura

### `tables/`
Tablas CSV listos para integrar en papers académicos:

- **Table_v4_Glicko_Summary.csv** ⭐ - Resumen Glicko-2 (σ, μ, std, max, min, median, Q1, Q3)
- **Table_v4_All_Metrics.csv** - 24 métricas principales por categoría
- **Table_v4_Statistical_Tests.csv** - Resultados tests: t-test, Cohen's d, Levene, KS
- **Turns_Analysis_v4.csv** - Análisis por las 6 curvas Jerez
- **Table3_Comparative_Metrics.csv** - Comparativa entre versiones

### `figures/`
Visualizaciones publicables en formato PDF (300 DPI) y PNG:

- **Figure_5_TimeSeries** - Series temporales (v1 y v3)
- **Figure_6_Statistical** - Validación estadística y distribuciones
- **Figure_7_PhaseSpace** - Espacio de fase de dinámicas
- **Figure_8_HeatMap** - Mapa de calor de correlaciones

Total: 16 archivos (8 PDF + 8 PNG)

### `mdf4/`
Formatos binarios industriales (ASAM MDF4):

Vacío actualmente, pendiente generar v4.0 MDF4 (usar `generate_mdf4_binary_v3.py` como base)

### `reports/`
Documentos y resúmenes ejecutivos:

- **v4.0_MEGA_EXPANDED_SUMMARY.md** - Resumen ejecutivo v4.0 (400+ líneas)

## 📊 Resultados Principales (v4.0)

### Glicko-2 Volatility (σ)
| Setup | μ | σ_std | max | min |
|-------|---|-------|-----|-----|
| Baseline | 0.1290 | 0.0458 | 0.3632 | 0.0051 |
| Optimized | 0.0212 | 0.0071 | 0.0578 | 0.0002 |
| **Mejora** | **+83.6%** ↓ | **+84.4%** ↓ | **+84.1%** ↓ | **+96.1%** ↓ |

### Validación Estadística
- Welch's t-test: **t = 232.63**, p = **0.00e+00** ✅
- Cohen's d: **3.290** (efecto MASIVO) ✅
- Levene's Test: F = 809.09 (varianzas desiguales)
- KS Test: KS = 1.0000 (distribuciones significativamente diferentes)

### Mejoras Adicionales
- Engine Efficiency: **94.83% → 97.15%** (+2.32%)
- Wheel Slip: **6.26% → 3.75%** (-40.1%)
- Brake Temp: **-4.2%** reducción

## Cómo Usar

### Copiar tablas a Paper
```bash
# Para sección Results (4.4)
cat outputs/tables/Table_v4_Glicko_Summary.csv

# Para sección Methods (estadística)
cat outputs/tables/Table_v4_Statistical_Tests.csv

# Para supplementary (análisis por curva)
cat outputs/tables/Turns_Analysis_v4.csv
```

### Insertar Figuras
```bash
# PDF 300 DPI (publicable)
open outputs/figures/Figure_6_Statistical_v3.pdf

# PNG para web
convert outputs/figures/Figure_5_TimeSeries_v3.png -resize 800x600 web-version.png
```

### Examinar Resultados
```bash
# Ver Glicko-2 summary
head -5 outputs/tables/Table_v4_Glicko_Summary.csv

# Estadísticas detalladas
cat outputs/tables/Table_v4_All_Metrics.csv | column -t -s,

# Per-turn breakdown
cat outputs/tables/Turns_Analysis_v4.csv
```

## Integración en Paper (LaTeX)

```latex
% Insertar tabla
\begin{table}[h]
\input{outputs/tables/Table_v4_Glicko_Summary.csv}
\caption{Glicko-2 volatility metrics (v4.0)}
\end{table}

% Insertar figura
\begin{figure}[h]
\includegraphics[width=0.8\textwidth]{outputs/figures/Figure_6_Statistical_v3.pdf}
\caption{Statistical validation and distributions}
\end{figure}
```

---

**Para más detalles:** Ver [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
