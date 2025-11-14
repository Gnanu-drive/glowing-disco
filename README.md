# glowing-disco
Data Version Control Demo with DVC

## Overview

This project demonstrates a complete data version control workflow using DVC (Data Version Control). It includes:
- Automated environment setup for Windows, macOS, and Linux
- Sample data download and processing
- Exploratory Data Analysis (EDA)
- Principal Component Analysis (PCA)
- Data version control with DVC

## Features

- 📦 **Cross-platform Makefile**: Works on Windows, macOS, and Linux
- 🔄 **Data Version Control**: Track data files with DVC
- 📊 **EDA Pipeline**: Comprehensive exploratory data analysis
- 🎯 **PCA Analysis**: Principal component analysis with visualizations
- 🔍 **Data Modifications**: Feature engineering and data transformations
- 📈 **Visualizations**: Automated generation of plots and reports

## Project Structure

```
.
├── Makefile                 # Cross-platform build automation
├── requirements.txt         # Python dependencies
├── data_pipeline.py        # Main pipeline script
├── data/                   # Data directory (tracked by DVC)
│   ├── raw/               # Raw downloaded data
│   └── processed/         # Processed data files
├── outputs/               # Analysis outputs
│   ├── eda/              # EDA visualizations and reports
│   └── pca/              # PCA visualizations and reports
└── dvc.yaml              # DVC pipeline configuration
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git
- make (usually pre-installed on macOS/Linux, install via Chocolatey on Windows)

## Quick Start

### 1. Setup Environment

Choose the appropriate command for your operating system:

**All Platforms (using Make):**
```bash
make install
```

This will:
- Create a virtual environment
- Install all required dependencies
- Set up DVC

**Manual Setup (if Make is not available):**

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize DVC

```bash
make init-dvc
```

Or manually:
```bash
dvc init
```

### 3. Run the Complete Workflow

**Using Make:**
```bash
make run
```

**Or run Python directly:**

Windows:
```cmd
venv\Scripts\python data_pipeline.py --all
```

macOS/Linux:
```bash
venv/bin/python data_pipeline.py --all
```

This will:
1. Download sample data (Iris dataset)
2. Perform Exploratory Data Analysis
3. Create modified dataset with engineered features
4. Perform Principal Component Analysis
5. Track all data files with DVC

## Usage

### Makefile Commands

```bash
make help          # Show all available commands
make info          # Display system information
make setup         # Create virtual environment
make install       # Install dependencies
make init-dvc      # Initialize DVC
make download-data # Download sample data only
make run           # Run complete workflow
make test          # Test the environment
make clean         # Remove generated files
```

### Python Script Options

```bash
# Run individual steps
python data_pipeline.py --download  # Download data only
python data_pipeline.py --eda       # Run EDA only
python data_pipeline.py --pca       # Run PCA only
python data_pipeline.py --track     # Track files with DVC
python data_pipeline.py --all       # Run complete workflow
```

## Output Files

### Data Files (tracked by DVC)
- `data/raw/iris_raw.csv` - Original downloaded data
- `data/processed/iris_modified.csv` - Modified data with engineered features
- `data/processed/iris_pca.csv` - PCA transformed data

### EDA Outputs
- `outputs/eda/statistics.txt` - Statistical summary
- `outputs/eda/distributions.png` - Feature distributions
- `outputs/eda/correlation_heatmap.png` - Correlation matrix
- `outputs/eda/boxplots.png` - Box plots for outlier detection
- `outputs/eda/pairplot.png` - Pairwise feature relationships

### PCA Outputs
- `outputs/pca/pca_report.txt` - Detailed PCA analysis
- `outputs/pca/explained_variance.png` - Variance explained by components
- `outputs/pca/pca_scatter.png` - 2D PCA projection
- `outputs/pca/component_loadings.png` - Feature loadings

## Data Version Control with DVC

### Basic DVC Workflow

1. **Initialize DVC** (already done):
```bash
dvc init
```

2. **Track data files**:
```bash
dvc add data/raw/iris_raw.csv
dvc add data/processed/iris_modified.csv
```

3. **Commit DVC files to Git**:
```bash
git add data/raw/iris_raw.csv.dvc data/processed/iris_modified.csv.dvc .gitignore
git commit -m "Track data with DVC"
```

4. **Run DVC pipeline**:
```bash
dvc repro
```

### Setting up Remote Storage (Optional)

To share data with your team, configure a DVC remote:

```bash
# Local remote (for testing)
dvc remote add -d myremote /tmp/dvc-storage

# S3 remote
dvc remote add -d myremote s3://mybucket/dvcstore

# Push data to remote
dvc push

# Pull data from remote
dvc pull
```

## Data Processing Pipeline

### 1. Data Download
- Downloads Iris dataset from OpenML
- Saves raw data to `data/raw/`

### 2. Exploratory Data Analysis (EDA)
- Generates statistical summaries
- Creates distribution plots
- Correlation analysis
- Outlier detection with box plots
- Pairwise feature relationships

### 3. Data Modification
- Feature engineering:
  - Ratio features
  - Sum features
  - Squared features
  - Normalized features
- Saves modified data to `data/processed/`

### 4. Principal Component Analysis (PCA)
- Standardizes features
- Applies PCA transformation
- Generates component loadings
- Creates visualizations
- Saves PCA results

### 5. Version Control
- Tracks all data files with DVC
- Creates `.dvc` files for version control
- Generates DVC pipeline configuration

## Platform-Specific Notes

### Windows
- Activate virtual environment: `venv\Scripts\activate`
- Use backslashes in paths: `venv\Scripts\python`
- Make sure Python is in your PATH

### macOS/Linux
- Activate virtual environment: `source venv/bin/activate`
- Use forward slashes in paths: `venv/bin/python`
- May need to use `python3` instead of `python`

## Troubleshooting

### Issue: Make command not found (Windows)
**Solution**: Install Make via Chocolatey:
```cmd
choco install make
```
Or use the Python commands directly.

### Issue: Permission denied (macOS/Linux)
**Solution**: Make the script executable:
```bash
chmod +x data_pipeline.py
```

### Issue: Module not found
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
make install
# or
pip install -r requirements.txt
```

### Issue: DVC not initialized
**Solution**: Initialize DVC:
```bash
make init-dvc
# or
dvc init
```

## Dependencies

Key Python packages:
- `dvc==3.48.1` - Data Version Control
- `pandas==2.2.0` - Data manipulation
- `numpy==1.26.3` - Numerical computing
- `scikit-learn==1.4.0` - Machine learning
- `matplotlib==3.8.2` - Plotting
- `seaborn==0.13.1` - Statistical visualizations

See `requirements.txt` for complete list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## License

This project is for educational purposes.

## Next Steps

After running the workflow:

1. **Review Outputs**: Check the generated visualizations and reports in `outputs/`
2. **Examine Data**: Explore the modified and PCA-transformed data
3. **Experiment**: Modify the pipeline to work with your own data
4. **Share**: Set up DVC remote storage to collaborate with your team
5. **Iterate**: Use DVC to track different versions of your data

## Resources

- [DVC Documentation](https://dvc.org/doc)
- [DVC Tutorial](https://dvc.org/doc/start)
- [Git Version Control](https://git-scm.com/doc)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

## Contact

For questions or issues, please open a GitHub issue.
