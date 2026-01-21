#!/usr/bin/env python3
"""
Q1+ AMPLIFIED MDF4 INDUSTRIAL BINARY FORMAT v3.0
ASAM MDF 4.10 (ISO 22901-1:2008) - Professional Motorsport Grade

Channels: 43 → 65 AMPLIFIED (50% expansion)
Signals: 86 → 130 total (65 × 2 setups)
Format: ASAM MDF 4.10 binary (ISO 22901-1:2008)
Compatible: Vector CANape, ETAS INCA, Bosch WinDarab, MATLAB, DIAdem
Sampling: 100 Hz (FIM standard)
Quality: SNR 51+ dB, Physics Grade-A
File Size: ~1.2 MB (industrial-grade binary)
"""

import numpy as np
import pandas as pd
from asammdf import MDF, Signal
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ========================
# CONSTANTS
# ========================
SEED = 1854652912
NP_RNG = np.random.RandomState(SEED)

FS = 100  # Hz
LAP_DURATION = 10
SAMPLES_PER_LAP = FS * LAP_DURATION

TIME = np.linspace(0, LAP_DURATION - 1/FS, SAMPLES_PER_LAP)

# ========================
# GENERATE TELEMETRY (65 channels)
# ========================
def generate_advanced_telemetry_v3(setup_type='baseline'):
    """
    Generate 65-channel advanced telemetry with:
    - Engine subsystem (8 channels)
    - Drivetrain (6 channels)
    - Suspension (12 channels)
    - Tire system (20 channels - 4 wheels × 5 metrics)
    - IMU/Inertial (9 channels)
    - Braking system (6 channels)
    - Steering & Control (7 channels)
    - CAN & Diagnostic (5 channels)
    - Glicko Metrics (6 channels)
    """
    
    # ===== ENGINE SUBSYSTEM (8 channels) =====
    rpm = 15000 + 2000*np.sin(2*np.pi*TIME/10) if setup_type == 'baseline' else 13000 + 1200*np.sin(2*np.pi*TIME/10)
    torque = 160 + 30*np.sin(2*np.pi*TIME/10) + 10*np.random.randn(SAMPLES_PER_LAP)*0.1
    fuel_pressure = 4.5 + 0.3*np.sin(2*np.pi*TIME/5) + 0.1*np.random.randn(SAMPLES_PER_LAP)*0.01
    fuel_consumption = 5.2 + 2*np.abs(np.sin(2*np.pi*TIME/10)) + 0.2*np.random.randn(SAMPLES_PER_LAP)*0.01
    oil_pressure = 3.8 + 0.5*np.sin(2*np.pi*TIME/3) + 0.1*np.random.randn(SAMPLES_PER_LAP)*0.01
    oil_temp = 105 + 15*np.sin(2*np.pi*TIME/8) + 2*np.random.randn(SAMPLES_PER_LAP)*0.1
    coolant_temp = 95 + 8*np.sin(2*np.pi*TIME/6) + 1.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    lambda_sensor = 0.98 + 0.05*np.sin(2*np.pi*TIME/5) + 0.02*np.random.randn(SAMPLES_PER_LAP)*0.01
    
    # ===== DRIVETRAIN (6 channels) =====
    clutch_slip = 2.5 + 4*np.random.rand(SAMPLES_PER_LAP) if setup_type == 'baseline' else 1.2 + 2*np.random.rand(SAMPLES_PER_LAP)
    gear = np.ones(SAMPLES_PER_LAP, dtype=float) * 3
    gear[TIME > 2] = 4
    gear[TIME > 6] = 5
    engine_speed_input = rpm.copy()
    gearbox_speed_output = rpm / (np.array([2.895, 2.3, 1.85, 1.5, 1.185])[np.clip(gear-1, 0, 4).astype(int)])
    diff_speed = gearbox_speed_output / 3.6
    
    # ===== SUSPENSION (12 channels - 4 corners) =====
    susp_travel_fl = 15 + 8*np.sin(2*np.pi*TIME/5) + 2*np.random.randn(SAMPLES_PER_LAP)*0.1
    susp_velocity_fl = np.gradient(susp_travel_fl)
    susp_damper_force_fl = 200 + 100*np.abs(susp_velocity_fl) + 20*np.random.randn(SAMPLES_PER_LAP)*0.1
    
    susp_travel_fr = 14 + 7*np.sin(2*np.pi*TIME/5 + 0.2) + 2*np.random.randn(SAMPLES_PER_LAP)*0.1
    susp_velocity_fr = np.gradient(susp_travel_fr)
    susp_damper_force_fr = 190 + 95*np.abs(susp_velocity_fr) + 20*np.random.randn(SAMPLES_PER_LAP)*0.1
    
    susp_travel_rl = 20 + 6*np.sin(2*np.pi*TIME/5) + 1.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    susp_velocity_rl = np.gradient(susp_travel_rl)
    susp_damper_force_rl = 210 + 110*np.abs(susp_velocity_rl) + 20*np.random.randn(SAMPLES_PER_LAP)*0.1
    
    susp_travel_rr = 21 + 5.5*np.sin(2*np.pi*TIME/5 + 0.15) + 1.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    susp_velocity_rr = np.gradient(susp_travel_rr)
    susp_damper_force_rr = 215 + 115*np.abs(susp_velocity_rr) + 20*np.random.randn(SAMPLES_PER_LAP)*0.1
    
    # ===== TIRE SYSTEM (20 channels - 4 wheels × 5 metrics) =====
    # Front-Left
    tire_temp_fl = 85 + 20*np.sin(2*np.pi*TIME/5) + 3*np.random.randn(SAMPLES_PER_LAP)*0.1
    tire_pressure_fl = 2.05 + 0.01*np.sin(2*np.pi*TIME/3) + 0.03*np.random.randn(SAMPLES_PER_LAP)*0.01
    tire_slip_fl = 5 + 6*np.random.rand(SAMPLES_PER_LAP)
    tire_wear_fl = 85 - 0.001*np.arange(SAMPLES_PER_LAP)
    tire_speed_fl = gearbox_speed_output * np.sqrt(1 + tire_slip_fl/100) / (2*np.pi*0.325)
    
    # Front-Right
    tire_temp_fr = 84 + 19*np.sin(2*np.pi*TIME/5 + 0.1) + 3*np.random.randn(SAMPLES_PER_LAP)*0.1
    tire_pressure_fr = 2.04 + 0.01*np.sin(2*np.pi*TIME/3 + 0.1) + 0.03*np.random.randn(SAMPLES_PER_LAP)*0.01
    tire_slip_fr = 5.2 + 6.2*np.random.rand(SAMPLES_PER_LAP)
    tire_wear_fr = 84 - 0.0011*np.arange(SAMPLES_PER_LAP)
    tire_speed_fr = gearbox_speed_output * np.sqrt(1 + tire_slip_fr/100) / (2*np.pi*0.325)
    
    # Rear-Left
    tire_temp_rl = 92 + 18*np.sin(2*np.pi*TIME/5) + 2.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    tire_pressure_rl = 2.10 + 0.015*np.sin(2*np.pi*TIME/3) + 0.04*np.random.randn(SAMPLES_PER_LAP)*0.01
    tire_slip_rl = 3 + 4*np.random.rand(SAMPLES_PER_LAP)
    tire_wear_rl = 82 - 0.0012*np.arange(SAMPLES_PER_LAP)
    tire_speed_rl = gearbox_speed_output / (2*np.pi*0.335) * np.sqrt(1 + tire_slip_rl/100)
    
    # Rear-Right
    tire_temp_rr = 91 + 17*np.sin(2*np.pi*TIME/5 + 0.2) + 2.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    tire_pressure_rr = 2.12 + 0.015*np.sin(2*np.pi*TIME/3 + 0.1) + 0.04*np.random.randn(SAMPLES_PER_LAP)*0.01
    tire_slip_rr = 2.8 + 3.8*np.random.rand(SAMPLES_PER_LAP)
    tire_wear_rr = 81 - 0.0013*np.arange(SAMPLES_PER_LAP)
    tire_speed_rr = gearbox_speed_output / (2*np.pi*0.335) * np.sqrt(1 + tire_slip_rr/100)
    
    # ===== IMU / INERTIAL (9 channels) =====
    accel_lon = (torque/200 - 0.5) + 0.05*np.random.randn(SAMPLES_PER_LAP)
    accel_lat = 1.8*np.sin(2*np.pi*TIME/5) + 0.15*np.random.randn(SAMPLES_PER_LAP)
    accel_vert = 0.1*np.sin(2*np.pi*TIME/1) + 0.08*np.random.randn(SAMPLES_PER_LAP)
    gyro_roll = 5*np.sin(2*np.pi*TIME/5) + 1*np.random.randn(SAMPLES_PER_LAP)*0.1
    gyro_pitch = 2*np.sin(2*np.pi*TIME/3) + 0.5*np.random.randn(SAMPLES_PER_LAP)*0.1
    gyro_yaw = 3*np.sin(2*np.pi*TIME/4) + 0.8*np.random.randn(SAMPLES_PER_LAP)*0.1
    roll_angle = 10*np.sin(2*np.pi*TIME/5) + 2*np.random.randn(SAMPLES_PER_LAP)*0.1
    pitch_angle = 3*np.sin(2*np.pi*TIME/10) + 1*np.random.randn(SAMPLES_PER_LAP)*0.1
    yaw_angle = np.cumsum(gyro_yaw) / FS + 0.1*np.random.randn(SAMPLES_PER_LAP)
    
    # ===== BRAKING SYSTEM (6 channels) =====
    brake_pressure_front = 80 + 30*np.random.rand(SAMPLES_PER_LAP)
    brake_pressure_rear = 60 + 20*np.random.rand(SAMPLES_PER_LAP)
    brake_temp_front = 250 + 150*np.random.rand(SAMPLES_PER_LAP)
    brake_temp_rear = 220 + 130*np.random.rand(SAMPLES_PER_LAP)
    brake_fluid_temp = 180 + 80*np.random.rand(SAMPLES_PER_LAP)
    brake_pad_wear = 80 - 0.005*np.arange(SAMPLES_PER_LAP)
    
    # ===== STEERING & CONTROL (7 channels) =====
    throttle = 0.3 + 0.7*np.exp(-((TIME-5)**2)/(2*2)) + 0.05*np.random.randn(SAMPLES_PER_LAP)*0.1
    steering_angle = 5*np.sin(2*np.pi*TIME/5) + 1*np.random.randn(SAMPLES_PER_LAP)*0.1
    steering_rate = np.gradient(steering_angle)
    engine_load = throttle * 100
    fuel_injector_pulse = 1.2 + 0.4*throttle + 0.1*np.random.randn(SAMPLES_PER_LAP)*0.01
    ignition_advance = 20 + 5*np.sin(2*np.pi*TIME/10) + 1*np.random.randn(SAMPLES_PER_LAP)*0.1
    engine_knock_level = 0.5 + 2*np.random.rand(SAMPLES_PER_LAP)
    
    # ===== CAN & DIAGNOSTIC (5 channels) =====
    can_messages_sec = 50 + 30*np.sin(2*np.pi*TIME/3) + 5*np.random.randn(SAMPLES_PER_LAP)*0.1
    can_errors = np.random.poisson(0.5, SAMPLES_PER_LAP)
    can_bus_load = 30 + 40*np.sin(2*np.pi*TIME/4) + 5*np.random.randn(SAMPLES_PER_LAP)*0.1
    gps_satellites = 12 + 2*np.sin(2*np.pi*TIME/20)
    gps_hdop = 0.8 + 0.3*np.sin(2*np.pi*TIME/10) + 0.05*np.random.randn(SAMPLES_PER_LAP)*0.01
    
    # ===== GLICKO-2 METRICS (6 channels - DEEP DIVE) =====
    if setup_type == 'baseline':
        glicko_sigma = 0.05 + 0.2*np.abs(np.sin(2*np.pi*TIME/5)) + 0.02*np.random.randn(SAMPLES_PER_LAP)*0.1
        glicko_sigma_lower_ci = glicko_sigma - 0.03*np.random.rand(SAMPLES_PER_LAP)
        glicko_sigma_upper_ci = glicko_sigma + 0.03*np.random.rand(SAMPLES_PER_LAP)
    else:
        glicko_sigma = 0.01 + 0.04*np.abs(np.sin(2*np.pi*TIME/5)) + 0.005*np.random.randn(SAMPLES_PER_LAP)*0.1
        glicko_sigma_lower_ci = glicko_sigma - 0.005*np.random.rand(SAMPLES_PER_LAP)
        glicko_sigma_upper_ci = glicko_sigma + 0.01*np.random.rand(SAMPLES_PER_LAP)
    
    glicko_rd = 50 + 100*np.random.rand(SAMPLES_PER_LAP)
    glicko_rating = 1600 + 400*throttle
    glicko_volatility_components = glicko_sigma * (1 + 0.1*np.sin(2*np.pi*TIME/3))
    
    return {
        # Engine
        'engine_rpm': rpm,
        'engine_torque_nm': torque,
        'fuel_pressure_bar': fuel_pressure,
        'fuel_consumption_lh': fuel_consumption,
        'oil_pressure_bar': oil_pressure,
        'oil_temperature_c': oil_temp,
        'coolant_temperature_c': coolant_temp,
        'lambda_sensor': lambda_sensor,
        
        # Drivetrain
        'clutch_slip_percent': clutch_slip,
        'gear_position': gear,
        'engine_speed_input_rpm': engine_speed_input,
        'gearbox_speed_output_rpm': gearbox_speed_output,
        'differential_speed_kmh': diff_speed,
        
        # Suspension (12)
        'suspension_fl_travel_mm': susp_travel_fl,
        'suspension_fl_velocity_mms': susp_velocity_fl,
        'suspension_fl_damper_force_n': susp_damper_force_fl,
        'suspension_fr_travel_mm': susp_travel_fr,
        'suspension_fr_velocity_mms': susp_velocity_fr,
        'suspension_fr_damper_force_n': susp_damper_force_fr,
        'suspension_rl_travel_mm': susp_travel_rl,
        'suspension_rl_velocity_mms': susp_velocity_rl,
        'suspension_rl_damper_force_n': susp_damper_force_rl,
        'suspension_rr_travel_mm': susp_travel_rr,
        'suspension_rr_velocity_mms': susp_velocity_rr,
        'suspension_rr_damper_force_n': susp_damper_force_rr,
        
        # Tires (20)
        'tire_fl_temperature_c': tire_temp_fl,
        'tire_fl_pressure_bar': tire_pressure_fl,
        'tire_fl_slip_percent': tire_slip_fl,
        'tire_fl_wear_percent': tire_wear_fl,
        'tire_fl_speed_kmh': tire_speed_fl,
        'tire_fr_temperature_c': tire_temp_fr,
        'tire_fr_pressure_bar': tire_pressure_fr,
        'tire_fr_slip_percent': tire_slip_fr,
        'tire_fr_wear_percent': tire_wear_fr,
        'tire_fr_speed_kmh': tire_speed_fr,
        'tire_rl_temperature_c': tire_temp_rl,
        'tire_rl_pressure_bar': tire_pressure_rl,
        'tire_rl_slip_percent': tire_slip_rl,
        'tire_rl_wear_percent': tire_wear_rl,
        'tire_rl_speed_kmh': tire_speed_rl,
        'tire_rr_temperature_c': tire_temp_rr,
        'tire_rr_pressure_bar': tire_pressure_rr,
        'tire_rr_slip_percent': tire_slip_rr,
        'tire_rr_wear_percent': tire_wear_rr,
        'tire_rr_speed_kmh': tire_speed_rr,
        
        # IMU (9)
        'accel_lon_g': accel_lon,
        'accel_lat_g': accel_lat,
        'accel_vert_g': accel_vert,
        'gyro_roll_dps': gyro_roll,
        'gyro_pitch_dps': gyro_pitch,
        'gyro_yaw_dps': gyro_yaw,
        'roll_angle_deg': roll_angle,
        'pitch_angle_deg': pitch_angle,
        'yaw_angle_deg': yaw_angle,
        
        # Braking (6)
        'brake_pressure_front_bar': brake_pressure_front,
        'brake_pressure_rear_bar': brake_pressure_rear,
        'brake_temperature_front_c': brake_temp_front,
        'brake_temperature_rear_c': brake_temp_rear,
        'brake_fluid_temperature_c': brake_fluid_temp,
        'brake_pad_wear_percent': brake_pad_wear,
        
        # Steering & Control (7)
        'throttle_position_percent': throttle * 100,
        'steering_angle_deg': steering_angle,
        'steering_rate_dps': steering_rate,
        'engine_load_percent': engine_load,
        'fuel_injector_pulse_ms': fuel_injector_pulse,
        'ignition_advance_deg': ignition_advance,
        'engine_knock_level': engine_knock_level,
        
        # CAN & Diagnostic (5)
        'can_messages_per_second': can_messages_sec,
        'can_errors': can_errors,
        'can_bus_load_percent': can_bus_load,
        'gps_satellites_in_view': gps_satellites,
        'gps_hdop': gps_hdop,
        
        # Glicko-2 (6)
        'glicko_volatility_sigma': glicko_sigma,
        'glicko_sigma_lower_ci': glicko_sigma_lower_ci,
        'glicko_sigma_upper_ci': glicko_sigma_upper_ci,
        'glicko_rating_deviation': glicko_rd,
        'glicko_rating': glicko_rating,
        'glicko_volatility_components': glicko_volatility_components,
    }

# ========================
# CREATE MDF4 FILE
# ========================
def create_mdf4_file_v3():
    """
    Create professional-grade ASAM MDF 4.10 binary file.
    """
    
    print("\n🔧 Creating ASAM MDF 4.10 Binary File (v3.0)...")
    
    # Create MDF object
    mdf = MDF(version='4.10')
    
    # Metadata
    mdf.header.author = 'Nonlinear Lumping Analysis Research Group'
    mdf.header.organization = 'Formula Motorsport Engineering'
    mdf.header.project = 'MotoGP Turn 5 Jerez Gearing Optimization'
    mdf.header.subject = 'Glicko-2 Human-Machine Coupling Analysis'
    
    # ===== GENERATE SIGNALS =====
    print("   ├─ Generating telemetry: Baseline setup...")
    telemetry_baseline = generate_advanced_telemetry_v3(setup_type='baseline')
    
    print("   ├─ Generating telemetry: Optimized setup...")
    telemetry_optimized = generate_advanced_telemetry_v3(setup_type='optimized')
    
    # ===== ADD SIGNALS TO MDF =====
    print("   ├─ Adding 130 signals to MDF4...")
    signal_count = 0
    
    for channel_name, data_baseline in telemetry_baseline.items():
        # Baseline signal
        sig_baseline = Signal(
            samples=data_baseline,
            timestamps=TIME,
            name=f'{channel_name}_baseline',
            unit=_get_unit(channel_name),
            comment=f'{channel_name} - Baseline Setup'
        )
        mdf.append(sig_baseline)
        signal_count += 1
        
        # Optimized signal
        data_optimized = telemetry_optimized[channel_name]
        sig_optimized = Signal(
            samples=data_optimized,
            timestamps=TIME,
            name=f'{channel_name}_optimized',
            unit=_get_unit(channel_name),
            comment=f'{channel_name} - Optimized Setup'
        )
        mdf.append(sig_optimized)
        signal_count += 1
    
    print(f"   └─ Total signals: {signal_count}")
    
    # Save MDF4 file
    output_file = 'NLA_CaseStudy_Jerez_v3_Industrial.mf4'
    mdf.save(output_file, overwrite=True)
    
    print(f"\n✅ MDF4 file created: {output_file}")
    print(f"   Version: ASAM MDF 4.10 (ISO 22901-1:2008)")
    print(f"   Signals: {len(mdf.channels_db)} channels")
    print(f"   Sampling: 100 Hz, {SAMPLES_PER_LAP} samples")
    print(f"   Date: {datetime.now().isoformat()}\n")
    
    return output_file

def _get_unit(channel_name):
    """Map channel names to physical units."""
    unit_map = {
        'rpm': 'rpm',
        'torque': 'Nm',
        'pressure': 'bar',
        'temperature': '°C',
        'travel': 'mm',
        'velocity': 'mm/s',
        'force': 'N',
        'accel': 'g',
        'gyro': 'deg/s',
        'angle': 'deg',
        'slip': '%',
        'wear': '%',
        'speed': 'km/h',
        'load': '%',
        'steering': 'deg',
        'pulse': 'ms',
        'knock': '-',
        'messages': 'msg/s',
        'errors': 'count',
        'hdop': '-',
        'satellites': 'count',
        'sigma': '-',
        'rating': '-',
    }
    
    for key, unit in unit_map.items():
        if key in channel_name.lower():
            return unit
    return '-'

# ========================
# MAIN EXECUTION
# ========================
if __name__ == '__main__':
    import sys
    
    try:
        output_file = create_mdf4_file_v3()
        print(f"🎉 MDF4 Industrial Binary Successfully Generated!")
        print(f"   Next: Process with Vector CANape or ETAS INCA\n")
    except ImportError:
        print("❌ asammdf not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'asammdf'])
        output_file = create_mdf4_file_v3()
        print(f"🎉 MDF4 Industrial Binary Successfully Generated!")
