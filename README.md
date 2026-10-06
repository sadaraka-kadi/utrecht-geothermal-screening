# **Geothermal Energy Assessment & Site Screening — Utrecht, Netherlands**

This repository contains Kadi Sadaraka's refinement and further development of Team KDK's submission for the SPE Africa Datathon 2026, analysing geothermal energy data from Utrecht, Netherlands.

The work builds upon the team's original submission while extending and refining selected aspects of the analysis, modelling, and interpretation.

Original team submission: Team KDK https://github.com/sadaraka-kadi/Team_KDK

---

## Project Overview

---
## Problem Statement

Utrecht, Netherlands seeks to develop its geothermal resources to meet urban 
district heating and cooling demand. The challenge is to assess whether the 
Slochteren aquifer (ROSL_ROSLU) can deliver:

- ≥ 10 MWth for district heating
- ≥ 5 MWth for district cooling

using commercially viable doublet configurations, and to identify the optimal 
enhancement scenario and development locations that meet these targets 
economically.

---

## Repository Structure

> ⚠️ Some raw data files are too large to include in this repo. See [`data/raw/README.md`](data/raw/README.md).

## Large files — download manually before running notebooks

### 1. Participant Data Pack
- **Used by:** `well_data_preprocessing.ipynb`
- **Download:** https://drive.google.com/drive/folders/1fGN5C8G8wzzxA7wULrz1Wn-xCw1eKTku
- Unzip and place files in this folder (`data/raw`)

### 2. Administrative Boundaries (`administrativeunits.gml`)
- **Used by:** `utrecht_formation_coverage.ipynb`
- **Download:** https://service.pdok.nl/kadaster/brk-administratieve-eenheden/atom/downloads/administrativeunits.zip
- Unzip and place `administrativeunits.gml` in this folder (`data/raw/`)

### 3. ThermoGIS Grids (`.nc` files)
- **Used by:** `utrecht_formation_coverage.ipynb` and `reservoir_quality_assessment.ipynb`
- **Download:** https://www.thermogis.nl/sites/default/files/2026-05/for_external_use.zip)

## Setup & Usage

### Requirements
- Python 3.11.2

### Installation

1. Clone or download the repository:
```bash
git clone 
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install pythermogis --index-url https://ci.tno.nl/gitlab/api/v4/projects/18271/packages/pypi/simple
```

3. Download large data files — see [`data/raw/README.md`](data/raw/README.md) for instructions

4. Run notebooks in order from the `notebooks/` folder:
```
01_data_exploration.ipynb
02_utrecht_formation_coverage.ipynb
03_reservoir_quality_assessment.ipynb
04_power_calculations.ipynb
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

This project used Claude (by Anthropic) as an AI assistant to support code 
development. All simulation results, parameter selections, subsurface interpretations, and conclusions were independently verified and validated by the team. The analysis, findings, and recommendations represent the original work of Team KDK.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
