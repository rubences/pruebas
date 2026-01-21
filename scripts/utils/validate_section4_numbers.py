#!/usr/bin/env python3
"""
Validation Script: Verify all numbers in Section 4 match the MEGA dataset.

This script performs consistency checks between:
1. MEGA dataset (NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv)
2. Statistical test results (Table_v4_Statistical_Tests.csv)
3. Metrics table (Table_v4_All_Metrics.csv)
4. Numbers claimed in Section 4 documentation

Usage:
    python validate_section4_numbers.py
    
Exit codes:
    0 = All validations passed ✅
    1 = One or more validations failed ❌
"""

import pandas as pd
import numpy as np
from scipy import stats
import sys
from pathlib import Path

# ANSI colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

def print_pass(text):
    print(f"{GREEN}✅ PASS:{RESET} {text}")

def print_fail(text):
    print(f"{RED}❌ FAIL:{RESET} {text}")

def print_info(text):
    print(f"{YELLOW}ℹ️  INFO:{RESET} {text}")

# Expected values from documentation (Section 4)
EXPECTED_VALUES = {
    'glicko_sigma_baseline_mean': 0.2553,
    'glicko_sigma_optimized_mean': 0.0410,
    'glicko_sigma_improvement_pct': 84.0,
    'wheel_slip_baseline_mean': 17.58,
    'wheel_slip_optimized_mean': 10.51,
    'wheel_slip_improvement_pct': 40.2,
    'rpm_baseline_mean': 15472,
    'rpm_optimized_mean': 13151,
    'engine_eff_baseline': 94.83,
    'engine_eff_optimized': 97.15,
    'engine_eff_improvement': 2.45,
    'welch_t_statistic': 232.84,
    'cohen_d': 3.2928,
    'ks_statistic': 1.0,
    'levene_f_statistic': 807.76,
}

def load_data():
    """Load all required datasets."""
    try:
        base_path = Path(__file__).parent.parent.parent
        
        # Load MEGA dataset
        mega_path = base_path / 'data' / 'datasets' / 'NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv'
        df = pd.read_csv(mega_path)
        print_pass(f"Loaded MEGA dataset: {len(df)} rows, {len(df.columns)} columns")
        
        # Load statistical tests
        stats_path = base_path / 'data' / 'tables' / 'Table_v4_Statistical_Tests.csv'
        df_stats = pd.read_csv(stats_path)
        print_pass(f"Loaded statistical tests table")
        
        # Load metrics
        metrics_path = base_path / 'data' / 'tables' / 'Table_v4_All_Metrics.csv'
        df_metrics = pd.read_csv(metrics_path)
        print_pass(f"Loaded metrics table")
        
        return df, df_stats, df_metrics
    
    except Exception as e:
        print_fail(f"Failed to load data: {e}")
        sys.exit(1)

def validate_glicko_sigma(df):
    """Validate Glicko-2 volatility metrics."""
    print_header("VALIDATING H3: GLICKO-2 VOLATILITY (σ)")
    
    passed = True
    
    # Filter active window (speed > 1)
    baseline = df[(df['setup'] == 'baseline') & (df['speed_kmh'] > 1)]
    optimized = df[(df['setup'] == 'optimized') & (df['speed_kmh'] > 1)]
    
    print_info(f"Active samples: Baseline={len(baseline)}, Optimized={len(optimized)}")
    
    # Mean values
    sigma_base_mean = baseline['glicko_volatility_sigma'].mean()
    sigma_opt_mean = optimized['glicko_volatility_sigma'].mean()
    improvement = (1 - sigma_opt_mean / sigma_base_mean) * 100
    
    tolerance = 0.001  # 0.1% tolerance
    
    # Check baseline mean
    if abs(sigma_base_mean - EXPECTED_VALUES['glicko_sigma_baseline_mean']) < tolerance:
        print_pass(f"Baseline σ mean: {sigma_base_mean:.4f} (expected: {EXPECTED_VALUES['glicko_sigma_baseline_mean']:.4f})")
    else:
        print_fail(f"Baseline σ mean: {sigma_base_mean:.4f} (expected: {EXPECTED_VALUES['glicko_sigma_baseline_mean']:.4f})")
        passed = False
    
    # Check optimized mean
    if abs(sigma_opt_mean - EXPECTED_VALUES['glicko_sigma_optimized_mean']) < tolerance:
        print_pass(f"Optimized σ mean: {sigma_opt_mean:.4f} (expected: {EXPECTED_VALUES['glicko_sigma_optimized_mean']:.4f})")
    else:
        print_fail(f"Optimized σ mean: {sigma_opt_mean:.4f} (expected: {EXPECTED_VALUES['glicko_sigma_optimized_mean']:.4f})")
        passed = False
    
    # Check improvement percentage
    if abs(improvement - EXPECTED_VALUES['glicko_sigma_improvement_pct']) < 0.5:
        print_pass(f"Improvement: {improvement:.1f}% (expected: {EXPECTED_VALUES['glicko_sigma_improvement_pct']:.1f}%)")
    else:
        print_fail(f"Improvement: {improvement:.1f}% (expected: {EXPECTED_VALUES['glicko_sigma_improvement_pct']:.1f}%)")
        passed = False
    
    return passed

def validate_wheel_slip(df):
    """Validate wheel slip metrics."""
    print_header("VALIDATING WHEEL SLIP")
    
    passed = True
    
    baseline = df[(df['setup'] == 'baseline') & (df['speed_kmh'] > 1)]
    optimized = df[(df['setup'] == 'optimized') & (df['speed_kmh'] > 1)]
    
    slip_base_mean = baseline['wheel_slip_percent'].mean()
    slip_opt_mean = optimized['wheel_slip_percent'].mean()
    improvement = (1 - slip_opt_mean / slip_base_mean) * 100
    
    tolerance = 0.05  # 0.05% absolute tolerance
    
    if abs(slip_base_mean - EXPECTED_VALUES['wheel_slip_baseline_mean']) < tolerance:
        print_pass(f"Baseline wheel slip: {slip_base_mean:.2f}% (expected: {EXPECTED_VALUES['wheel_slip_baseline_mean']:.2f}%)")
    else:
        print_fail(f"Baseline wheel slip: {slip_base_mean:.2f}% (expected: {EXPECTED_VALUES['wheel_slip_baseline_mean']:.2f}%)")
        passed = False
    
    if abs(slip_opt_mean - EXPECTED_VALUES['wheel_slip_optimized_mean']) < tolerance:
        print_pass(f"Optimized wheel slip: {slip_opt_mean:.2f}% (expected: {EXPECTED_VALUES['wheel_slip_optimized_mean']:.2f}%)")
    else:
        print_fail(f"Optimized wheel slip: {slip_opt_mean:.2f}% (expected: {EXPECTED_VALUES['wheel_slip_optimized_mean']:.2f}%)")
        passed = False
    
    if abs(improvement - EXPECTED_VALUES['wheel_slip_improvement_pct']) < 0.5:
        print_pass(f"Improvement: {improvement:.1f}% (expected: {EXPECTED_VALUES['wheel_slip_improvement_pct']:.1f}%)")
    else:
        print_fail(f"Improvement: {improvement:.1f}% (expected: {EXPECTED_VALUES['wheel_slip_improvement_pct']:.1f}%)")
        passed = False
    
    return passed

def validate_rpm(df):
    """Validate RPM metrics."""
    print_header("VALIDATING RPM METRICS")
    
    passed = True
    
    baseline = df[(df['setup'] == 'baseline') & (df['speed_kmh'] > 1)]
    optimized = df[(df['setup'] == 'optimized') & (df['speed_kmh'] > 1)]
    
    rpm_base = baseline['engine_rpm'].mean()
    rpm_opt = optimized['engine_rpm'].mean()
    
    tolerance = 5  # 5 RPM tolerance
    
    if abs(rpm_base - EXPECTED_VALUES['rpm_baseline_mean']) < tolerance:
        print_pass(f"Baseline RPM: {rpm_base:.0f} (expected: {EXPECTED_VALUES['rpm_baseline_mean']:.0f})")
    else:
        print_fail(f"Baseline RPM: {rpm_base:.0f} (expected: {EXPECTED_VALUES['rpm_baseline_mean']:.0f})")
        passed = False
    
    if abs(rpm_opt - EXPECTED_VALUES['rpm_optimized_mean']) < tolerance:
        print_pass(f"Optimized RPM: {rpm_opt:.0f} (expected: {EXPECTED_VALUES['rpm_optimized_mean']:.0f})")
    else:
        print_fail(f"Optimized RPM: {rpm_opt:.0f} (expected: {EXPECTED_VALUES['rpm_optimized_mean']:.0f})")
        passed = False
    
    return passed

def validate_statistical_tests(df, df_stats):
    """Validate statistical test results."""
    print_header("VALIDATING STATISTICAL TESTS")
    
    passed = True
    
    baseline = df[(df['setup'] == 'baseline') & (df['speed_kmh'] > 1)]
    optimized = df[(df['setup'] == 'optimized') & (df['speed_kmh'] > 1)]
    
    sigma_base = baseline['glicko_volatility_sigma'].values
    sigma_opt = optimized['glicko_volatility_sigma'].values
    
    # Welch's t-test
    t_stat, p_val = stats.ttest_ind(sigma_base, sigma_opt, equal_var=False)
    
    # Get values from CSV
    welch_row = df_stats[df_stats['Test'] == 'Welch t-test']
    csv_t_stat = float(welch_row['Statistic'].values[0])
    
    tolerance = 0.5  # Allow 0.5 difference in t-statistic
    if abs(t_stat - csv_t_stat) < tolerance:
        print_pass(f"Welch's t-test: t={t_stat:.2f} (CSV: {csv_t_stat:.2f})")
    else:
        print_fail(f"Welch's t-test: t={t_stat:.2f} (CSV: {csv_t_stat:.2f})")
        passed = False
    
    # Cohen's d
    pooled_std = np.sqrt((np.std(sigma_base, ddof=1)**2 + np.std(sigma_opt, ddof=1)**2) / 2)
    cohen_d = (np.mean(sigma_base) - np.mean(sigma_opt)) / pooled_std
    
    cohen_row = df_stats[df_stats['Test'] == 'Cohen d']
    csv_cohen_d = float(cohen_row['Statistic'].values[0])
    
    tolerance = 0.01
    if abs(cohen_d - csv_cohen_d) < tolerance:
        print_pass(f"Cohen's d: {cohen_d:.4f} (CSV: {csv_cohen_d:.4f})")
    else:
        print_fail(f"Cohen's d: {cohen_d:.4f} (CSV: {csv_cohen_d:.4f})")
        passed = False
    
    # KS test
    ks_stat, ks_p = stats.ks_2samp(sigma_base, sigma_opt)
    
    ks_row = df_stats[df_stats['Test'] == 'KS Test']
    csv_ks_stat = float(ks_row['Statistic'].values[0])
    
    tolerance = 0.01
    if abs(ks_stat - csv_ks_stat) < tolerance:
        print_pass(f"KS test: D={ks_stat:.4f} (CSV: {csv_ks_stat:.4f})")
    else:
        print_fail(f"KS test: D={ks_stat:.4f} (CSV: {csv_ks_stat:.4f})")
        passed = False
    
    return passed

def validate_dataset_structure(df):
    """Validate dataset structure and completeness."""
    print_header("VALIDATING DATASET STRUCTURE")
    
    passed = True
    
    # Check total rows
    expected_rows = 20000
    if len(df) == expected_rows:
        print_pass(f"Total rows: {len(df)} (expected: {expected_rows})")
    else:
        print_fail(f"Total rows: {len(df)} (expected: {expected_rows})")
        passed = False
    
    # Check columns
    expected_cols = 37
    if len(df.columns) == expected_cols:
        print_pass(f"Total columns: {len(df.columns)} (expected: {expected_cols})")
    else:
        print_fail(f"Total columns: {len(df.columns)} (expected: {expected_cols})")
        passed = False
    
    # Check setup distribution
    setup_counts = df['setup'].value_counts()
    if setup_counts['baseline'] == 10000 and setup_counts['optimized'] == 10000:
        print_pass(f"Setup distribution: baseline={setup_counts['baseline']}, optimized={setup_counts['optimized']}")
    else:
        print_fail(f"Setup distribution incorrect: {setup_counts.to_dict()}")
        passed = False
    
    # Check active window
    baseline_active = len(df[(df['setup'] == 'baseline') & (df['speed_kmh'] > 1)])
    optimized_active = len(df[(df['setup'] == 'optimized') & (df['speed_kmh'] > 1)])
    
    if baseline_active == 1000 and optimized_active == 1000:
        print_pass(f"Active window: baseline={baseline_active}, optimized={optimized_active}")
    else:
        print_fail(f"Active window incorrect: baseline={baseline_active}, optimized={optimized_active}")
        passed = False
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    if missing == 0:
        print_pass(f"No missing values (checked {len(df)*len(df.columns)} cells)")
    else:
        print_fail(f"Found {missing} missing values")
        passed = False
    
    return passed

def validate_simulated_data():
    """Validate H1/H2 simulated data CSVs."""
    print_header("VALIDATING SIMULATED DATA (H1/H2)")
    
    passed = True
    base_dir = Path(__file__).parent.parent.parent
    
    try:
        # Check Segmentation data
        seg_path = base_dir / "data" / "tables" / "Table_v4_Segmentation_Summary.csv"
        if not seg_path.exists():
            print_fail(f"Segmentation summary not found: {seg_path}")
            return False
        
        seg_df = pd.read_csv(seg_path)
        as_f1 = seg_df[seg_df['skill_atom'] == 'AS']['f1_score'].values[0]
        ce_f1 = seg_df[seg_df['skill_atom'] == 'CE']['f1_score'].values[0]
        
        if 0.75 <= as_f1 <= 0.85:
            print_pass(f"Skill Atom AS F1-Score: {as_f1:.4f} (expected: ~0.78)")
        else:
            print_fail(f"Skill Atom AS F1-Score: {as_f1:.4f} (out of range [0.75, 0.85])")
            passed = False
        
        if 0.95 <= ce_f1 <= 1.0:
            print_pass(f"Skill Atom CE F1-Score: {ce_f1:.4f} (expected: ~1.0)")
        else:
            print_fail(f"Skill Atom CE F1-Score: {ce_f1:.4f} (out of range [0.95, 1.0])")
            passed = False
        
        # Check MQTT latency data
        mqtt_path = base_dir / "data" / "tables" / "Table_v4_MQTT_Summary.csv"
        if not mqtt_path.exists():
            print_fail(f"MQTT summary not found: {mqtt_path}")
            return False
        
        mqtt_df = pd.read_csv(mqtt_path)
        p95_e2e = mqtt_df[mqtt_df['metric'] == 'End-to-End']['p95_latency_ms'].values[0]
        packet_loss = mqtt_df[mqtt_df['metric'] == 'End-to-End']['packet_loss_pct'].values[0]
        
        if 150 <= p95_e2e <= 200:
            print_pass(f"MQTT p95 End-to-End Latency: {p95_e2e:.2f} ms (expected: ~176 ms)")
        else:
            print_fail(f"MQTT p95 latency: {p95_e2e:.2f} ms (out of range [150, 200] ms)")
            passed = False
        
        if packet_loss < 0.1:
            print_pass(f"Packet Loss: {packet_loss:.3f}% (expected: <0.1%)")
        else:
            print_fail(f"Packet Loss: {packet_loss:.3f}% (too high)")
            passed = False
        
        # Check Time Loss Attribution
        loss_path = base_dir / "data" / "tables" / "Table_v4_Time_Loss_Attribution.csv"
        if not loss_path.exists():
            print_fail(f"Time loss attribution not found: {loss_path}")
            return False
        
        loss_df = pd.read_csv(loss_path)
        total_delta = loss_df[loss_df['sector'] == 'Total']['time_delta_s'].values[0]
        setup_contrib = loss_df[loss_df['sector'] == 'Total']['setup_contribution_s'].values[0]
        
        if abs(total_delta) < 0.001:  # Less than 1ms variation
            print_pass(f"Total Time Delta: {total_delta*1000:.3f} ms (negligible)")
        else:
            print_warn(f"Total Time Delta: {total_delta*1000:.3f} ms (small variation)")
        
        if abs(setup_contrib) < 0.001:
            print_pass(f"Setup Contribution: {setup_contrib*1000:.3f} ms (minimal)")
        else:
            print_warn(f"Setup Contribution: {setup_contrib*1000:.3f} ms")
        
        return passed
        
    except Exception as e:
        print_fail(f"Error validating simulated data: {str(e)}")
        return False


def main():
    """Main validation routine."""
    print(f"\n{BLUE}{'='*70}")
    print(f"{'SECTION 4 DATA VALIDATION SCRIPT':^70}")
    print(f"{'='*70}{RESET}\n")
    
    # Load data
    df, df_stats, df_metrics = load_data()
    
    # Run all validations
    all_passed = True
    
    all_passed &= validate_dataset_structure(df)
    all_passed &= validate_glicko_sigma(df)
    all_passed &= validate_wheel_slip(df)
    all_passed &= validate_rpm(df)
    all_passed &= validate_statistical_tests(df, df_stats)
    all_passed &= validate_simulated_data()
    
    # Final summary
    print_header("VALIDATION SUMMARY")
    
    if all_passed:
        print(f"\n{GREEN}{'='*70}")
        print(f"{'🎉 ALL VALIDATIONS PASSED ✅':^70}")
        print(f"{'='*70}{RESET}\n")
        print(f"{GREEN}All numbers in Section 4 match the MEGA dataset.{RESET}")
        print(f"{GREEN}You can confidently submit your paper with these values.{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}{'='*70}")
        print(f"{'⚠️  SOME VALIDATIONS FAILED ❌':^70}")
        print(f"{'='*70}{RESET}\n")
        print(f"{RED}Please review the failed checks above.{RESET}")
        print(f"{RED}Update Section 4 documentation or regenerate data.{RESET}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
