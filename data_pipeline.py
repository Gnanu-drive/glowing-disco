#!/usr/bin/env python3
"""
Data Version Control Pipeline
This script downloads sample data, performs EDA, PCA, and manages data versions with DVC.
"""

import os
import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import fetch_openml


# Configuration
DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path("outputs")
EDA_DIR = OUTPUT_DIR / "eda"
PCA_DIR = OUTPUT_DIR / "pca"


def setup_directories():
    """Create necessary directories."""
    print("Setting up directories...")
    for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EDA_DIR, PCA_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    print("✓ Directories created")


def download_sample_data():
    """Download sample dataset (Iris dataset from sklearn)."""
    print("\nDownloading sample data...")
    try:
        # Try to download Iris dataset from sklearn/openml
        try:
            iris = fetch_openml('iris', version=1, as_frame=True, parser='auto')
            df = iris.frame
        except Exception as network_error:
            print(f"  ⚠ Network download failed: {network_error}")
            print("  Using built-in sklearn Iris dataset instead...")
            # Use sklearn's built-in Iris dataset as fallback
            from sklearn.datasets import load_iris
            iris = load_iris()
            df = pd.DataFrame(
                data=iris.data,
                columns=iris.feature_names
            )
            df['class'] = iris.target
            # Map numeric class to string names
            df['class'] = df['class'].map({0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'})
        
        # Save raw data
        raw_file = RAW_DATA_DIR / "iris_raw.csv"
        df.to_csv(raw_file, index=False)
        print(f"✓ Raw data saved to {raw_file}")
        
        # Display basic info
        print(f"  - Shape: {df.shape}")
        print(f"  - Columns: {list(df.columns)}")
        print(f"  - First few rows:")
        print(df.head())
        
        return df
    except Exception as e:
        print(f"✗ Error downloading data: {e}")
        sys.exit(1)


def perform_eda(df=None):
    """Perform Exploratory Data Analysis."""
    print("\nPerforming Exploratory Data Analysis...")
    
    if df is None:
        # Load raw data if not provided
        raw_file = RAW_DATA_DIR / "iris_raw.csv"
        if not raw_file.exists():
            print("✗ Raw data not found. Please download data first.")
            return
        df = pd.read_csv(raw_file)
    
    # Basic statistics
    stats_file = EDA_DIR / "statistics.txt"
    with open(stats_file, 'w') as f:
        f.write("DATASET STATISTICS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Shape: {df.shape}\n\n")
        f.write("Data Types:\n")
        f.write(str(df.dtypes) + "\n\n")
        f.write("Basic Statistics:\n")
        f.write(str(df.describe()) + "\n\n")
        f.write("Missing Values:\n")
        f.write(str(df.isnull().sum()) + "\n\n")
        f.write("Class Distribution:\n")
        f.write(str(df['class'].value_counts()) + "\n")
    
    print(f"✓ Statistics saved to {stats_file}")
    
    # Create visualizations
    create_eda_visualizations(df)
    
    # Create modified dataset
    create_modified_data(df)
    
    print("✓ EDA completed")


def create_eda_visualizations(df):
    """Create EDA visualizations."""
    print("  Creating visualizations...")
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # 1. Distribution plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Feature Distributions', fontsize=16)
    
    for idx, col in enumerate(numeric_cols[:4]):
        ax = axes[idx // 2, idx % 2]
        df[col].hist(bins=20, ax=ax, edgecolor='black')
        ax.set_title(f'{col} Distribution')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(EDA_DIR / "distributions.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Distribution plots saved")
    
    # 2. Correlation heatmap
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Heatmap', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(EDA_DIR / "correlation_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Correlation heatmap saved")
    
    # 3. Box plots
    fig, axes = plt.subplots(1, len(numeric_cols), figsize=(15, 5))
    fig.suptitle('Feature Box Plots', fontsize=16)
    
    for idx, col in enumerate(numeric_cols):
        if len(numeric_cols) > 1:
            ax = axes[idx]
        else:
            ax = axes
        df.boxplot(column=col, ax=ax)
        ax.set_title(col)
        ax.set_ylabel('Value')
    
    plt.tight_layout()
    plt.savefig(EDA_DIR / "boxplots.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Box plots saved")
    
    # 4. Pairplot (if we have class column)
    if 'class' in df.columns:
        try:
            pairplot_fig = sns.pairplot(df, hue='class', diag_kind='hist', 
                                       palette='husl', plot_kws={'alpha': 0.6})
            pairplot_fig.fig.suptitle('Pairwise Feature Relationships', y=1.01, fontsize=16)
            plt.savefig(EDA_DIR / "pairplot.png", dpi=300, bbox_inches='tight')
            plt.close()
            print("    ✓ Pairplot saved")
        except Exception as e:
            print(f"    ⚠ Could not create pairplot: {e}")


def create_modified_data(df):
    """Create modified version of the dataset."""
    print("  Creating modified dataset...")
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Modifications:
    # 1. Add derived features
    df_modified = df.copy()
    
    if len(numeric_cols) >= 2:
        # Create ratio features
        df_modified[f'{numeric_cols[0]}_to_{numeric_cols[1]}_ratio'] = \
            df_modified[numeric_cols[0]] / (df_modified[numeric_cols[1]] + 1e-10)
        
        # Create sum features
        df_modified[f'{numeric_cols[0]}_{numeric_cols[1]}_sum'] = \
            df_modified[numeric_cols[0]] + df_modified[numeric_cols[1]]
    
    # 2. Add squared features for first numeric column
    if len(numeric_cols) >= 1:
        df_modified[f'{numeric_cols[0]}_squared'] = df_modified[numeric_cols[0]] ** 2
    
    # 3. Add normalized features
    for col in numeric_cols:
        col_mean = df_modified[col].mean()
        col_std = df_modified[col].std()
        df_modified[f'{col}_normalized'] = (df_modified[col] - col_mean) / (col_std + 1e-10)
    
    # Save modified data
    modified_file = PROCESSED_DATA_DIR / "iris_modified.csv"
    df_modified.to_csv(modified_file, index=False)
    print(f"  ✓ Modified data saved to {modified_file}")
    print(f"    - Original features: {len(df.columns)}")
    print(f"    - Modified features: {len(df_modified.columns)}")
    
    return df_modified


def perform_pca(df=None):
    """Perform Principal Component Analysis."""
    print("\nPerforming Principal Component Analysis...")
    
    if df is None:
        # Load processed data if not provided
        processed_file = PROCESSED_DATA_DIR / "iris_modified.csv"
        if not processed_file.exists():
            print("✗ Processed data not found. Please run EDA first.")
            return
        df = pd.read_csv(processed_file)
    
    # Select numeric columns (exclude class if present)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    X = df[numeric_cols].values
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    n_components = min(len(numeric_cols), 4)  # Use up to 4 components
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    
    # Save PCA results
    pca_df = pd.DataFrame(
        X_pca,
        columns=[f'PC{i+1}' for i in range(n_components)]
    )
    
    # Add class column if it exists
    if 'class' in df.columns:
        pca_df['class'] = df['class'].values
    
    pca_file = PROCESSED_DATA_DIR / "iris_pca.csv"
    pca_df.to_csv(pca_file, index=False)
    print(f"✓ PCA results saved to {pca_file}")
    
    # Create PCA visualizations and report
    create_pca_visualizations(X_pca, pca, df, n_components)
    
    print("✓ PCA completed")


def create_pca_visualizations(X_pca, pca, df, n_components):
    """Create PCA visualizations and report."""
    print("  Creating PCA visualizations...")
    
    # 1. Explained variance plot
    plt.figure(figsize=(10, 6))
    explained_var = pca.explained_variance_ratio_
    cumulative_var = np.cumsum(explained_var)
    
    x_pos = np.arange(1, len(explained_var) + 1)
    plt.bar(x_pos, explained_var, alpha=0.7, label='Individual')
    plt.plot(x_pos, cumulative_var, 'ro-', label='Cumulative')
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.title('PCA Explained Variance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PCA_DIR / "explained_variance.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Explained variance plot saved")
    
    # 2. PCA scatter plot (first 2 components)
    if n_components >= 2:
        plt.figure(figsize=(10, 8))
        
        if 'class' in df.columns:
            # Color by class
            classes = df['class'].unique()
            for cls in classes:
                mask = df['class'] == cls
                plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                          label=cls, alpha=0.7, s=50)
            plt.legend()
        else:
            plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.7, s=50)
        
        plt.xlabel(f'PC1 ({explained_var[0]:.2%} variance)')
        plt.ylabel(f'PC2 ({explained_var[1]:.2%} variance)')
        plt.title('PCA: First Two Principal Components')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(PCA_DIR / "pca_scatter.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ PCA scatter plot saved")
    
    # 3. Component loadings heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    loadings = pca.components_
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(loadings, 
                xticklabels=numeric_cols,
                yticklabels=[f'PC{i+1}' for i in range(n_components)],
                cmap='RdBu_r', center=0, annot=True, fmt='.2f',
                square=False, linewidths=0.5)
    plt.title('PCA Component Loadings')
    plt.xlabel('Original Features')
    plt.ylabel('Principal Components')
    plt.tight_layout()
    plt.savefig(PCA_DIR / "component_loadings.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Component loadings heatmap saved")
    
    # 4. Save PCA report
    report_file = PCA_DIR / "pca_report.txt"
    with open(report_file, 'w') as f:
        f.write("PCA ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Number of components: {n_components}\n")
        f.write(f"Total variance explained: {cumulative_var[-1]:.4f}\n\n")
        f.write("Explained Variance by Component:\n")
        for i, var in enumerate(explained_var):
            f.write(f"  PC{i+1}: {var:.4f} ({var*100:.2f}%)\n")
        f.write("\nCumulative Explained Variance:\n")
        for i, var in enumerate(cumulative_var):
            f.write(f"  Up to PC{i+1}: {var:.4f} ({var*100:.2f}%)\n")
        f.write("\nComponent Loadings:\n")
        for i in range(n_components):
            f.write(f"\nPC{i+1}:\n")
            for j, col in enumerate(numeric_cols):
                f.write(f"  {col}: {loadings[i, j]:.4f}\n")
    
    print(f"  ✓ PCA report saved to {report_file}")


def track_with_dvc(files_to_track):
    """Track files with DVC."""
    print("\nTracking files with DVC...")
    
    for file_path in files_to_track:
        if not Path(file_path).exists():
            print(f"  ⚠ File not found: {file_path}")
            continue
        
        try:
            # Try to use DVC from venv first, then system
            dvc_paths = [
                'venv/bin/dvc',  # Linux/macOS venv
                'venv\\Scripts\\dvc.exe',  # Windows venv
                'dvc'  # System DVC
            ]
            
            dvc_cmd = None
            for dvc_path in dvc_paths:
                if Path(dvc_path).exists() or dvc_path == 'dvc':
                    dvc_cmd = dvc_path
                    break
            
            if not dvc_cmd:
                print("  ✗ DVC not found. Please install DVC first.")
                return
            
            # Add file to DVC
            result = subprocess.run(
                [dvc_cmd, 'add', str(file_path)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  ✓ Tracked: {file_path}")
            
            # Show what was created
            dvc_file = f"{file_path}.dvc"
            if Path(dvc_file).exists():
                print(f"    Created: {dvc_file}")
        
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error tracking {file_path}: {e.stderr}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def create_dvc_pipeline():
    """Create DVC pipeline configuration."""
    print("\nCreating DVC pipeline...")
    
    pipeline_yaml = """stages:
  download_data:
    cmd: python data_pipeline.py --download
    deps:
      - data_pipeline.py
    outs:
      - data/raw/iris_raw.csv
    
  perform_eda:
    cmd: python data_pipeline.py --eda
    deps:
      - data_pipeline.py
      - data/raw/iris_raw.csv
    outs:
      - data/processed/iris_modified.csv
      - outputs/eda
    
  perform_pca:
    cmd: python data_pipeline.py --pca
    deps:
      - data_pipeline.py
      - data/processed/iris_modified.csv
    outs:
      - data/processed/iris_pca.csv
      - outputs/pca
"""
    
    pipeline_file = Path("dvc.yaml")
    with open(pipeline_file, 'w') as f:
        f.write(pipeline_yaml)
    
    print(f"✓ DVC pipeline created: {pipeline_file}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Data Version Control Pipeline with DVC"
    )
    parser.add_argument(
        '--download',
        action='store_true',
        help='Download sample data'
    )
    parser.add_argument(
        '--eda',
        action='store_true',
        help='Perform Exploratory Data Analysis'
    )
    parser.add_argument(
        '--pca',
        action='store_true',
        help='Perform Principal Component Analysis'
    )
    parser.add_argument(
        '--track',
        action='store_true',
        help='Track data files with DVC'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run complete workflow'
    )
    
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Run complete workflow if --all is specified
    if args.all or (not args.download and not args.eda and not args.pca and not args.track):
        print("\n" + "=" * 80)
        print("RUNNING COMPLETE DATA VERSION CONTROL WORKFLOW")
        print("=" * 80)
        
        # Step 1: Download data
        df = download_sample_data()
        
        # Step 2: Perform EDA
        perform_eda(df)
        
        # Step 3: Perform PCA
        # Load the modified data from EDA
        modified_file = PROCESSED_DATA_DIR / "iris_modified.csv"
        df_modified = pd.read_csv(modified_file)
        perform_pca(df_modified)
        
        # Step 4: Track with DVC (simple file tracking)
        files_to_track = [
            "data/raw/iris_raw.csv",
            "data/processed/iris_modified.csv",
            "data/processed/iris_pca.csv"
        ]
        track_with_dvc(files_to_track)
        
        # Step 5: Create DVC pipeline (optional for advanced users)
        print("\nNote: DVC pipeline configuration is also available.")
        print("  For pipeline-based tracking, use: dvc repro")
        
        print("\n" + "=" * 80)
        print("WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nGenerated files:")
        print("  Data:")
        print("    - data/raw/iris_raw.csv")
        print("    - data/processed/iris_modified.csv")
        print("    - data/processed/iris_pca.csv")
        print("  EDA outputs:")
        print("    - outputs/eda/statistics.txt")
        print("    - outputs/eda/*.png")
        print("  PCA outputs:")
        print("    - outputs/pca/pca_report.txt")
        print("    - outputs/pca/*.png")
        print("  DVC files:")
        print("    - *.dvc files for tracked data")
        print("\nNext steps:")
        print("  1. Review the generated visualizations and reports")
        print("  2. Commit .dvc files to git: git add *.dvc .gitignore")
        print("  3. Optional: Use DVC pipeline with 'dvc repro' for reproducible workflows")
        return
    
    # Run individual steps
    if args.download:
        download_sample_data()
    
    if args.eda:
        perform_eda()
    
    if args.pca:
        perform_pca()
    
    if args.track:
        files_to_track = [
            "data/raw/iris_raw.csv",
            "data/processed/iris_modified.csv",
            "data/processed/iris_pca.csv"
        ]
        track_with_dvc(files_to_track)


if __name__ == "__main__":
    main()
