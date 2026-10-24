# Data and third-party licences

The MIT licence in `LICENSE` covers only the original code and notebooks written for this
project. Every dataset and third-party component below keeps its own terms.

| Item | Used for | Source | Licence / terms | Status |
|---|---|---|---|---|
| Administrative boundaries (`administrativeunits.gml`, `.gfs`, derived `utrecht_*.gpkg`) | Municipality and province polygons | PDOK, Kadaster, "BRK administratieve eenheden" (https://api.pdok.nl/kadaster/brk-administratieve-eenheden/ogc/v1) | CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/deed.nl). Derived from the Basisregistratie Kadaster (BRK) | CONFIRMED |
| ThermoGIS grids (`ROSL_ROSLU_*.nc`, `ThermoGIS Data.xlsx`, `utrecht_grid_arrays.npz`) | Depth, thickness, permeability, power, etc. | TNO Geological Survey of the Netherlands, ThermoGIS release 2.5.1 (https://www.thermogis.nl) | The NLOG ThermoGIS page says only "freely available". No licence named. The NLOG.NL disclaimer (version 9 Aug 2016) permits copying and editing with NLOG.NL cited as source, but does not mention ThermoGIS | UNVERIFIED. Ask support@geologicalsurvey.nl for the licence on the grids |
| Well logs and tables (`BLT-01`, `JUT-01`, `EVD-01`, `PKP-01` `.las`; `Well Path Data.xlsx`; `Lithostratigraphic Data.xlsx`; `target_lithologies.csv`) | Petrophysics, porosity prediction | SPE Africa Geothermal Datathon 2026 participant data pack. Underlying origin not stated by the organisers | No terms found on the public datathon announcement. EPOS-NL, a related public well-data publication, also states no licence | UNVERIFIED. Ask the organisers whether the pack may be republished, and where the wells originate |
| `LCOE.xlsx` and `src/lcoe.py` | Cost model | J.-D. van Wees, L. ten Kulve, D. Straathof, M. Pluymaekers (TNO/ECN), 2011, version 2012.1 | No licence found. `lcoe.py` is a translation of this spreadsheet, so it is a derivative work | UNVERIFIED. Ask TNO or the authors before applying MIT to `lcoe.py` |
| Well cost formula in `lcoe.py` | Drilling capex | Vrijlandt et al., ThermoGIS update, European Geothermal Congress 2019 | Published formula, well capex = 375,000 + 1150*d + 0.3*d^2   (euro, d = depth in m) | Cite |

## Attribution to include in the README and report

- Boundaries: Kadaster / PDOK, BRK administratieve eenheden, CC0 1.0.
- ThermoGIS: TNO Geological Survey of the Netherlands. Source: NLOG.NL / ThermoGIS.
- Wells and datathon data: SPE Africa Geothermal Datathon 2026 data pack (organiser-supplied).
- Cost model: van Wees et al. (TNO/ECN, 2011).
