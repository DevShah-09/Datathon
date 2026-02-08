import streamlit as st
import time
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

# --- IMPORT MODULES ---
from src.network_manager import NetworkManager
from src.ccp import CCP
from src import predictor  # Your AI Brain

# ======================================================
# CONFIG & STYLING
# ======================================================
st.set_page_config(layout="wide", page_title="NetRisk Nexus", page_icon="⚡")

# Theme Colors
BG_COLOR = "#fcfffd"
SIDEBAR_COLOR = "#153b50"
TEXT_COLOR = "#2C231E"
CARD_BG = "#134074"
METRIC_BG = "#4f5d75"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Base App Styling */
    .stApp {{
        background: {BG_COLOR};
        color: {TEXT_COLOR};
    }}

    [data-testid="stSidebar"] {{
        background: {SIDEBAR_COLOR};
        color: #FFFFFF;
    }}

    /* Card Styling */
    .glass-card {{
        background: {CARD_BG};
        border-radius: 26px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        color: #FFFBEE;
        text-align: center;
        padding: 25px;
    }}

    /* Metric Override */
    div[data-testid="stMetric"], .stMetric {{
        background-color: {METRIC_BG} !important;
        padding: 14px 20px !important;
        border-radius: 12px !important;
        color: #FFFBEE !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    div[data-testid="stMetricLabel"] p {{
        color: #FFFBEE !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stMetricValue"] div {{
        color: #FFFBEE !important;
        font-size: 26px !important;
        font-weight: 800 !important;
    }}

    /* --- BUTTON STYLING (FIXED BLACK COLOR ISSUE) --- */
    
    /* Default Buttons (Start, Pause, Recovery, Reset) */
    div[data-testid="stButton"] > button {{
        background-color: #27AE60;
        color: white !important;
        border: none;
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }}
    div[data-testid="stButton"] > button:hover {{
        background-color: #2ECC71;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: white !important;
    }}

    /* Primary Buttons (Trigger Crash - RED) */
    button[kind="primary"] {{
        background-color: #b23a48 !important;
        color: white !important;
        border: 1px solid #7a1c29 !important;
    }}
    button[kind="primary"]:hover {{
        background-color: #d64556 !important;
        color: white !important;
    }}

    /* Payoff Table Styling */
    .payoff-table-container {{
        background: {CARD_BG};
        border-radius: 20px;
        padding: 15px;
        margin-top: 20px;
        overflow: hidden;
    }}
    .payoff-table {{
        width: 100%;
        border-collapse: collapse;
        color: #FFFBEE;
        font-size: 14px;
    }}
    .payoff-table th {{
        background: {METRIC_BG};
        padding: 15px;
        text-align: left;
        font-weight: 800;
        text-transform: uppercase;
    }}
    .payoff-table td {{
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255,251,238,0.1);
    }}
    .status-badge {{
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
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
def calculate_risk_score(active_companies, ccp_stress=0):
    if not active_companies: return 1.0
    base_risk = 1.0
    alert_penalty = sum(2.0 for c in active_companies if c.get('ai_alert'))
    default_penalty = sum(4.0 for c in active_companies if "DEFAULT" in c.get('status', ''))
    stress_penalty = ccp_stress * 1.5
    total_risk = base_risk + alert_penalty + default_penalty + stress_penalty
    return min(9.9, round(total_risk, 1))

def calculate_global_margin(risk_score):
    if risk_score < 3: return 10.0
    if risk_score < 6: return 15.0
    if risk_score < 8: return 20.0
    return 25.0

def get_market_sentiment(risk_score):
    if risk_score < 3: return "BULLISH"
    if risk_score < 5: return "NEUTRAL"
    if risk_score < 7: return "NERVOUS"
    return "PANIC"

def generate_company_data(name):
    exposure = random.randint(100, 300) 
    return {
        "id": name,
        "name": name,
        "exposure": exposure,
        "margin": round(exposure * 0.10, 2),  
        # FIXED: Collateral is now LESS than debt (80% to 95%) to create Gap Risk
        "collateral": round(exposure * random.uniform(0.80, 0.95), 2), 
        "status": "HEALTHY",
        "news": f"{name} {random.choice(NEWS_TEMPLATES)}",
        "ai_alert": False
    }

def generate_healthy_transaction(active_companies):
    if not active_companies: return "Market Quiet..."
    lender = random.choice(BANKS)
    borrower = random.choice(active_companies)['name']
    amount = random.randint(20, 100)
    return f"{lender} ➔ {borrower}: ₹{amount} Cr (Settled)"

# ======================================================
# SESSION STATE INIT
# ======================================================
for key, default in [('iteration', 0), ('logs', []), ('show_payoffs', False), 
                     ('show_ccp_funds', False), ('is_playing', False), ('ccp_stress', 0), 
                     ('risk_score', 1.0), ('global_margin', 10.0)]:
    if key not in st.session_state:
        st.session_state[key] = default

if 'active_companies' not in st.session_state:
    st.session_state.active_companies = [generate_company_data(n) for n in random.sample(ALL_COMPANY_NAMES, 4)]

if 'network' not in st.session_state:
    st.session_state.network = NetworkManager()
    st.session_state.ccp = CCP()

# ======================================================
# SIMULATION ENGINE
# ======================================================
if st.session_state.is_playing:
    st.session_state.iteration += 1
    
    # 1. Shuffle Companies (Every 3 ticks)
    if st.session_state.iteration % 3 == 0:
        st.session_state.active_companies.pop(0)
        new_name = random.choice([n for n in ALL_COMPANY_NAMES if n not in [c['name'] for c in st.session_state.active_companies]])
        st.session_state.active_companies.append(generate_company_data(new_name))
        st.session_state.logs.insert(0, f"MARKET UPDATE: {new_name} entered the market.")

    # 2. Transactions
    for _ in range(2): 
        txn = generate_healthy_transaction(st.session_state.active_companies)
        st.session_state.logs.insert(0, txn)
    st.session_state.logs = st.session_state.logs[:10]

    # 3. AI Risk Scan
    if random.random() < 0.05:
        target = random.choice(st.session_state.active_companies)
        ai_result = predictor.get_ai_risk_assessment()
        
        target['status'] = "RISK DETECTED"
        target['ai_alert'] = True
        target['margin'] = round(target['exposure'] * (ai_result['recommended_margin']/100), 2)
        # Squeeze collateral to create gap risk
        target['collateral'] = round(target['exposure'] * random.uniform(0.7, 0.8), 2)
        target['news'] = f"BREAKING: {target['name']} CFO resigns amid scandal!"
        
        st.session_state.is_playing = False
        st.toast(f"AI ALERT: {target['name']} flagged! Simulation Paused.", icon="🛑")
    
    st.session_state.risk_score = calculate_risk_score(st.session_state.active_companies, st.session_state.ccp_stress)
    st.session_state.global_margin = calculate_global_margin(st.session_state.risk_score)
    
    time.sleep(1) 
    st.rerun()

# ======================================================
# DASHBOARD UI
# ======================================================

with st.sidebar:
    st.title("NetRisk Nexus")
    st.metric("Iteration", st.session_state.iteration)
    
    if st.button("View Payoffs", use_container_width=True):
        st.session_state.show_payoffs = not st.session_state.show_payoffs
        st.rerun()
    
    if st.button("CCP Funds", use_container_width=True):
        st.session_state.show_ccp_funds = not st.session_state.show_ccp_funds
        st.rerun()
    
    c1, c2 = st.columns(2)
    if c1.button("▶ START"): st.session_state.is_playing = True; st.rerun()
    if c2.button("⏸ PAUSE"): st.session_state.is_playing = False; st.rerun()
    
    st.divider()
    st.markdown("### Live Feed")
    for log in st.session_state.logs:
        st.caption(log)


# --- METRICS ---
# ALWAYS recalculate risk score before display (even when paused)
st.session_state.risk_score = calculate_risk_score(st.session_state.active_companies, st.session_state.ccp_stress)
st.session_state.global_margin = calculate_global_margin(st.session_state.risk_score)

m1, m2, m3, m4 = st.columns(4)

# Determine if intervention is required based on crisis events
has_alert = any(c.get('ai_alert') for c in st.session_state.active_companies)
has_default = any("DEFAULT" in c.get('status', '') for c in st.session_state.active_companies)
needs_intervention = has_alert or has_default or st.session_state.ccp_stress > 0

# Get market sentiment for display
market_sentiment = get_market_sentiment(st.session_state.risk_score)

with m1: st.metric("System Status", "Intervention Req" if needs_intervention else "Normal")
with m2: st.metric("Market Sentiment", market_sentiment)
with m3: st.metric("Global Margin", f"{st.session_state.global_margin}%")
with m4: st.metric("Risk Score", f"{st.session_state.risk_score}/10")



# --- MAIN CONTENT ---
col_graph, col_monitor = st.columns([1.5, 2])

# 1. Graph
with col_graph:
    st.markdown('<div class="glass-card"><h4>Live Market Map</h4>', unsafe_allow_html=True)
    net = Network(height="400px", width="100%", bgcolor="#edf6f9", font_color="#2C231E")
    for bank in BANKS:
        net.add_node(bank, color="#134074", size=20, label=bank)
    for comp in st.session_state.active_companies:
        color = "#b23a48" if "DEFAULT" in comp['status'] else ("#4f5d75" if comp['ai_alert'] else "#27AE60")
        net.add_node(comp['id'], color=color, size=18, label=comp['name'])
        net.add_edge(random.choice(BANKS), comp['id'])
    
    try:
        net.save_graph('net.html')
        with open('net.html', 'r', encoding='utf-8') as f:
            components.html(f.read(), height=420)
    except:
        st.error("Graph Error")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Monitor
with col_monitor:
    st.markdown('<div class="glass-card"><h4>Institutional Monitor</h4>', unsafe_allow_html=True)

    for i, comp in enumerate(st.session_state.active_companies):
        border_color = "#4f5d75" 
        bg_color = "#f4f7f9"
        
        if comp['ai_alert']: border_color = "#134074"; bg_color = "#e6f0ff"
        if "DEFAULT" in comp['status']: border_color = "#b23a48"; bg_color = "#fce8e8"
        if "SAFE" in comp['status']: border_color = "#27AE60"; bg_color = "#e8f5e9"

        with st.container():
            st.markdown(f"""
            <div class="glass-card" style="border-left: 6px solid {border_color}; background: {bg_color}; border-radius: 30px; color: #092327;">
                <div style="padding: 10px;">
                    <div style="display:flex; justify-content:space-between; align-items: center;">
                        <h4 style="margin:0;">{comp['name']}</h4>
                        <span style="font-weight:bold; color:{border_color};">{comp['status']}</span>
                    </div>
                    <div style="font-size:12px; color:#666; margin-top:5px;">📰 {comp['news']}</div>
                    <hr style="margin:10px 0;">
                    <div style="display:flex; justify-content:space-between; text-align:center;">
                        <div><small>Debt</small><br><b>₹{comp['exposure']}</b></div>
                        <div><small>Margin</small><br><b>₹{comp['margin']}</b></div>
                        <div><small>Collateral</small><br><b>₹{comp['collateral']}</b></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1,1,2])
            
            # TRIGGER CRASH (Use primary type for RED styling)
            if comp['ai_alert'] and "DEFAULT" not in comp['status'] and "SAFE" not in comp['status']:
                if st.button(f"Trigger Crash ({comp['name']})", key=f"crash_{i}", type="primary"):
                    comp['status'] = "DEFAULTED"
                    comp['news'] = "CRITICAL: Default triggered."
                    comp['collateral'] = round(comp['exposure'] * random.uniform(0.6, 0.8), 2)
                    # IMMEDIATELY UPDATE RISK SCORE
                    st.session_state.risk_score = calculate_risk_score(st.session_state.active_companies, st.session_state.ccp_stress)
                    st.session_state.global_margin = calculate_global_margin(st.session_state.risk_score)
                    st.rerun()

            # RECOVERY (Use default type which is styled GREEN via CSS)
            if "DEFAULT" in comp['status']:
                if st.button(f"Execute Recovery ({comp['name']})", key=f"rec_{i}"):
                    loss = comp['exposure']
                    margin = comp['margin']
                    remaining = loss - margin
                    sold = round(comp['collateral'] * 0.9, 2)
                    gap = remaining - sold
                    
                    if gap > 0:
                        comp['news'] = f"RECOVERED: Margin + Assets + Fund (₹{round(gap,2)} Cr) covered debt."
                        comp['status'] = "SAFE (CCP FUND USED)"
                        st.session_state.ccp_stress += 1
                        
                        # UPDATE CCP FUNDS
                        st.session_state.ccp.cash_waterfall -= gap
                        st.session_state.ccp.allotment_log.append({
                            'target_bank': 'Lender Consortium',
                            'failed_bank': comp['name'],
                            'allotment': gap,
                            'status': 'Fully Protected'
                        })
                    else:
                        comp['news'] = "RECOVERED: Margin + Assets were sufficient."
                        comp['status'] = "SAFE (RECOVERED)"
                    
                    comp['ai_alert'] = False
                    # IMMEDIATELY UPDATE RISK SCORE
                    st.session_state.risk_score = calculate_risk_score(st.session_state.active_companies, st.session_state.ccp_stress)
                    st.session_state.global_margin = calculate_global_margin(st.session_state.risk_score)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- PAYOFF SUMMARY (FIXED) ---
if st.session_state.show_payoffs:
    st.divider()
    st.markdown("### 💰 Entity Payoff Summary")
    
    payoff_data = []
    
    # 1. Add Banks (Mock Data for Display)
    for b in BANKS:
        payoff_data.append({
            "Entity Name": b,
            "Type": "CORE BANK",
            "Status": "HEALTHY",
            "Net Payoff": "₹500.00 Cr"
        })

    # 2. Add Companies
    if 'active_companies' in st.session_state:
        for comp in st.session_state.active_companies:
            equity = round(comp.get('margin',0) + comp.get('collateral',0) - comp.get('exposure',0), 2)
            payoff_data.append({
                "Entity Name": comp.get('name', 'Unknown'),
                "Type": "BORROWER",
                "Status": comp.get('status', 'Unknown'),
                "Net Payoff": f"₹{equity} Cr"
            })
    
    # Render HTML Table Safely
    if payoff_data:
        # We build this string carefully without indentation to avoid Markdown treating it as code
        html_rows = ""
        for item in payoff_data:
            status = item['Status']
            badge_bg = "#27AE60" if "SAFE" in status or "HEALTHY" in status else "#b23a48"
            html_rows += f"<tr><td><b>{item['Entity Name']}</b></td><td><small>{item['Type']}</small></td><td><span class='status-badge' style='background:{badge_bg}; color:white;'>{status}</span></td><td style='font-weight:800; color:#adc178;'>{item['Net Payoff']}</td></tr>"

        html_structure = f"""
        <div class="payoff-table-container">
            <table class="payoff-table">
                <thead><tr><th>Entity</th><th>Type</th><th>Status</th><th>Net Payoff</th></tr></thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
        </div>
        """
        st.markdown(html_structure, unsafe_allow_html=True)
    else:
        st.info("No data available.")

# --- CCP FUNDS DISPLAY ---
if st.session_state.show_ccp_funds:
    st.divider()
    st.markdown("### 🏦 CCP Fund Status")
    
    # Get CCP data
    ccp = st.session_state.ccp
    initial_fund = 50000  # Initial $50B
    current_fund = ccp.cash_waterfall
    used_fund = initial_fund - current_fund
    utilization_pct = (used_fund / initial_fund) * 100
    
    # Display fund metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Cash Waterfall", f"${current_fund:,.0f}M")
    with col2:
        st.metric("📊 Fund Utilization", f"{utilization_pct:.1f}%")
    with col3:
        st.metric("🚨 Total Interventions", st.session_state.ccp_stress)
    with col4:
        st.metric("💸 Funds Deployed", f"${used_fund:,.0f}M")
    
    # Display allotment history if available
    if ccp.allotment_log:
        st.markdown("#### 📋 Intervention History")
        
        allotment_rows = ""
        for i, event in enumerate(reversed(ccp.allotment_log[-10:])):  # Show last 10 events
            status_color = "#27AE60" if event['status'] == 'Fully Protected' else "#f4a261"
            allotment_rows += f"<tr><td><b>#{len(ccp.allotment_log) - i}</b></td><td>{event['failed_bank']}</td><td>{event['target_bank']}</td><td style='font-weight:800; color:#adc178;'>${event['allotment']:,.2f}M</td><td><span class='status-badge' style='background:{status_color}; color:white;'>{event['status']}</span></td></tr>"
        
        allotment_table = f"""<div class="payoff-table-container"><table class="payoff-table"><thead><tr><th>#</th><th>Failed Entity</th><th>Protected Entity</th><th>CCP Allotment</th><th>Status</th></tr></thead><tbody>{allotment_rows}</tbody></table></div>"""
        st.markdown(allotment_table, unsafe_allow_html=True)
    else:
        st.info("No CCP interventions yet. The fund remains at full capacity.")
    
    # Fund health indicator
    st.markdown("#### 🎯 Fund Health")
    if utilization_pct < 20:
        st.success(f"✅ **HEALTHY** - CCP fund is at {100-utilization_pct:.1f}% capacity. System can absorb significant losses.")
    elif utilization_pct < 50:
        st.warning(f"⚠️ **MODERATE** - CCP fund is at {100-utilization_pct:.1f}% capacity. Monitor for additional stress.")
    elif utilization_pct < 80:
        st.warning(f"🟠 **STRESSED** - CCP fund is at {100-utilization_pct:.1f}% capacity. Limited buffer remaining.")
    else:
        st.error(f"🚨 **CRITICAL** - CCP fund is at {100-utilization_pct:.1f}% capacity. System at risk of failure!")
