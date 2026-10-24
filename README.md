# Geothermal Energy Assessment & Site Screening — Utrecht, Netherlands
## Project Overview

This project screens the Slochteren aquifer (ROSL_ROSLU) for geothermal doublet development in the Utrecht region. It combines porosity prediction from well logs (validated by leave-one-well-out cross-validation), multi-criteria ranking of four wells, a Monte Carlo treatment of transmissivity uncertainty, and a cost comparison of 32 design scenarios.

The full write-up is in [reports/report.pdf](reports/report.pdf), 

---

## Problem Statement

Utrecht, Netherlands seeks to develop its geothermal resources to meet urban district heating and cooling demand. The challenge is to assess whether the Slochteren aquifer (ROSL_ROSLU) can deliver:

- ≥ 10 MWth for district heating
- ≥ 5 MWth for district cooling

using commercially viable doublet configurations, and to identify the optimal enhancement scenario and development locations that meet these targets economically.

---
## Key Results

- The preferred design is one stimulated doublet at BLT-01 with a 60 bar drawdown and 211 m3/h flow
- The design gives 12.2 MWth in the deterministic case, with surface electric chillers for the 5 MWth cooling load. 
- A Monte Carlo run over ThermoGIS transmissivity gives a 56% probability that the wells alone reach 10 MWth, a median of 12.7 MWth and a low case (P90) of 1.7 MWth.
- The whole-system capital cost is 23.3 M€, LCOE is 69€/MWh against 68€/MWh for a gas and chiller baseline

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
Terms for every dataset and third-party component is in [DATA_LICENSE](DATA_LICENSE.md)
