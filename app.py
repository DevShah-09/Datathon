
import streamlit as st
import time
import random
from pyvis.network import Network
import streamlit.components.v1 as components

# --- IMPORT MODULES ---
from src.network_manager import NetworkManager
from src.ccp import CCP
from src import predictor  # Your AI Brain

# ======================================================
# CONFIG & STYLING
# ======================================================
st.set_page_config(layout="wide", page_title="NetRisk Nexus", page_icon="⚡")

BG, SIDEBAR, TEXT = "#F5F2E7", "#2E4032", "#2C231E"

st.markdown(f"""
<style>

    /* =========================
       BASE APP STYLING
    ========================= */
    .stApp {{
        background: #F5F2E7;
        color: #2C231E;
    }}

    [data-testid="stSidebar"] {{
        background: #2E4032;
        color: #F5F2E7;
    }}

    /* =========================
       GENERIC CARD
    ========================= */
    .glass-card {{
        background: #FFFBEE;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        color: #2C231E;
    }}
/* ======================================================
       🔥 FINAL FIX — FORCE METRIC BACKGROUND COLOR
       This overrides Streamlit’s injected blue theme
    ====================================================== */

    div[data-testid="stMetric"] {{
        background-color: #c8691c !important;
        padding: 14px 20px !important;
        border-radius: 12px !important;
        color: #FFFBEE !important;

        display: inline-flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;

        min-width: 140px;
    }}

    /* Label */
    div[data-testid="stMetric"] > div[data-testid="stMetricLabel"] {{
        color: #FFFBEE !important;
        opacity: 0.8;
        font-size: 12px !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }}

    /* Value */
    div[data-testid="stMetric"] > div[data-testid="stMetricValue"] {{
        color: #FFFBEE !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
    }}

    /* =========================
       COLUMN FIX
    ========================= */
    [data-testid="column"] > div {{
        align-items: flex-start !important;
    }}

    /* =========================
       CRASH BUTTON OVERRIDE
    ========================= */
    .crash-btn div[data-testid="stButton"] > button {{
    background-color: #adc178 !important;
    color: #ffffff !important;
    border: 2px solid #7a5c2e !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: 0.3s all ease !important;
    box-shadow: 0 4px 0 #7a5c2e !important;
}}

    .crash-btn div[data-testid="stButton"] > button:hover {{
    background-color: #cfe1b9 !important;
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0 #7a5c2e !important;
    }}

    .crash-btn div[data-testid="stButton"] > button:active {{
    transform: translateY(4px) !important;
    box-shadow: none !important;
}}

    div.recovery-btn button {{
    background-color: #27AE60 !important;
    color: white !important;
    border: 2px solid #145A32 !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: 0.3s all ease !important;
    box-shadow: 0 4px 0 #145A32 !important;
}}

div.recovery-btn button:hover {{
    background-color: #2ECC71 !important;
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0 #145A32 !important;
}}

div.recovery-btn button:active {{
    transform: translateY(4px) !important;
    box-shadow: none !important;
}}

</style>

""", unsafe_allow_html=True)



# ======================================================
# DATA POOLS
# ======================================================
ALL_COMPANY_NAMES = [
    "TechCorp", "BioHealth", "SolarSys", "AutoMotive X", "FinServe", 
    "AgriGrow", "CyberDyne", "BlueOcean", "OmegaRetail", "QuantumSoft",
    "Constructo", "MediaGiant", "LogiTrans", "EcoPower", "NanoMed"
]
BANKS = ["Bank A", "Bank B", "Bank C", "Bank D"]
NEWS_TEMPLATES = [
    "reports record quarterly growth",
    "announces new merger talks",
    "expands into European markets",
    "faces minor supply chain delay",
    "launches new AI product line"
]

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def generate_company_data(name):
    """Creates a fresh company with RISKY collateral (Less than Loan)."""
    exposure = random.randint(100, 300) # Loan Amount
    return {
        "id": name,
        "name": name,
        "exposure": exposure,
        "margin": round(exposure * 0.10, 2),  # 10% Initial Margin
        # FIX 1: Collateral is LESS than Loan (70% to 90%)
        # This forces the CCP to use Margin + Default Fund to survive
        "collateral": round(exposure * random.uniform(0.7, 0.9), 2), 
        "status": "HEALTHY",
        "news": f"{name} {random.choice(NEWS_TEMPLATES)}",
        "ai_alert": False
    }

def generate_healthy_transaction(active_companies):
    if not active_companies: return "Market Quiet..."
    lender = random.choice(BANKS)
    borrower = random.choice(active_companies)['name']
    amount = random.randint(20, 100)
    return f"✅ {lender} ➔ {borrower}: ₹{amount} Cr (Settled)"

# ======================================================
# SESSION STATE INITIALIZATION
# ======================================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.is_playing = False
    st.session_state.iteration = 0
    st.session_state.logs = []
    
    # KPIs
    st.session_state.risk_score = 3.5
    st.session_state.global_margin = 10.0
    
    # Pick initial 4 companies
    st.session_state.active_companies = [generate_company_data(n) for n in random.sample(ALL_COMPANY_NAMES, 4)]
    
    st.session_state.network = NetworkManager()
    st.session_state.ccp = CCP()

# ======================================================
# SIMULATION LOOP
# ======================================================
if st.session_state.is_playing:
    st.session_state.iteration += 1
    
    # 1. SHUFFLE COMPANIES (Every 3 iterations)
    if st.session_state.iteration % 3 == 0:
        st.session_state.active_companies.pop(0)
        new_name = random.choice([n for n in ALL_COMPANY_NAMES if n not in [c['name'] for c in st.session_state.active_companies]])
        st.session_state.active_companies.append(generate_company_data(new_name))
        st.session_state.logs.insert(0, f"🔄 MARKET UPDATE: {new_name} entered the market.")

    # 2. GENERATE TRANSACTIONS
    for _ in range(2): 
        txn = generate_healthy_transaction(st.session_state.active_companies)
        st.session_state.logs.insert(0, txn)
    st.session_state.logs = st.session_state.logs[:10]

    # 3. AI RISK SCAN (5% Chance)
    if random.random() < 0.05:
        target = random.choice(st.session_state.active_companies)
        
        # Trigger AI
        ai_result = predictor.get_ai_risk_assessment()
        
        # Update Target
        target['status'] = "RISK DETECTED ⚠️"
        target['ai_alert'] = True
        target['margin'] = round(target['exposure'] * (ai_result['recommended_margin']/100), 2)
        target['news'] = f"⚠️ BREAKING: {target['name']} CFO resigns amid scandal!"
        
        # PAUSE
        st.session_state.is_playing = False
        st.toast(f"🚨 AI ALERT: {target['name']} flagged! Simulation Paused.", icon="🛑")
    
    time.sleep(1) 
    st.rerun()

# ======================================================
# DASHBOARD LAYOUT
# ======================================================

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ NetRisk Nexus")
    st.metric("⏱️ Iteration", st.session_state.iteration)
    
    c1, c2 = st.columns(2)
    if c1.button("▶ START"): st.session_state.is_playing = True; st.rerun()
    if c2.button("⏸ PAUSE"): st.session_state.is_playing = False; st.rerun()
    
    st.divider()
    st.markdown("### 📜 Live Transaction Feed")
    for log in st.session_state.logs:
        st.caption(log)

# --- HEADER METRICS ---
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "System Status",
        "Stable" if st.session_state.is_playing else "Intervention Req"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Active Entities",
        len(st.session_state.active_companies) + 4
    )
    st.markdown('</div>', unsafe_allow_html=True)

with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Global Margin",
        f"{st.session_state.global_margin}%"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with m4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Risk Score",
        f"{st.session_state.risk_score}/10"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# --- MAIN SPLIT ---
col_graph, col_monitor = st.columns([1.5, 2])

# 1. DYNAMIC GRAPH
with col_graph:
    st.markdown('<div class="glass-card"><h4>🌐 Live Market Map</h4>', unsafe_allow_html=True)
    net = Network(height="400px", width="100%", bgcolor="#F5F2E7", font_color="#2C231E")
    for bank in BANKS:
        net.add_node(bank, color="#E67E22", size=20, label=bank)
    for comp in st.session_state.active_companies:
        color = "#C0392B" if "DEFAULT" in comp['status'] else ("#E74C3C" if comp['ai_alert'] else "#27AE60")
        net.add_node(comp['id'], color=color, size=18, label=comp['name'])
        net.add_edge(random.choice(BANKS), comp['id'])
    
    try:
        net.save_graph('net.html')
        with open('net.html', 'r', encoding='utf-8') as f:
            components.html(f.read(), height=420)
    except:
        st.error("Graph Error")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. INSTITUTIONAL MONITOR
with col_monitor:
    st.markdown(
        '<div class="glass-card"><h4>🏢 Institutional Monitor</h4>',
        unsafe_allow_html=True
    )

    for i, comp in enumerate(st.session_state.active_companies):
        border_color = "#E67E22" # Orange (Institutional)
        bg_color = "rgba(39, 174, 96, 0.05)" # Very faint emerald green tint
        
        if comp['ai_alert']: border_color = "#E74C3C"; bg_color = "#FDEDEC" # Bright Red
        if "DEFAULT" in comp['status']: border_color = "#C0392B"; bg_color = "#FFEBEE" # Strong Crimson
        if "SAFE" in comp['status']: border_color = "#27AE60"; bg_color = "#E8F5E9" # Emerald

        st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid {border_color}; background: {bg_color};">
            <div style="display:flex; justify-content:space-between;">
                <h4 style="margin:0;">{comp['name']}</h4>
                <span style="font-weight:bold; color:{border_color};">{comp['status']}</span>
            </div>
            <div style="font-size:12px; color:#666; margin-top:5px;">
                📰 {comp['news']}
            </div>
            <hr style="margin:8px 0;">
            <div style="display:flex; justify-content:space-between; text-align:center;">
                <div><small>Debt (Loan)</small><br><b>₹{comp['exposure']} Cr</b></div>
                <div><small>Margin (Held)</small><br><b>₹{comp['margin']} Cr</b></div>
                <div><small>Collateral (Assets)</small><br><b>₹{comp['collateral']} Cr</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,1,2])

        if comp['ai_alert'] and "DEFAULT" not in comp['status'] and "SAFE" not in comp['status']:
            st.markdown('<div class="crash-btn">', unsafe_allow_html=True)
            if st.button(f"📉 Trigger Crash ({comp['name']})", key=f"crash_{i}"):
                comp['status'] = "DEFAULTED 🚨"
                comp['news'] = "CRITICAL: Company defaulted on loan payment."
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "DEFAULT" in comp['status']:
            if st.button(f"🛡️ Execute Recovery ({comp['name']})", key=f"rec_{i}"):
                loss = comp['exposure']
                margin = comp['margin']
                remaining_debt = loss - margin
                assets_sold_value = round(comp['collateral'] * 0.9, 2)
                final_gap = remaining_debt - assets_sold_value

                if final_gap > 0:
                    comp['news'] = f"✅ RECOVERED: Margin + Assets + CCP Default Fund (₹{round(final_gap,2)} Cr) covered debt."
                    comp['status'] = "SAFE (CCP FUND USED)"
                else:
                    comp['news'] = "✅ RECOVERED: Margin + Assets were sufficient."
                    comp['status'] = "SAFE (RECOVERED)"

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
