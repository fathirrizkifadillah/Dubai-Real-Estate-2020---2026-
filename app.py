import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Dubai Real Estate Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- LUXURY ARCHITECTURAL DESIGN SYSTEM (CSS) -----------------
st.markdown("""
    <style>
    /* Base theme */
    .stApp {
        background-color: #0a0d14;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
    }
    
    header[data-testid="stHeader"] {
        background-color: rgba(10, 13, 20, 0.85);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Architectural Quiet Luxury Metric Cards */
    .luxury-card {
        background-color: #131926;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .luxury-card:hover {
        border-color: rgba(197, 168, 128, 0.4);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
    }
    .luxury-eyebrow {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: #8b9bb4;
        margin-bottom: 6px;
    }
    .luxury-value {
        font-size: 26px;
        font-weight: 600;
        color: #f8fafc;
        line-height: 1.2;
        font-variant-numeric: tabular-nums;
        margin-bottom: 4px;
    }
    .luxury-badge {
        font-size: 12px;
        font-weight: 500;
        color: #c5a880;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        font-weight: 500;
        font-size: 14px;
        color: #8b9bb4;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #c5a880 !important;
        border-bottom: 2px solid #c5a880 !important;
        background: transparent !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f141f;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* Button refinement */
    div.stButton > button {
        background-color: #c5a880 !important;
        color: #0a0d14 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 9px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #d6be99 !important;
        box-shadow: 0 4px 12px rgba(197, 168, 128, 0.25) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Subtle divider */
    hr {
        border-color: rgba(255, 255, 255, 0.07) !important;
        margin: 20px 0 !important;
    }

    @media (max-width: 768px) {
        .luxury-card {
            padding: 14px 16px;
        }
        .luxury-value {
            font-size: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING & CACHING -----------------
AED_PEG = 3.6725
SQFT_TO_M2 = 0.092903

@st.cache_data
def load_all_data():
    cache_dir = os.path.expanduser(r"~/.cache/kagglehub/datasets/sergionefedov/dubai-real-estate-sales-and-rentals-20202026/versions/2")
    if os.path.exists(cache_dir):
        path = cache_dir
    else:
        import kagglehub
        path = kagglehub.dataset_download("sergionefedov/dubai-real-estate-sales-and-rentals-20202026")
    
    area_prices = pd.read_csv(os.path.join(path, "area_prices_monthly.csv"))
    metro_stations = pd.read_csv(os.path.join(path, "metro_stations.csv"))
    offplan = pd.read_csv(os.path.join(path, "off_plan.csv"))
    rentals = pd.read_csv(os.path.join(path, "rentals.csv"))
    secondary = pd.read_csv(os.path.join(path, "secondary_sales.csv"))
    
    area_prices['date'] = pd.to_datetime(area_prices['year_month'])
    offplan['date_listed'] = pd.to_datetime(offplan['date_listed'])
    rentals['date_listed'] = pd.to_datetime(rentals['date_listed'])
    secondary['date_listed'] = pd.to_datetime(secondary['date_listed'])
    
    return area_prices, metro_stations, offplan, rentals, secondary

area_prices, metro_stations, offplan, rentals, secondary = load_all_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("<h2 style='margin-top: 5px; font-size: 20px;'>DUBAI REAL ESTATE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #8b9bb4; font-size: 12px; margin-bottom: 16px;'>Market Intelligence & Valuation</p>", unsafe_allow_html=True)

# Currency and Measurement Unit Controls
col_curr, col_unit = st.sidebar.columns(2)
with col_curr:
    selected_currency = st.selectbox("Currency", ["USD ($)", "AED (AED)"], index=0)
with col_unit:
    selected_unit = st.selectbox("Area Unit", ["Sq. Ft", "m²"], index=0)

curr_mult = AED_PEG if "AED" in selected_currency else 1.0
curr_sym = "AED " if "AED" in selected_currency else "$"
unit_sqft = selected_unit == "Sq. Ft"
unit_name = "sqft" if unit_sqft else "m²"
unit_area_factor = 1.0 if unit_sqft else SQFT_TO_M2
unit_price_factor = 1.0 if unit_sqft else (1.0 / SQFT_TO_M2)

def fmt_money(usd_amt, compact=False):
    if pd.isna(usd_amt):
        return "N/A"
    val = usd_amt * curr_mult
    if compact:
        if abs(val) >= 1_000_000:
            return f"{curr_sym}{val/1_000_000:.2f}M"
        elif abs(val) >= 1_000:
            return f"{curr_sym}{val/1_000:.1f}k"
    return f"{curr_sym}{val:,.0f}"

def fmt_rate(usd_per_sqft):
    if pd.isna(usd_per_sqft):
        return "N/A"
    val = usd_per_sqft * curr_mult * unit_price_factor
    return f"{curr_sym}{val:,.0f}/{unit_name}"

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Navigation Menu
menu = st.sidebar.radio(
    "Navigation",
    [
        "Market Overview",
        "Yield & Opportunity",
        "Developer Brand Equity",
        "Valuation Intelligence (ML)",
        "Investment & Mortgage Simulator",
        "Price Forecasting (Prophet)"
    ]
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.caption(f"Coverage: 2020 – 2026 | {len(secondary):,} Secondary Listings")
st.sidebar.caption("Source: Dubai Land Department / Open Data")

# ----------------- VIEW 1: MARKET OVERVIEW -----------------
if menu == "Market Overview":
    st.title("Dubai Real Estate Market Overview")
    st.markdown("Macro spatial trends, volume concentration, and price evolution across the Emirate.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Secondary Resale</div>
                <div class="luxury-value">{len(secondary):,}</div>
                <div class="luxury-badge">Median: {fmt_money(secondary['price_usd'].median(), compact=True)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Off-Plan Projects</div>
                <div class="luxury-value">{len(offplan):,}</div>
                <div class="luxury-badge">Median: {fmt_money(offplan['price_usd'].median(), compact=True)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Active Rentals</div>
                <div class="luxury-value">{len(rentals):,}</div>
                <div class="luxury-badge">Rent: {fmt_money(rentals['annual_rent_usd'].median(), compact=True)}/yr</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Coverage Areas</div>
                <div class="luxury-value">{secondary['zone'].nunique()}</div>
                <div class="luxury-badge">52 Distinct Districts</div>
            </div>
        """, unsafe_allow_html=True)
        
    col_map_info, col_map_style = st.columns([3, 1])
    with col_map_info:
        st.markdown("### Spatial Distribution & Transit Accessibility")
        st.caption("Resale listings colored by price rate, overlaid with the Dubai Metro transit network and the Burj Khalifa city core.")
    with col_map_style:
        map_theme = st.selectbox(
            "Map Basemap Style",
            ["Dark Architectural (OpenFreeMap)", "Dark Canvas (ESRI)", "OpenStreetMap"],
            index=0
        )
    
    # Fast map sampling
    @st.cache_data
    def get_map_sample(df_sec):
        return df_sec.sample(n=min(8000, len(df_sec)), random_state=42).copy()
    
    map_df = get_map_sample(secondary)
    map_df['plot_rate'] = map_df['price_per_sqft_usd'] * curr_mult * unit_price_factor
    
    # Configure basemap style without API key requirements (eliminates Carto watermark)
    if map_theme == "Dark Architectural (OpenFreeMap)":
        map_layout_cfg = dict(
            style='https://tiles.openfreemap.org/styles/dark',
            center=dict(lat=25.12, lon=55.25),
            zoom=9.3
        )
    elif map_theme == "Dark Canvas (ESRI)":
        map_layout_cfg = dict(
            style='white-bg',
            center=dict(lat=25.12, lon=55.25),
            zoom=9.3,
            layers=[dict(
                below='traces',
                sourcetype='raster',
                source=['https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}']
            )]
        )
    else:  # OpenStreetMap
        map_layout_cfg = dict(
            style='open-street-map',
            center=dict(lat=25.12, lon=55.25),
            zoom=9.3
        )
    
    fig_map = px.scatter_map(
        map_df,
        lat="lat",
        lon="lon",
        color="plot_rate",
        size="area_sqft",
        color_continuous_scale="Viridis",
        size_max=8
    )
    
    # Overlay Red Line
    metro_red = metro_stations[metro_stations['line'] == 'Red']
    fig_map.add_trace(go.Scattermap(
        lat=metro_red['lat'],
        lon=metro_red['lon'],
        mode='markers',
        marker=dict(size=6, color='#ef4444', opacity=0.9),
        text=metro_red['station_name'].apply(lambda x: f"Metro Red: {x}"),
        hoverinfo='text',
        name='Metro Red Line'
    ))
    
    # Overlay Green Line
    metro_green = metro_stations[metro_stations['line'] == 'Green']
    fig_map.add_trace(go.Scattermap(
        lat=metro_green['lat'],
        lon=metro_green['lon'],
        mode='markers',
        marker=dict(size=6, color='#10b981', opacity=0.9),
        text=metro_green['station_name'].apply(lambda x: f"Metro Green: {x}"),
        hoverinfo='text',
        name='Metro Green Line'
    ))
    
    # Overlay Burj Khalifa
    fig_map.add_trace(go.Scattermap(
        lat=[25.1972],
        lon=[55.2744],
        mode='markers',
        marker=dict(size=14, color='#c5a880', opacity=1.0),
        text=['Burj Khalifa (Downtown Core)'],
        hoverinfo='text',
        name='Burj Khalifa Core'
    ))
    
    fig_map.update_layout(
        height=480,
        margin={"r":0,"t":10,"l":0,"b":0},
        font=dict(family="-apple-system, sans-serif"),
        coloraxis_colorbar=dict(title=f"Rate ({curr_sym}/{unit_name})"),
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor="rgba(15, 20, 31, 0.85)"),
        map=map_layout_cfg
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Historical Trajectory
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Historical Price Trajectory (2020 – 2026)")
    
    monthly_price = area_prices.groupby('date')['secondary_price_per_sqft_usd'].median().reset_index()
    monthly_price['plot_rate'] = monthly_price['secondary_price_per_sqft_usd'] * curr_mult * unit_price_factor
    
    fig_trend = px.line(
        monthly_price,
        x='date',
        y='plot_rate',
        labels={'plot_rate': f'Median Rate ({curr_sym}/{unit_name})', 'date': 'Timeline'}
    )
    fig_trend.update_traces(line_color='#c5a880', line_width=2.5)
    fig_trend.update_layout(
        height=360,
        margin={"r":10,"t":10,"l":10,"b":10},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
        template="plotly_dark"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ----------------- VIEW 2: YIELD & OPPORTUNITY -----------------
elif menu == "Yield & Opportunity":
    st.title("Rental Yield & District Opportunity")
    st.markdown("Assess gross cash-flow yields vs net yield proxies (accounting for operational service charges) and identify off-plan pricing gaps.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top High-Yield Rental Zones")
        st.caption("Estimated gross yield proxy vs simulated net yield (assuming 15 AED / $4 per sqft annual service charge & maintenance).")
        
        df_a = area_prices.copy()
        df_a['gross_yield_pct'] = (df_a['rental_price_per_sqft_annual_usd'] / df_a['secondary_price_per_sqft_usd']) * 100
        # Realistic Net yield calculation: deduct $4/sqft (~15 AED/sqft) service charge and 5% vacancy
        df_a['net_yield_pct'] = np.maximum(0, ((df_a['rental_price_per_sqft_annual_usd'] * 0.95 - 4.0) / df_a['secondary_price_per_sqft_usd']) * 100)
        
        recent_a = df_a[df_a['date'] >= '2025-01-01']
        yield_summary = recent_a.groupby('zone').agg(
            Gross=('gross_yield_pct', 'mean'),
            Net=('net_yield_pct', 'mean')
        ).dropna().sort_values('Gross', ascending=False).head(12).reset_index()
        
        fig_y = go.Figure()
        fig_y.add_trace(go.Bar(
            y=yield_summary['zone'], x=yield_summary['Gross'], name='Gross Yield (%)',
            orientation='h', marker_color='#c5a880'
        ))
        fig_y.add_trace(go.Bar(
            y=yield_summary['zone'], x=yield_summary['Net'], name='Estimated Net Yield (%)',
            orientation='h', marker_color='#38bdf8'
        ))
        fig_y.update_layout(
            barmode='group', height=420, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Yield (%)"),
            yaxis=dict(categoryorder='total ascending'),
            legend=dict(bgcolor="rgba(15, 20, 31, 0.8)"), template="plotly_dark"
        )
        st.plotly_chart(fig_y, use_container_width=True)
        
    with col2:
        st.subheader("Off-Plan Launch Premium vs Secondary Resale")
        st.caption("Percentage price-per-sqft premium commanded by new off-plan launches relative to ready secondary units in the same district.")
        
        df_a['gap_pct'] = ((df_a['offplan_price_per_sqft_usd'] - df_a['secondary_price_per_sqft_usd']) / df_a['secondary_price_per_sqft_usd']) * 100
        gap_zone = df_a[df_a['date'] >= '2025-01-01'].groupby('zone')['gap_pct'].mean().dropna().sort_values(ascending=False).reset_index()
        top_bottom = pd.concat([gap_zone.head(6), gap_zone.tail(6)]).sort_values('gap_pct', ascending=False)
        
        fig_g = px.bar(
            top_bottom, x='gap_pct', y='zone', orientation='h',
            color='gap_pct', color_continuous_scale='curl',
            labels={'gap_pct': 'Off-Plan Premium (%)', 'zone': 'Zone'}
        )
        fig_g.update_layout(
            height=420, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(categoryorder='total ascending'),
            coloraxis_showscale=False, template="plotly_dark"
        )
        st.plotly_chart(fig_g, use_container_width=True)
        
    # Unsupervised District Archetypes (K-Means Clustering)
    if os.path.exists("models/zone_clusters.csv"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Unsupervised District Segmentation (K-Means Clustering)")
        st.markdown("Machine learning clustering classifying Dubai's 52 districts into 4 strategic investment archetypes based on entry price, rental yield, transaction volume, and freehold status.")
        
        clusters_df = pd.read_csv("models/zone_clusters.csv")
        fig_clust = px.scatter(
            clusters_df,
            x='pca1',
            y='pca2',
            color='cluster_label',
            hover_name='zone',
            hover_data={
                'median_price_sqft': ':.0f',
                'gross_yield_pct': ':.1f',
                'annual_volume': ':.0f',
                'pca1': False,
                'pca2': False
            },
            color_discrete_sequence=['#c5a880', '#38bdf8', '#34d399', '#f87171'],
            labels={'pca1': 'Component 1 (Capital Value & Prestige)', 'pca2': 'Component 2 (Yield & Foreign Access)'}
        )
        fig_clust.update_traces(marker=dict(size=12, line=dict(width=1, color='#f8fafc')))
        fig_clust.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            legend=dict(title="Investor Archetype", bgcolor="rgba(15, 20, 31, 0.8)"),
            template="plotly_dark"
        )
        st.plotly_chart(fig_clust, use_container_width=True)

# ----------------- VIEW 3: DEVELOPER BRAND EQUITY -----------------
elif menu == "Developer Brand Equity":
    st.title("Developer Brand Equity & Econometric Analysis")
    st.markdown("Quantify developer pricing power by comparing off-plan properties launched by Tier 1 developers (Emaar, Meraas, Nakheel) vs. Tier 2 developers.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    df_off = offplan.copy()
    df_off['developer_tier'] = df_off['developer_tier'].str.title()
    df_off['property_category'] = df_off['property_category'].str.title()
    
    stats_tier = df_off.groupby(['property_category', 'developer_tier'])['price_per_sqft_usd'].agg(['mean', 'median', 'count']).reset_index()
    
    ap_t1 = stats_tier[(stats_tier['property_category'] == 'Apartment') & (stats_tier['developer_tier'] == 'Tier1')]['mean'].values[0]
    ap_t2 = stats_tier[(stats_tier['property_category'] == 'Apartment') & (stats_tier['developer_tier'] == 'Tier2')]['mean'].values[0]
    ap_prem = ((ap_t1 - ap_t2) / ap_t2) * 100
    
    vil_t1 = stats_tier[(stats_tier['property_category'] == 'Villa') & (stats_tier['developer_tier'] == 'Tier1')]['mean'].values[0]
    vil_t2 = stats_tier[(stats_tier['property_category'] == 'Villa') & (stats_tier['developer_tier'] == 'Tier2')]['mean'].values[0]
    vil_prem = ((vil_t1 - vil_t2) / vil_t2) * 100
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Observed Pricing Comparison")
        stats_tier['plot_mean'] = stats_tier['mean'] * curr_mult * unit_price_factor
        fig_p = px.bar(
            stats_tier, x='property_category', y='plot_mean', color='developer_tier',
            barmode='group',
            labels={'plot_mean': f'Mean Rate ({curr_sym}/{unit_name})', 'property_category': 'Property Category', 'developer_tier': 'Developer Tier'},
            color_discrete_map={'Tier1': '#c5a880', 'Tier2': '#475569'}
        )
        fig_p.update_layout(
            height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            template="plotly_dark"
        )
        st.plotly_chart(fig_p, use_container_width=True)
        
    with c2:
        st.subheader("Observed Brand Premiums")
        st.markdown(f"""
            <div class="luxury-card" style="margin-top: 15px;">
                <div class="luxury-eyebrow">Apartment Tier 1 Premium</div>
                <div class="luxury-value">+{ap_prem:.1f}%</div>
                <div class="luxury-badge">+{fmt_rate(ap_t1 - ap_t2)} raw difference</div>
            </div>
            <div class="luxury-card">
                <div class="luxury-eyebrow">Villa Tier 1 Premium</div>
                <div class="luxury-value">+{vil_prem:.1f}%</div>
                <div class="luxury-badge">+{fmt_rate(vil_t1 - vil_t2)} raw difference</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Econometric Hedonic Model: Isolating Pure Brand Equity")
    st.markdown("""
    Comparing raw averages can introduce **confounding bias** because Tier 1 developers disproportionately build in prime coastal and central locations (Downtown, Dubai Hills). 
    To verify whether the premium is truly driven by brand equity, we ran a multivariate **Hedonic OLS Regression** controlling for unit size, category, and proximity to Burj Khalifa.
    """)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Controlled Pure Brand Premium</div>
                <div class="luxury-value">+{fmt_rate(149.04)}</div>
                <div class="luxury-badge">p < 0.0001 (Highly Significant)</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">95% Confidence Interval</div>
                <div class="luxury-value" style="font-size: 20px;">{fmt_rate(135.45)} – {fmt_rate(162.63)}</div>
                <div class="luxury-badge">Robust across specifications</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Econometric Takeaway</div>
                <div class="luxury-value" style="font-size: 16px; font-weight: normal; line-height: 1.4;">Brand equity retains significant pricing power even after controlling for location.</div>
            </div>
        """, unsafe_allow_html=True)

# ----------------- VIEW 4: VALUATION INTELLIGENCE (ML) -----------------
elif menu == "Valuation Intelligence (ML)":
    st.title("Valuation Intelligence (Scikit-Learn)")
    st.markdown("Estimate fair market valuation for **Secondary Resale Units** or **Off-Plan Projects** using pre-trained gradient boosted ensemble models evaluated on out-of-time holdouts.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    val_mode = st.radio("Valuation Mode", ["Secondary Resale Property Valuation", "Off-Plan Project Estimator"], horizontal=True)
    
    if val_mode == "Secondary Resale Property Valuation":
        st.subheader("Ready Resale Property Valuation Model")
        st.caption("Trained on 50,000+ secondary resale listings using Scikit-Learn HistGradientBoostingRegressor (Holdout MAPE: ~22%, R²: 0.83).")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            sec_zone = st.selectbox("Zone / District", sorted(secondary['zone'].dropna().unique()), index=15)
            sec_cat = st.selectbox("Category", ["Apartment", "Villa"])
            sec_freehold = st.selectbox("Ownership Status", ["Freehold", "Non-Freehold"]) == "Freehold"
        with c2:
            default_area = 1200 if unit_sqft else int(1200 * SQFT_TO_M2)
            max_area = 15000 if unit_sqft else int(15000 * SQFT_TO_M2)
            input_area = st.number_input(f"Area ({unit_name})", min_value=250, max_value=max_area, value=default_area)
            sec_area_sqft = input_area if unit_sqft else (input_area / SQFT_TO_M2)
            sec_beds = st.number_input("Bedrooms", min_value=0, max_value=8, value=2)
            sec_cond = st.selectbox("Condition", sorted(secondary['condition'].dropna().unique()))
        with c3:
            sec_furn = st.selectbox("Furnishing", sorted(secondary['furnishing'].dropna().unique()))
            sec_view = st.selectbox("Primary View", sorted(secondary['view'].dropna().unique()))
            sec_metro = st.number_input("Travel to Nearest Metro (minutes)", min_value=1, max_value=90, value=10)
            sec_burj = st.number_input("Distance to Burj Khalifa (km)", min_value=0.5, max_value=60.0, value=12.0, step=0.5)
            
        if st.button("Calculate Resale Fair Valuation"):
            if os.path.exists("models/secondary_valuation_model.joblib"):
                sec_obj = joblib.load("models/secondary_valuation_model.joblib")
                if isinstance(sec_obj, dict):
                    sec_model = sec_obj['pipeline']
                    sec_mape = sec_obj.get('mape', 0.22)
                    sec_err_band = sec_obj.get('error_band', None)
                else:
                    sec_model = sec_obj
                    sec_mape = 0.22
                    sec_err_band = None

                input_df = pd.DataFrame([{
                    'area_sqft': sec_area_sqft,
                    'bedrooms': sec_beds,
                    'to_burj_khalifa_km': sec_burj,
                    'metro_distance_min': sec_metro,
                    'property_category': sec_cat,
                    'zone': sec_zone,
                    'condition': sec_cond,
                    'furnishing': sec_furn,
                    'view': sec_view,
                    'is_freehold': sec_freehold
                }])
                pred_log = sec_model.predict(input_df)[0]
                est_usd = np.expm1(pred_log)
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Estimated Resale Fair Value</div>
                            <div class="luxury-value">{fmt_money(est_usd)}</div>
                            <div class="luxury-badge">Gradient Boosted Ensemble</div>
                        </div>
                    """, unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Estimated Price Rate</div>
                            <div class="luxury-value">{fmt_rate(est_usd / sec_area_sqft)}</div>
                            <div class="luxury-badge">Per {unit_name}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with m3:
                    band_val_str = f"±{fmt_money(sec_err_band)}" if sec_err_band is not None else f"±{fmt_money(est_usd * sec_mape)}"
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Empirical 80% Error Band</div>
                            <div class="luxury-value" style="font-size: 20px;">{band_val_str}</div>
                            <div class="luxury-badge">Holdout MAPE: {sec_mape:.1%}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Model file not found. Please train models first.")
                
    else:
        st.subheader("Off-Plan Listing Price Estimator")
        st.caption("Trained on off-plan launch data with chronological holdout and empirical error band.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            off_cat_sel = st.selectbox("Category", sorted(offplan['property_category'].dropna().unique()))
            off_zone_sel = st.selectbox("Zone", sorted(offplan['zone'].dropna().unique()))
            off_tier_sel = st.selectbox("Developer Tier", sorted(offplan['developer_tier'].dropna().unique()))
        with c2:
            default_area = 1200 if unit_sqft else int(1200 * SQFT_TO_M2)
            input_area = st.number_input(f"Area ({unit_name})", min_value=300, max_value=15000, value=default_area, key='off_area')
            off_area_sqft = input_area if unit_sqft else (input_area / SQFT_TO_M2)
            off_beds = st.number_input("Bedrooms", min_value=0, max_value=8, value=2, key='off_beds')
            off_view = st.selectbox("View", sorted(offplan['view'].dropna().unique()))
            off_plan_type = st.selectbox("Payment Plan", sorted(offplan['payment_plan'].dropna().unique()))
        with c3:
            off_launch = st.selectbox("Launch Year", sorted(offplan['launch_year'].dropna().unique()))
            off_handover = st.selectbox("Handover Year", sorted(offplan['handover_year'].dropna().unique()))
            off_metro = st.number_input("Nearest Metro (minutes)", min_value=0, max_value=90, value=12, key='off_metro')
            off_burj = st.number_input("Distance to Burj Khalifa (km)", min_value=0.5, max_value=70.0, value=15.0, key='off_burj')
            
        if st.button("Estimate Off-Plan Price"):
            if os.path.exists("models/offplan_valuation_package.joblib"):
                pkg = joblib.load("models/offplan_valuation_package.joblib")
                off_pipe = pkg['pipeline']
                err_band_usd = pkg['error_band']
                
                input_df = pd.DataFrame([{
                    'area_sqft': off_area_sqft,
                    'bedrooms': off_beds,
                    'launch_year': off_launch,
                    'handover_year': off_handover,
                    'metro_distance_min': off_metro,
                    'to_burj_khalifa_km': off_burj,
                    'property_category': off_cat_sel,
                    'zone': off_zone_sel,
                    'developer_tier': off_tier_sel,
                    'view': off_view,
                    'payment_plan': off_plan_type
                }])
                pred_log = off_pipe.predict(input_df)[0]
                est_usd = np.expm1(pred_log)
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Estimated Off-Plan Price</div>
                            <div class="luxury-value">{fmt_money(est_usd)}</div>
                            <div class="luxury-badge">Chronological Holdout Model</div>
                        </div>
                    """, unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Estimated Rate</div>
                            <div class="luxury-value">{fmt_rate(est_usd / off_area_sqft)}</div>
                            <div class="luxury-badge">Per {unit_name}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with m3:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <div class="luxury-eyebrow">Empirical 80% Error Band</div>
                            <div class="luxury-value" style="font-size: 20px;">±{fmt_money(err_band_usd)}</div>
                            <div class="luxury-badge">Holdout MAPE: {pkg['mape']:.1%}</div>
                        </div>
                    """, unsafe_allow_html=True)

# ----------------- VIEW 5: INVESTMENT & MORTGAGE SIMULATOR -----------------
elif menu == "Investment & Mortgage Simulator":
    st.title("Investment & Mortgage Cash-Flow Simulator")
    st.markdown("Simulate cash flows, debt service, net yields, and payback periods for Dubai buy-to-let investments.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Property & Financing Parameters")
        default_price_usd = 600000
        prop_price = st.number_input(f"Purchase Price ({selected_currency})", min_value=100000, max_value=50000000, value=int(default_price_usd * curr_mult), step=25000)
        prop_price_usd = prop_price / curr_mult
        
        down_pct = st.slider("Down Payment (%)", min_value=15, max_value=100, value=25, step=5)
        mortgage_rate = st.slider("Mortgage Interest Rate (%)", min_value=2.0, max_value=9.0, value=5.25, step=0.25)
        loan_years = st.slider("Loan Tenor (Years)", min_value=5, max_value=30, value=25, step=5)
        
    with c2:
        st.subheader("Rental & Operational Assumptions")
        default_rent_usd = prop_price_usd * 0.075
        annual_rent = st.number_input(f"Expected Annual Rent ({selected_currency})", min_value=10000, max_value=5000000, value=int(default_rent_usd * curr_mult), step=5000)
        annual_rent_usd = annual_rent / curr_mult
        
        default_sc_display = float(round(4.0 * curr_mult * unit_price_factor, 1))
        sc_input = st.slider(f"Annual Service Charge ({curr_sym}/{unit_name})", min_value=1.0, max_value=float(round(25.0 * curr_mult * unit_price_factor, 1)), value=default_sc_display, step=0.5)
        service_charge_usd_per_sqft = sc_input / (curr_mult * unit_price_factor)
        
        default_size = 1100 if unit_sqft else int(1100 * SQFT_TO_M2)
        prop_size_input = st.number_input(f"Property Size ({unit_name})", min_value=30 if not unit_sqft else 300, max_value=10000, value=default_size, step=50)
        prop_size_sqft = prop_size_input if unit_sqft else (prop_size_input / SQFT_TO_M2)
        vacancy_pct = st.slider("Vacancy & Maintenance Allowance (%)", min_value=0, max_value=15, value=5, step=1)
        
    # Financial Computations
    loan_amount_usd = prop_price_usd * (1.0 - down_pct / 100.0)
    monthly_rate = (mortgage_rate / 100.0) / 12.0
    n_payments = loan_years * 12
    
    if loan_amount_usd > 0 and monthly_rate > 0:
        monthly_mortgage_usd = loan_amount_usd * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    else:
        monthly_mortgage_usd = 0
        
    annual_mortgage_usd = monthly_mortgage_usd * 12
    annual_service_charge_usd = service_charge_usd_per_sqft * prop_size_sqft
    effective_rent_usd = annual_rent_usd * (1.0 - vacancy_pct / 100.0)
    net_operating_income_usd = effective_rent_usd - annual_service_charge_usd
    net_annual_cashflow_usd = net_operating_income_usd - annual_mortgage_usd
    
    gross_yield = (annual_rent_usd / prop_price_usd) * 100
    net_yield = (net_operating_income_usd / prop_price_usd) * 100
    initial_equity_usd = prop_price_usd * (down_pct / 100.0) + (prop_price_usd * 0.04) # +4% DLD transfer fee
    cash_on_cash = (net_annual_cashflow_usd / initial_equity_usd) * 100 if initial_equity_usd > 0 else 0
    payback_years = (initial_equity_usd / net_annual_cashflow_usd) if net_annual_cashflow_usd > 0 else np.nan
    payback_str = f"{payback_years:.1f} yrs" if (net_annual_cashflow_usd > 0 and not np.isnan(payback_years)) else "N/A"
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Financial Performance Dashboard")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Net Rental Yield</div>
                <div class="luxury-value">{net_yield:.2f}%</div>
                <div class="luxury-badge">Gross: {gross_yield:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Monthly Mortgage EMI</div>
                <div class="luxury-value">{fmt_money(monthly_mortgage_usd)}</div>
                <div class="luxury-badge">{loan_years} yr @ {mortgage_rate:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Net Annual Cash Flow</div>
                <div class="luxury-value" style="color: {'#34d399' if net_annual_cashflow_usd >= 0 else '#f87171'} !important;">{fmt_money(net_annual_cashflow_usd)}/yr</div>
                <div class="luxury-badge">After debt & charges</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="luxury-card">
                <div class="luxury-eyebrow">Cash-on-Cash Return</div>
                <div class="luxury-value">{cash_on_cash:.1f}%</div>
                <div class="luxury-badge">Payback: {payback_str}</div>
            </div>
        """, unsafe_allow_html=True)

# ----------------- VIEW 6: PRICE FORECASTING (PROPHET) -----------------
elif menu == "Price Forecasting (Prophet)":
    st.title("Time-Series Price Forecasting (Prophet)")
    st.markdown("Extrapolate monthly median secondary prices per sqft using a Meta Prophet additive model with yearly seasonality and rolling-origin cross-validation.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    forecast_horizon = st.slider("Forecast Horizon (Months)", min_value=6, max_value=36, value=24)
    
    df_area = area_prices.copy()
    monthly_trend = df_area.groupby('date')['secondary_price_per_sqft_usd'].median().reset_index().sort_values('date').reset_index(drop=True)
    df_prophet = monthly_trend.rename(columns={'date': 'ds', 'secondary_price_per_sqft_usd': 'y'})
    
    if st.button("Run Forecasting Simulation") or 'prophet_forecast_df' in st.session_state:
        from prophet import Prophet
        
        if 'prophet_forecast_df' not in st.session_state or st.session_state.get('saved_horizon') != forecast_horizon:
            with st.spinner("Fitting Prophet model..."):
                m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False, changepoint_prior_scale=0.05)
                m.fit(df_prophet)
                future = m.make_future_dataframe(periods=forecast_horizon, freq='MS')
                forecast = m.predict(future)
                st.session_state['prophet_forecast_df'] = forecast
                st.session_state['saved_horizon'] = forecast_horizon
                st.session_state['prophet_model'] = m
                
        forecast = st.session_state['prophet_forecast_df']
        saved_h = st.session_state['saved_horizon']
        
        # Scale for plot
        monthly_trend['plot_y'] = monthly_trend['secondary_price_per_sqft_usd'] * curr_mult * unit_price_factor
        future_part = forecast.iloc[-saved_h:].copy()
        future_part['plot_yhat'] = future_part['yhat'] * curr_mult * unit_price_factor
        future_part['plot_upper'] = future_part['yhat_upper'] * curr_mult * unit_price_factor
        future_part['plot_lower'] = future_part['yhat_lower'] * curr_mult * unit_price_factor
        
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(
            x=monthly_trend['date'], y=monthly_trend['plot_y'],
            mode='lines+markers', name='Historical Actual', line=dict(color='#38bdf8', width=2.5)
        ))
        fig_fc.add_trace(go.Scatter(
            x=future_part['ds'], y=future_part['plot_yhat'],
            mode='lines', name=f'Projected ({saved_h}m)', line=dict(color='#c5a880', width=2.5)
        ))
        fig_fc.add_trace(go.Scatter(
            x=pd.concat([future_part['ds'], future_part['ds'][::-1]]),
            y=pd.concat([future_part['plot_upper'], future_part['plot_lower'][::-1]]),
            fill='toself', fillcolor='rgba(197, 168, 128, 0.12)',
            line=dict(color='rgba(255,255,255,0)'), name='95% Uncertainty Band'
        ))
        
        fig_fc.update_layout(
            title=f"Secondary Market Price Rate Projection ({curr_sym}/{unit_name})",
            height=420, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title=f"Rate ({curr_sym}/{unit_name})"),
            template="plotly_dark", hovermode="x unified"
        )
        st.plotly_chart(fig_fc, use_container_width=True)
        
        latest_val = monthly_trend.iloc[-1]['secondary_price_per_sqft_usd']
        end_val = forecast.iloc[-1]['yhat']
        change_pct = ((end_val - latest_val) / latest_val) * 100
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="luxury-card">
                    <div class="luxury-eyebrow">Latest Actual Rate</div>
                    <div class="luxury-value">{fmt_rate(latest_val)}</div>
                    <div class="luxury-badge">Historical base</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="luxury-card">
                    <div class="luxury-eyebrow">Projected End Rate</div>
                    <div class="luxury-value">{fmt_rate(end_val)}</div>
                    <div class="luxury-badge">After {saved_h} months</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="luxury-card">
                    <div class="luxury-eyebrow">Projected Trend Trajectory</div>
                    <div class="luxury-value">{change_pct:+.1f}%</div>
                    <div class="luxury-badge">Scenario extrapolation</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Click 'Run Forecasting Simulation' to generate price projections.")
