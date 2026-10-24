# Geothermal Energy Assessment & Site Screening — Utrecht, Netherlands
## Project Overview

This project integrates machine learning petrophysics, multi-criteria reservoir ranking, and technoeconomic optimization to assess geothermal development opportunities in the Utrecht region.

## Key Results

- The workflow evaluates whether the Slochteren aquifer can support commercially viable geothermal doublets for district heating and cooling.
- The analysis combines subsurface characterization, reservoir-quality screening, and economic viability assessment for candidate development locations.

---

## Problem Statement

Utrecht, Netherlands seeks to develop its geothermal resources to meet urban district heating and cooling demand. The challenge is to assess whether the Slochteren aquifer (ROSL_ROSLU) can deliver:

- ≥ 10 MWth for district heating
- ≥ 5 MWth for district cooling

using commercially viable doublet configurations, and to identify the optimal enhancement scenario and development locations that meet these targets economically.

---

## Data

> ⚠️ Some raw data files are too large to include in this repo. See [`data/raw/README.md`](data/raw/README.md).

## Setup & Usage

### Requirements
- Python 3.11.2

### Installation

1. Clone or download the repository:
```bash
git clone https://github.com/sadaraka-kadi/utrecht-geothermal-screening.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install pythermogis --index-url https://ci.tno.nl/gitlab/api/v4/projects/18271/packages/pypi/simple
```

3. Download large data files — see [`data/raw/README.md`](data/raw/README.md) for instructions

4. Run notebooks in order from the `notebooks/` folder:
```bash
01_data_exploration.ipynb
02_utrecht_formation_coverage.ipynb
03_reservoir_quality_assessment.ipynb
04_power_economics.ipynb
```

> **Note:** Run cells in order within each notebook. Processed files will be automatically saved to `data/processed/` and simulation outputs to `outputs/`.

---

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `lasio` | Reading LAS well log files |
| `scikit-learn` | Machine learning (Random Forest) |
| `openpyxl` | Reading Excel well path data |
| `geopandas` | Geospatial data processing |
| `xarray` | Reading NetCDF grid files |
| `matplotlib` | Plotting and figures |
| `pythermogis` | ThermoGIS geothermal simulation |
| `pygridsio` | Reading ThermoGIS grid files |
| `rioxarray` | Raster clipping and CRS handling |
| `shapely` | Geometric operations |

---

## Acknowledgements / Technical recommendations

- Dr. Daniel Wamriew
- Elias Drescher

## AI Assistance Disclosure

This project used Claude (by Anthropic) as an AI assistant to support code development. All simulation results, parameter selections, subsurface interpretations, and conclusions were independently verified and validated by the team. The analysis, findings, and recommendations remain the responsibility of the project contributors.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
