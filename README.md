# Motor Physics and Glicko Rating System Simulator

A Python script that simulates motor physics (torque, RPM, power) and the Glicko rating system for competitive scenarios. The simulator generates CSV output files and optionally MF4 binary format for automotive data analysis.

## Features

- **Motor Physics Simulation**
  - Realistic torque curve simulation based on RPM
  - Power calculation in kW
  - Acceleration simulation from idle to maximum RPM
  - Configurable motor parameters (max RPM, max torque)

- **Glicko Rating System**
  - Implementation of the Glicko rating algorithm
  - Competitive match simulation with multiple players
  - Rating and rating deviation updates based on match results
  - Win/loss/draw tracking

- **Data Output**
  - CSV format for motor physics data
  - CSV format for Glicko rating history
  - Sample combined CSV data for documentation
  - MF4 binary format (when asammdf library is available)

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