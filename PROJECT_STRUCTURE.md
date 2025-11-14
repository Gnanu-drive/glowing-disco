# Project Structure

This document provides an overview of the Data Version Control project structure.

## Directory Structure

```
glowing-disco/
├── .dvc/                           # DVC configuration directory
│   ├── .gitignore                  # DVC internal files to ignore
│   ├── config                      # DVC configuration
│   └── tmp/                        # DVC temporary files
│
├── .git/                           # Git repository
│
├── data/                           # Data directory (tracked by DVC)
│   ├── raw/                        # Raw data files
│   │   ├── iris_raw.csv            # Original Iris dataset (ignored by git)
│   │   └── iris_raw.csv.dvc        # DVC metadata (tracked by git)
│   │
│   └── processed/                  # Processed data files
│       ├── iris_modified.csv       # Modified dataset (ignored by git)
│       ├── iris_modified.csv.dvc   # DVC metadata (tracked by git)
│       ├── iris_pca.csv            # PCA-transformed data (ignored by git)
│       └── iris_pca.csv.dvc        # DVC metadata (tracked by git)
│
├── outputs/                        # Analysis outputs (ignored by git)
│   ├── eda/                        # EDA visualizations and reports
│   │   ├── boxplots.png            # Box plots for outlier detection
│   │   ├── correlation_heatmap.png # Feature correlation heatmap
│   │   ├── distributions.png       # Feature distributions
│   │   ├── pairplot.png            # Pairwise feature relationships
│   │   └── statistics.txt          # Statistical summary
│   │
│   └── pca/                        # PCA analysis outputs
│       ├── component_loadings.png  # PCA component loadings
│       ├── explained_variance.png  # Variance explained by components
│       ├── pca_report.txt          # Detailed PCA report
│       └── pca_scatter.png         # 2D PCA projection
│
├── venv/                           # Virtual environment (ignored by git)
│
├── .dvcignore                      # Files to ignore in DVC
├── .gitignore                      # Files to ignore in Git
├── data_pipeline.py                # Main data processing pipeline
├── dvc.yaml                        # DVC pipeline configuration
├── Makefile                        # Cross-platform build automation
├── QUICKSTART.md                   # Quick start guide
├── README.md                       # Main documentation
├── requirements.txt                # Python dependencies
└── run_pipeline.py                 # DVC pipeline runner script
```

## Key Files

### Configuration Files

- **`.dvcignore`** - Specifies files for DVC to ignore
- **`.gitignore`** - Specifies files for Git to ignore (data files, outputs, venv)
- **`dvc.yaml`** - Defines the DVC pipeline stages and dependencies
- **`requirements.txt`** - Lists all Python package dependencies

### Scripts

- **`data_pipeline.py`** - Main pipeline script
  - Downloads sample data
  - Performs EDA with visualizations
  - Applies PCA transformation
  - Tracks files with DVC
  
- **`run_pipeline.py`** - DVC pipeline runner
  - Checks DVC installation
  - Shows pipeline DAG
  - Runs the complete pipeline
  - Displays results

### Build Automation

- **`Makefile`** - Cross-platform build automation
  - Environment setup (Windows, macOS, Linux)
  - Dependency installation
  - DVC initialization
  - Workflow execution

### Documentation

- **`README.md`** - Comprehensive project documentation
  - Overview and features
  - Installation instructions
  - Usage guide
  - Platform-specific notes
  
- **`QUICKSTART.md`** - Quick start guide
  - Platform-specific installation
  - Basic usage examples
  - Common commands
  - Troubleshooting

## Data Flow

```
1. Download Data
   └─> data/raw/iris_raw.csv
       └─> iris_raw.csv.dvc (tracked by Git)

2. Exploratory Data Analysis (EDA)
   ├─> data/processed/iris_modified.csv
   │   └─> iris_modified.csv.dvc (tracked by Git)
   └─> outputs/eda/
       ├─> statistics.txt
       ├─> distributions.png
       ├─> correlation_heatmap.png
       ├─> boxplots.png
       └─> pairplot.png

3. Principal Component Analysis (PCA)
   ├─> data/processed/iris_pca.csv
   │   └─> iris_pca.csv.dvc (tracked by Git)
   └─> outputs/pca/
       ├─> pca_report.txt
       ├─> explained_variance.png
       ├─> pca_scatter.png
       └─> component_loadings.png
```

## Git vs DVC Tracking

### Tracked by Git
- Source code (.py files)
- Configuration files (.yaml, .txt)
- Documentation (.md files)
- DVC metadata (.dvc files)
- Build automation (Makefile)

### Tracked by DVC (ignored by Git)
- Raw data files (.csv in data/raw/)
- Processed data files (.csv in data/processed/)
- Analysis outputs (outputs/ directory)

### Ignored by Both
- Virtual environment (venv/)
- Python cache (__pycache__/, *.pyc)
- DVC cache (.dvc/cache/)
- Temporary files (.dvc/tmp/)

## Workflow Commands

### Setup
```bash
make install        # Create venv and install dependencies
make init-dvc      # Initialize DVC
```

### Run Pipeline
```bash
make run           # Run complete workflow
python data_pipeline.py --all  # Alternative method
python run_pipeline.py         # Using DVC pipeline
```

### DVC Operations
```bash
dvc add data/file.csv    # Track a file
dvc push                 # Upload to remote storage
dvc pull                 # Download from remote storage
dvc repro                # Run pipeline
```

## Platform Support

The project supports:
- **Windows** - Tested with Python 3.8+, Make (via Chocolatey)
- **macOS** - Tested with Python 3.8+, native Make
- **Linux** - Tested with Python 3.8+, native Make

## Dependencies

### Core Dependencies
- dvc==3.48.1 - Data Version Control
- pandas==2.2.0 - Data manipulation
- numpy==1.26.3 - Numerical computing
- scikit-learn==1.4.0 - Machine learning

### Visualization
- matplotlib==3.8.2 - Plotting
- seaborn==0.13.1 - Statistical visualizations

### Development
- jupyter==1.0.0 - Interactive notebooks
- notebook==7.0.6 - Jupyter notebook server

## Version Control Strategy

1. **Code Changes**: Commit to Git
   ```bash
   git add *.py Makefile
   git commit -m "Update pipeline"
   ```

2. **Data Changes**: Track with DVC, commit .dvc files
   ```bash
   dvc add data/file.csv
   git add data/file.csv.dvc
   git commit -m "Update data"
   ```

3. **Share Data**: Push to DVC remote
   ```bash
   dvc push
   ```

4. **Pull Data**: Download from DVC remote
   ```bash
   dvc pull
   ```

## Best Practices

1. **Keep data files out of Git** - Use DVC to track large files
2. **Commit .dvc files to Git** - These are small metadata files
3. **Use DVC pipelines** - For reproducible workflows
4. **Document changes** - Update README when adding features
5. **Test cross-platform** - Ensure Makefile works on all platforms
6. **Use virtual environments** - Isolate project dependencies
7. **Version your data** - Track different versions with DVC
8. **Set up remote storage** - Enable team collaboration

## Troubleshooting

See QUICKSTART.md for common issues and solutions:
- Virtual environment activation
- Module not found errors
- DVC configuration
- Platform-specific issues
