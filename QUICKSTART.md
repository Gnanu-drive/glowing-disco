# Quick Start Guide

This guide will help you get started with the Data Version Control (DVC) project.

## Installation

### Windows

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **Install Make** (optional but recommended):
   ```cmd
   choco install make
   ```
3. **Clone the repository**:
   ```cmd
   git clone https://github.com/Gnanu-drive/glowing-disco.git
   cd glowing-disco
   ```
4. **Run the setup**:
   ```cmd
   make install
   ```
   Or manually:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### macOS

1. **Install Python 3.8+** (usually pre-installed or via Homebrew):
   ```bash
   brew install python3
   ```
2. **Clone the repository**:
   ```bash
   git clone https://github.com/Gnanu-drive/glowing-disco.git
   cd glowing-disco
   ```
3. **Run the setup**:
   ```bash
   make install
   ```

### Linux

1. **Install Python 3.8+**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-venv python3-pip
   ```
2. **Clone the repository**:
   ```bash
   git clone https://github.com/Gnanu-drive/glowing-disco.git
   cd glowing-disco
   ```
3. **Run the setup**:
   ```bash
   make install
   ```

## Running the Workflow

### Option 1: Using Make (Recommended)

```bash
# Initialize DVC (first time only)
make init-dvc

# Run the complete workflow
make run
```

### Option 2: Using Python Directly

**Activate virtual environment first:**

Windows:
```cmd
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**Run the workflow:**
```bash
python data_pipeline.py --all
```

## What Gets Generated?

After running the workflow, you'll have:

### Data Files (tracked by DVC)
- `data/raw/iris_raw.csv` - Original Iris dataset
- `data/processed/iris_modified.csv` - Dataset with engineered features
- `data/processed/iris_pca.csv` - PCA-transformed dataset

### EDA Visualizations
- `outputs/eda/statistics.txt` - Statistical summary
- `outputs/eda/distributions.png` - Feature distributions
- `outputs/eda/correlation_heatmap.png` - Feature correlations
- `outputs/eda/boxplots.png` - Outlier detection
- `outputs/eda/pairplot.png` - Pairwise relationships

### PCA Analysis
- `outputs/pca/pca_report.txt` - Detailed PCA analysis
- `outputs/pca/explained_variance.png` - Variance by component
- `outputs/pca/pca_scatter.png` - 2D PCA projection
- `outputs/pca/component_loadings.png` - Feature importance

### DVC Files
- `data/raw/iris_raw.csv.dvc` - DVC metadata for raw data
- `data/processed/iris_modified.csv.dvc` - DVC metadata for processed data
- `data/processed/iris_pca.csv.dvc` - DVC metadata for PCA data
- `dvc.yaml` - DVC pipeline configuration

## Understanding DVC

DVC (Data Version Control) treats data files like Git treats code:

1. **Track data files**: `dvc add data/myfile.csv`
   - Creates `myfile.csv.dvc` (tracked by Git)
   - Original file is ignored by Git

2. **Commit DVC files to Git**: `git add myfile.csv.dvc && git commit`

3. **Share with team**:
   - Set up remote storage: `dvc remote add -d myremote s3://mybucket`
   - Push data: `dvc push`
   - Others pull data: `dvc pull`

## Common Commands

### Makefile Commands
```bash
make help          # Show all commands
make info          # System information
make setup         # Create virtual environment
make install       # Install dependencies
make init-dvc      # Initialize DVC
make download-data # Download data only
make run           # Complete workflow
make test          # Test environment
make clean         # Clean up
```

### Python Script Commands
```bash
python data_pipeline.py --download  # Download data
python data_pipeline.py --eda       # Run EDA
python data_pipeline.py --pca       # Run PCA
python data_pipeline.py --track     # Track with DVC
python data_pipeline.py --all       # Complete workflow
```

### DVC Commands
```bash
dvc init                    # Initialize DVC
dvc add data/file.csv       # Track a file
dvc push                    # Upload data to remote
dvc pull                    # Download data from remote
dvc repro                   # Run pipeline
dvc dag                     # Show pipeline graph
dvc diff                    # Compare data versions
```

## Troubleshooting

### Virtual environment not activating
**Windows**: Use `venv\Scripts\activate.bat` in CMD or `venv\Scripts\Activate.ps1` in PowerShell
**macOS/Linux**: Use `source venv/bin/activate`

### Module not found errors
Ensure you've activated the virtual environment and installed dependencies:
```bash
make install
# or
pip install -r requirements.txt
```

### DVC not found
Make sure DVC is installed in your virtual environment:
```bash
pip install dvc
```

### Permission denied (Linux/macOS)
Make scripts executable:
```bash
chmod +x data_pipeline.py
```

## Next Steps

1. **Review the outputs**: Check the visualizations in `outputs/`
2. **Modify the pipeline**: Edit `data_pipeline.py` to work with your data
3. **Set up remote storage**: Configure DVC remote for team collaboration
4. **Experiment**: Try different parameters and analyses
5. **Share**: Commit `.dvc` files to Git and push data to remote

## Learn More

- [DVC Documentation](https://dvc.org/doc)
- [Git Documentation](https://git-scm.com/doc)
- [Python Data Science](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Scikit-learn](https://scikit-learn.org/)

## Support

For issues or questions, please:
1. Check the main README.md
2. Review this Quick Start Guide
3. Open a GitHub issue
