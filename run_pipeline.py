#!/usr/bin/env python3
"""
DVC Pipeline Runner
This script demonstrates how to use DVC pipelines for reproducible workflows.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*80)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Info:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: Command not found. Make sure DVC is installed.")
        return False


def check_dvc():
    """Check if DVC is installed."""
    # Try different DVC paths
    dvc_paths = [
        'venv/bin/dvc',  # Linux/macOS venv
        'venv\\Scripts\\dvc.exe',  # Windows venv
        'dvc'  # System DVC
    ]
    
    for dvc_path in dvc_paths:
        try:
            result = subprocess.run(
                [dvc_path, 'version'],
                capture_output=True,
                text=True
            )
            print(f"✓ DVC version: {result.stdout.strip()}")
            print(f"✓ Using DVC from: {dvc_path}")
            return dvc_path
        except (FileNotFoundError, OSError):
            continue
    
    print("✗ DVC not found. Please install DVC first:")
    print("  pip install dvc")
    return None


def main():
    """Main function to run DVC pipeline."""
    print("\nDVC Pipeline Runner")
    print("=" * 80)
    
    # Check if DVC is installed
    dvc_cmd = check_dvc()
    if not dvc_cmd:
        sys.exit(1)
    
    # Check if dvc.yaml exists
    if not Path("dvc.yaml").exists():
        print("\n✗ dvc.yaml not found!")
        print("Run the main workflow first:")
        print("  python data_pipeline.py --all")
        sys.exit(1)
    
    print("\nThis script will run the DVC pipeline defined in dvc.yaml")
    print("\nStages:")
    print("  1. download_data - Download sample data")
    print("  2. perform_eda   - Exploratory Data Analysis")
    print("  3. perform_pca   - Principal Component Analysis")
    
    # Show pipeline DAG
    print("\n" + "="*80)
    print("Pipeline Structure:")
    print("="*80)
    run_command([dvc_cmd, 'dag'], "Show pipeline DAG")
    
    # Run the pipeline
    response = input("\nDo you want to run the pipeline? (y/n): ").lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    # Reproduce the pipeline
    success = run_command(
        [dvc_cmd, 'repro'],
        "Run DVC pipeline (dvc repro)"
    )
    
    if success:
        print("\n" + "="*80)
        print("Pipeline completed successfully!")
        print("="*80)
        
        # Show pipeline metrics
        print("\nPipeline Status:")
        run_command([dvc_cmd, 'status'], "Check pipeline status")
        
        # Show what was generated
        print("\n" + "="*80)
        print("Generated Files:")
        print("="*80)
        print("\nData files (tracked by DVC):")
        for dvc_file in Path('.').rglob('*.dvc'):
            print(f"  - {dvc_file}")
        
        print("\nVisualizations:")
        for viz_file in Path('outputs').rglob('*.png'):
            print(f"  - {viz_file}")
        
        print("\nReports:")
        for report_file in Path('outputs').rglob('*.txt'):
            print(f"  - {report_file}")
        
        print("\n" + "="*80)
        print("Next Steps:")
        print("="*80)
        print("1. Review the generated visualizations in outputs/")
        print("2. Commit DVC files to Git:")
        print("   git add *.dvc dvc.lock")
        print("   git commit -m 'Update data pipeline'")
        print("3. Set up DVC remote storage (optional):")
        print("   dvc remote add -d myremote <storage-url>")
        print("   dvc push")
    else:
        print("\n✗ Pipeline failed. Check the errors above.")


if __name__ == "__main__":
    main()
