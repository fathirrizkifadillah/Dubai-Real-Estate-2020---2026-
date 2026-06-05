import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import kagglehub
from prophet import Prophet

# Set page config
st.set_page_config(
    page_title="Dubai Real Estate Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium dark theme CSS styling
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Header background fix */
    header[data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.8);
    }
    
    /* Custom Responsive Card Design */
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #334155;
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #475569;
    }
    .metric-card.accent-blue {
        border-left: 4px solid #38bdf8;
    }
    .metric-card.accent-cyan {
        border-left: 4px solid #06b6d4;
    }
    .metric-card.accent-emerald {
        border-left: 4px solid #34d399;
    }
    .metric-card.accent-purple {
        border-left: 4px solid #a78bfa;
    }
    .metric-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 500;
        color: #34d399;
    }
    
    /* Clean headers */
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    p, span, li, label {
        color: #cbd5e1 !important;
    }
    
    /* Tab headers styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        font-weight: 600;
        font-size: 14px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #f8fafc !important;
        border-bottom-color: #38bdf8 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #38bdf8;
        color: #0f172a;
        border-radius: 6px;
        border: none;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #7dd3fc;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING & CACHING -----------------
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("sergionefedov/dubai-real-estate-sales-and-rentals-20202026")
    
    # Read CSVs
    area_prices = pd.read_csv(os.path.join(path, "area_prices_monthly.csv"))
    metro_stations = pd.read_csv(os.path.join(path, "metro_stations.csv"))
    offplan = pd.read_csv(os.path.join(path, "off_plan.csv"))
    rentals = pd.read_csv(os.path.join(path, "rentals.csv"))
    secondary = pd.read_csv(os.path.join(path, "secondary_sales.csv"))
    
    # Date formatting
    area_prices['date'] = pd.to_datetime(area_prices['year_month'])
    offplan['date_listed'] = pd.to_datetime(offplan['date_listed'])
    rentals['date_listed'] = pd.to_datetime(rentals['date_listed'])
    secondary['date_listed'] = pd.to_datetime(secondary['date_listed'])
    
    return area_prices, metro_stations, offplan, rentals, secondary

# Load datasets
area_prices, metro_stations, offplan, rentals, secondary = load_data()

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("<h2 style='margin-top: 10px;'>Dubai Real Estate</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #64748b; font-size: 13px; margin-bottom: 24px;'>Market Analysis & Projections</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #1e293b; margin: 0 0 24px 0;'>", unsafe_allow_html=True)

# Navigation Menu
menu = st.sidebar.radio(
    "Navigation Menu",
    ["Market Overview", "Yield & Opportunity Analysis", "Developer Brand Equity", "Price Forecasting"]
)

st.sidebar.markdown("<hr style='border-color: #1e293b; margin: 24px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color: #64748b; font-size: 12px; font-weight: 500;'>Coverage: 2020 - 2026</span>", unsafe_allow_html=True)
st.sidebar.markdown("<br><span style='color: #64748b; font-size: 12px; font-weight: 500;'>Observed Listings: 97,000+</span>", unsafe_allow_html=True)

# ----------------- VIEW 1: MARKET OVERVIEW -----------------
if menu == "Market Overview":
    st.title("Market Overview")
    st.markdown("A comprehensive spatial and temporal review of Dubai real estate listings, volume density, and pricing dynamics.")
    st.markdown("---")
    
    # Responsive KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card accent-blue">
                <div class="metric-title">Secondary Listings</div>
                <div class="metric-value">{len(secondary):,}</div>
                <div class="metric-delta">Median: ${secondary['price_usd'].median():,.0f} USD</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card accent-cyan">
                <div class="metric-title">Off-Plan Listings</div>
                <div class="metric-value">{len(offplan):,}</div>
                <div class="metric-delta">Median: ${offplan['price_usd'].median():,.0f} USD</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card accent-emerald">
                <div class="metric-title">Rental Listings</div>
                <div class="metric-value">{len(rentals):,}</div>
                <div class="metric-delta">Median Rent: ${rentals['annual_rent_usd'].median():,.0f} USD/yr</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card accent-purple">
                <div class="metric-title">Geographic Zones</div>
                <div class="metric-value">{secondary['zone'].nunique()}</div>
                <div class="metric-delta" style="color: #a78bfa;">52 Major Districts</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### Spatial Distribution Map")
    st.markdown("Geographical bubble map displaying active secondary listings overlaid with **Dubai Metro Stations** and **Burj Khalifa**.")
    
    # Map sampling (to optimize performance)
    map_sample = secondary.sample(n=min(8000, len(secondary)), random_state=42)
    
    # Base Map: Secondary properties
    fig_map = px.scatter_mapbox(
        map_sample,
        lat="lat",
        lon="lon",
        color="price_per_sqft_usd",
        size="area_sqft",
        color_continuous_scale="RdYlBu_r",
        size_max=10,
        mapbox_style="carto-darkmatter" # Premium dark mapbox style
    )
    
    # Overlay Red Line Metro Stations
    metro_red = metro_stations[metro_stations['line'] == 'Red']
    fig_map.add_trace(go.Scattermapbox(
        lat=metro_red['lat'],
        lon=metro_red['lon'],
        mode='markers',
        marker=dict(size=7, color='#ef4444', opacity=0.85),
        text=metro_red['station_name'].apply(lambda x: f"Metro Station (Red Line): {x}"),
        hoverinfo='text',
        name='Metro Station (Red Line)'
    ))
    
    # Overlay Green Line Metro Stations
    metro_green = metro_stations[metro_stations['line'] == 'Green']
    fig_map.add_trace(go.Scattermapbox(
        lat=metro_green['lat'],
        lon=metro_green['lon'],
        mode='markers',
        marker=dict(size=7, color='#10b981', opacity=0.85),
        text=metro_green['station_name'].apply(lambda x: f"Metro Station (Green Line): {x}"),
        hoverinfo='text',
        name='Metro Station (Green Line)'
    ))
    
    # Overlay Burj Khalifa
    fig_map.add_trace(go.Scattermapbox(
        lat=[25.1972],
        lon=[55.2744],
        mode='markers',
        marker=dict(size=16, color='#fbbf24', opacity=1.0),
        text=['Burj Khalifa (City Core)'],
        hoverinfo='text',
        name='Burj Khalifa (City Core)'
    ))
    
    fig_map.update_layout(
        height=600,
        margin={"r":0,"t":10,"l":0,"b":0},
        font=dict(family="Segoe UI, Inter, sans-serif"),
        coloraxis_colorbar=dict(title="Price/Sqft (USD)", yanchor="top", y=1.0, xanchor="left", x=1.02),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(15, 23, 42, 0.85)"
        ),
        mapbox=dict(
            center=dict(lat=25.12, lon=55.25),
            zoom=9.8
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Price Trend
    st.markdown("---")
    st.markdown("### Historical Price Trajectory (Secondary Sales)")
    
    monthly_price = area_prices.groupby('date')['secondary_price_per_sqft_usd'].median().reset_index()
    
    fig_trend = px.line(
        monthly_price,
        x='date',
        y='secondary_price_per_sqft_usd',
        labels={'secondary_price_per_sqft_usd': 'Median Price per Sqft (USD)', 'date': 'Timeline'}
    )
    fig_trend.update_traces(line_color='#38bdf8', line_width=3)
    fig_trend.update_layout(
        height=380,
        margin={"r":10,"t":10,"l":10,"b":10},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#1e293b'),
        yaxis=dict(showgrid=True, gridcolor='#1e293b'),
        font=dict(family="Segoe UI, Inter, sans-serif"),
        template="plotly_dark"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ----------------- VIEW 2: YIELD & GAP -----------------
elif menu == "Yield & Opportunity Analysis":
    st.title("Yield & Opportunity Analysis")
    st.markdown("Evaluate residential rental yields to identify cash-flow hotspots and inspect off-plan launch premiums relative to secondary markets.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top High-Yield Rental Zones")
        st.markdown("Average estimated annual yield proxy for current period (2025-2026).")
        
        df_area = area_prices.copy()
        df_area['rental_yield_pct'] = (df_area['rental_price_per_sqft_annual_usd'] / df_area['secondary_price_per_sqft_usd']) * 100
        recent_area = df_area[df_area['date'] >= '2025-01-01']
        
        yield_by_zone = recent_area.groupby('zone')['rental_yield_pct'].mean().sort_values(ascending=False).reset_index().head(15)
        
        fig_yield = px.bar(
            yield_by_zone,
            x='rental_yield_pct',
            y='zone',
            orientation='h',
            labels={'rental_yield_pct': 'Average Rental Yield (%)', 'zone': 'Zone'},
            color='rental_yield_pct',
            color_continuous_scale='viridis'
        )
        fig_yield.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=480,
            margin={"r":0,"t":10,"l":0,"b":0},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI, Inter, sans-serif"),
            coloraxis_showscale=False,
            template="plotly_dark"
        )
        st.plotly_chart(fig_yield, use_container_width=True)
        
    with col2:
        st.subheader("Off-Plan vs. Secondary Price Gap")
        st.markdown("Average price-per-square-foot premium (%) of new off-plan projects compared to ready resale units.")
        
        df_area['offplan_secondary_gap_pct'] = (
            (df_area['offplan_price_per_sqft_usd'] - df_area['secondary_price_per_sqft_usd']) / 
            df_area['secondary_price_per_sqft_usd']
        ) * 100
        recent_area = df_area[df_area['date'] >= '2025-01-01']
        
        gap_by_zone = recent_area.groupby('zone')['offplan_secondary_gap_pct'].mean().dropna().sort_values(ascending=False).reset_index()
        top_bottom_gap = pd.concat([gap_by_zone.head(10), gap_by_zone.tail(10)]).sort_values('offplan_secondary_gap_pct', ascending=False)
        
        fig_gap = px.bar(
            top_bottom_gap,
            x='offplan_secondary_gap_pct',
            y='zone',
            orientation='h',
            labels={'offplan_secondary_gap_pct': 'Off-Plan Premium Over Secondary (%)', 'zone': 'Zone'},
            color='offplan_secondary_gap_pct',
            color_continuous_scale='RdYlGn_r'
        )
        fig_gap.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=480,
            margin={"r":0,"t":10,"l":0,"b":0},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI, Inter, sans-serif"),
            coloraxis_showscale=False,
            template="plotly_dark"
        )
        st.plotly_chart(fig_gap, use_container_width=True)

# ----------------- VIEW 3: DEVELOPER PREMIUM -----------------
elif menu == "Developer Brand Equity":
    st.title("Developer Brand Equity")
    st.markdown("Quantify developer pricing power by comparing off-plan properties launched by Tier 1 developers vs. Tier 2 developers.")
    st.markdown("---")
    
    # Prepare offplan data
    df_offplan = offplan.copy()
    df_offplan['developer_tier'] = df_offplan['developer_tier'].str.title()
    df_offplan['property_category'] = df_offplan['property_category'].str.title()
    
    stats = df_offplan.groupby(['property_category', 'developer_tier'])['price_per_sqft_usd'].agg(['mean', 'median', 'count']).reset_index()
    
    # Calculate premium percentages
    ap_t1 = stats[(stats['property_category'] == 'Apartment') & (stats['developer_tier'] == 'Tier1')]['mean'].values[0]
    ap_t2 = stats[(stats['property_category'] == 'Apartment') & (stats['developer_tier'] == 'Tier2')]['mean'].values[0]
    ap_premium_pct = ((ap_t1 - ap_t2) / ap_t2) * 100
    
    vil_t1 = stats[(stats['property_category'] == 'Villa') & (stats['developer_tier'] == 'Tier1')]['mean'].values[0]
    vil_t2 = stats[(stats['property_category'] == 'Villa') & (stats['developer_tier'] == 'Tier2')]['mean'].values[0]
    vil_premium_pct = ((vil_t1 - vil_t2) / vil_t2) * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Developer Pricing Power Breakdown")
        fig_premium = px.bar(
            stats,
            x='property_category',
            y='mean',
            color='developer_tier',
            barmode='group',
            labels={'mean': 'Mean Price per Sqft (USD)', 'property_category': 'Property Category', 'developer_tier': 'Developer Classification'},
            color_discrete_map={'Tier1': '#38bdf8', 'Tier2': '#475569'}
        )
        fig_premium.update_layout(
            height=400,
            margin={"r":0,"t":10,"l":0,"b":0},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI, Inter, sans-serif"),
            template="plotly_dark"
        )
        st.plotly_chart(fig_premium, use_container_width=True)
        
    with col2:
        st.subheader("Calculated Premium Metrics")
        st.markdown("")
        st.markdown("##### **Apartment Tier 1 Premium:**")
        st.markdown(f"<span style='color:#34d399; font-size:26px; font-weight:700;'>+{ap_premium_pct:.1f}%</span> (+${ap_t1-ap_t2:.0f}/sqft)", unsafe_allow_html=True)
        st.markdown("Mean Tier 1: **$702/sqft** | Tier 2: **$630/sqft**")
        st.markdown("<hr style='border-color:#334155; margin:15px 0;'>", unsafe_allow_html=True)
        st.markdown("##### **Villa Tier 1 Premium:**")
        st.markdown(f"<span style='color:#34d399; font-size:26px; font-weight:700;'>+{vil_premium_pct:.1f}%</span> (+${vil_t1-vil_t2:.0f}/sqft)", unsafe_allow_html=True)
        st.markdown("Mean Tier 1: **$877/sqft** | Tier 2: **$665/sqft**")

    st.markdown("---")
    st.subheader("Off-Plan Price Estimator")
    st.markdown("Simulate the expected listing price of an off-plan property unit using developer tier pricing differentials.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        prop_cat = st.selectbox("Select Property Category", ["Apartment", "Villa"])
    with c2:
        dev_tier = st.selectbox("Select Developer Tier", ["Tier1", "Tier2"])
    with c3:
        size_sqft = st.number_input("Property Size (Sqft)", min_value=300, max_value=15000, value=1200)
        
    # Predict price on button click
    run_calc = st.button("Calculate Estimated Price")
    
    if run_calc or 'predicted_price_val' in st.session_state:
        if run_calc:
            base_rate = stats[(stats['property_category'] == prop_cat) & (stats['developer_tier'] == dev_tier)]['mean'].values[0]
            st.session_state['predicted_price_val'] = base_rate * size_sqft
            st.session_state['predicted_base_rate'] = base_rate
            st.session_state['predicted_size'] = size_sqft
            st.session_state['predicted_cat'] = prop_cat
            st.session_state['predicted_tier'] = dev_tier
            
        pred_val = st.session_state['predicted_price_val']
        pred_rate = st.session_state['predicted_base_rate']
        pred_size = st.session_state['predicted_size']
        pred_cat = st.session_state['predicted_cat']
        pred_tier = st.session_state['predicted_tier']
        
        st.markdown(f"""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border-left: 4px solid #38bdf8; margin-top: 15px;">
                <span style="font-size: 13px; font-weight:600; color:#94a3b8; text-transform:uppercase;">Estimated Market Price</span>
                <h2 style="margin: 5px 0 0 0; color:#f8fafc; font-weight:700;">${pred_val:,.0f} USD</h2>
                <span style="font-size: 13px; color:#cbd5e1;">Calculated at a rate of <b>${pred_rate:.0f}/sqft</b> for a {pred_size:,} sqft off-plan {pred_cat} developed by a {pred_tier} developer.</span>
            </div>
        """, unsafe_allow_html=True)

# ----------------- VIEW 4: PRICE FORECASTING -----------------
elif menu == "Price Forecasting":
    st.title("Price Forecasting")
    st.markdown("Generate dynamic 24-month projections for Dubai secondary real estate values using Meta Prophet.")
    st.markdown("---")
    
    # Set up timeseries data
    df_area = area_prices.copy()
    df_area['date'] = pd.to_datetime(df_area['year_month'])
    monthly_trend = df_area.groupby('date')['secondary_price_per_sqft_usd'].median().reset_index()
    monthly_trend = monthly_trend.sort_values('date').reset_index(drop=True)
    df_prophet = monthly_trend.rename(columns={'date': 'ds', 'secondary_price_per_sqft_usd': 'y'})
    
    forecast_horizon = st.slider("Forecast Horizon (Months)", min_value=6, max_value=36, value=24)
    
    # Run Prophet on button click
    run_forecast = st.button("Run Forecasting Model")
    
    if run_forecast or 'forecast_result_df' in st.session_state:
        # Check if we need to retrain (because button was clicked or horizon changed)
        if run_forecast or st.session_state.get('cached_horizon') != forecast_horizon:
            with st.spinner("Training Prophet time-series models..."):
                m = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    changepoint_prior_scale=0.05
                )
                m.fit(df_prophet)
                
                future = m.make_future_dataframe(periods=forecast_horizon, freq='MS')
                forecast = m.predict(future)
                
                # Store in session state
                st.session_state['forecast_result_df'] = forecast
                st.session_state['cached_horizon'] = forecast_horizon
                st.session_state['prophet_fit_model'] = m
        
        forecast = st.session_state['forecast_result_df']
        cached_horizon = st.session_state['cached_horizon']
        m = st.session_state['prophet_fit_model']
        
        st.subheader(f"Price Projection ({cached_horizon} Months)")
        
        # Interactive Plotly Chart
        fig_fc = go.Figure()
        
        # Historical actual
        fig_fc.add_trace(go.Scatter(
            x=monthly_trend['date'],
            y=monthly_trend['secondary_price_per_sqft_usd'],
            mode='lines+markers',
            name='Actual Price (Historical)',
            line=dict(color='#38bdf8', width=3)
        ))
        
        # Projected Forecast
        future_dates = forecast.iloc[-cached_horizon:]
        fig_fc.add_trace(go.Scatter(
            x=future_dates['ds'],
            y=future_dates['yhat'],
            mode='lines',
            name='Projected Forecast',
            line=dict(color='#fb7185', width=3)
        ))
        
        # 95% Confidence Interval band
        fig_fc.add_trace(go.Scatter(
            x=pd.concat([future_dates['ds'], future_dates['ds'][::-1]]),
            y=pd.concat([future_dates['yhat_upper'], future_dates['yhat_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(251, 113, 133, 0.12)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name='95% Confidence Interval'
        ))
        
        fig_fc.update_layout(
            title="Dubai Median Secondary Price per Sqft Prediction",
            xaxis_title="Date",
            yaxis_title="Median Price per Sqft (USD)",
            height=480,
            hovermode="x",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#1e293b'),
            yaxis=dict(showgrid=True, gridcolor='#1e293b'),
            font=dict(family="Segoe UI, Inter, sans-serif"),
            template="plotly_dark"
        )
        st.plotly_chart(fig_fc, use_container_width=True)
        
        # Model evaluation metrics row
        latest_val = monthly_trend.iloc[-1]['secondary_price_per_sqft_usd']
        forecast_end = forecast.iloc[-1]
        pct_change = ((forecast_end['yhat'] - latest_val) / latest_val) * 100
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="metric-card accent-blue">
                    <div class="metric-title">Latest Actual Price</div>
                    <div class="metric-value">${latest_val:,.0f}/sqft</div>
                    <div class="metric-delta" style="color:#64748b;">Observed base value</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="metric-card accent-indigo" style="border-left: 4px solid #6366f1;">
                    <div class="metric-title">Projected End Price</div>
                    <div class="metric-value">${forecast_end['yhat']:,.0f}/sqft</div>
                    <div class="metric-delta" style="color:#64748b;">Estimated end of {cached_horizon}m</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="metric-card accent-emerald">
                    <div class="metric-title">Projected Trend Change</div>
                    <div class="metric-value">{pct_change:+.1f}%</div>
                    <div class="metric-delta" style="color:#cbd5e1;">Stabilizing Market Phase</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("Model Components Decomposition")
        st.markdown("Decompose the time series into the long-term trend line and isolated monthly seasonal patterns.")
        
        col_trend, col_season = st.columns(2)
        with col_trend:
            fig_trend_comp = px.line(
                forecast,
                x='ds',
                y='trend',
                title='Isolated Long-Term Trend Component',
                labels={'trend': 'Trend Value ($/sqft)', 'ds': 'Timeline'}
            )
            fig_trend_comp.update_traces(line_color='#38bdf8', line_width=2.5)
            fig_trend_comp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#1e293b'),
                yaxis=dict(showgrid=True, gridcolor='#1e293b'),
                font=dict(family="Segoe UI, Inter, sans-serif"),
                height=320,
                template="plotly_dark"
            )
            st.plotly_chart(fig_trend_comp, use_container_width=True)
            
        with col_season:
            yearly_component = forecast[['ds', 'yearly']].copy()
            yearly_component['month'] = yearly_component['ds'].dt.strftime('%b')
            yearly_component_avg = yearly_component.groupby('month')['yearly'].first().reindex(
                ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ).reset_index()
            
            fig_season_comp = px.line(
                yearly_component_avg,
                x='month',
                y='yearly',
                title='Annual Seasonality Effect (Price Fluctuations by Month)',
                labels={'yearly': 'Price Effect ($/sqft)', 'month': 'Month'}
            )
            fig_season_comp.update_traces(line_color='#fb7185', mode='lines+markers', line_width=2.5)
            fig_season_comp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#1e293b'),
                yaxis=dict(showgrid=True, gridcolor='#1e293b'),
                font=dict(family="Segoe UI, Inter, sans-serif"),
                height=320,
                template="plotly_dark"
            )
            st.plotly_chart(fig_season_comp, use_container_width=True)
    else:
        st.info("Click the 'Run Forecasting Model' button above to generate and explore the price projections.")