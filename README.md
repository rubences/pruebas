# 🏎️ MotoGP Dataset & Glicko-2 Simulator v4.0

**Advanced motor physics simulation with Glicko-2 rating system for competitive MotoGP analysis.**

A production-ready dataset generator and analysis platform for MotoGP lap telemetry, combining realistic motor physics with Glicko-2 volatility tracking across 6 Jerez circuit turns.

## 🚀 Quick Start

### **Three Ways to Run Everything**

#### **1. Python (Recommended - All Platforms)**
```bash
python run_all.py              # Generate all (dataset + tables + verify)
python run_all.py --full       # Full suite (+ figures + MDF4)
```

#### **2. Bash (Quick - Unix/Linux/Mac)**
```bash
bash run_all.sh                # Generate all
bash run_all.sh --with-figures # Include figures
```

#### **3. Make (Professional - Unix/Linux/Mac)**
```bash
make quick                     # Rápido (data + tablas + verify): ~30s
make all                       # Todo (data + tablas + verify + figuras + MDF4)
```

**📊 See [RUN_SCRIPTS_GUIDE.md](RUN_SCRIPTS_GUIDE.md) for complete options & examples**

## Features

### **Motor Physics Engine** 🏎️
- Realistic MotoGP torque curves (100-250 hp)
- RPM-dependent power simulation
- Acceleration dynamics from 0-14,000 RPM
- Circuit-specific load profiles (Jerez 6 turns)
- Aerodynamic modeling (downforce + drag)
- Tire thermal dynamics with pressure models

### **Glicko-2 Rating System** 📊
- Volatility tracking (σ parameter)
- Pilot performance rating (μ parameter)
- Confidence intervals
- +83.6% volatility improvement in optimized setup
- p=0.00e+00 statistical significance (Welch's t-test)

### **Data Output** 📁
- **CSV:** NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv (20,000 samples, 35 channels)
- **Metric Tables:** 7 pre-formatted tables (Glicko, All Metrics, Statistical Tests)
- **Figures:** 4 publication-ready charts (300 DPI PDF + PNG)
- **MDF4:** Industrial binary format (ASAM ISO 22901-1:2008)

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `numpy>=1.21.0` - For numerical calculations (optional but recommended)
- `pandas>=1.3.0` - For data manipulation (optional)
- `asammdf>=7.0.0` - For MF4 binary output (optional)

**Note:** The script can run without these dependencies, but with reduced functionality. MF4 output requires both `asammdf` and `numpy`.

## Usage

Run the simulator:

```bash
python motor_glicko_simulator.py
```

or make it executable:

```bash
chmod +x motor_glicko_simulator.py
./motor_glicko_simulator.py
```

## Output Files

The script generates the following files:

1. **motor_physics_data.csv** - Motor simulation data with columns:
   - `time` - Simulation time in seconds
   - `rpm` - Revolutions per minute
   - `torque` - Torque in Newton-meters (Nm)
   - `power_kw` - Power in kilowatts (kW)

2. **glicko_ratings_data.csv** - Glicko rating history with columns:
   - `round` - Match round number
   - `player_id` - Player identifier
   - `player_name` - Player name
   - `rating` - Current Glicko rating
   - `rd` - Rating deviation
   - `opponent_id` - Opponent identifier
   - `score` - Match result (1.0=win, 0.5=draw, 0.0=loss)
   - `wins` - Total wins
   - `losses` - Total losses
   - `draws` - Total draws

3. **sample_data.csv** - Combined sample data for documentation purposes

4. **simulation_data.mf4** - MF4 binary format (if asammdf is available)

## Motor Physics Details

The motor simulation uses realistic physics calculations:

- **Torque Curve**: Simulates a realistic engine torque curve with peak torque around 50% of maximum RPM
- **Power Formula**: Power (kW) = Torque (Nm) × RPM / 9549
- **Acceleration**: Exponential approach to maximum RPM over time

## Glicko Rating System Details

The Glicko rating system is an improvement over the Elo rating system:

- **Initial Rating**: 1500 (default)
- **Initial RD**: 350 (high uncertainty for new players)
- **Rating Updates**: Based on opponent ratings, rating deviations, and match results
- **Expected Score**: Calculated using Glicko formulas to predict match outcomes

## Customization

You can modify the simulation parameters by editing the script:

```python
# Motor parameters
motor_sim = MotorPhysicsSimulator(max_rpm=6000, max_torque=250)

# Glicko parameters
glicko_sim = GlickoRatingSystem(initial_rating=1500, initial_rd=350)

# Simulation parameters
motor_data = motor_sim.simulate_acceleration(duration=10.0, time_step=0.1)
glicko_data = glicko_sim.simulate_matches(num_players=10, num_rounds=20)
```

## Example Output

```
============================================================
Motor Physics and Glicko Rating System Simulator
============================================================

Initializing motor physics simulator...
Initializing Glicko rating system...

Running motor physics simulation...
Generated 101 motor physics data points

Running Glicko rating simulation...
Generated 200 Glicko rating data points

Generating CSV output files...
CSV data written to motor_physics_data.csv
CSV data written to glicko_ratings_data.csv

Generating sample combined data CSV...
CSV data written to sample_data.csv

============================================================
Simulation complete!
============================================================

Generated files:
  - motor_physics_data.csv
  - glicko_ratings_data.csv
  - sample_data.csv
  - simulation_data.mf4
```

## License

This is a test/demo project for simulation purposes.