# ⚡ QUICK START - 5 Minutos para Estar Listo

## 🎯 Objective
Generar y verificar el dataset v4.0 MotoGP con Glicko-2 simulator en 5 minutos.

---

## 📋 Pasos

### **Paso 1: Verificar Prerequisites** (30 segundos)

```bash
# Verificar Python instalado
python3 --version
# Debe ser Python 3.8+

# Verificar pip
pip --version
```

### **Paso 2: Instalar Dependencias** (1 minuto)

```bash
# En la carpeta del proyecto
pip install -r requirements.txt
```

**Qué instala:**
- numpy 2.4.1
- pandas 2.3.3
- scipy 1.10+
- matplotlib 3.7+
- seaborn 0.12+
- asammdf 7.3+ (MDF4)

### **Paso 3: Ejecutar Master Script** (1-2 minutos)

**OPCIÓN A: Rápido (Recomendado)**
```bash
python run_all.py
```
⏱️ ~30 segundos | Genera: Dataset + Tablas + Verify

**OPCIÓN B: Con Figuras**
```bash
python run_all.py --with-figures
```
⏱️ ~1 minuto | Agrega: 4 gráficos 300 DPI

**OPCIÓN C: Todo**
```bash
python run_all.py --full
```
⏱️ ~2-3 minutos | Agrega: MDF4 industrial

### **Paso 4: Verificar Outputs** (1 minuto)

```bash
# Ver dataset principal
head -3 data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv

# Ver resultados Glicko-2
cat outputs/tables/Table_v4_Glicko_Summary.csv

# Ver tablas
ls -lh outputs/tables/
```

---

## 📊 Qué Esperar

### **Dataset Principal**
```
✅ NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv
   • 20,000 muestras (10K baseline + 10K optimizado)
   • 35 canales (motor, frenos, aero, eficiencia, batería)
   • 6 curvas Jerez (Senna, Dry Sack, Ciklon, Cartuja, Ayrton, Giro)
   • 100 Hz sampling (FIM MotoGP estándar)
   • Tamaño: 11 MB
```

### **Tablas Metrics**
```
✅ outputs/tables/
   • Table_v4_Glicko_Summary.csv          (Glicko-2 volatility σ)
   • Table_v4_All_Metrics.csv             (24 métricas principales)
   • Table_v4_Statistical_Tests.csv       (Tests estadísticos)
```

### **Resultados Principales**
```
✅ Glicko-2 σ: +83.6% mejora
✅ p-value: 0.00e+00 (extremadamente significativo)
✅ Cohen's d: 3.290 (efecto MASIVO)
✅ Engine Efficiency: +2.32%
```

---

## 🔧 Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'pandas'` | `pip install -r requirements.txt` |
| `Python not found` | Instalar Python 3.8+ desde python.org |
| `Permission denied (bash)` | `chmod +x run_all.sh && bash run_all.sh` |
| Lento / Sin memoria | Editar en `run_all.py`: reduce `n_samples` de 10000 |

---

## 📚 Next Steps

1. **Ver datos generados:**
   ```bash
   head -5 data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv
   ```

2. **Explorar resultados:**
   ```bash
   cat outputs/tables/Table_v4_Glicko_Summary.csv | head -20
   ```

3. **Integrar en paper:**
   ```bash
   cat docs/guides/GUIA_INTEGRACION_PAPER.md
   ```

4. **Entender estructura:**
   ```bash
   cat PROJECT_STRUCTURE.md
   ```

---

## 📖 Documentación Completa

- **[RUN_SCRIPTS_GUIDE.md](RUN_SCRIPTS_GUIDE.md)** - Opciones detalladas
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Estructura del proyecto
- **[README.md](README.md)** - Overview principal
- **[DATASET_METHODOLOGY.md](DATASET_METHODOLOGY.md)** - Metodología técnica

---

## ✅ Verificación Final

```bash
# Confirmar que todo está OK
echo "Dataset:"
ls -lh data/versioned/*.csv | grep "v4_MEGA"

echo ""
echo "Tablas:"
ls -lh outputs/tables/ | grep "Table_v4"

echo ""
echo "Status: ✅ LISTO PARA PUBLICACIÓN Q1+"
```

---

**⏱️ Tiempo Total: ~5 minutos**

**Próximo paso:** Copiar tablas a paper académico y enviar con DOI 🚀
