# Data Sources

## Large files — download manually before running notebooks

### 1. Participant Data Pack
#### i. BLT-01.las, EVD-01.las, JUT-01.las, PKP-01.las
#### ii. LCOE.xslx
c. Lithostratigraphic Data.xslx
d. ThermoGIS Data.xslx
e. Well Path Data.xlsx
f. target_lithologiies.csv
- **Used by:** `data_exploration.ipynb`, `reservoir_quality_assessment.ipynb`, `LCOE.py`
- **Download:** https://drive.google.com/drive/folders/1fGN5C8G8wzzxA7wULrz1Wn-xCw1eKTku
- Unzip and place files in this folder (`data/raw`)

### 2. Administrative Boundaries (`administrativeunits.gml`)
- **Used by:** `utrecht_formation_coverage.ipynb`
- **Download:** https://service.pdok.nl/kadaster/brk-administratieve-eenheden/atom/downloads/administrativeunits.zip
- Unzip and place `administrativeunits.gml` in this folder (`data/raw/`)

### 3. ThermoGIS Grids (`.nc` files)
- **Used by:** `utrecht_formation_coverage.ipynb`
- **Download:** https://www.thermogis.nl/sites/default/files/2026-05/for_external_use.zip)
- Navigate to: `ThermoGIS_grids_2_5_1 > 6_Permian > Slochteren Fm & Upper Slochteren Mb (ROSL&ROSLU) > BaseCase`
- Place all `.nc` files in this folder (`data/raw/`)
