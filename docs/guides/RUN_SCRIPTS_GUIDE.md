# 🚀 Master Scripts - Ejecutar Todo el Proyecto

Este archivo explica cómo usar los **3 métodos** para ejecutar todos los generadores y análisis del proyecto.

## 📋 Opciones Disponibles

### 1️⃣ **Python (Recomendado - Multiplataforma)**

**Archivo:** `run_all.py`

```bash
# Ejecutar TODO (dataset + tablas + verify)
python run_all.py

# Solo generar dataset v4.0
python run_all.py --data-only

# Solo generar tablas (requiere dataset existente)
python run_all.py --tables-only

# Incluir figuras
python run_all.py --with-figures

# Incluir MDF4 industrial
python run_all.py --with-mdf4

# Ejecutar ABSOLUTAMENTE TODO
python run_all.py --full
```

**Ventajas:**
- ✅ Multiplataforma (Windows, Mac, Linux)
- ✅ Control granular con opciones
- ✅ Salida detallada y mensajes de error claros
- ✅ Gestión de dependencias automática

### 2️⃣ **Bash (Rápido - Solo Unix/Linux/Mac)**

**Archivo:** `run_all.sh`

```bash
# Ejecutar TODO
bash run_all.sh

# Solo dataset
bash run_all.sh --data-only

# Con figuras
bash run_all.sh --with-figures

# Completo
bash run_all.sh --full

# Ayuda
bash run_all.sh --help
```

**Ventajas:**
- ✅ Muy rápido
- ✅ Minimalista
- ✅ Integrable en pipelines CI/CD

### 3️⃣ **Make (Profesional - Unix/Linux/Mac)**

**Archivo:** `Makefile`

```bash
# Ver todos los comandos
make help

# Instalar dependencias
make install

# Generar dataset v4.0
make data

# Generar tablas
make tables

# Verificar dataset
make verify

# Generar figuras
make figures

# Generar MDF4
make mdf4

# Ejecutar rápido (data + tablas + verify)
make quick

# Ejecutar TODO
make all
make full

# Limpiar outputs
make clean

# Ver estado del proyecto
make status

# Ver documentación
make docs
```

**Ventajas:**
- ✅ Profesional y estándar en industria
- ✅ Comandos cortos y memorizables
- ✅ Parfecto para CI/CD
- ✅ Reproducibilidad garantizada

---

## 🎯 Flujo de Trabajo Recomendado

### **Opción A: Todo de una vez (Python)**

```bash
python run_all.py --full
```

Esto ejecuta:
1. Generar dataset v4.0 (20,000 muestras, 35 canales)
2. Generar 7 tablas métricas
3. Verificar integridad
4. Generar figuras 300 DPI
5. Generar MDF4 industrial

**Tiempo:** ~2-3 minutos (depende de CPU)

### **Opción B: Rápido (Make)**

```bash
make quick
```

Esto ejecuta:
1. Generar dataset
2. Generar tablas
3. Verificar integridad

**Tiempo:** ~30 segundos

### **Opción C: Paso a Paso (Make)**

```bash
make install          # Instalar deps (1 vez)
make data             # Generar dataset
make tables           # Generar tablas
make verify           # Verificar
make figures          # Figuras (opcional)
```

---

## 📊 Estructura de Ejecución

```
run_all.py / run_all.sh / make
  │
  ├─→ 1. generate_case_study_data_v4.py
  │     └─ Output: data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv (20K rows)
  │
  ├─→ 2. generate_tables_v4.py
  │     └─ Output: outputs/tables/Table_v4_*.csv (3 archivos)
  │
  ├─→ 3. verify_dataset.py
  │     └─ Output: Estadísticas y validación
  │
  ├─→ 4. visualize_results_v3.py (--with-figures)
  │     └─ Output: outputs/figures/Figure_*.pdf/png
  │
  └─→ 5. generate_mdf4_binary_v3.py (--with-mdf4)
        └─ Output: outputs/mdf4/*.mf4
```

---

## 📈 Resultados Esperados

### **Dataset v4.0**
- ✅ 20,000 muestras (10K baseline + 10K optimizado)
- ✅ 35 canales (motor, frenos, aero, eficiencia, batería)
- ✅ 6 curvas Jerez (Senna, Dry Sack, Ciklon, Cartuja, Ayrton, Giro)
- ✅ 100 Hz sampling (FIM estándar)
- ✅ ~11 MB CSV file

### **Tablas Métricas**
- ✅ Table_v4_Glicko_Summary.csv (Glicko-2 volatility)
- ✅ Table_v4_All_Metrics.csv (24 métricas)
- ✅ Table_v4_Statistical_Tests.csv (Tests estadísticos)

### **Validación Estadística**
- ✅ Welch t-test: t=232.63, p=0.00e+00
- ✅ Cohen's d: 3.290 (efecto MASIVO)
- ✅ Glicko-2 σ: +83.6% mejora

---

## 🔧 Solución de Problemas

### **Error: "Module not found"**
```bash
pip install -r requirements.txt
```

### **Error: "Permission denied" (Bash)**
```bash
chmod +x run_all.sh
bash run_all.sh
```

### **Error: "Python3 not found"**
Instalar Python 3.8+ desde python.org

### **Dataset generado pero sin tablas**
```bash
python run_all.py --tables-only
```

### **Limpiar y empezar de nuevo**
```bash
make clean
make all
```

---

## 📚 Ver Documentación

```bash
# Estructura del proyecto
cat PROJECT_STRUCTURE.md

# Metodología del dataset
cat DATASET_METHODOLOGY.md

# Cómo integrar en paper
cat docs/guides/GUIA_INTEGRACION_PAPER.md

# Resumen ejecutivo v4.0
cat outputs/reports/v4.0_MEGA_EXPANDED_SUMMARY.md
```

---

## ⏱️ Tiempos de Ejecución (Aproximados)

| Comando | Tiempo |
|---------|--------|
| `make data` | ~15-20s |
| `make tables` | ~5s |
| `make verify` | ~5s |
| `make quick` | ~30s |
| `make figures` | ~30-60s |
| `make mdf4` | ~10s |
| `make all` | ~2-3 min |

---

## 🚀 Casos de Uso

### **Caso 1: Publicar en paper**
```bash
python run_all.py          # Generar todo
cat outputs/tables/Table_v4_Glicko_Summary.csv | copy
# Peguar en paper Results section
```

### **Caso 2: CI/CD Pipeline**
```bash
make install
make quick
# Verificar exit code 0
```

### **Caso 3: Desarrollo/Debugging**
```bash
make data           # Generar datos
python -i scripts/analysis/verify_dataset.py data/versioned/...
# Inspeccionar interactivamente
```

### **Caso 4: Reproducir Resultados**
```bash
make clean
make all
# Compara outputs con versión anterior
```

---

## 📝 Notas

- **Reproducibilidad:** Todos los scripts usan seeds determinísticos
- **Versioning:** Cada ejecutable preserva versiones anteriores en `data/versioned/`
- **Modularidad:** Cada paso puede ejecutarse independientemente
- **Logging:** Todos los comandos generan output detallado

---

**Última actualización:** 21 Enero 2026
**Status:** ✅ LISTO PARA PRODUCCIÓN
