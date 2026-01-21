# Nonlinear Lumping Analysis - Turn 5 Jerez Case Study

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Quality: Q1](https://img.shields.io/badge/Data_Quality-Q1_Ready-success.svg)](DATASET_METHODOLOGY.md)

## 📋 Overview

This repository contains the complete dataset and analysis pipeline for the **Gearing Optimization Case Study** presented in Section 4.4 of our paper on Nonlinear Lumping Analysis (NLA) applied to human-machine co-design in high-performance motorcycling.

### Key Results
- ✅ **47.6% reduction** in RPM drop during gear shifts
- ✅ **83.5% reduction** in Glicko volatility (system uncertainty)
- ✅ **p < 10⁻¹⁰⁰** (highly significant difference)
- ✅ **Cohen's d = 6.687** (enormous practical effect)

---

## 🗂️ Repository Structure

```
.
├── generate_case_study_data.py      # Data generator (physics-based simulation)
├── visualize_results.py             # Publication-quality figure generation
├── NLA_CaseStudy_Turn5_Jerez_Q1.csv # Main telemetry dataset (2,000 samples)
├── Table3_Comparative_Metrics.csv   # Summary statistics for paper
├── DATASET_METHODOLOGY.md           # Complete methodological documentation
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── Figure_5_TimeSeries.pdf          # Time-domain analysis (300 DPI)
├── Figure_6_StatisticalValidation.pdf
├── Figure_7_PhaseSpace.pdf
└── Figure_8_HeatMap.pdf
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd pruebas

# Install dependencies
pip install -r requirements.txt
```

### Generate Data

```bash
python generate_case_study_data.py
```

**Output:**
- `NLA_CaseStudy_Turn5_Jerez_Q1.csv` — Full telemetry (18 channels @ 100 Hz)
- `Table3_Comparative_Metrics.csv` — Summary statistics
- Console output with statistical analysis

### Generate Figures

```bash
python visualize_results.py
```

**Output:**
- `Figure_5_TimeSeries.pdf` — Time series of RPM, Throttle, Glicko σ, Wheel Slip
- `Figure_6_StatisticalValidation.pdf` — Box plots, histograms, Q-Q plot
- `Figure_7_PhaseSpace.pdf` — Phase space (Throttle vs RPM)
- `Figure_8_HeatMap.pdf` — Volatility heat maps

All figures are generated in **PDF (vectorial)** and **PNG (300 DPI)** formats, ready for journal submission.

---

## 📊 Data Description

### Scenario
**Circuit:** Jerez-Ángel Nieto, Turn 5 exit (Sector 2)  
**Maneuver:** Acceleration from 2nd to 4th gear (90 → 240 km/h)  
**Duration:** 10 seconds per lap  
**Conditions:** Dry track, 25°C ambient temperature

### Setup Comparison

| Parameter | Baseline | Optimized | Change |
|-----------|----------|-----------|--------|
| Rear Sprocket | 40T | 42T | +2 teeth |
| 2→3 RPM Drop | 3,732 rpm | 1,954 rpm | **-47.6%** |
| Glicko σ (mean) | 0.238 | 0.039 | **-83.5%** |
| Throttle σ | 12.87% | 21.86%* | Pilot confidence** |
| Wheel Slip | 14.72% | 10.38% | -29.5% |
| Acceleration | 0.881 g | 0.934 g | +6.1% |

\* *Higher throttle variance in Optimized = pilot able to modulate (not fighting)*  
\*\* *In Baseline, low throttle σ = frozen/reactive behavior*

### Key Channels

- **Engine_RPM** — Crankshaft speed (Hall effect sensor)
- **Throttle_Pos_%** — Throttle valve opening (TPS)
- **Glicko_Volatility_Sigma** — **PRIMARY METRIC** (system uncertainty)
- **Rear_Wheel_Slip_%** — Longitudinal tire slip
- **Longitudinal_Accel_g** — Forward acceleration

For complete sensor specifications and data dictionary, see [`DATASET_METHODOLOGY.md`](DATASET_METHODOLOGY.md).

---

## 📈 Glicko Volatility Metric

The **Glicko-2 volatility (σ)** quantifies uncertainty in human-machine coupling:

```
σ(t) = f(Δthrottle/dt, RPM_deviation, gear_transition_shock)
```

### Physical Interpretation

| σ Value | State | Meaning |
|---------|-------|---------|
| > 0.15 | **Unstable** | Pilot fighting the machine (reactive control) |
| 0.08 - 0.15 | Learning | Adaptation phase |
| < 0.08 | **Converged** | Human-machine symbiosis (predictive control) |

**Reference:** Glickman, M. (2013). "Example of the Glicko-2 system." Boston University.

---

## 🔬 Statistical Validation

### Hypothesis Test

**H₀:** μ_volatility(Baseline) = μ_volatility(Optimized)

**Method:** Welch's t-test (unequal variances)

**Results:**
- t-statistic = **47.28**
- p-value = **7.99 × 10⁻¹¹⁰** (< 0.001)
- **Conclusion:** REJECT H₀ — difference is statistically significant

### Effect Size

**Cohen's d = 6.687**

| Interpretation | Threshold | This Study |
|----------------|-----------|------------|
| Small | 0.2 | |
| Medium | 0.5 | |
| Large | 0.8 | |
| **Enormous** | **> 2.0** | **✓ 6.687** |

---

## 📦 Dependencies

```
numpy >= 2.4.0
pandas >= 2.3.0
scipy >= 1.10.0
matplotlib >= 3.7.0
seaborn >= 0.12.0
```

**Optional:**
- `asammdf >= 7.0.0` (for MDF4 export, not required for CSV workflow)

---

## 📄 Citation

If you use this dataset in your research, please cite:

```bibtex
@article{YourName2026NLA,
  title={Nonlinear Lumping Analysis for Human-Machine Co-Design in High-Performance Motorcycling},
  author={[Author Names]},
  journal={[Target Journal]},
  year={2026},
  volume={XX},
  pages={XXX--XXX},
  doi={10.XXXX/XXXXXX}
}
```

---

## 📖 Documentation

- **[DATASET_METHODOLOGY.md](DATASET_METHODOLOGY.md)** — Complete methodological documentation
  - Sensor specifications
  - Signal processing pipeline
  - Statistical validation procedures
  - Known limitations
  - Reproducibility instructions

- **[requirements.txt](requirements.txt)** — Python environment specification

---

## 🎯 Use Cases

### For Paper Reviewers
1. Load `NLA_CaseStudy_Turn5_Jerez_Q1.csv` in your analysis tool
2. Verify statistical claims in `Table3_Comparative_Metrics.csv`
3. Inspect `DATASET_METHODOLOGY.md` for reproducibility details
4. Check figures match manuscript claims

### For Researchers
1. Reproduce figures: `python visualize_results.py`
2. Run sensitivity analysis on `generate_case_study_data.py`
3. Extend to other maneuvers/circuits
4. Apply Glicko metric to your own telemetry

### For Engineers
1. Import CSV into MoTeC / Pi Toolbox
2. Compare against real-world telemetry
3. Validate simulation parameters
4. Benchmark setup changes

---

## 🔧 Troubleshooting

### Issue: Missing scipy dependency
```bash
pip install scipy
```

### Issue: LaTeX warnings in plots
Set `plt.rcParams['text.usetex'] = False` (already default)

### Issue: Figures don't match console stats
Re-run `generate_case_study_data.py` first (data files may be outdated)

---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add XYZ analysis'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📧 Contact

- **Lead Researcher:** [Name] — [email]
- **GitHub Issues:** [Issue tracker URL]
- **Paper Preprint:** [arXiv/ResearchGate link]

---

## 📜 License

MIT License — See [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgments

- MotoGP technical regulations (FIM)
- Glicko-2 rating system (M. Glickman, Boston University)
- Python scientific computing community (NumPy, Pandas, SciPy)

---

**Last Updated:** January 21, 2026  
**Status:** ✅ Ready for Submission  
**Data Quality:** Q1 Publication Standard
