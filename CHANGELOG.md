# ════════════════════════════════════════════════════════════════
# CHANGELOG - MotoGP Dataset & Glicko-2 Analysis Project
# ════════════════════════════════════════════════════════════════

## [4.1.0] - 2026-01-21 - Production Release

### 🎯 Major Changes
- **Complete project restructuring** for professional organization
- **Fixed visualization script** (create_figure_7 was missing)
- **Production deployment** ready with automated scripts

### 📁 Project Structure
- Reorganized from flat structure to hierarchical:
  - `bin/` - Executable scripts (run_all.py, cleanup.sh, etc.)
  - `data/datasets/` - Generated datasets (20k samples)
  - `data/tables/` - Statistical metrics tables
  - `data/mdf4/` - Industrial binary format
  - `scripts/generators/` - Data generation scripts
  - `scripts/analysis/` - Analysis and visualization
  - `outputs/figures/` - Publication-quality figures
  - `docs/` - Complete documentation

### ✨ New Features
- **deploy.sh**: Automated production deployment script
- **Updated Makefile**: Commands aligned with new structure
- **Enhanced .gitignore**: Proper exclusion of generated files
- **DEPLOYMENT_INFO.txt**: Auto-generated deployment metadata

### 🔧 Bug Fixes
- Fixed `create_figure_7()` missing function error
- Corrected mixed code in `create_figure_6()` and `create_figure_8()`
- Updated all path references to new structure
- Replaced non-existent metrics with valid alternatives

### 📊 Figures (v4.1 Advanced)
- **Figure 5**: Time Series Multi-Metrics
- **Figure 6**: Statistical Validation (KDE + histograms + p-values)
- **Figure 7**: Performance Metrics Comparison (bar charts + deltas) ⭐ NEW
- **Figure 8**: Quantile Time Series (speed, throttle, yaw with IQR bands) ⭐ UPDATED
- **Figure 9**: Distribution Analysis
- **Figure 10**: Efficiency & Power Management
- **Figure 11**: Phase Space & Correlations
- **Figure 12**: Lap-by-Lap Breakdown

### 📈 Key Metrics
- Glicko Volatility: **83.6% improvement**
- Engine Efficiency: **+2.32%**
- Wheel Slip: **40% reduction**
- p-value: **< 1×10⁻¹²** (highly significant)
- Cohen's d: **3.29** (very large effect)

### 🚀 Commands
```bash
make help       # Show all commands
make all        # Complete pipeline
make data       # Generate dataset (20k samples)
make tables     # Generate 4 statistical tables
make figures    # Generate 8 Q1 figures (300dpi PDF+PNG)
make status     # Show project structure
make clean      # Clean generated files
```

---

## [4.0.0] - 2026-01-20 - MEGA Dataset Expansion

### ✨ Features
- **v4.0 MEGA Dataset**: 20,000 samples (10k per setup)
- **37 channels**: Added 7 new channels (aero, efficiency, battery)
- **Multi-curve analysis**: 6 turns Jerez circuit
- **Enhanced physics**: Grade-A+ circuit-specific loads

### 📊 New Channels
- `aero_downforce_n` - Aerodynamic downforce (N)
- `aero_drag_n` - Aerodynamic drag (N)
- `gear_ratio_efficiency_percent` - Gear ratio efficiency (%)
- `engine_efficiency_percent` - Engine efficiency (%)
- `battery_voltage_v` - Battery voltage (V)
- `battery_current_a` - Battery current (A)

### 📋 Tables
- `Table_v4_All_Metrics.csv` - Complete performance metrics
- `Table_v4_Glicko_Summary.csv` - Glicko-2 statistics
- `Table_v4_Statistical_Tests.csv` - Hypothesis testing results
- `Turns_Analysis_v4.csv` - Per-turn analysis

---

## [3.0.0] - 2026-01-15 - Industrial Format Support

### ✨ Features
- **MDF4 binary export** for industrial telemetry systems
- **Enhanced turn analysis** with 5 characteristic turns
- **Improved visualizations** with Q1-grade aesthetics

---

## [2.0.0] - Initial Release

### ✨ Features
- Basic dataset generation (2k samples)
- Core telemetry channels (30 channels)
- Glicko-2 volatility analysis
- Basic visualization suite

---

## Versioning
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes in data structure or API
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, minor improvements
