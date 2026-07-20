import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="AutoOracle AI — Sri Lanka Car Valuation",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PREMIUM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    scroll-behavior: smooth;
}

/* ── BACKGROUND ── */
.stApp {
    background: #020817;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(56,189,248,0.12), transparent),
        radial-gradient(ellipse 60% 40% at 100% 60%, rgba(168,85,247,0.08), transparent),
        radial-gradient(ellipse 50% 60% at 0% 80%, rgba(20,184,166,0.07), transparent);
    color: #e2e8f0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(2, 10, 28, 0.85) !important;
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-right: 1px solid rgba(56,189,248,0.1) !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}
[data-testid="stSidebarNavItems"] { display: none; }

/* ── INPUTS ── */
.stSelectbox [data-baseweb="select"] > div,
.stNumberInput input,
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    transition: border-color 0.2s ease !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within,
.stNumberInput input:focus {
    border-color: rgba(56,189,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12) !important;
}

/* Slider Track */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    box-shadow: 0 0 12px rgba(56,189,248,0.5) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.4) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px rgba(99,102,241,0.6) !important;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
}
.stButton > button:active { transform: translateY(-1px) !important; }

/* ── DIVIDERS & TEXT ── */
hr { border-color: rgba(56,189,248,0.1) !important; margin: 1.5rem 0 !important; }
p, span, div { color: #cbd5e1; }
h1, h2, h3, h4 { color: #f8fafc !important; }
strong, b { color: #f1f5f9 !important; }

/* ── HERO SECTION ── */
.hero-container {
    background: linear-gradient(135deg,
        rgba(14,165,233,0.08) 0%,
        rgba(99,102,241,0.08) 50%,
        rgba(168,85,247,0.08) 100%);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 30%, rgba(56,189,248,0.06), transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 900;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    letter-spacing: -2px;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #94a3b8;
    font-weight: 400;
    margin: 0;
    max-width: 600px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.hero-stat {
    display: flex;
    flex-direction: column;
}
.hero-stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #38bdf8;
}
.hero-stat-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}

/* ── METRIC CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.75rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    cursor: default;
}
.kpi-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    opacity: 0;
    transition: opacity 0.3s ease;
    background: radial-gradient(circle at 50% 0%, rgba(56,189,248,0.08), transparent 70%);
}
.kpi-card:hover {
    transform: translateY(-6px);
    border-color: rgba(56,189,248,0.3);
    box-shadow: 0 20px 60px -10px rgba(56,189,248,0.2);
}
.kpi-card:hover::after { opacity: 1; }

.kpi-card.accent-green { border-top: 3px solid #10b981; }
.kpi-card.accent-blue  { border-top: 3px solid #38bdf8; }
.kpi-card.accent-red   { border-top: 3px solid #f43f5e; }

.kpi-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
    display: block;
}
.kpi-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.kpi-value.green { color: #10b981; }
.kpi-value.blue  { color: #38bdf8; }
.kpi-value.red   { color: #f43f5e; }
.kpi-delta {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
}

/* ── SECTION HEADER ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2.5rem 0 1.25rem 0;
}
.section-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    flex-shrink: 0;
    box-shadow: 0 0 12px rgba(56,189,248,0.6);
}
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
    letter-spacing: -0.5px;
}

/* ── PRICE RANGE BANNER ── */
.price-range-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(16,185,129,0.05));
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.price-range-banner::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #10b981, #059669);
    border-radius: 4px 0 0 4px;
}
.price-range-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #10b981;
    margin-bottom: 0.5rem;
}
.price-range-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.5px;
}
.price-range-note {
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 0.25rem;
}

/* ── FACTOR PILLS ── */
.factor-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.85rem;
    margin: 4px 4px 4px 0;
    color: #cbd5e1;
    transition: all 0.2s ease;
}
.factor-pill.positive { border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.06); }
.factor-pill.neutral  { border-color: rgba(250,204,21,0.3); background: rgba(250,204,21,0.06); }
.factor-pill.negative { border-color: rgba(244,63,94,0.3); background: rgba(244,63,94,0.06); }

/* ── EXAMPLE CARDS ── */
.example-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    height: 100%;
}
.example-card:hover {
    border-color: rgba(56,189,248,0.25);
    transform: translateY(-4px);
    box-shadow: 0 16px 40px -10px rgba(56,189,248,0.15);
}
.example-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.example-card-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.88rem;
}
.example-card-row:last-child { border-bottom: none; }
.example-card-key { color: #64748b; font-weight: 500; }
.example-card-val { color: #cbd5e1; font-weight: 600; }
.example-card-estimate {
    margin-top: 1rem;
    padding: 10px;
    background: rgba(56,189,248,0.07);
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
    color: #38bdf8;
    font-size: 1rem;
}

/* ── SIDEBAR SIDEBAR LABEL ── */
.sidebar-section {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #475569 !important;
    margin: 1.25rem 0 0.5rem 0;
    display: block;
}

/* ── STREAMLIT OVERRIDES ── */
.block-container { padding-top: 2rem !important; max-width: 1200px !important; }
.stPlotlyChart { border-radius: 16px; overflow: hidden; }
[data-testid="stMarkdownContainer"] p { color: #cbd5e1; line-height: 1.7; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── ANIMATIONS ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-container { animation: fadeInUp 0.6s ease both; }
.kpi-card { animation: fadeInUp 0.6s ease both; }
.kpi-card:nth-child(2) { animation-delay: 0.1s; }
.kpi-card:nth-child(3) { animation-delay: 0.2s; }
</style>
""", unsafe_allow_html=True)


# ─── MODEL ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return joblib.load('car_prediction_model_sl.pkl')
    except FileNotFoundError:
        return None

model = load_model()

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="font-size:1.4rem; font-weight:800; color:#f8fafc; letter-spacing:-0.5px;">
            🚘 AutoOracle <span style="color:#38bdf8;">AI</span>
        </div>
        <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">Sri Lanka Vehicle Valuation</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="sidebar-section">📅 Basic Details</span>', unsafe_allow_html=True)
    year = st.slider('Manufacturing Year', 2000, 2024, 2015)
    present_price = st.number_input('Ex-Showroom Price (Rs. Lakhs)', 0.0, 1000.0, 75.0, 1.0)
    kms_driven    = st.number_input('Kilometers Driven', 0, 500000, 50000, 1000)

    st.markdown('<span class="sidebar-section">⚙️ Specifications</span>', unsafe_allow_html=True)
    fuel_type    = st.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG'])
    seller_type  = st.selectbox('Seller Type', ['Dealer', 'Individual'])
    transmission = st.selectbox('Transmission', ['Manual', 'Automatic'])
    owner        = st.selectbox('Previous Owners', [0, 1, 2, 3])

    st.markdown("---")
    predict_btn = st.button("⚡ Get AI Valuation", use_container_width=True)

    # Quick info pill
    current_year = 2024
    car_age = current_year - year
    st.markdown(f"""
    <div style="margin-top:1rem; padding:12px; background:rgba(56,189,248,0.06);
                border-radius:12px; border:1px solid rgba(56,189,248,0.12); text-align:center;">
        <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Car Age</div>
        <div style="font-size:1.8rem; font-weight:800; color:#38bdf8;">{car_age} yrs</div>
    </div>
    """, unsafe_allow_html=True)

# ─── HERO SECTION ──────────────────────────────────────────────────────────────
if model is None:
    st.error("⚠️ **Model not found.** Please run `car-price-prediction.ipynb` first to train the model.")
    st.stop()

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🇱🇰 &nbsp; Sri Lanka Edition &nbsp;·&nbsp; AI Powered</div>
    <h1 class="hero-title">AutoOracle AI</h1>
    <p class="hero-subtitle">
        Enterprise-grade machine learning that predicts the true market value of your
        vehicle in seconds — tailored for the Sri Lankan automotive market.
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-value">~85%</span>
            <span class="hero-stat-label">Model Accuracy</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-value">300+</span>
            <span class="hero-stat-label">Data Points</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-value">3</span>
            <span class="hero-stat-label">ML Algorithms</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── RESULTS ───────────────────────────────────────────────────────────────────
if predict_btn:
    fuel_encoded         = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}[fuel_type]
    seller_encoded       = {'Dealer': 0, 'Individual': 1}[seller_type]
    transmission_encoded = {'Manual': 0, 'Automatic': 1}[transmission]

    input_data = pd.DataFrame({
        'Year': [year], 'Present_Price': [present_price], 'Kms_Driven': [kms_driven],
        'Fuel_Type': [fuel_encoded], 'Seller_Type': [seller_encoded],
        'Transmission': [transmission_encoded], 'Owner': [owner]
    })

    predicted_price       = model.predict(input_data)[0]
    depreciation          = present_price - predicted_price
    depreciation_percent  = (depreciation / present_price) * 100 if present_price > 0 else 0
    retention_rate        = 100 - depreciation_percent

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3 class="section-title">Valuation Results</h3>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card accent-green">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">Estimated Selling Price</div>
            <div class="kpi-value green">Rs. {predicted_price:,.1f}L</div>
            <div class="kpi-delta">AI-predicted fair market value</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card accent-blue">
            <span class="kpi-icon">🏷️</span>
            <div class="kpi-label">Original Showroom Price</div>
            <div class="kpi-value blue">Rs. {present_price:,.1f}L</div>
            <div class="kpi-delta">Brand-new ex-showroom value</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card accent-red">
            <span class="kpi-icon">📉</span>
            <div class="kpi-label">Total Depreciation</div>
            <div class="kpi-value red">Rs. {depreciation:,.1f}L</div>
            <div class="kpi-delta">↓ {depreciation_percent:.1f}% value lost · {retention_rate:.1f}% retained</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Market Analysis ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3 class="section-title">Market Analysis</h3>
    </div>""", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        lower_est = predicted_price * 0.9
        upper_est = predicted_price * 1.1

        st.markdown(f"""
        <div class="price-range-banner">
            <div class="price-range-label">✅ Expected Price Range</div>
            <div class="price-range-value">Rs. {lower_est:,.1f}L — Rs. {upper_est:,.1f}L</div>
            <div class="price-range-note">Typical negotiation range for similar vehicles in the Sri Lankan used-car market.</div>
        </div>""", unsafe_allow_html=True)

        # Factor pills
        st.markdown("<div style='margin-bottom:0.5rem; font-size:0.85rem; font-weight:600; color:#94a3b8;'>VALUE FACTORS</div>", unsafe_allow_html=True)
        pills_html = ""
        if car_age <= 2:
            pills_html += '<span class="factor-pill positive">🟢 Near-new · Low depreciation</span>'
        elif car_age <= 5:
            pills_html += '<span class="factor-pill positive">🟡 Relatively new · Good resale</span>'
        elif car_age <= 10:
            pills_html += '<span class="factor-pill neutral">🟠 Moderate age · Avg value</span>'
        else:
            pills_html += '<span class="factor-pill negative">🔴 High age · Heavy depreciation</span>'

        if kms_driven < 30000:
            pills_html += '<span class="factor-pill positive">🟢 Low mileage · Value boost</span>'
        elif kms_driven < 80000:
            pills_html += '<span class="factor-pill neutral">🟡 Average mileage</span>'
        else:
            pills_html += '<span class="factor-pill negative">🔴 High mileage · Value drop</span>'

        if transmission == 'Automatic':
            pills_html += '<span class="factor-pill positive">🟢 Automatic · Premium tag</span>'
        if fuel_type == 'Diesel':
            pills_html += '<span class="factor-pill positive">🟢 Diesel · Economy preferred</span>'
        elif fuel_type == 'Petrol':
            pills_html += '<span class="factor-pill neutral">🟡 Petrol · Standard</span>'
        if owner == 0:
            pills_html += '<span class="factor-pill positive">🟢 First owner · Premium</span>'
        elif owner >= 2:
            pills_html += '<span class="factor-pill negative">🔴 Multiple owners · Reduced</span>'

        st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:6px;">{pills_html}</div>', unsafe_allow_html=True)

        # Depreciation bar chart
        st.markdown("<br>", unsafe_allow_html=True)
        bar_data = pd.DataFrame({
            'Category': ['Current Selling Value', 'Depreciation Lost'],
            'Amount': [predicted_price, depreciation],
            'Color': ['#10b981', '#f43f5e']
        })
        fig_bar = px.bar(
            bar_data, x='Amount', y='Category', orientation='h',
            color='Category',
            color_discrete_map={'Current Selling Value': '#10b981', 'Depreciation Lost': '#f43f5e'},
            text=[f"Rs. {predicted_price:.1f}L", f"Rs. {depreciation:.1f}L"]
        )
        fig_bar.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Inter', 'color': '#94a3b8'},
            margin=dict(l=10, r=20, t=10, b=10),
            height=180,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False),
        )
        fig_bar.update_traces(textposition='inside', textfont_color='white', textfont_size=13, textfont_family='Inter', marker_line_width=0, selector=dict(type='bar'))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        # Premium Gauge
        max_price = present_price * 1.1
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_price,
            number={
                'prefix': "Rs. ", 'suffix': "L",
                'font': {'color': '#f8fafc', 'size': 32, 'family': 'Inter'},
                'valueformat': ',.1f'
            },
            gauge={
                'axis': {
                    'range': [0, max_price],
                    'tickwidth': 1,
                    'tickcolor': "rgba(255,255,255,0.12)",
                    'tickfont': {'color': '#475569', 'size': 10}
                },
                'bar': {'color': 'rgba(56,189,248,0.9)', 'thickness': 0.25},
                'bgcolor': 'rgba(255,255,255,0.03)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, max_price * 0.4],              'color': 'rgba(244,63,94,0.2)'},
                    {'range': [max_price * 0.4, max_price * 0.75], 'color': 'rgba(250,204,21,0.2)'},
                    {'range': [max_price * 0.75, max_price],      'color': 'rgba(16,185,129,0.2)'},
                ],
                'threshold': {
                    'line': {'color': '#818cf8', 'width': 4},
                    'thickness': 0.8,
                    'value': present_price * 0.95
                }
            }
        ))
        fig_gauge.add_annotation(
            text=f"Showroom: Rs. {present_price:.0f}L",
            x=0.5, y=-0.12, showarrow=False,
            font={'color': '#64748b', 'size': 11, 'family': 'Inter'},
            xref='paper', yref='paper'
        )
        fig_gauge.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#94a3b8', 'family': 'Inter'}
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

    # ── Summary Table ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="margin-top:2rem;">
        <div class="section-dot"></div>
        <h3 class="section-title">Vehicle Summary</h3>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    details = [
        ("🗓️ Manufacturing Year", str(year)),
        ("⏳ Vehicle Age", f"{car_age} years"),
        ("🛣️ Kilometers Driven", f"{kms_driven:,} km"),
        ("⛽ Fuel Type", fuel_type),
        ("⚙️ Transmission", transmission),
        ("🏪 Seller Type", seller_type),
        ("👤 Previous Owners", str(owner)),
        ("💵 Showroom Price", f"Rs. {present_price:.2f} Lakhs"),
    ]
    rows_html = ""
    for key, val in details:
        rows_html += f"""
        <div class="example-card-row">
            <span class="example-card-key">{key}</span>
            <span class="example-card-val">{val}</span>
        </div>"""
    half = len(details) // 2
    with col_a:
        html_a = "".join(f"""<div class="example-card-row">
            <span class="example-card-key">{k}</span>
            <span class="example-card-val">{v}</span></div>""" for k,v in details[:half])
        st.markdown(f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">{html_a}</div>', unsafe_allow_html=True)
    with col_b:
        html_b = "".join(f"""<div class="example-card-row">
            <span class="example-card-key">{k}</span>
            <span class="example-card-val">{v}</span></div>""" for k,v in details[half:])
        st.markdown(f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">{html_b}</div>', unsafe_allow_html=True)

# ─── LANDING PAGE ──────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3 class="section-title">Sample Valuations</h3>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    examples = [
        ("🏎️", "Recent Model", "2020", "Rs. 130L", "20,000 km", "Petrol / Auto", "Rs. 100L – 115L"),
        ("🚗", "Mid-Range",    "2015", "Rs. 90L",  "50,000 km", "Diesel / Manual", "Rs. 55L – 65L"),
        ("🚙", "Older Model",  "2010", "Rs. 75L",  "100,000 km","Petrol / Manual", "Rs. 25L – 35L"),
    ]
    for col, (icon, title, yr, price, km, spec, est) in zip([col1, col2, col3], examples):
        with col:
            st.markdown(f"""
            <div class="example-card">
                <div class="example-card-title">{icon} {title}</div>
                <div class="example-card-row">
                    <span class="example-card-key">Year</span>
                    <span class="example-card-val">{yr}</span>
                </div>
                <div class="example-card-row">
                    <span class="example-card-key">Showroom</span>
                    <span class="example-card-val">{price}</span>
                </div>
                <div class="example-card-row">
                    <span class="example-card-key">Mileage</span>
                    <span class="example-card-val">{km}</span>
                </div>
                <div class="example-card-row">
                    <span class="example-card-key">Specs</span>
                    <span class="example-card-val">{spec}</span>
                </div>
                <div class="example-card-estimate">Est. Value: {est}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3 class="section-title">System Intelligence</h3>
    </div>""", unsafe_allow_html=True)

    sys_col1, sys_col2, sys_col3, sys_col4 = st.columns(4)
    sys_info = [
        ("🤖", "Algorithm", "Random Forest"),
        ("🎯", "Accuracy", "~85%"),
        ("📊", "Training Samples", "300+"),
        ("🇱🇰", "Market", "Sri Lanka"),
    ]
    for col, (icon, label, val) in zip([sys_col1, sys_col2, sys_col3, sys_col4], sys_info):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:center; padding:1.25rem 1rem;">
                <span class="kpi-icon" style="font-size:1.5rem;">{icon}</span>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value blue" style="font-size:1.25rem;">{val}</div>
            </div>""", unsafe_allow_html=True)
