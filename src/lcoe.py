"""

Geothermal direct-heat LCOE model.

Translated from LCOE.xlsx
Authors: Jan-Diederik van Wees, Lars ten Kulve, Derk Straathof, Maarten Pluymaekers 
Date: 10-07-2011
Sources: Cash flow methodology is largely based on dutch economic models and spreadsheets developed by Energie Centrum Nederland (ECN, www.ecn.nl)
Version: 2012.1

Reproduces:
  - subsurface capex (well drilling cost scaling + stimulation + pumps)
  - surface heat-plant capex
  - annual cash flows over the project lifetime (revenue, opex, depreciation,
    debt amortization, tax)
  - debt/equity financed NPV, discounted at the required equity return
  - LCOE solved as the flat €/GJ price that makes the equity investor's NPV
    equal to their equity outlay

Section "System-level cost" (bottom of this file) was added for the heating + cooling
system study: it prices a finished design with the SAME cash-flow engine and returns ONE
LCOE for the whole system (heat + cooling together).

"""

import numpy as np
from dataclasses import dataclass

# ---------------------------------------------------------------------
# Financial helpers
# ---------------------------------------------------------------------

def npv(rate, cashflows):
    """Excel NPV convention: first cashflow occurs at the end of the first period"""
    cashflows = np.asarray(cashflows, dtype=float)
    periods = np.arange(1, len(cashflows) + 1)
    return np.sum(cashflows / (1 + rate) ** periods)


def loan_amortization_schedule(rate, nper, principal):
    """
    Returns (interest, principal_payment) arrays, length nper, following
    Excel's IPMT/PPMT sign convention (values are negative = cash outflow).
    Constant total payment (fixed-rate annuity), fv=0, type=0.
    """
    if nper <= 0 or principal <= 0:
        return np.zeros(max(nper, 0)), np.zeros(max(nper, 0))

    if rate == 0:
        pmt = -principal / nper
    else:
        pmt = -principal * rate / (1 - (1 + rate) ** (-nper))

    interest = np.zeros(nper)
    principal_paid = np.zeros(nper)
    balance = principal
    for t in range(nper):
        interest[t] = -balance * rate
        principal_paid[t] = pmt - interest[t]
        balance += principal_paid[t]
    return interest, principal_paid


# ---------------------------------------------------------------------
# Capex building blocks
# ---------------------------------------------------------------------

def well_cost_mln(depth_m, well_cost_scaling=1.0):
    """
    Drilling cost per well, mln euro.
    Uses the TNO ThermoGIS (2019) Dutch-calibrated formula:
        well capex = 375,000 + 1150*d + 0.3*d^2   (euro, d = depth in m)
    (Vrijlandt et al., "ThermoGIS update", European Geothermal Congress 2019.)
    well_cost_scaling allows scaling up/down for a specific site if needed;
    defaults to 1.0.
    """
    return well_cost_scaling * (375_000 + 1150 * depth_m + 0.3 * depth_m ** 2) * 1e-6

def subsurface_capex_mln(depth_m, n_wells, well_cost_scaling=1.0,
                          stim_cost_per_well_mln=0.0,
                          pump_investment_mln=0.3, n_pumps=None):
    """Total subsurface capex, mln euro"""
    if n_pumps is None:
        n_pumps = n_wells
    wc = well_cost_mln(depth_m, well_cost_scaling)
    return (stim_cost_per_well_mln + wc) * n_wells + pump_investment_mln * n_pumps

def payback_period(equity_amount, net_revenue_series, discount_rate=None):
    """
    Simple payback: first year cumulative net revenue >= equity invested.
    If discount_rate is given, computes discounted payback instead.
    Returns years (float, interpolated within the crossing year) or None if never recovered.
    """
    cashflows = np.asarray(net_revenue_series, dtype=float)
    if discount_rate is not None:
        periods = np.arange(1, len(cashflows) + 1)
        cashflows = cashflows / (1 + discount_rate) ** periods

    cumulative = np.cumsum(cashflows)
    recovered = cumulative >= equity_amount

    if not recovered.any():
        return None 

    year_index = np.argmax(recovered) 
    prev_cum = cumulative[year_index - 1] if year_index > 0 else 0
    fraction = (equity_amount - prev_cum) / (cumulative[year_index] - prev_cum)
    return year_index + fraction

# ---------------------------------------------------------------------
# System-level cost
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class CostParams:
    """All cost assumptions of the system study. Override with dataclasses.replace(CostParams(), esc=1.0)."""
    stim_cost_per_well_mln: float = 0.25   # mln EUR per well (0.5 mln for both wells of a doublet)
    C_surf_base: float = 3e6               # EUR per doublet, surface installation base cost
    C_surf_kw: float = 300.0               # EUR per kW installed thermal power
    contingency: float = 0.15              # on wells + pumps + surface installation
    opex_kw: float = 60.0                  # EUR per kW per year
    opex_mwh: float = 1.9                  # EUR per MWh geothermal heat (0.19 ct/kWh)
    C_hp_kw: float = 200.0                 # EUR per kW heat pump capex
    opex_hp_kw: float = 20.0               # EUR per kW per year heat pump opex
    price_el: float = 80.0                 # EUR/MWh electricity (ThermoGIS: 8 ct/kWh)

    lifetime: int = 30
    depreciation_time: int = 15
    term_loan: int = 15
    loan_rate: float = 0.05
    equity_return: float = 0.07
    equity_share: float = 0.2
    tax: float = 0.25
    inflation: float = 0.02

    pump_investment_mln: float = 0.3       # mln EUR per well pump. Set 0 if surface cost already covers pumps
    pump_replace_interval: int = 5         # years between pump replacements

    esc: float = 1.25                      # escalation 2019 -> 2026 on wells and surface plant
    price_gas: float = 60.0                # EUR/MWh heat from the backup boiler (fuel)
    C_boiler_MW: float = 0.1e6             # EUR per MW backup boiler
    C_ch_MW: float = 0.3e6                 # EUR per MW electric chiller plant (no escalation applied)
    # ---- ATES cooling option ----
    C_ates_kW: float = 300.0               # EUR per kW installed capacity, Herrmann et al. 2025 (> 2 MW)
    ates_esc: float = 1.0                  # > 1 if the benchmark is in older prices
    ates_contingency: float = 0.0
    opex_ates: float = 0.03                # fraction of ATES capex per year (2-5%, Dutch HT-ATES factsheet)


def _timeline(p):
    """Years 1..n, a mask for the operating years, and the inflation factor of each year."""
    n = max(p.lifetime, p.term_loan, p.depreciation_time)
    years = np.arange(1, n + 1)
    return years, years <= p.lifetime, (1 + p.inflation) ** (years - 1)


def _net_cash_flow(capex_eur, fixed_opex_eur, energy_cost_eur, pump_replace_eur, income, p):
    """Cash flow to the equity investor, years 1..n. `income` is zeros when solving for the LCOE."""
    years, active, infl = _timeline(p)
    opex = np.where(active, -(fixed_opex_eur + energy_cost_eur) * infl, 0.0)
    pump = np.where(active & (years % p.pump_replace_interval == 0), -pump_replace_eur * infl, 0.0)
    gross = income + opex + pump

    equity = p.equity_share * capex_eur
    loan = capex_eur - equity
    interest_s, principal_s = loan_amortization_schedule(p.loan_rate, p.term_loan, loan)
    interest, principal = np.zeros(len(years)), np.zeros(len(years))
    interest[:len(interest_s)], principal[:len(principal_s)] = interest_s, principal_s

    depreciation = np.where(years <= p.depreciation_time, -capex_eur / p.depreciation_time, 0.0)
    tax_paid = -p.tax * (gross + depreciation + interest)
    return gross + interest + principal + tax_paid, equity


def _price_project(capex_eur, fixed_opex_eur, energy_cost_eur, pump_replace_eur, energy_GJ, p):
    """Flat price in EUR/GJ that makes the equity investor's NPV equal to the equity outlay."""
    years, active, infl = _timeline(p)
    net, equity = _net_cash_flow(capex_eur, fixed_opex_eur, energy_cost_eur, pump_replace_eur,
                                 np.zeros(len(years)), p)
    energy_after_tax = np.where(active, (1 - p.tax) * energy_GJ, 0.0)
    return (equity - npv(p.equity_return, net)) / npv(p.equity_return, energy_after_tax)


def system_cost(D, p=None, sell_price=None, price_indexed=True):
    """
    Price a finished design and return ONE LCOE for the whole system (heat + cooling).

    D is the dict returned by design_system() in the notebook. Keys used:
      wells (dict of well dicts with "Depth"), stim, hp, cooling ("electric" or "ates"),
      P_wells_MW, backup_MW, chiller_MW, cool_MW,
      E_wells, E_gas, E_heat, E_cool (MWh/yr), el_wells, el_cool (MWh/yr).
    """
    p = p or CostParams()
    n = len(D["wells"])
    P_w = D["P_wells_MW"]

    # ---- capex (EUR), all spent in year 0 ----
    wells_pumps = 1e6 * sum(subsurface_capex_mln(w["Depth"], 2, p.esc, 0.0, p.pump_investment_mln)
                            for w in D["wells"].values())
    surface = p.esc * (n * p.C_surf_base + p.C_surf_kw * P_w * 1000)
    stim = n * 2 * p.stim_cost_per_well_mln * 1e6 if D["stim"] else 0.0
    cap_geo = (wells_pumps + surface) * (1 + p.contingency) + stim \
              + (p.C_hp_kw * P_w * 1000 if D["hp"] else 0.0)
    cap_backup = p.C_boiler_MW * D["backup_MW"]
    if D["cooling"] == "ates":
        cap_cool = p.ates_esc * p.C_ates_kW * D["cool_MW"] * 1000 * (1 + p.ates_contingency)
    else:
        cap_cool = p.C_ch_MW * D["chiller_MW"]
    capex = cap_geo + cap_backup + cap_cool

    # ---- yearly costs in year-1 money (inflated inside the engine) ----
    fixed_opex = (p.opex_kw * P_w * 1000 + p.opex_mwh * D["E_wells"]
                  + (p.opex_hp_kw * P_w * 1000 if D["hp"] else 0.0)
                  + (p.opex_ates * cap_cool if D["cooling"] == "ates" else 0.0))
    energy_cost = p.price_el * (D["el_wells"] + D["el_cool"]) + p.price_gas * D["E_gas"]
    pump_replace = n * 2 * p.pump_investment_mln * 1e6

    useful_MWh = D["E_heat"] + D["E_cool"]                       # all useful energy, heat + cooling
    lcoe_GJ = _price_project(capex, fixed_opex, energy_cost, pump_replace, useful_MWh * 3.6, p)
    lcoe_MWh = lcoe_GJ * 3.6

    payback = {}
    if sell_price is not None:
        years, active, infl = _timeline(p)
        income = np.where(active, sell_price * useful_MWh * (infl if price_indexed else 1.0), 0.0)
        net, equity = _net_cash_flow(capex, fixed_opex, energy_cost, pump_replace, income, p)
        payback = dict(payback_years=payback_period(equity, net),
                       payback_discounted_years=payback_period(equity, net, discount_rate=p.equity_return))

    return dict(
        **payback,
        capex_M=capex / 1e6,
        annual_M=lcoe_MWh * useful_MWh / 1e6,                    # flat revenue needed per year (nominal)
        useful_GWh=useful_MWh / 1e3,
        LCOE_system=lcoe_MWh,                                    # EUR/MWh of heat + cooling
        LCOE_eur_per_GJ=lcoe_GJ,
        equity_M=p.equity_share * capex / 1e6,
        capex_split_M=dict(geothermal=cap_geo / 1e6, backup=cap_backup / 1e6, cooling=cap_cool / 1e6),
        year1_costs_M=dict(fixed_opex=fixed_opex / 1e6, energy=energy_cost / 1e6),
    )

def cost_breakdown(D, p=None):
    """Capex items (M EUR) and the LCOE split (EUR/MWh). The split adds up exactly to LCOE_system."""
    p = p or CostParams()
    n, P_w = len(D["wells"]), D["P_wells_MW"]

    wells = 1e6 * sum(2 * well_cost_mln(w["Depth"], p.esc) for w in D["wells"].values())
    pumps = n * 2 * p.pump_investment_mln * 1e6
    surface = p.esc * (n * p.C_surf_base + p.C_surf_kw * P_w * 1000)
    contingency = p.contingency * (wells + pumps + surface)
    stim = n * 2 * p.stim_cost_per_well_mln * 1e6 if D["stim"] else 0.0
    heat_pump = p.C_hp_kw * P_w * 1000 if D["hp"] else 0.0
    backup = p.C_boiler_MW * D["backup_MW"]
    if D["cooling"] == "ates":
        cooling = p.ates_esc * p.C_ates_kW * D["cool_MW"] * 1000 * (1 + p.ates_contingency)
    else:
        cooling = p.C_ch_MW * D["chiller_MW"]
    items = dict(wells=wells, pumps=pumps, surface=surface, contingency=contingency,
                 stimulation=stim, heat_pump=heat_pump, backup_boiler=backup, cooling_plant=cooling)
    capex = sum(items.values())

    fixed_opex = (p.opex_kw * P_w * 1000 + p.opex_mwh * D["E_wells"]
                  + (p.opex_hp_kw * P_w * 1000 if D["hp"] else 0.0)
                  + (p.opex_ates * cooling if D["cooling"] == "ates" else 0.0))
    electricity = p.price_el * (D["el_wells"] + D["el_cool"])
    gas = p.price_gas * D["E_gas"]
    pump_replace = n * 2 * p.pump_investment_mln * 1e6

    years, active, infl = _timeline(p)
    useful_GJ = (D["E_heat"] + D["E_cool"]) * 3.6
    energy_after_tax = np.where(active, (1 - p.tax) * useful_GJ, 0.0)

    def part(capex_, fixed_, energy_, pump_):
        net, equity = _net_cash_flow(capex_, fixed_, energy_, pump_, np.zeros(len(years)), p)
        return 3.6 * (equity - npv(p.equity_return, net)) / npv(p.equity_return, energy_after_tax)

    split = {"Capital (wells, plant, financing)": part(capex, 0, 0, 0),
             "Fixed O&M": part(0, fixed_opex, 0, 0),
             "Electricity": part(0, 0, electricity, 0),
             "Backup gas": part(0, 0, gas, 0),
             "Pump replacement": part(0, 0, 0, pump_replace)}
    return dict(capex_M={k: v / 1e6 for k, v in items.items()}, lcoe_split=split)

def baseline_cost(E_heat, E_cool, heat_peak, cool_peak, COP_ch, p=None):
    """LCOE (EUR/MWh) of the reference system: gas boiler for heat + electric chillers for cooling,
    priced with the same cash-flow engine."""
    p = p or CostParams()
    capex = p.C_boiler_MW * heat_peak + p.C_ch_MW * cool_peak
    energy_cost = p.price_gas * E_heat + p.price_el * E_cool / COP_ch
    return 3.6 * _price_project(capex, 0.0, energy_cost, 0.0, (E_heat + E_cool) * 3.6, p)
