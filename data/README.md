# 📊 Carpeta Data

Contiene todos los datasets del proyecto en diferentes versiones.

## Estructura

### `raw/`
Datos crudos/originales sin procesar:
- `sample_data.csv` - Ejemplo inicial simple
- `NLA_CaseStudy_Turn5_Jerez.csv` - Turn 5 sin procesar

### `processed/`
Datos procesados y limpios (vacío, para futuros desarrollos)

### `versioned/`
Todas las versiones del dataset del proyecto:

| Archivo | Versión | Muestras | Canales | Formato | Tamaño |
|---------|---------|----------|---------|---------|--------|
| NLA_CaseStudy_Turn5_Jerez_Q1.csv | v1.0 | 2,000 | 18 | CSV | 320K |
| NLA_CaseStudy_Jerez_Industrial.mf4 | v2.0 | 2,000 | 43 | MDF4 | 708K |
| NLA_CaseStudy_Turn5_Jerez_Q1_v3.csv | v3.0 | 5,000 | 28 | CSV | 828K |
| NLA_CaseStudy_Jerez_v3_Industrial.mf4 | v3.0 | 5,000 | 65 | MDF4 | 2.5M |
| NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv | v4.0 | 20,000 | 35 | CSV | 11M |

## 🎯 Dataset Principal (v4.0)

**`NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv`** ⭐

- **Muestras:** 20,000 (10,000 baseline + 10,000 optimizado)
- **Canales:** 35 (motor, frenos, aero, eficiencia, batería, etc.)
- **Circuito:** 6 turns Jerez (Senna, Dry Sack, Ciklon, Cartuja, Ayrton, Giro)
- **Sampleo:** 100 Hz (FIM estándar MotoGP)
- **Duración:** ~10 segundos por setup
- **Status:** ✅ Listo para publicación Q1+

### Resultados Principales (v4.0)
- Glicko-2 σ: **+83.6%** mejora
- p-value: **0.00e+00** (extremadamente significativo)
- Cohen's d: **3.290** (efecto masivo)
- Eficiencia motor: **+2.32%**

## Cómo Usar

```bash
# Ver primeras líneas
head -5 versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv

# Contar filas
wc -l versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv

# Análisis con Python
import pandas as pd
df = pd.read_csv('versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv')
print(df.info())
```

## Historial de Versiones

- **v1.0:** Dataset base, Turn 5 solamente, 2,000 muestras
- **v2.0:** Agregado MDF4 formato industrial (43 canales)
- **v3.0:** Expandido a 5,000 muestras, 28 canales CSV, validación completa
- **v4.0:** MEGA expansion - 20,000 muestras, 6 curvas, 35 canales, p=0.00e+00

---

**Para más detalles:** Ver [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
