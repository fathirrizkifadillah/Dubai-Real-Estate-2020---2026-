# Dubai Real Estate Market Analysis (2020–2026)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dubai-real-estate-fathir.streamlit.app/)

An end-to-end data analytics portfolio project exploring Dubai residential-market listings and area-level indicators. It combines exploratory analysis, spatial analysis, statistical comparison, and **Prophet time-series forecasting** in an interactive Streamlit dashboard.

## Business Questions

- Which areas combine relatively high rental-yield proxies with lower entry prices?
- How do location, metro proximity, ownership status, property type, and developer tier relate to listed price per square foot?
- How has the market moved since 2020, and what does a Prophet model project under the historical pattern?

## Data Source and Scope

- **Source:** [Dubai Real Estate Sales and Rentals 2020–2026 on Kaggle](https://www.kaggle.com/datasets/sergionefedov/dubai-real-estate-sales-and-rentals-20202026), downloaded with `kagglehub`.
- **Coverage used:** January 2020 through April 2026, as supplied by the source dataset.
- **Tables:** area-level monthly prices, metro stations, secondary listings, off-plan listings, and rental listings.
- **Important scope:** These are source-supplied listing and area-level records. They are not a complete official transaction register, and they should not be used as investment advice or a property valuation.

## Key Findings

- Listed secondary prices are concentrated in premium coastal and central zones; the analysis visualizes how prices vary with proximity to the Burj Khalifa and metro stations.
- Freehold and non-freehold areas show materially different observed price distributions. The Welch t-test evaluates a difference in sample means; it does **not** establish that ownership status alone causes the difference.
- Rental-yield figures are gross **yield proxies** calculated from source rent and secondary-price fields. They exclude service charges, vacancy, financing, maintenance, taxes, and transaction costs.
- Tier 1 developers have higher average listed off-plan price per square foot in the observed sample. This is an association and may also reflect location, project type, size, and unobserved quality differences.

## Forecasting: Prophet, Not a Property-Valuation Model

The forecasting chapter aggregates monthly median secondary price per square foot and fits a **Prophet** time-series model with yearly seasonality. It produces a 6–36 month scenario projection and 95% model uncertainty interval.

- The forecast describes an extrapolation of the historical series; it does not predict an individual property's sale price.
- The notebook runs Prophet rolling-origin cross-validation and prints RMSE and MAPE. Review those values alongside a seasonal-naive benchmark before relying on the projection.
- Macro shocks, supply changes, policy, and future listing composition may change the market pattern; the forecast is not investment advice.

## Dashboard Features

1. **Market Overview** — Macro KPIs, interactive Mapbox of active listings overlaid with Dubai Metro lines and Burj Khalifa core, historical price trajectories, with live **USD / AED** currency and **Sq. Ft / m²** unit toggles.
2. **Yield & Opportunity Analysis** — Gross vs. estimated Net rental yields (adjusted for service charges and vacancy), off-plan launch premiums, and **Unsupervised District Archetypes (K-Means & PCA Clustering)**.
3. **Developer Brand Equity & Econometrics** — Observed Tier 1 vs Tier 2 pricing comparison, complemented by a multivariate **Hedonic OLS model** isolating pure brand pricing power (+$149/sqft) after controlling for unit size and proximity to Downtown.
4. **Valuation Intelligence (Scikit-Learn)** — Dual ML valuation engine: **Secondary Resale Fair Valuation** (HistGradientBoostingRegressor with holdout MAPE ~22%) and **Off-Plan Project Estimator** with empirical error bands.
5. **Investment & Mortgage Simulator** — Interactive buy-to-let cash-flow calculator computing monthly mortgage EMI, net annual cash flow, net rental yield, and payback period.
6. **Prophet Forecast Explorer** — Configurable forecast horizon (6–36 months), 95% model uncertainty band, trend, and yearly seasonality decomposition.

## Project Structure

```text
Dubai Real Estate (2020-2026)/
├── main.ipynb                         # EDA, rigorous statistical testing, ML pipelines, Prophet forecast
├── app.py                              # Streamlit intelligence dashboard (refined architectural UI)
├── models/                             # Pre-trained Scikit-Learn pipelines and cluster taxonomy
├── requirements.txt                    # Python dependencies
├── LICENSE                             # MIT license for this repository's code
├── plots/                              # Exported publication-grade charts
└── *_Explanation.md                    # Bilingual dataset field documentation
```

## Run Locally

Tested with Python 3.10+.

```bash
git clone <your-repository-url>
cd "Dubai Real Estate (2020-2026)"
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The notebook and dashboard download the source dataset through `kagglehub` on first run. Kaggle authentication or internet access may be required depending on your environment.

## Limitations

- Observational relationships in this project do not establish causality.
- Listing and area-level data can differ from completed transactions and may have selection bias.
- The off-plan estimator is an exploratory Random Forest listing-price model; it uses source-supplied, hedonic-model-generated listing data and is not an automated valuation model.
- Prophet forecasts are scenario projections based on past monthly medians, not guarantees of future market performance.

## Portfolio Value

This project demonstrates an analyst workflow from raw multi-table data through quality checks, spatial and investment-oriented EDA, statistical testing, time-series forecasting, and a client-facing dashboard.
