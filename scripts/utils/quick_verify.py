#!/usr/bin/env python3
"""
Quick verification script for Section 4 data files.
Checks existence and basic stats of all required files.
"""

from pathlib import Path
import pandas as pd
import sys

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{RESET}\n")

def check_file(filepath, expected_size_kb=None):
    """Check if file exists and optionally verify size."""
    if not filepath.exists():
        print(f"{RED}❌ MISSING: {filepath.name}{RESET}")
        return False
    
    size_kb = filepath.stat().st_size / 1024
    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
    
    if expected_size_kb:
        if abs(size_kb - expected_size_kb) < expected_size_kb * 0.5:  # 50% tolerance
            print(f"{GREEN}✅ {filepath.name:50s} {size_str:>10s}{RESET}")
        else:
            print(f"{YELLOW}⚠️  {filepath.name:50s} {size_str:>10s} (expected: ~{expected_size_kb:.1f} KB){RESET}")
    else:
        print(f"{GREEN}✅ {filepath.name:50s} {size_str:>10s}{RESET}")
    
    return True

def main():
    base_dir = Path(__file__).parent.parent.parent
    
    print(f"\n{BLUE}{'='*70}")
    print(f"{'SECTION 4 FILE VERIFICATION':^70}")
    print(f"{'='*70}{RESET}\n")
    
    all_ok = True
    
    # Check documentation files
    print_header("DOCUMENTATION FILES (docs/paper/)")
    
    doc_files = [
        ("SECTION_4_EXPERIMENTAL_EVALUATION.md", 14),
        ("TABLES_LATEX_READY.tex", 9),
        ("INTEGRATION_GUIDE.md", 15),
        ("QUICK_REFERENCE.md", 9),
        ("GENERATED_DATA_SUMMARY.md", 10),
        ("RESUMEN_FINAL_ES.md", 9),
    ]
    
    for filename, size_kb in doc_files:
        filepath = base_dir / "docs" / "paper" / filename
        all_ok &= check_file(filepath, size_kb)
    
    # Check data files
    print_header("DATA FILES (data/tables/)")
    
    data_files = [
        ("Table_v4_All_Metrics.csv", 2),
        ("Table_v4_Glicko_Summary.csv", 0.5),
        ("Table_v4_Statistical_Tests.csv", 0.2),
        ("Table_v4_Skill_Atom_Segmentation.csv", 12),
        ("Table_v4_Segmentation_Summary.csv", 0.2),
        ("Table_v4_MQTT_Latency.csv", 72),
        ("Table_v4_MQTT_Summary.csv", 0.4),
        ("Table_v4_Time_Loss_Attribution.csv", 1),
    ]
    
    for filename, size_kb in data_files:
        filepath = base_dir / "data" / "tables" / filename
        all_ok &= check_file(filepath, size_kb)
    
    # Quick data sanity checks
    print_header("DATA SANITY CHECKS")
    
    try:
        # Check MEGA dataset
        mega_path = base_dir / "data" / "datasets" / "NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv"
        df = pd.read_csv(mega_path)
        if len(df) == 20000 and len(df.columns) == 37:
            print(f"{GREEN}✅ MEGA dataset: {len(df)} rows, {len(df.columns)} columns{RESET}")
        else:
            print(f"{RED}❌ MEGA dataset: unexpected shape ({len(df)} rows, {len(df.columns)} cols){RESET}")
            all_ok = False
        
        # Check segmentation
        seg_path = base_dir / "data" / "tables" / "Table_v4_Segmentation_Summary.csv"
        seg_df = pd.read_csv(seg_path)
        as_f1 = seg_df[seg_df['skill_atom'] == 'AS']['f1_score'].values[0]
        ce_f1 = seg_df[seg_df['skill_atom'] == 'CE']['f1_score'].values[0]
        print(f"{GREEN}✅ Skill Atom F1-scores: AS={as_f1:.4f}, CE={ce_f1:.4f}{RESET}")
        
        # Check MQTT
        mqtt_path = base_dir / "data" / "tables" / "Table_v4_MQTT_Summary.csv"
        mqtt_df = pd.read_csv(mqtt_path)
        p95 = mqtt_df[mqtt_df['metric'] == 'End-to-End']['p95_latency_ms'].values[0]
        print(f"{GREEN}✅ MQTT p95 latency: {p95:.2f} ms{RESET}")
        
        # Check statistical tests
        stats_path = base_dir / "data" / "tables" / "Table_v4_Statistical_Tests.csv"
        stats_df = pd.read_csv(stats_path)
        t_val = stats_df[stats_df['Test'] == 'Welch t-test']['Statistic'].values[0]
        d_val = stats_df[stats_df['Test'] == 'Cohen d']['Statistic'].values[0]
        print(f"{GREEN}✅ Statistical tests: t={t_val:.2f}, d={d_val:.4f}{RESET}")
        
    except Exception as e:
        print(f"{RED}❌ Error reading data files: {str(e)}{RESET}")
        all_ok = False
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    if all_ok:
        print(f"{GREEN}{'='*70}")
        print(f"{'🎉 ALL FILES VERIFIED SUCCESSFULLY ✅':^70}")
        print(f"{'='*70}{RESET}\n")
        print(f"{GREEN}Ready for paper submission!{RESET}")
        print(f"\nNext steps:")
        print(f"  1. Generate figures: python scripts/analysis/visualize_results_v4_advanced.py")
        print(f"  2. Integrate Section 4 text into main paper")
        print(f"  3. Copy LaTeX tables from TABLES_LATEX_READY.tex")
        print(f"  4. Add Data Availability Statement\n")
        sys.exit(0)
    else:
        print(f"{RED}{'='*70}")
        print(f"{'⚠️  SOME FILES ARE MISSING OR INCORRECT ❌':^70}")
        print(f"{'='*70}{RESET}\n")
        print(f"{RED}Review the errors above and regenerate if needed:{RESET}")
        print(f"  python scripts/generators/generate_simulated_data_h1h2.py\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
