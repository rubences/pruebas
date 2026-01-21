#!/usr/bin/env python3
"""
Motor Physics and Glicko Rating System Simulator

This script simulates:
1. Motor physics (torque, RPM, power)
2. Glicko rating system for competitive scenarios
3. Generates CSV and optionally MF4 binary output files
"""

import math
import csv
from typing import List, Dict, Tuple

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: numpy not available. Using basic Python for calculations.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available. Using basic CSV for output.")

try:
    from asammdf import MDF, Signal
    ASAMMDF_AVAILABLE = True
except ImportError:
    ASAMMDF_AVAILABLE = False
    print("Warning: asammdf not available. MF4 output will be skipped.")


class MotorPhysicsSimulator:
    """Simulates motor physics including torque, RPM, and power."""
    
    def __init__(self, max_rpm: float = 6000, max_torque: float = 250):
        """
        Initialize motor simulator.
        
        Args:
            max_rpm: Maximum RPM of the motor
            max_torque: Maximum torque in Nm
        """
        self.max_rpm = max_rpm
        self.max_torque = max_torque
        
    def calculate_torque(self, rpm: float) -> float:
        """
        Calculate torque based on RPM using a realistic torque curve.
        
        Args:
            rpm: Current RPM
            
        Returns:
            Torque in Nm
        """
        if rpm < 0 or rpm > self.max_rpm:
            return 0.0
        
        # Simulate a realistic torque curve with peak around 3000-4000 RPM
        normalized_rpm = rpm / self.max_rpm
        torque = self.max_torque * (
            0.3 + 0.7 * math.sin(normalized_rpm * math.pi) * 
            math.exp(-((normalized_rpm - 0.5) ** 2) / 0.3)
        )
        return max(0.0, torque)
    
    def calculate_power(self, torque: float, rpm: float) -> float:
        """
        Calculate power in kW from torque and RPM.
        
        Args:
            torque: Torque in Nm
            rpm: RPM
            
        Returns:
            Power in kW
        """
        # Power (kW) = Torque (Nm) × RPM / 9549
        if rpm <= 0:
            return 0.0
        return (torque * rpm) / 9549.0
    
    def simulate_acceleration(self, duration: float = 10.0, time_step: float = 0.1) -> List[Dict]:
        """
        Simulate motor acceleration from idle to max RPM.
        
        Args:
            duration: Total simulation time in seconds
            time_step: Time step for simulation in seconds
            
        Returns:
            List of simulation data points
        """
        data = []
        time = 0.0
        rpm = 0.0
        
        while time <= duration:
            # Simulate acceleration with exponential approach to max RPM
            rpm = self.max_rpm * (1 - math.exp(-time / 3.0))
            torque = self.calculate_torque(rpm)
            power = self.calculate_power(torque, rpm)
            
            data.append({
                'time': round(time, 2),
                'rpm': round(rpm, 2),
                'torque': round(torque, 2),
                'power_kw': round(power, 2)
            })
            
            time += time_step
        
        return data


class GlickoRatingSystem:
    """
    Implements the Glicko rating system for competitive scenarios.
    
    The Glicko rating system is used in competitive gaming and sports
    to rate player skill levels.
    """
    
    # System constants
    Q = math.log(10) / 400
    MIN_RD = 30  # Minimum rating deviation
    MAX_RD = 350  # Maximum rating deviation
    C_SQUARED = (350 ** 2 - 30 ** 2) / 365  # Rating deviation increase per day
    
    def __init__(self, initial_rating: float = 1500, initial_rd: float = 350):
        """
        Initialize Glicko rating system.
        
        Args:
            initial_rating: Initial rating value
            initial_rd: Initial rating deviation
        """
        self.initial_rating = initial_rating
        self.initial_rd = initial_rd
    
    def g_function(self, rd: float) -> float:
        """
        Calculate g(RD) function used in Glicko calculations.
        
        Args:
            rd: Rating deviation
            
        Returns:
            g(RD) value
        """
        return 1 / math.sqrt(1 + 3 * (self.Q ** 2) * (rd ** 2) / (math.pi ** 2))
    
    def expected_score(self, rating: float, opponent_rating: float, opponent_rd: float) -> float:
        """
        Calculate expected score against an opponent.
        
        Args:
            rating: Player's rating
            opponent_rating: Opponent's rating
            opponent_rd: Opponent's rating deviation
            
        Returns:
            Expected score (0 to 1)
        """
        g_rd = self.g_function(opponent_rd)
        exponent = -g_rd * (rating - opponent_rating) / 400
        return 1 / (1 + math.pow(10, exponent))
    
    def update_rating(self, rating: float, rd: float, opponents: List[Tuple[float, float, float]]) -> Tuple[float, float]:
        """
        Update rating based on match results.
        
        Args:
            rating: Current rating
            rd: Current rating deviation
            opponents: List of (opponent_rating, opponent_rd, score) tuples
                      where score is 1 for win, 0.5 for draw, 0 for loss
            
        Returns:
            Tuple of (new_rating, new_rd)
        """
        if not opponents:
            return rating, rd
        
        # Calculate d^2
        d_squared_inv = 0
        for opp_rating, opp_rd, _ in opponents:
            g_rd = self.g_function(opp_rd)
            e_score = self.expected_score(rating, opp_rating, opp_rd)
            d_squared_inv += (g_rd ** 2) * e_score * (1 - e_score)
        
        d_squared_inv *= (self.Q ** 2)
        
        if d_squared_inv == 0:
            return rating, rd
        
        d_squared = 1 / d_squared_inv
        
        # Calculate new RD
        new_rd_squared = 1 / ((1 / (rd ** 2)) + (1 / d_squared))
        new_rd = math.sqrt(new_rd_squared)
        
        # Calculate rating change
        rating_change = 0
        for opp_rating, opp_rd, score in opponents:
            g_rd = self.g_function(opp_rd)
            e_score = self.expected_score(rating, opp_rating, opp_rd)
            rating_change += g_rd * (score - e_score)
        
        rating_change *= (self.Q / ((1 / (rd ** 2)) + (1 / d_squared)))
        new_rating = rating + rating_change
        
        return new_rating, max(self.MIN_RD, new_rd)
    
    def simulate_matches(self, num_players: int = 10, num_rounds: int = 20) -> List[Dict]:
        """
        Simulate a series of competitive matches.
        
        Args:
            num_players: Number of players in the simulation
            num_rounds: Number of match rounds to simulate
            
        Returns:
            List of rating history data
        """
        # Initialize players
        players = []
        for i in range(num_players):
            players.append({
                'id': i,
                'name': f'Player_{i}',
                'rating': self.initial_rating,
                'rd': self.initial_rd,
                'wins': 0,
                'losses': 0,
                'draws': 0
            })
        
        history = []
        
        for round_num in range(num_rounds):
            # Shuffle and pair players
            if NUMPY_AVAILABLE:
                indices = np.random.permutation(num_players)
            else:
                import random
                indices = list(range(num_players))
                random.shuffle(indices)
            
            # Process matches in pairs
            for i in range(0, num_players - 1, 2):
                player1_idx = indices[i]
                player2_idx = indices[i + 1]
                
                player1 = players[player1_idx]
                player2 = players[player2_idx]
                
                # Calculate expected scores
                expected1 = self.expected_score(player1['rating'], player2['rating'], player2['rd'])
                
                # Simulate match result based on expected scores
                if NUMPY_AVAILABLE:
                    rand = np.random.random()
                else:
                    import random
                    rand = random.random()
                
                if rand < expected1 - 0.1:
                    # Player 1 wins
                    score1, score2 = 1.0, 0.0
                    player1['wins'] += 1
                    player2['losses'] += 1
                elif rand > expected1 + 0.1:
                    # Player 2 wins
                    score1, score2 = 0.0, 1.0
                    player1['losses'] += 1
                    player2['wins'] += 1
                else:
                    # Draw
                    score1, score2 = 0.5, 0.5
                    player1['draws'] += 1
                    player2['draws'] += 1
                
                # Update ratings
                new_rating1, new_rd1 = self.update_rating(
                    player1['rating'], player1['rd'],
                    [(player2['rating'], player2['rd'], score1)]
                )
                new_rating2, new_rd2 = self.update_rating(
                    player2['rating'], player2['rd'],
                    [(player1['rating'], player1['rd'], score2)]
                )
                
                # Record history before update
                history.append({
                    'round': round_num + 1,
                    'player_id': player1['id'],
                    'player_name': player1['name'],
                    'rating': round(player1['rating'], 2),
                    'rd': round(player1['rd'], 2),
                    'opponent_id': player2['id'],
                    'score': score1,
                    'wins': player1['wins'],
                    'losses': player1['losses'],
                    'draws': player1['draws']
                })
                
                history.append({
                    'round': round_num + 1,
                    'player_id': player2['id'],
                    'player_name': player2['name'],
                    'rating': round(player2['rating'], 2),
                    'rd': round(player2['rd'], 2),
                    'opponent_id': player1['id'],
                    'score': score2,
                    'wins': player2['wins'],
                    'losses': player2['losses'],
                    'draws': player2['draws']
                })
                
                # Update ratings
                player1['rating'] = new_rating1
                player1['rd'] = new_rd1
                player2['rating'] = new_rating2
                player2['rd'] = new_rd2
        
        return history


def write_csv(filename: str, data: List[Dict], fieldnames: List[str] = None):
    """
    Write data to CSV file.
    
    Args:
        filename: Output filename
        data: List of dictionaries containing data
        fieldnames: Optional list of field names (keys to include)
    """
    if not data:
        print(f"Warning: No data to write to {filename}")
        return
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"CSV data written to {filename}")


def write_mf4(filename: str, motor_data: List[Dict], glicko_data: List[Dict]):
    """
    Write data to MF4 binary format using asammdf.
    
    Args:
        filename: Output filename
        motor_data: Motor simulation data
        glicko_data: Glicko rating data
    """
    if not ASAMMDF_AVAILABLE:
        print("MF4 output skipped: asammdf library not available")
        return
    
    try:
        signals = []
        
        # Add motor physics signals
        if motor_data and NUMPY_AVAILABLE:
            time_array = np.array([d['time'] for d in motor_data])
            rpm_array = np.array([d['rpm'] for d in motor_data])
            torque_array = np.array([d['torque'] for d in motor_data])
            power_array = np.array([d['power_kw'] for d in motor_data])
            
            signals.append(Signal(samples=rpm_array, timestamps=time_array, name='RPM', unit='rpm'))
            signals.append(Signal(samples=torque_array, timestamps=time_array, name='Torque', unit='Nm'))
            signals.append(Signal(samples=power_array, timestamps=time_array, name='Power', unit='kW'))
        
        # Create MF4 file
        mdf = MDF()
        for signal in signals:
            mdf.append(signal)
        
        mdf.save(filename)
        print(f"MF4 binary data written to {filename}")
    except Exception as e:
        print(f"Error writing MF4 file: {e}")


def main():
    """Main function to run simulations and generate output files."""
    print("=" * 60)
    print("Motor Physics and Glicko Rating System Simulator")
    print("=" * 60)
    print()
    
    # Initialize simulators
    print("Initializing motor physics simulator...")
    motor_sim = MotorPhysicsSimulator(max_rpm=6000, max_torque=250)
    
    print("Initializing Glicko rating system...")
    glicko_sim = GlickoRatingSystem(initial_rating=1500, initial_rd=350)
    
    # Run motor physics simulation
    print("\nRunning motor physics simulation...")
    time_step = 0.1
    motor_data = motor_sim.simulate_acceleration(duration=10.0, time_step=time_step)
    print(f"Generated {len(motor_data)} motor physics data points")
    
    # Run Glicko rating simulation
    print("\nRunning Glicko rating simulation...")
    glicko_data = glicko_sim.simulate_matches(num_players=10, num_rounds=20)
    print(f"Generated {len(glicko_data)} Glicko rating data points")
    
    # Generate CSV outputs
    print("\nGenerating CSV output files...")
    write_csv('motor_physics_data.csv', motor_data)
    write_csv('glicko_ratings_data.csv', glicko_data)
    
    # Generate combined CSV with sample data
    print("\nGenerating sample combined data CSV...")
    sample_data = []
    for i, motor_point in enumerate(motor_data[:10]):  # First 10 points
        sample_data.append({
            'timestamp': i * time_step,
            'data_type': 'motor_physics',
            'value1': motor_point['rpm'],
            'value2': motor_point['torque'],
            'value3': motor_point['power_kw'],
            'label1': 'RPM',
            'label2': 'Torque(Nm)',
            'label3': 'Power(kW)'
        })
    
    for i, glicko_point in enumerate(glicko_data[:10]):  # First 10 points
        sample_data.append({
            'timestamp': i,
            'data_type': 'glicko_rating',
            'value1': glicko_point['rating'],
            'value2': glicko_point['rd'],
            'value3': glicko_point['score'],
            'label1': 'Rating',
            'label2': 'RD',
            'label3': 'Score'
        })
    
    write_csv('sample_data.csv', sample_data)
    
    # Generate MF4 output if available
    if ASAMMDF_AVAILABLE and NUMPY_AVAILABLE:
        print("\nGenerating MF4 binary output...")
        write_mf4('simulation_data.mf4', motor_data, glicko_data)
    else:
        print("\nMF4 output skipped (requires asammdf and numpy libraries)")
    
    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - motor_physics_data.csv")
    print("  - glicko_ratings_data.csv")
    print("  - sample_data.csv")
    if ASAMMDF_AVAILABLE and NUMPY_AVAILABLE:
        print("  - simulation_data.mf4")
    print()


if __name__ == "__main__":
    main()
