"""
Shared Analytics & Financial Engine for Dubai Real Estate Intelligence (2020-2026).
Provides authoritative calculations, financial modeling, unit conversions, and statistical utilities
shared across the Streamlit intelligence platform and Jupyter analytical notebook.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats

# ----------------- CONSTANTS & CONVERSIONS -----------------
AED_PEG: float = 3.6725
SQFT_TO_M2: float = 0.092903
M2_TO_SQFT: float = 1.0 / SQFT_TO_M2
DLD_TRANSFER_FEE_PCT: float = 0.04  # 4% Dubai Land Department standard purchase transfer fee


def convert_currency(usd_amount: float | np.ndarray, to_aed: bool = False) -> float | np.ndarray:
    """Convert USD amount to AED if requested, or keep in USD."""
    mult = AED_PEG if to_aed else 1.0
    return usd_amount * mult


def convert_area(area_sqft: float | np.ndarray, to_m2: bool = False) -> float | np.ndarray:
    """Convert square feet to square meters if requested."""
    factor = SQFT_TO_M2 if to_m2 else 1.0
    return area_sqft * factor


def convert_rate(usd_per_sqft: float | np.ndarray, to_aed: bool = False, to_m2: bool = False) -> float | np.ndarray:
    """Convert USD/sqft to target currency and area unit."""
    curr_mult = AED_PEG if to_aed else 1.0
    area_factor = M2_TO_SQFT if to_m2 else 1.0
    return usd_per_sqft * curr_mult * area_factor


def format_currency(usd_val: float, currency: str = "USD", compact: bool = False) -> str:
    """Format numeric monetary value cleanly with proper symbol and compact notation."""
    if pd.isna(usd_val) or usd_val is None:
        return "N/A"
    is_aed = "AED" in currency.upper()
    val = usd_val * (AED_PEG if is_aed else 1.0)
    sym = "AED " if is_aed else "$"
    
    if compact:
        if abs(val) >= 1_000_000:
            return f"{sym}{val/1_000_000:.2f}M"
        elif abs(val) >= 1_000:
            return f"{sym}{val/1_000:.1f}k"
    return f"{sym}{val:,.0f}"


def format_rate(usd_per_sqft: float, currency: str = "USD", unit: str = "sqft") -> str:
    """Format price per area rate."""
    if pd.isna(usd_per_sqft) or usd_per_sqft is None:
        return "N/A"
    is_aed = "AED" in currency.upper()
    is_m2 = "M" in unit.upper() or "M²" in unit.upper()
    rate = convert_rate(usd_per_sqft, to_aed=is_aed, to_m2=is_m2)
    sym = "AED " if is_aed else "$"
    unit_label = "m²" if is_m2 else "sqft"
    return f"{sym}{rate:,.0f}/{unit_label}"


# ----------------- FINANCIAL & CASH-FLOW MODELING -----------------
def calculate_mortgage_emi(loan_amount_usd: float, annual_rate_pct: float, tenor_years: int) -> float:
    """
    Compute standard monthly Equated Monthly Installment (EMI) for real estate financing.
    Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    """
    if loan_amount_usd <= 0 or annual_rate_pct <= 0 or tenor_years <= 0:
        return 0.0
    r = (annual_rate_pct / 100.0) / 12.0
    n = tenor_years * 12
    emi = loan_amount_usd * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return float(emi)


def simulate_buy_to_let_cashflow(
    purchase_price_usd: float,
    annual_rent_usd: float,
    property_size_sqft: float,
    down_payment_pct: float = 25.0,
    mortgage_rate_pct: float = 5.25,
    loan_tenor_years: int = 25,
    service_charge_usd_per_sqft: float = 4.0,
    vacancy_maintenance_pct: float = 5.0,
) -> dict[str, float | None]:
    """
    Authoritative buy-to-let cash-flow and investment return simulator.
    Accounts for operational service charges, maintenance & vacancy leakage, and 4% DLD transfer fee.
    """
    down_pct = max(0.0, min(100.0, down_payment_pct))
    loan_amount_usd = purchase_price_usd * (1.0 - down_pct / 100.0)
    monthly_emi_usd = calculate_mortgage_emi(loan_amount_usd, mortgage_rate_pct, loan_tenor_years)
    annual_mortgage_usd = monthly_emi_usd * 12.0
    
    # Operational income & expenses
    effective_rent_usd = annual_rent_usd * (1.0 - (vacancy_maintenance_pct / 100.0))
    annual_service_charge_usd = service_charge_usd_per_sqft * property_size_sqft
    net_operating_income_usd = effective_rent_usd - annual_service_charge_usd
    net_annual_cashflow_usd = net_operating_income_usd - annual_mortgage_usd
    
    # Investment returns
    gross_yield_pct = (annual_rent_usd / purchase_price_usd * 100.0) if purchase_price_usd > 0 else 0.0
    net_yield_pct = (net_operating_income_usd / purchase_price_usd * 100.0) if purchase_price_usd > 0 else 0.0
    
    # Capital required (Equity + 4% DLD registration fee)
    initial_equity_usd = purchase_price_usd * (down_pct / 100.0) + (purchase_price_usd * DLD_TRANSFER_FEE_PCT)
    cash_on_cash_pct = (net_annual_cashflow_usd / initial_equity_usd * 100.0) if initial_equity_usd > 0 else 0.0
    payback_years = (initial_equity_usd / net_annual_cashflow_usd) if net_annual_cashflow_usd > 0 else None
    
    return {
        'loan_amount_usd': loan_amount_usd,
        'monthly_emi_usd': monthly_emi_usd,
        'annual_mortgage_usd': annual_mortgage_usd,
        'effective_rent_usd': effective_rent_usd,
        'annual_service_charge_usd': annual_service_charge_usd,
        'net_operating_income_usd': net_operating_income_usd,
        'net_annual_cashflow_usd': net_annual_cashflow_usd,
        'gross_yield_pct': gross_yield_pct,
        'net_yield_pct': net_yield_pct,
        'initial_equity_usd': initial_equity_usd,
        'cash_on_cash_pct': cash_on_cash_pct,
        'payback_years': payback_years
    }


# ----------------- STATISTICAL & GEOGRAPHIC UTILITIES -----------------
def compute_distance_decay(
    df: pd.DataFrame,
    dist_col: str,
    price_col: str = 'price_per_sqft_usd',
    bin_width: float = 2.0,
    max_dist: float = 35.0,
    min_count: int = 30
) -> pd.DataFrame:
    """Aggregate median price decay curves with count thresholds to eliminate thin-volume tail noise."""
    bins = np.arange(0, max_dist + bin_width, bin_width)
    df_clean = df.dropna(subset=[dist_col, price_col]).copy()
    df_clean['bin'] = pd.cut(df_clean[dist_col], bins=bins)
    
    agg = df_clean.groupby('bin', observed=False)[price_col].agg(['median', 'count', 'mean']).reset_index()
    agg['dist_mid'] = agg['bin'].apply(lambda x: x.mid if pd.notna(x) else np.nan)
    agg = agg[agg['count'] >= min_count].dropna(subset=['dist_mid'])
    return agg.sort_values('dist_mid')


def compute_rental_contract_seasonality(rentals_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Analyze short-term vs yearly rental dynamics by month.
    Returns monthly comparison dataframe and key summary statistics.
    """
    df = rentals_df.copy()
    if 'date_listed' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['date_listed']):
        df['date_listed'] = pd.to_datetime(df['date_listed'])
        
    df['month'] = df['date_listed'].dt.to_period('M')
    
    monthly_grp = df.groupby(['month', 'contract_type'])['rent_per_sqft_usd'].median().reset_index()
    monthly_grp['month_dt'] = monthly_grp['month'].dt.to_timestamp()
    
    short = monthly_grp[monthly_grp['contract_type'] == 'short_term'].rename(columns={'rent_per_sqft_usd': 'short_term_rate'})
    yearly = monthly_grp[monthly_grp['contract_type'] == 'yearly'].rename(columns={'rent_per_sqft_usd': 'yearly_rate'})
    
    comp = pd.merge(short[['month_dt', 'short_term_rate']], yearly[['month_dt', 'yearly_rate']], on='month_dt').sort_values('month_dt')
    comp['premium_pct'] = ((comp['short_term_rate'] - comp['yearly_rate']) / comp['yearly_rate']) * 100.0
    comp['premium_ma3'] = comp['premium_pct'].rolling(window=3, min_periods=1).mean()
    comp['premium_ma12'] = comp['premium_pct'].rolling(window=12, min_periods=1).mean()
    
    stats_dict = {
        'mean_premium_pct': float(comp['premium_pct'].mean()),
        'median_premium_pct': float(comp['premium_pct'].median()),
        'max_premium_pct': float(comp['premium_pct'].max()),
        'min_premium_pct': float(comp['premium_pct'].min()),
    }
    return comp, stats_dict


def compute_community_freehold_test(area_prices_df: pd.DataFrame) -> dict[str, float | int]:
    """
    Run cross-sectional statistical hypothesis test on community medians to avoid panel autocorrelation bias.
    """
    df = area_prices_df.dropna(subset=['secondary_price_per_sqft_usd', 'is_freehold']).copy()
    comm_summary = df.groupby(['community', 'is_freehold'])['secondary_price_per_sqft_usd'].median().reset_index()
    
    fh_comm = comm_summary[comm_summary['is_freehold'] == True]['secondary_price_per_sqft_usd']
    nfh_comm = comm_summary[comm_summary['is_freehold'] == False]['secondary_price_per_sqft_usd']
    
    t_stat, t_pval = stats.ttest_ind(fh_comm, nfh_comm, equal_var=False)
    u_stat, u_pval = stats.mannwhitneyu(fh_comm, nfh_comm, alternative='two-sided')
    
    return {
        'n_freehold': len(fh_comm),
        'n_non_freehold': len(nfh_comm),
        'fh_median': float(fh_comm.median()),
        'nfh_median': float(nfh_comm.median()),
        'fh_mean': float(fh_comm.mean()),
        'nfh_mean': float(nfh_comm.mean()),
        'welch_t_stat': float(t_stat),
        'welch_p_val': float(t_pval),
        'mann_whitney_u': float(u_stat),
        'mann_whitney_p_val': float(u_pval)
    }
