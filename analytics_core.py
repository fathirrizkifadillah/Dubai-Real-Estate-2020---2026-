"""
Shared Analytics & Financial Engine for Dubai Real Estate Intelligence (2020-2026).
Provides authoritative calculations, financial modeling, unit conversions, and statistical utilities
shared across the Streamlit intelligence platform and Jupyter analytical notebook.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import cdist

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


# ----------------- ADVANCED FEATURE ENGINEERING & ECONOMETRICS -----------------
def engineer_secondary_features(df_sec: pd.DataFrame, df_rentals: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Enrich secondary sales transactions with domain-specific engineering:
    - property_age: depreciation horizon in desert climate
    - floor_ratio & is_penthouse_tier: vertical elevation premium
    - is_golden_visa_tier: post-Oct 2022 AED 2M ($544,500) residency threshold
    - implied_gross_yield_pct: cross-table fundamental cap rate synthesis
    """
    df = df_sec.copy()
    if 'date_listed' in df.columns:
        dates = pd.to_datetime(df['date_listed'], errors='coerce')
        df['listing_year'] = dates.dt.year.fillna(2023).astype(int)
    else:
        df['listing_year'] = 2023

    # Property age & brand new indicator
    if 'year_built' in df.columns:
        df['property_age'] = (df['listing_year'] - df['year_built']).clip(lower=0, upper=50)
        df['is_brand_new'] = (df['property_age'] <= 1).astype(int)
    else:
        df['property_age'] = 5
        df['is_brand_new'] = 0

    # Vertical elevation & floor ratio
    is_villa = df['property_category'].str.lower() == 'villa' if 'property_category' in df.columns else False
    floor_clean = np.where(is_villa, 0, df['floor'].fillna(3)) if 'floor' in df.columns else np.zeros(len(df))
    total_floors_clean = np.where(is_villa, 2, df['total_floors'].fillna(10)) if 'total_floors' in df.columns else np.ones(len(df)) * 10
    
    total_floors_clean = np.where(total_floors_clean <= 0, 1, total_floors_clean)
    df['floor_ratio'] = (floor_clean / total_floors_clean).clip(0.0, 1.0)
    df['is_penthouse_tier'] = ((floor_clean >= (total_floors_clean - 2)) & (floor_clean >= 15)).astype(int)

    # Golden Visa eligibility flag
    if 'price_usd' in df.columns:
        df['is_golden_visa_tier'] = ((df['price_usd'] >= 544500) & (df['listing_year'] >= 2022)).astype(int)

    # Cross-table rental synthesis
    if df_rentals is not None and 'area_sqft' in df.columns and 'price_usd' in df.columns:
        rent = df_rentals.copy()
        if 'annual_rent_usd' in rent.columns and 'area_sqft' in rent.columns:
            rent['rent_per_sqft'] = rent['annual_rent_usd'] / rent['area_sqft'].replace(0, np.nan)
            zone_rent_map = rent.groupby(['zone', 'bedrooms'])['rent_per_sqft'].median().to_dict()
            global_rent = rent['rent_per_sqft'].median()
            
            tuples = list(zip(df['zone'], df['bedrooms']))
            df['zone_rent_sqft'] = pd.Series(tuples, index=df.index).map(zone_rent_map).fillna(global_rent)
            df['implied_gross_yield_pct'] = (df['zone_rent_sqft'] * df['area_sqft'] / df['price_usd'].replace(0, np.nan) * 100.0).clip(0.0, 25.0)

    return df


def engineer_offplan_features(df_off: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich off-plan listings with developer pipeline and handover risk dimensions.
    """
    df = df_off.copy()
    if 'date_listed' in df.columns:
        dates = pd.to_datetime(df['date_listed'], errors='coerce')
        df['listing_year'] = dates.dt.year.fillna(2023).astype(int)
    else:
        df['listing_year'] = 2023

    if 'handover_year' in df.columns and 'launch_year' in df.columns:
        df['construction_lead_time'] = (df['handover_year'] - df['launch_year']).clip(lower=0, upper=12)
        df['years_to_handover'] = (df['handover_year'] - df['listing_year']).clip(lower=0, upper=10)
    else:
        df['construction_lead_time'] = 3
        df['years_to_handover'] = 2

    if 'total_project_units' in df.columns:
        med_units = df['total_project_units'].median()
        df['log_project_units'] = np.log1p(df['total_project_units'].fillna(med_units))

    if 'price_usd' in df.columns:
        df['is_golden_visa_tier'] = ((df['price_usd'] >= 544500) & (df['listing_year'] >= 2022)).astype(int)

    return df


def compute_spatial_moran_i(
    df: pd.DataFrame,
    value_col: str = 'price_per_sqft_usd',
    group_col: str = 'zone',
    n_permutations: int = 999
) -> dict[str, float | int]:
    """
    Calculate Global Moran's I spatial autocorrelation coefficient with Monte Carlo permutation testing.
    Proves whether geographic pricing clusters systematically across Dubai districts.
    """
    zone_geo = df.groupby(group_col).agg(
        val=(value_col, 'median'),
        lat=('lat', 'mean'),
        lon=('lon', 'mean'),
        cnt=('id', 'count') if 'id' in df.columns else (value_col, 'count')
    ).reset_index()

    zone_geo = zone_geo[zone_geo['cnt'] >= 15].dropna()
    coords = zone_geo[['lat', 'lon']].values
    vals = zone_geo['val'].values
    n = len(vals)

    if n < 5:
        return {'error': 'Insufficient spatial zones for Moran analysis'}

    dist_mat = cdist(coords, coords, metric='euclidean')
    np.fill_diagonal(dist_mat, np.inf)
    W = 1.0 / dist_mat
    row_sums = W.sum(axis=1, keepdims=True)
    W_std = W / row_sums

    z = vals - vals.mean()
    s0 = W_std.sum()
    numerator = np.sum(W_std * np.outer(z, z))
    denominator = np.sum(z**2)
    moran_i = float((n / s0) * (numerator / denominator))
    expected_i = float(-1.0 / (n - 1))

    # Monte Carlo permutation test
    perm_dist = []
    np.random.seed(42)
    for _ in range(n_permutations):
        z_perm = np.random.permutation(z)
        num_p = np.sum(W_std * np.outer(z_perm, z_perm))
        perm_dist.append((n / s0) * (num_p / denominator))

    perm_dist = np.array(perm_dist)
    p_val = float((np.sum(perm_dist >= moran_i) + 1) / (len(perm_dist) + 1))
    z_score = float((moran_i - perm_dist.mean()) / (perm_dist.std() + 1e-9))

    return {
        'n_zones': n,
        'moran_i': moran_i,
        'expected_i': expected_i,
        'z_score': z_score,
        'pseudo_p_val': p_val,
        'is_spatially_clustered': p_val < 0.05 and moran_i > expected_i
    }


def run_hedonic_price_decomposition(df_sec: pd.DataFrame, sample_size: int = 10000, random_state: int = 42) -> dict:
    """
    Fit an econometric log-linear hedonic regression model via statsmodels OLS to decompose marginal
    price elasticity of physical, spatial, and institutional attributes.
    """
    import statsmodels.api as sm

    df = df_sec.dropna(subset=['price_usd', 'area_sqft', 'bedrooms', 'to_burj_khalifa_km', 'metro_distance_min', 'property_age', 'floor_ratio']).copy()
    df = df[(df['price_usd'] >= 50000) & (df['area_sqft'] >= 200) & (df['area_sqft'] <= 15000)]
    
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=random_state)

    df['log_price'] = np.log(df['price_usd'])
    df['log_area'] = np.log(df['area_sqft'])
    df['is_freehold_num'] = df['is_freehold'].astype(float) if 'is_freehold' in df.columns else 1.0

    view_dummies = pd.get_dummies(df['view'], prefix='view', drop_first=True, dtype=float) if 'view' in df.columns else pd.DataFrame(index=df.index)

    base_cols = ['log_area', 'bedrooms', 'to_burj_khalifa_km', 'metro_distance_min', 'property_age', 'floor_ratio', 'is_freehold_num', 'is_brand_new', 'is_penthouse_tier']
    X = pd.concat([df[base_cols], view_dummies], axis=1).astype(float)
    X = sm.add_constant(X)
    y = df['log_price'].astype(float)

    model = sm.OLS(y, X).fit()

    return {
        'rsquared': float(model.rsquared),
        'rsquared_adj': float(model.rsquared_adj),
        'fvalue': float(model.fvalue),
        'pvalues': model.pvalues.to_dict(),
        'params': model.params.to_dict(),
        'summary_str': str(model.summary())
    }


def compute_supply_pipeline_analysis(df_off: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Examine developer off-plan delivery timelines (2024-2028+) to identify supply concentration risks.
    """
    df = df_off.dropna(subset=['handover_year', 'price_per_sqft_usd']).copy()
    pipeline_yr = df.groupby('handover_year').agg(
        listings_count=('id', 'count') if 'id' in df.columns else ('price_per_sqft_usd', 'count'),
        mean_sqft_rate=('price_per_sqft_usd', 'mean'),
        median_price_usd=('price_usd', 'median')
    ).reset_index()

    comm_pipeline = df.groupby('community').agg(
        total_listings=('id', 'count') if 'id' in df.columns else ('price_per_sqft_usd', 'count'),
        median_handover=('handover_year', 'median'),
        median_rate_usd=('price_per_sqft_usd', 'median')
    ).sort_values('total_listings', ascending=False).head(10).reset_index()

    return pipeline_yr, comm_pipeline


# ----------------- DECISION SUPPORT SYSTEM (DSS) & PORTFOLIO ENGINE -----------------
def stress_test_cashflow(
    purchase_price_usd: float,
    annual_rent_usd: float,
    property_size_sqft: float,
    base_mortgage_rate_pct: float = 5.25,
    rate_shock_bps: float = 150.0,
    base_vacancy_pct: float = 5.0,
    rental_correction_pct: float = 10.0,
    down_payment_pct: float = 25.0,
    loan_tenor_years: int = 25,
    service_charge_usd_per_sqft: float = 4.0,
) -> dict[str, float | str]:
    """
    Simulate adverse macroeconomic shocks on buy-to-let property investments.
    Computes Debt Service Coverage Ratio (DSCR), net cash-flow delta, and stress resilience verdict.
    """
    down_pct = max(0.0, min(100.0, down_payment_pct))
    loan_amount_usd = purchase_price_usd * (1.0 - down_pct / 100.0)
    initial_equity_usd = purchase_price_usd * (down_pct / 100.0) + (purchase_price_usd * DLD_TRANSFER_FEE_PCT)
    annual_service_charge_usd = service_charge_usd_per_sqft * property_size_sqft

    # --- BASE CASE ---
    base_emi = calculate_mortgage_emi(loan_amount_usd, base_mortgage_rate_pct, loan_tenor_years)
    base_annual_mortgage = base_emi * 12.0
    base_eff_rent = annual_rent_usd * (1.0 - (base_vacancy_pct / 100.0))
    base_noi = base_eff_rent - annual_service_charge_usd
    base_annual_cf = base_noi - base_annual_mortgage
    base_dscr = (base_noi / base_annual_mortgage) if base_annual_mortgage > 0 else 999.0
    base_coc_pct = (base_annual_cf / initial_equity_usd * 100.0) if initial_equity_usd > 0 else 0.0

    # --- STRESSED CASE ---
    stressed_rate = base_mortgage_rate_pct + (rate_shock_bps / 100.0)
    stressed_emi = calculate_mortgage_emi(loan_amount_usd, stressed_rate, loan_tenor_years)
    stressed_annual_mortgage = stressed_emi * 12.0
    stressed_rent = annual_rent_usd * (1.0 - (rental_correction_pct / 100.0))
    stressed_eff_rent = stressed_rent * (1.0 - (base_vacancy_pct / 100.0))
    stressed_noi = stressed_eff_rent - annual_service_charge_usd
    stressed_annual_cf = stressed_noi - stressed_annual_mortgage
    stressed_dscr = (stressed_noi / stressed_annual_mortgage) if stressed_annual_mortgage > 0 else 999.0
    stressed_coc_pct = (stressed_annual_cf / initial_equity_usd * 100.0) if initial_equity_usd > 0 else 0.0

    # Breakeven rental drop under base mortgage
    # NOI = eff_rent - sc = base_annual_mortgage => eff_rent = base_annual_mortgage + sc
    # rent * (1 - vac) = base_annual_mortgage + sc => rent_be = (base_annual_mortgage + sc) / (1 - vac)
    vac_mult = (1.0 - (base_vacancy_pct / 100.0))
    if vac_mult > 0 and annual_rent_usd > 0:
        rent_breakeven_usd = (base_annual_mortgage + annual_service_charge_usd) / vac_mult
        breakeven_drop_pct = max(0.0, ((annual_rent_usd - rent_breakeven_usd) / annual_rent_usd) * 100.0)
    else:
        breakeven_drop_pct = 0.0

    # Institutional Risk Verdict
    if stressed_dscr >= 1.25 and stressed_annual_cf > 0:
        risk_verdict = "Resilient (Low Risk)"
        verdict_color = "#10b981"
        action_directive = "High debt-service buffer; resistant to aggressive rate cycles."
    elif stressed_dscr >= 1.00 and stressed_annual_cf >= 0:
        risk_verdict = "Marginal Buffer (Moderate Risk)"
        verdict_color = "#f59e0b"
        action_directive = "Cash flow remains positive but sensitive; consider higher initial down-payment."
    else:
        risk_verdict = "Cash Deficit Warning (High Risk)"
        verdict_color = "#ef4444"
        action_directive = "Stressed debt service exceeds net rental income; capital injection required."

    return {
        'initial_equity_usd': initial_equity_usd,
        'loan_amount_usd': loan_amount_usd,
        'base_mortgage_rate_pct': base_mortgage_rate_pct,
        'base_monthly_emi_usd': base_emi,
        'base_annual_mortgage_usd': base_annual_mortgage,
        'base_noi_usd': base_noi,
        'base_annual_cashflow_usd': base_annual_cf,
        'base_dscr': base_dscr,
        'base_coc_pct': base_coc_pct,
        'stressed_rate_pct': stressed_rate,
        'stressed_monthly_emi_usd': stressed_emi,
        'stressed_annual_mortgage_usd': stressed_annual_mortgage,
        'stressed_noi_usd': stressed_noi,
        'stressed_annual_cashflow_usd': stressed_annual_cf,
        'stressed_dscr': stressed_dscr,
        'stressed_coc_pct': stressed_coc_pct,
        'cashflow_gap_usd': stressed_annual_cf - base_annual_cf,
        'dscr_gap': stressed_dscr - base_dscr,
        'breakeven_drop_pct': breakeven_drop_pct,
        'risk_verdict': risk_verdict,
        'verdict_color': verdict_color,
        'action_directive': action_directive
    }


def optimize_portfolio_allocation(
    total_capital_usd: float,
    risk_archetype: str,
    target_hold_years: int = 5,
) -> dict:
    """
    Institutional Multi-Asset Real Estate Portfolio Allocator.
    Deploys available investor capital across strategic Dubai real estate archetypes:
    - High Cash-Flow Yield Engine (Cluster 2: JVC, Al Furjan, Silicon Oasis)
    - Prime Capital Growth & Prestige (Cluster 0: Downtown, Palm Jumeirah, Marina)
    - Balanced Barbell Allocation (50/50 Split)
    """
    total_capital = max(100000.0, total_capital_usd)
    is_golden_visa = total_capital >= 544500.0  # AED 2M statutory requirement

    if "Cash-Flow" in risk_archetype:
        # High rental yield focus: higher cash-on-cash, lower capital appreciation
        cf_weight = 0.85
        cg_weight = 0.15
        annual_appreciation_pct = 3.5
        gross_yield_pct = 8.85
        net_yield_pct = 7.15
        description = "Prioritizes immediate quarterly dividend-style cash distributions through high-yielding transit corridor assets."
        recommended_assets = [
            {"Asset Type": "1-Bed Executive Apartment", "District Target": "Jumeirah Village Circle (JVC)", "Allocation Share": "45%", "Target Yield": "8.9% Gross", "Role": "High Cash Yield"},
            {"Asset Type": "2-Bed Family Apartment", "District Target": "Al Furjan / Discovery Gardens", "Allocation Share": "40%", "Target Yield": "8.6% Gross", "Role": "Stable Tenancy"},
            {"Asset Type": "Studio Liquidity Unit", "District Target": "Dubai Silicon Oasis", "Allocation Share": "15%", "Target Yield": "9.1% Gross", "Role": "High Liquidity"}
        ]
    elif "Capital Growth" in risk_archetype:
        # Prime luxury focus: lower rental yield, high capital appreciation & trophy prestige
        cf_weight = 0.15
        cg_weight = 0.85
        annual_appreciation_pct = 6.8
        gross_yield_pct = 5.60
        net_yield_pct = 4.25
        description = "Focuses on scarce prime waterfront and central downtown trophy assets with institutional exit liquidity."
        recommended_assets = [
            {"Asset Type": "2-Bed Waterfront Luxury", "District Target": "Dubai Marina / Palm Jumeirah", "Allocation Share": "55%", "Target Yield": "5.4% Gross", "Role": "Prime Capital Growth"},
            {"Asset Type": "1-Bed High-Floor Core", "District Target": "Downtown Dubai (Burj District)", "Allocation Share": "30%", "Target Yield": "5.8% Gross", "Role": "Institutional Flagship"},
            {"Asset Type": "Off-Plan Launch Unit", "District Target": "Dubai Hills Estate (Emaar)", "Allocation Share": "15%", "Target Yield": "6.2% Gross", "Role": "Capital Step-Up"}
        ]
    else:  # Balanced Barbell
        cf_weight = 0.50
        cg_weight = 0.50
        annual_appreciation_pct = 5.2
        gross_yield_pct = 7.20
        net_yield_pct = 5.70
        description = "Institutional Barbell approach balancing dependable rental cash distributions with premium capital growth."
        recommended_assets = [
            {"Asset Type": "2-Bed Core Apartment", "District Target": "Business Bay / Downtown Fringe", "Allocation Share": "40%", "Target Yield": "6.8% Gross", "Role": "Balanced Growth"},
            {"Asset Type": "1-Bed High-Yield Unit", "District Target": "Jumeirah Village Circle (JVC)", "Allocation Share": "35%", "Target Yield": "8.8% Gross", "Role": "Cash Flow Yield Anchor"},
            {"Asset Type": "Off-Plan Tier 1 Equity", "District Target": "Dubai Creek Harbour (Emaar)", "Allocation Share": "25%", "Target Yield": "6.5% Gross", "Role": "Development Appreciation"}
        ]

    # Projections
    annual_net_rental_usd = total_capital * (net_yield_pct / 100.0)
    cumulative_net_rental_usd = annual_net_rental_usd * target_hold_years
    terminal_asset_value_usd = total_capital * ((1.0 + (annual_appreciation_pct / 100.0)) ** target_hold_years)
    capital_gain_usd = terminal_asset_value_usd - total_capital
    total_net_gain_usd = cumulative_net_rental_usd + capital_gain_usd
    total_roi_pct = (total_net_gain_usd / total_capital) * 100.0
    annualized_irr_pct = ((1.0 + (total_roi_pct / 100.0)) ** (1.0 / target_hold_years) - 1.0) * 100.0

    return {
        'total_capital_usd': total_capital,
        'risk_archetype': risk_archetype,
        'target_hold_years': target_hold_years,
        'is_golden_visa': is_golden_visa,
        'cf_weight': cf_weight,
        'cg_weight': cg_weight,
        'annual_appreciation_pct': annual_appreciation_pct,
        'gross_yield_pct': gross_yield_pct,
        'net_yield_pct': net_yield_pct,
        'annual_net_rental_usd': annual_net_rental_usd,
        'cumulative_net_rental_usd': cumulative_net_rental_usd,
        'terminal_asset_value_usd': terminal_asset_value_usd,
        'capital_gain_usd': capital_gain_usd,
        'total_net_gain_usd': total_net_gain_usd,
        'total_roi_pct': total_roi_pct,
        'annualized_irr_pct': annualized_irr_pct,
        'description': description,
        'recommended_assets': recommended_assets
    }

