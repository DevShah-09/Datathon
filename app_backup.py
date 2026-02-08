
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components
from src.data_engine import DataEngine
from src.news_analyzer import NewsAnalyzer
from src.predictor import PricePredictor
from src.network_manager import NetworkManager
from src.ccp import CCP
import os 
import random
import re

st.set_page_config(layout="wide", page_title="Financial Stability Dashboard")

# --- Professional Light UI Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Universal Text Reset */
    html, body, [class*="css"], .stMarkdown, p, label, li, span {
        font-family: 'Inter', sans-serif !important;
        color: #003566 !important; /* Dark Blue */
    }

    .stApp {
        background-color: #f8fafc !important; /* Slate 50 */
    }

    /* Sidebar - Force Light Consistency */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #ffffff !important;
        color: #003566 !important;
    }

    /* Make the sidebar static / fixed to the left and remove its internal scrollbar */
    [data-testid="stSidebar"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        height: 100vh !important;
        width: 300px !important;
        padding: 1.25rem !important;
        box-shadow: 1px 0 0 rgba(14, 20, 32, 0.04) inset;
        overflow-y: auto !important; /* Allow scrolling */
        z-index: 9999 !important;
        border-right: 1px solid #e2e8f0 !important;
        background-clip: padding-box !important;
        max-height: 100vh !important;
        overscroll-behavior: contain !important;
    }

    /* Hide webkit scrollbars for any inner elements */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Prevent child elements from creating their own scrollbars */
    [data-testid="stSidebar"] * {
        overflow: visible !important;
        max-height: none !important;
    }

    /* Push the main app content to the right so it does not sit under the fixed sidebar */
    div[data-testid="stAppViewContainer"] {
        margin-left: 320px !important; /* sidebar width + gap */
    }

    /* Also ensure the content area inside the app gets enough left padding */
    main, .main {
        margin-left: 0 !important;
    }

    /* Responsive: on small screens revert to normal stacked layout */
    @media (max-width: 900px) {
        [data-testid="stSidebar"] {
            position: relative !important;
            height: auto !important;
            width: 100% !important;
            box-shadow: none !important;
        }
        div[data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
        }
    }

    /* Professional Card Containers */
    .glass-card {
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
    }

    /* Typography */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #003566 !important; /* Dark Blue */
        letter-spacing: -0.025em;
        margin-bottom: 0.25rem;
    }
    
    .subheader {
        font-size: 1.125rem;
        color: #003566 !important; /* Dark Blue */
        margin-bottom: 2rem;
    }
    
    /* Metrics Highlighting */
    [data-testid="stMetricValue"] {
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        color: #003566 !important; /* Dark Blue */
    }
    
    [data-testid="stMetricLabel"] {
        color: #003566 !important; /* Dark Blue */
        font-weight: 500 !important;
    }

    /* News Feed */
    .news-card {
        background-color: #f1f5f9 !important;
        border-left: 4px solid #003566 !important; /* Dark Blue */
        padding: 16px;
        border-radius: 4px;
        margin-top: 12px;
    }
    
    .news-card * {
        color: #003566 !important;
    }

    /* Buttons - Preserve White Text on Blue */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        padding: 12px;
        font-weight: 600;
        background-color: #ffffff !important;
        color: #003566 !important;
        border: 2px solid #003566 !important;
    }
    
    .stButton>button:hover {
        background-color: #f0f4f8 !important;
        border-color: #003566 !important;
    }
    
    /* Input Elements */
    .stSelectbox label, .stToggle label {
        color: #003566 !important;
        font-weight: 500 !important;
        text-align: left !important;
        display: block !important;
        padding: 8px 12px !important; /* increased breathing room around the label text */
        margin: 0 !important;
    }

    /* Ensure the toggle control aligns left and has comfortable padding */
    [data-testid="stSidebar"] .stToggle {
        padding: 6px 0 !important;
        margin: 0 0 10px 0 !important;
        display: flex !important;
        gap: 8px !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }

    [data-testid="stSidebar"] .stToggle label {
        padding: 8px 12px !important;
    }

    [data-testid="stSidebar"] .stToggle [role="switch"] {
        margin-left: 0 !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
    }
    
    /* Dropdown Menu Styling */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [role="option"] {
        background-color: #ffffff !important;
        color: #003566 !important;
    }
    
    [role="option"]:hover {
        background-color: #f0f4f8 !important;
    }
    
    /* Enhanced Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.25rem !important;
    }
    
    /* Sidebar Header */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #003566 !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
    }
    
    /* Section Headers */
    [data-testid="stSidebar"] h4 {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-top: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Divider Styling */
    [data-testid="stSidebar"] hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        border-top: 1px solid #e2e8f0 !important;
    }
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] button {
        width: 100% !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    /* Toggle Switch Styling */
    [data-testid="stSidebar"] [role="switch"] {
        width: 100% !important;
    }

    /* ===== MODERN SIDEBAR STYLING (Terlice Design) ===== */
    
    /* Sidebar Container - Clean Modern Look */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
        padding: 0 !important;
    }
    
    /* Sidebar Header / Logo Area */
    .sidebar-header {
        padding: 20px 16px !important;
        border-bottom: 1px solid #f3f4f6 !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    
    .sidebar-logo {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #003566 !important;
        margin: 0 !important;
    }
    
    /* Navigation Menu */
    .nav-item {
        padding: 12px 16px !important;
        margin: 4px 8px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        font-size: 14px !important;
        color: #6b7280 !important;
        font-weight: 500 !important;
    }
    
    .nav-item:hover {
        background-color: #f3f4f6 !important;
        color: #003566 !important;
    }
    
    .nav-item.active {
        background-color: #dbeafe !important;
        color: #003566 !important;
        font-weight: 600 !important;
    }
    
    .nav-icon {
        font-size: 18px !important;
    }
    
    /* Sidebar Section Title */
    .sidebar-section {
        padding: 24px 0 12px 0 !important;
    }
    
    .sidebar-section-title {
        padding: 12px 16px 8px 16px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #9ca3af !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Update sections headers */
    [data-testid="stSidebar"] h4 {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #9ca3af !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-top: 20px !important;
        margin-bottom: 12px !important;
        padding: 0 16px !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] button {
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }
    
    [data-testid="stSidebar"] hr {
        margin: 0 !important;
        display: none !important;
    }
    /* Collapse/Expand Text */
    [data-testid="collapsedControl"] {
        font-size: 0 !important;
    }
    
    [data-testid="collapsedControl"]::before {
        content: "Expand" !important;
        font-size: 0.85rem !important;
        color: #003566 !important;
    }
    
    [data-testid="expandedControl"] {
        font-size: 0 !important;
    }
    
    [data-testid="expandedControl"]::before {
        content: "Collapse" !important;
        font-size: 0.85rem !important;
        color: #003566 !important;
    }
    
    
    /* Total suppression of any text-based icon leaks */
    [data-testid="collapsedControl"],
    [data-testid="expandedControl"],
    button[aria-label*="sidebar"],
    button[aria-label*="Close"] {
        font-size: 0 !important;
        color: transparent !important;
        text-indent: -9999px !important; /* Move text far off-screen */
    }

    /* Restore custom symbols via pseudo-elements only */
    [data-testid="collapsedControl"]::before,
    button[aria-label*="sidebar"]::before {
        content: "▶" !important;
        text-indent: 0 !important;
        font-size: 1.2rem !important;
        color: #003566 !important;
        visibility: visible !important;
        display: block !important;
        float: none !important;
    }

    [data-testid="expandedControl"]::before,
    button[aria-label*="Close"]::before {
        content: "◀" !important;
        text-indent: 0 !important;
        font-size: 1.2rem !important;
        color: #003566 !important;
        visibility: visible !important;
        display: block !important;
        float: none !important;
    }

    /* Change PyVis navigation button and control colors from green to dark blue */
    /* CSS injected directly into network HTML for better targeting */

    /* Top navbar styling (dark blue with white text) */
    header, .stApp header, div[data-testid="stToolbar"] {
        background-color: #032b4a !important;
        color: #ffffff !important;
    }
    /* Make Streamlit top-menu items white */
    #MainMenu, #MainMenu * {
        visibility: visible !important;
        color: #ffffff !important;
    }

    /* Sidebar button focus/active highlight */
    [data-testid="stSidebar"] .stButton>button:focus,
    [data-testid="stSidebar"] .stButton>button:active {
        background-color: #003566 !important;
        color: #ffffff !important;
        border-color: #003566 !important;
    }

    /* Selectbox styling in sidebar: right-side dropdown indicator kept */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        border: 2px solid #003566 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        background-color: #ffffff !important;
    }

    /* Style selectboxes and buttons to be clean but visible */
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        border-color: #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #9ca3af !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* Hide white box columns in sidebar (Simulation buttons row) */
    [data-testid="stSidebar"] [data-testid="column"] {
        display: none !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- App Logic & Simulation ---

# Initialize Session State
if 'round' not in st.session_state:
    st.session_state.round = 0
    st.session_state.ai_enabled = True
    st.session_state.is_playing = False 
    st.session_state.show_details = False 
    st.session_state.history = []
    st.session_state.network = NetworkManager()
    st.session_state.ccp = CCP()
    st.session_state.data_engine = DataEngine()
    st.session_state.news_analyzer = NewsAnalyzer()
    st.session_state.predictor = PricePredictor()
    st.session_state.last_intervention = None 
    st.session_state.sidebar_collapsed = False
    
    # Pre-train LSTM
    with st.spinner("Training Neural Network Brain..."):
        hist_data = st.session_state.data_engine.get_historical_data(period="1y")
        jpm_data = hist_data['JPM']['Close']
        sequences = st.session_state.predictor.prepare_data(jpm_data)
        if sequences:
            st.session_state.predictor.train_model(sequences, epochs=3)
    st.session_state.market_data = jpm_data

# --- Hero Section ---
st.markdown('<h1 class="main-header">finance</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">AI-Driven Systemic Risk Management & Central Counterparty Simulation</p>', unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    # Sidebar Header
    st.markdown('<div class="sidebar-header"><div class="sidebar-logo">finance</div></div>', unsafe_allow_html=True)
    
    # Main Navigation
    st.markdown('<div class="sidebar-section-title">Main</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item active"><span class="nav-icon"></span><span>Dashboard</span></div>', unsafe_allow_html=True)
    
    # AI Settings
    st.markdown('<div class="sidebar-section-title" style="margin-top:20px;">Settings</div>', unsafe_allow_html=True)
    ai_toggle = st.toggle("AI Sentiment Analysis", value=st.session_state.ai_enabled)
    st.session_state.ai_enabled = ai_toggle
    st.session_state.ccp.set_mode(ai_toggle)
    
    # Simulation Section
    st.markdown('<div class="sidebar-section-title" style="margin-top:20px;">Simulation</div>', unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        if st.button("Advance Step", type="primary"):
            st.session_state.is_playing = False 
            advance_round = True
        else:
            advance_round = False
            
    with sim_col2:
        if st.session_state.is_playing:
            if st.button("Stop Simulation"):
                st.session_state.is_playing = False
                st.rerun()
        else:
            if st.button("Start Simulation"):
                st.session_state.is_playing = True
                st.rerun()

    # Risk Management Section
    st.markdown('<div class="sidebar-section-title" style="margin-top:20px;">Risk Management</div>', unsafe_allow_html=True)
    major_banks = [n for n, d in st.session_state.network.G.nodes(data=True) if d['type'] == 'hub']
    target_bank = st.selectbox("Select Bank to Fail", major_banks)
    
    if st.button("Trigger Bank Failure"):
        if target_bank:
            st.session_state.is_playing = False 
            st.session_state.round += 1
            st.session_state.network.fail_node(target_bank)
            impacted_banks, intervention = st.session_state.network.update_contagion(ccp=st.session_state.ccp)
            st.session_state.last_intervention = intervention
            st.session_state.show_details = True # AUTO-OPEN ON FAILURE
            
            headlines = st.session_state.news_analyzer.fetch_headlines()
            market_headline = random.choice(headlines) if headlines else "Global markets watch volatility closely."
            shock_headline = f"BREAKING: {target_bank} has officially entered Bankruptcy proceedings."
            analysis = st.session_state.news_analyzer.analyze_risk(shock_headline)
            margin = st.session_state.ccp.calculate_margin(analysis['health_score'], -0.25)
            
            st.session_state.history.append({
                'round': st.session_state.round,
                'headline': shock_headline,
                'market_news': [market_headline],
                'system_alerts': [shock_headline] + [f"Exposure Alert: {bank} capital buffer dropping." for bank in impacted_banks[:3]],
                'intervention': intervention,
                'analysis': analysis,
                'margin': margin,
                'margin_delta': 0,
                'actual_price': st.session_state.market_data.values[-1] * 0.75,
                'predicted_price': st.session_state.market_data.values[-1],
                'impacted_banks': impacted_banks,
                'system_health': np.mean([data['wealth'] for n, data in st.session_state.network.G.nodes(data=True)])
            })
            st.toast(f"{target_bank} HAS FAILED")
        else:
            st.warning("Please select a bank to trigger failure.")

    # --- View More Insights (Persistent Section) ---
    if st.session_state.last_intervention:
        st.markdown('<div class="sidebar-section-title" style="margin-top:20px;">System Analysis</div>', unsafe_allow_html=True)
        if st.button("View More Information", use_container_width=True):
            st.session_state.show_details = not st.session_state.show_details
            
        if st.session_state.show_details:
            report = st.session_state.last_intervention
            st.markdown(f"**CCP Report: {report['detailed_events'][0]['failed_bank'] if report['detailed_events'] else 'N/A'}**")
            
            sc1, sc2 = st.columns(2)
            with sc1:
                st.metric("Covered", f"${report['absorbed']:.1f}M")
            with sc2:
                status_color = "green" if report['remaining_loss'] == 0 else "red"
                status_text = "STABLE" if report['remaining_loss'] == 0 else "STRESSED"
                st.markdown(f"<div style='background:{status_color}; color:white; padding:4px 8px; border-radius:4px; text-align:center; font-weight:700; margin-top:10px;'>{status_text}</div>", unsafe_allow_html=True)
            
            if report.get('detailed_events'):
                df_inter = pd.DataFrame(report['detailed_events'])
                col_map = {'target_bank': 'Connected Bank', 'allotment': 'CCP Coverage ($M)', 'status': 'Status'}
                df_display = df_inter.rename(columns=col_map)
                st.dataframe(df_display[['Connected Bank', 'CCP Coverage ($M)', 'Status']], hide_index=True)
            else:
                st.info("No counterparty hits requiring cash waterfall injection.")

    # --- Simulation Execution (Moved to bottom of sidebar) ---
    if advance_round or st.session_state.is_playing:
        st.session_state.round += 1
        
        # 1. Prediction (ML Model)
        last_30_days = st.session_state.market_data.values[-30:]
        prediction = st.session_state.predictor.predict(last_30_days)
        actual_price = last_30_days[-1] * (1 + np.random.normal(0, 0.012)) 
        
        new_date = st.session_state.market_data.index[-1] + pd.Timedelta(days=1)
        st.session_state.market_data[new_date] = actual_price
        
        # 2. Fetch News & Analyze
        headlines = st.session_state.news_analyzer.fetch_headlines()
        selected_headline = random.choice(headlines) if headlines else "Market activity remains stable under CCP oversight."
        analysis = st.session_state.news_analyzer.analyze_risk(selected_headline)
        
        # 3. Update CCP & Novation
        price_change = (actual_price - last_30_days[-1]) / last_30_days[-1]
        old_margin = st.session_state.ccp.current_margin
        margin = st.session_state.ccp.calculate_margin(analysis['health_score'], price_change)
        
        # CCP handles random transaction volume
        trade_volume = random.randint(30, 150)
        st.session_state.ccp.perform_novation(num_trades=trade_volume)
        
        # 4. Update Network & Contagion
        G = st.session_state.network.G
        impacted_banks, intervention = st.session_state.network.update_contagion(ccp=st.session_state.ccp)
        if intervention:
            st.session_state.last_intervention = intervention
            
        for node in G.nodes():
            if G.nodes[node]['status'] != 'failed':
                G.nodes[node]['wealth'] *= (1 + np.random.normal(0, 0.015))
        
        # 5. Update History
        st.session_state.history.append({
            'round': st.session_state.round,
            'headline': selected_headline,
            'market_news': [selected_headline],
            'system_alerts': [f"Contagion monitoring: {len(impacted_banks)} alerts active."] if impacted_banks else [],
            'analysis': analysis,
            'margin': margin,
            'margin_delta': margin - old_margin,
            'actual_price': actual_price,
            'predicted_price': prediction,
            'impacted_banks': impacted_banks,
            'intervention': intervention,
            'system_health': np.mean([data['wealth'] for n, data in G.nodes(data=True)])
        })
        
        if st.session_state.is_playing:
            import time
            time.sleep(0.5)
            st.rerun()


# --- Main Page Layout ---
col_net, col_metrics = st.columns([2.2, 1])

with col_net:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Financial Contagion Map")
    
    # Configure Network with Light Theme focus & Navigation controls
    net = Network(height="520px", width="100%", bgcolor="white", font_color="#003566")
    
    # Disable zoom scroll, enable navigation buttons
    net.set_options("""
    {
      "interaction": {
        "zoomView": false,
        "navigationButtons": true
      }
    }
    """)
    
    G = st.session_state.network.G
    for node, data in G.nodes(data=True):
        label = f"<b>{node}</b><br>${data['wealth']:.1f}M"
        # Status-based coloring for clarity (UI-only change)
        if data['status'] == 'failed':
            # Maroon for the failing bank
            color = "#800000"
        else:
            # If any neighbor has failed, highlight this node as scarlet/orange
            try:
                neighbor_failed = any(G.nodes[nbr]['status'] == 'failed' for nbr in G.neighbors(node))
            except Exception:
                neighbor_failed = False

            if neighbor_failed:
                # Scarlet/orange for banks linked to a failing bank
                color = "#ff4500"
            elif data['status'] == 'stressed':
                color = "#f97316" # Orange for Contagion hit
            elif data['type'] == 'hub':
                color = "#7dd3fc" # Light Blue for Major Banks
            else:
                color = "#cbd5e1" # Slate for Regional Banks
            
        size = 35 if data['type'] == 'hub' else 18
        net.add_node(node, label=node, title=label, color=color, size=size, font={'color': '#003566', 'size': 14, 'face': 'Inter'})
    
    for u, v, data in G.edges(data=True):
        # Edge color based on contagion path
        u_failed = G.nodes[u]['status'] == 'failed'
        v_failed = G.nodes[v]['status'] == 'failed'
        if u_failed or v_failed:
            edge_color = "#ef4444" # Red link for active failure leakage
        elif G.nodes[u]['status'] == 'stressed' or G.nodes[v]['status'] == 'stressed':
            edge_color = "#f97316" # Orange for spreading stress
        else:
            edge_color = "#8b5cf6" # Normal violet links
            
        net.add_edge(u, v, color=edge_color, width=data['weight']*4)
    
    net.save_graph("network.html")
    with open("network.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace green color codes with dark blue #003566
    # Replace #00aa00 (hex) with #003566
    html_content = re.sub(r'#00aa00', '#003566', html_content, flags=re.IGNORECASE)
    # Replace #00AA00 (uppercase hex) with #003566
    html_content = re.sub(r'#00AA00', '#003566', html_content, flags=re.IGNORECASE)
    # Replace rgb(0, 170, 0) with rgb(0, 53, 102) [RGB equivalent of #003566]
    html_content = re.sub(r'rgb\(\s*0\s*,\s*170\s*,\s*0\s*\)', 'rgb(0, 53, 102)', html_content, flags=re.IGNORECASE)
    
    components.html(html_content, height=550)
    st.markdown('</div>', unsafe_allow_html=True)

with col_metrics:
    # Metric Grid
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("CCP Intelligence")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("Margin Req", f"{st.session_state.ccp.current_margin*100:.0f}%", 
                  delta=f"{st.session_state.history[-1]['margin_delta']*100:.1f}%" if st.session_state.history else None)
    with m_col2:
        st.metric("Risk Score", f"{st.session_state.history[-1]['analysis']['health_score'] if st.session_state.history else 10}/10")
    
    st.divider()
    
    st.write("**News Analysis**")
    if st.session_state.history:
        event = st.session_state.history[-1]
        
        # System Alerts (Priority)
        if event.get('system_alerts'):
            for alert in event['system_alerts']:
                st.markdown(f"""
                    <div class="news-card" style="border-left-color: #ef4444; background-color: rgba(239, 68, 68, 0.05);">
                        <small style="color: #ef4444; font-weight: 700;">SYSTEMIC ALERT</small><br>
                        <b style="color: #003566">{alert}</b>
                    </div>
                """, unsafe_allow_html=True)
        
        # Market News
        if event.get('market_news'):
            for news in event['market_news']:
                st.markdown(f"""
                    <div class="news-card">
                        <small style="color: #003566">MARKET FEED</small><br>
                        <b style="color: #003566">{news}</b>
                    </div>
                """, unsafe_allow_html=True)
                
        # AI Logic Reasoning
        st.markdown(f"""
            <div style="background: #f8fafc; padding: 12px; border-radius: 8px; margin-top: 15px; border: 2px solid #003566;">
                <p style="font-size: 0.85rem; color: #003566; margin: 0;"><b>AI Analysis:</b> {event['analysis']['reasoning']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("System initialized. Monitoring markets...")
        
    st.divider()
    m3, m4 = st.columns(2)
    with m3:
        st.metric("Cash Waterfall", f"${st.session_state.ccp.cash_waterfall/1000:.1f}B")
    with m4:
        st.metric("Contracts", f"{st.session_state.ccp.active_contracts}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Bottom Visuals ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Pattern Recognition & Stability Forecasting")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if st.session_state.history:
        h_df = pd.DataFrame(st.session_state.history)
        fig = px.line(h_df, x='round', y=['actual_price', 'predicted_price'], 
                     title="LSTM Market Prediction vs Reality",
                     template="plotly_white", color_discrete_sequence=["#2563eb", "#64748b"])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Awaiting simulation data for predictive analysis.")

with chart_col2:
    if st.session_state.history:
        h_df = pd.DataFrame(st.session_state.history)
        fig_health = px.area(h_df, x='round', y='system_health', 
                           title="Systemic Liquidity Index",
                           template="plotly_white", color_discrete_sequence=["#2563eb"])
        fig_health.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_health, use_container_width=True)
    else:
        st.info("Awaiting simulation statistics.")
st.markdown('</div>', unsafe_allow_html=True)
