

# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import plotly.express as px
# # # from pyvis.network import Network
# # # import streamlit.components.v1 as components
# # # from src.data_engine import DataEngine
# # # from src.news_analyzer import NewsAnalyzer
# # # from src.predictor import PricePredictor
# # # from src.network_manager import NetworkManager
# # # from src.ccp import CCP
# # # import random, re, time

# # # # ======================================================
# # # # PAGE CONFIG
# # # # ======================================================
# # # st.set_page_config(layout="wide", page_title="Financial Stability Dashboard")

# # # # ======================================================
# # # # 🔥 GLOBAL CSS (FIXES GHOST BARS)
# # # # ======================================================
# # # st.markdown("""
# # # <style>
# # # @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

# # # /* ---------- GLOBAL ---------- */
# # # html, body, [class*="css"] {
# # #     font-family: 'Inter', sans-serif !important;
# # #     background: #000000 !important;
# # #     color: #e6f7ff !important;
# # # }

# # # .stApp {
# # #     background: #000000 !important;
# # # }

# # # /* ---------- HERO ---------- */
# # # .main-header {
# # #     font-size: 2.6rem;
# # #     font-weight: 800;
# # #     color: #00e6ff;
# # #     margin-bottom: 0.2rem;
# # # }
# # # .subheader {
# # #     font-size: 1.15rem;
# # #     color: #9befff;
# # #     margin-bottom: 1.8rem;
# # # }

# # # /* ---------- CARDS ---------- */
# # # .glass-card {
# # #     background: #071226;
# # #     border-radius: 12px;
# # #     padding: 24px;
# # #     border: 1px solid rgba(0,230,255,0.12);
# # #     box-shadow: 0 6px 30px rgba(0,0,0,0.7);
# # #     margin-bottom: 24px;
# # # }

# # # /* ======================================================
# # #    🔥 ACTUAL FIX — REMOVE EMPTY STREAMLIT BLOCKS
# # ======================================================
# # THEME (LIGHT MODE ONLY — OLIVE UNDERTONES)
# # ======================================================
# # Dark mode removed; UI uses a fixed light theme with olive accents
# bg = "#f6f7f2"
# card = "#ffffff"
# text = "#21321a"
# accent = "#6B8E23"
# # # footer { visibility: hidden; }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # ======================================================
# # # # SESSION STATE
# # # # ======================================================
# # # if "round" not in st.session_state:
# # #     st.session_state.round = 0
# # #     st.session_state.is_playing = False
# # #     st.session_state.history = []
# # #     st.session_state.network = NetworkManager()
# # #     st.session_state.ccp = CCP()
# # #     st.session_state.data_engine = DataEngine()
# # #     st.session_state.news_analyzer = NewsAnalyzer()
# # #     st.session_state.predictor = PricePredictor()

# # #     with st.spinner("Training Neural Network Brain..."):
# # #         hist = st.session_state.data_engine.get_historical_data(period="1y")
# # #         prices = hist["JPM"]["Close"]
# # #         seq = st.session_state.predictor.prepare_data(prices)
# # #         if seq:
# # #             st.session_state.predictor.train_model(seq, epochs=3)
# # #         st.session_state.market_data = prices

# # # # ======================================================
# # # # HERO SECTION (NO EMPTY BLOCKS BELOW THIS)
# # # # ======================================================
# # # st.markdown('<h1 class="main-header">finance</h1>', unsafe_allow_html=True)
# # # st.markdown(
# # #     '<p class="subheader">AI-Driven Systemic Risk Management & Central Counterparty Simulation</p>',
# # #     unsafe_allow_html=True
# # # )

# # # # ======================================================
# # # # SIDEBAR
# # # # ======================================================
# # # with st.sidebar:
# # #     st.markdown("## finance")

# # #     st.markdown("### Simulation")
# # #     if st.button("Start / Stop Simulation"):
# # #         st.session_state.is_playing = not st.session_state.is_playing

# # #     st.markdown("### Risk Management")
# # #     hubs = [n for n, d in st.session_state.network.G.nodes(data=True) if d["type"] == "hub"]
# # #     bank = st.selectbox("Select Bank to Fail", hubs)

# # #     if st.button("Trigger Bank Failure"):
# # #         st.session_state.network.fail_node(bank)

# # # # ======================================================
# # # # SIMULATION LOOP
# # # # ======================================================
# # # if st.session_state.is_playing:
# # #     st.session_state.round += 1
# # #     time.sleep(0.4)

# # # # ======================================================
# # # # MAIN LAYOUT
# # # # ======================================================
# # # col_net, col_metrics = st.columns([2.2, 1])

# # # # ---------------- NETWORK ----------------
# # # with col_net:
# # #     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# # #     st.subheader("Financial Contagion Map")

# # #     net = Network(
# # #         height="520px",
# # #         width="100%",
# # #         bgcolor="#000000",
# # #         font_color="#e6f7ff"
# # #     )

# # #     net.set_options("""
# # #     {
# # #       "interaction": {
# # #         "zoomView": false,
# # #         "navigationButtons": true
# # #       }
# # #     }
# # #     """)

# # #     G = st.session_state.network.G
# # #     for node, data in G.nodes(data=True):
# # #         color = "#7dd3fc" if data["type"] == "hub" else "#cbd5e1"
# # #         if data["status"] == "failed":
# # #             color = "#800000"

# # #         net.add_node(
# # #             node,
# # #             label=node,
# # #             size=35 if data["type"] == "hub" else 18,
# # #             color=color,
# # #             font={"color": "#e6f7ff"}
# # #         )

# # #     for u, v, d in G.edges(data=True):
# # #         net.add_edge(u, v, width=d["weight"] * 4, color="#8b5cf6")

# # #     net.save_graph("network.html")
# # #     html = open("network.html", encoding="utf-8").read()
# # #     html = html.replace("background-color: white", "background-color: #000000")
# # #     components.html(html, height=550)

# # #     st.markdown("</div>", unsafe_allow_html=True)

# # # # ---------------- METRICS ----------------
# # # with col_metrics:
# # #     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# # #     st.subheader("CCP Intelligence")

# # #     st.metric("Margin Requirement", f"{st.session_state.ccp.current_margin*100:.0f}%")
# # #     st.metric("Risk Score", "10 / 10")

# # #     st.markdown("</div>", unsafe_allow_html=True)

# # # # ======================================================
# # # # CHARTS
# # # # ======================================================
# # # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# # # st.subheader("Pattern Recognition & Stability Forecasting")

# # # c1, c2 = st.columns(2)

# # # with c1:
# # #     if st.session_state.history:
# # #         df = pd.DataFrame(st.session_state.history)
# # #         fig = px.line(df, x="round", y=["actual_price", "predicted_price"])
# # #         fig.update_layout(
# # #             plot_bgcolor="rgba(0,0,0,0)",
# # #             paper_bgcolor="rgba(0,0,0,0)"
# # #         )
# # #         st.plotly_chart(fig, use_container_width=True)
# # #     else:
# # #         st.info("Awaiting simulation data.")

# # # with c2:
# # #     if st.session_state.history:
# # #         df = pd.DataFrame(st.session_state.history)
# # #         fig = px.area(df, x="round", y="system_health")
# # #         fig.update_layout(
# # #             plot_bgcolor="rgba(0,0,0,0)",
# # #             paper_bgcolor="rgba(0,0,0,0)"
# # #         )
# # #         st.plotly_chart(fig, use_container_width=True)
# # #     else:
# # #         st.info("Awaiting statistics.")

# # # st.markdown("</div>", unsafe_allow_html=True)


# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import plotly.express as px
# # from pyvis.network import Network
# # import streamlit.components.v1 as components
# # from src.data_engine import DataEngine
# # from src.news_analyzer import NewsAnalyzer
# # from src.predictor import PricePredictor
# # from src.network_manager import NetworkManager
# # from src.ccp import CCP
# # import time

# # # ======================================================
# # # PAGE CONFIG
# # # ======================================================
# # st.set_page_config(
# #     layout="wide",
# #     page_title="Financial Stability Dashboard",
# #     page_icon="⚡"
# # )


# # # ======================================================
# # # THEME COLORS (DARK/LIGHT)
# # # ======================================================
# # if "dark_mode" not in st.session_state:
# #     st.session_state.dark_mode = True

# # st.session_state.dark_mode = dark_mode

# # if st.session_state.dark_mode:
# #     bg = "#000000"
# #     card = "rgba(7,18,38,0.85)"
# #     text = "#e6f7ff"
# #     accent = "#00E6FF"
# # else:
# #     bg = "#f8fafc"
# #     card = "#ffffff"
# #     text = "#00121a"
# #     accent = "#003566"


# # # ======================================================
# # # 🔥 PREMIUM GLOBAL UI CSS
# # # ======================================================
# # st.markdown("""
# # <style>
# # @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

# # html, body {
# #     font-family: "Inter", sans-serif;
# #     background: radial-gradient(circle at top, #071226, #000000) !important;
# #     color: #e6f7ff !important;
# # }

# # .stApp {
# #     background: radial-gradient(circle at top, #071226, #000000) !important;
# # }

# # /* Sidebar */
# # section[data-testid="stSidebar"] {
# #     background: rgba(7,18,38,0.97) !important;
# #     border-right: 1px solid rgba(0,230,255,0.2);
# # }

# # section[data-testid="stSidebar"] h1 {
# #     font-size: 22px !important;
# #     font-weight: 800 !important;
# #     color: #00E6FF !important;
# # }

# # /* Buttons */
# # .stButton button {
# #     border-radius: 14px !important;
# #     padding: 12px !important;
# #     font-weight: 700 !important;
# #     border: 1px solid rgba(0,230,255,0.4) !important;
# #     background: rgba(0,230,255,0.06) !important;
# #     transition: 0.25s ease;
# # }

# # .stButton button:hover {
# #     background: rgba(0,230,255,0.18) !important;
# #     transform: scale(1.04);
# # }

# # /* Cards */
# # .glass-card {
# #     background: rgba(7,18,38,0.85);
# #     border-radius: 18px;
# #     padding: 24px;
# #     border: 1px solid rgba(0,230,255,0.15);
# #     box-shadow: 0 0 25px rgba(0,230,255,0.08);
# #     margin-bottom: 20px;
# # }

# # /* Metrics */
# # [data-testid="stMetricValue"] {
# #     font-size: 30px !important;
# #     font-weight: 800 !important;
# #     color: #00E6FF !important;
# # }

# # [data-testid="stMetricLabel"] {
# #     font-size: 13px !important;
# #     color: #9befff !important;
# # }

# # footer {visibility: hidden;}
            
# #             /* ✅ REMOVE EMPTY RECTANGLE GHOST BLOCKS */
# # [data-testid="stHorizontalBlock"]:empty {
# #     display: none !important;
# # }

# # [data-testid="column"]:empty {
# #     display: none !important;
# # }

# # div:empty {
# #     display: none !important;
# # }

# # </style>
# # """, unsafe_allow_html=True)

# # # ======================================================
# # # SESSION STATE INIT
# # # ======================================================
# # if "round" not in st.session_state:
# #     st.session_state.round = 0
# #     st.session_state.is_playing = False
# #     st.session_state.history = []

# #     st.session_state.network = NetworkManager()
# #     st.session_state.ccp = CCP()
# #     st.session_state.data_engine = DataEngine()
# #     st.session_state.news_analyzer = NewsAnalyzer()
# #     st.session_state.predictor = PricePredictor()

# #     with st.spinner("⚡ Training AI Risk Engine..."):
# #         hist = st.session_state.data_engine.get_historical_data(period="1y")
# #         prices = hist["JPM"]["Close"]

# #         seq = st.session_state.predictor.prepare_data(prices)
# #         if seq:
# #             st.session_state.predictor.train_model(seq, epochs=3)

# #         st.session_state.market_data = prices

# # # ======================================================
# # # HERO SECTION
# # # ======================================================
# # st.markdown("""
# # <h1 style="font-size:2.8rem;font-weight:800;color:#00E6FF;margin-bottom:0;">
# # finance ⚡
# # </h1>
# # <p style="font-size:1.15rem;color:#9befff;margin-top:0;">
# # AI-Driven Systemic Risk & CCP Contagion Simulation Engine
# # </p>
# # """, unsafe_allow_html=True)

# # # ======================================================
# # # KPI TOP ROW (Premium Dashboard Feel)
# # # ======================================================
# # k1, k2, k3, k4 = st.columns(4)

# # with k1:
# #     st.metric("System Health", "Stable")

# # with k2:
# #     st.metric("Active Banks", len(st.session_state.network.G.nodes()))

# # with k3:
# #     st.metric("Margin Req", f"{st.session_state.ccp.current_margin*100:.0f}%")

# # with k4:
# #     st.metric("Risk Score", "10 / 10")



# # # ======================================================
# # # SIDEBAR CONTROL CENTER
# # # ======================================================
# # with st.sidebar:
# #     st.markdown("finance ⚡ Risk Engine")

# #     dark_mode = st.toggle("🌙 Dark Mode", value=True)


# #     st.markdown("### Simulation Controls")
# #     col1, col2 = st.columns(2)

# #     with col1:
# #         if st.button("▶ Run"):
# #             st.session_state.is_playing = True

# #     with col2:
# #         if st.button("⏸ Pause"):
# #             st.session_state.is_playing = False

# #     st.markdown("### Stress Test Scenario")

# #     hubs = [n for n, d in st.session_state.network.G.nodes(data=True)
# #             if d["type"] == "hub"]

# #     bank = st.selectbox("Target Institution", hubs)

# #     if st.button("🔥 Trigger Failure"):
# #         st.session_state.network.fail_node(bank)
# #         st.toast(f"🚨 {bank} HAS FAILED")


# # st.session_state.dark_mode = dark_mode


# # # ======================================================
# # # SIMULATION LOOP
# # # ======================================================
# # if st.session_state.is_playing:
# #     st.session_state.round += 1

# #     # --- Market price (from historical data if available, otherwise simulate) ---
# #     try:
# #         prices = st.session_state.market_data
# #         idx = st.session_state.round % len(prices)
# #         actual_price = float(prices.iloc[idx])
# #     except Exception:
# #         actual_price = float(st.session_state.market_data.values[-1]) if hasattr(st.session_state, "market_data") else 100.0

# #     # --- Prediction using trained model (fallback to actual_price on error) ---
# #     try:
# #         last_seq = np.array(st.session_state.market_data.values[-30:])
# #         predicted_price = float(st.session_state.predictor.predict(last_seq))
# #     except Exception:
# #         predicted_price = actual_price

# #     # --- Update contagion dynamics via NetworkManager + CCP intervention ---
# #     try:
# #         impacted, report = st.session_state.network.update_contagion(ccp=st.session_state.ccp)
# #     except Exception:
# #         impacted, report = [], None

# #     total_nodes = st.session_state.network.G.number_of_nodes()
# #     failed_nodes = len([n for n, d in st.session_state.network.G.nodes(data=True) if d.get("status") == "failed"])
# #     system_health = max(0, 100 - (failed_nodes / total_nodes) * 100) if total_nodes else 100

# #     # --- Append to history for plotting ---
# #     st.session_state.history.append({
# #         "round": st.session_state.round,
# #         "actual_price": actual_price,
# #         "predicted_price": predicted_price,
# #         "system_health": system_health
# #     })

# #     time.sleep(0.4)
# #     st.experimental_rerun()

# # # ======================================================
# # # MAIN DASHBOARD LAYOUT
# # # ======================================================
# # col_net, col_metrics = st.columns([2.3, 1])

# # # ======================================================
# # # NETWORK GRAPH PANEL
# # # ======================================================
# # with col_net:
# #     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# #     st.subheader("Financial Contagion Map")

# #     net = Network(
# #         height="520px",
# #         width="100%",
# #         bgcolor="#000000",
# #         font_color="#e6f7ff"
# #     )

# #     net.set_options("""
# #         {
# #             "interaction": {
# #                 "zoomView": false,
# #                 "navigationButtons": true
# #             }
# #         }
# #         """)

# #     G = st.session_state.network.G

# #     for node, data in G.nodes(data=True):
# #         color = "#7dd3fc" if data["type"] == "hub" else "#cbd5e1"
# #         if data["status"] == "failed":
# #             color = "#ff0033"

# #         net.add_node(
# #             node,
# #             label=node,
# #             size=38 if data["type"] == "hub" else 18,
# #             color=color,
# #             font={"color": "#e6f7ff"}
# #         )

# #     for u, v, d in G.edges(data=True):
# #         net.add_edge(u, v, width=d["weight"] * 3.5, color="#8b5cf6")

# #     net.save_graph("network.html")

# #     html = open("network.html", encoding="utf-8").read()
# #     components.html(html, height=550)

# #     st.markdown("</div>", unsafe_allow_html=True)

# # # ======================================================
# # # CCP INTELLIGENCE PANEL
# # # ======================================================
# # with col_metrics:
# #     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# #     st.subheader("CCP Intelligence")

# #     st.metric("Cash Waterfall", f"${st.session_state.ccp.cash_waterfall/1000:.1f}B")
# #     st.metric("Contracts Active", st.session_state.ccp.active_contracts)

# #     st.markdown("#### Market Feed")
# #     st.info("System monitoring stability...")

# #     st.markdown("</div>", unsafe_allow_html=True)

# # # ======================================================
# # # FORECASTING CHARTS
# # # ======================================================
# # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# # st.subheader("Pattern Recognition & Stability Forecasting")

# # c1, c2 = st.columns(2)

# # with c1:
# #     if st.session_state.history:
# #         df = pd.DataFrame(st.session_state.history)
# #         fig = px.line(df, x="round", y=["actual_price", "predicted_price"], labels={"value":"Price","round":"Round"})
# #         fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
# #         st.plotly_chart(fig, use_container_width=True)
# #     else:
# #         st.info("Prediction Chart will appear once simulation data is added.")

# # with c2:
# #     if st.session_state.history:
# #         df = pd.DataFrame(st.session_state.history)
# #         fig2 = px.area(df, x="round", y="system_health", labels={"system_health":"System Health","round":"Round"})
# #         fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
# #         st.plotly_chart(fig2, use_container_width=True)
# #     else:
# #         st.info("Liquidity Index chart will appear once simulation runs.")

# # st.markdown("</div>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from pyvis.network import Network
# import streamlit.components.v1 as components

# from src.data_engine import DataEngine
# from src.news_analyzer import NewsAnalyzer
# from src.predictor import PricePredictor
# from src.network_manager import NetworkManager
# from src.ccp import CCP

# import time

# # ======================================================
# # PAGE CONFIG
# # ======================================================
# st.set_page_config(
#     layout="wide",
#     page_title="Financial Stability Dashboard",
#     page_icon="⚡"
# )

# # ======================================================
# # THEME TOGGLE (FIRST THING)
# # ======================================================
# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = True

# with st.sidebar:
#     st.markdown("## ⚡ finance Control Center")

#     # ✅ Toggle Switch
#     st.session_state.dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)

# # ======================================================
# # COLORS BASED ON MODE
# # ======================================================
# if st.session_state.dark_mode:
#     bg = "#000000"
#     card = "rgba(7,18,38,0.88)"
#     text = "#E6F7FF"
#     accent = "#00E6FF"
# else:
#     bg = "#F8FAFC"
#     card = "#FFFFFF"
#     text = "#00121A"
#     accent = "#003566"

# # ======================================================
# # PREMIUM GLOBAL CSS + REMOVE RECTANGLE BOXES
# # ======================================================
# st.markdown(f"""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

# html, body {{
#     font-family: "Inter", sans-serif;
#     background: {bg} !important;
#     color: {text} !important;
# }}

# .stApp {{
#     background: radial-gradient(circle at top, {card}, {bg}) !important;
# }}

# /* Sidebar */
# section[data-testid="stSidebar"] {{
#     background: {card} !important;
#     border-right: 1px solid rgba(0,230,255,0.2);
# }}

# /* Buttons */
# .stButton button {{
#     border-radius: 14px !important;
#     padding: 12px !important;
#     font-weight: 700 !important;
#     border: 1px solid {accent}55 !important;
#     background: {accent}15 !important;
#     transition: 0.25s ease;
# }}

# .stButton button:hover {{
#     background: {accent}30 !important;
#     transform: scale(1.03);
# }}

# /* Glass Cards */
# .glass-card {{
#     background: {card};
#     border-radius: 18px;
#     padding: 24px;
#     border: 1px solid {accent}25;
#     box-shadow: 0 0 25px rgba(0,0,0,0.25);
#     margin-bottom: 20px;
# }}

# /* Metrics */
# [data-testid="stMetricValue"] {{
#     font-size: 30px !important;
#     font-weight: 800 !important;
#     color: {accent} !important;
# }}

# [data-testid="stMetricLabel"] {{
#     font-size: 13px !important;
#     color: {text}aa !important;
# }}

# /* ✅ REMOVE EMPTY RECTANGLE BOXES */
# [data-testid="stHorizontalBlock"]:empty {{
#     display: none !important;
# }}
# [data-testid="column"]:empty {{
#     display: none !important;
# }}
# div:empty {{
#     display: none !important;
# }}

# footer {{
#     visibility: hidden;
# }}
# </style>
# """, unsafe_allow_html=True)

# # ======================================================
# # SESSION INIT
# # ======================================================
# if "round" not in st.session_state:
#     st.session_state.round = 0
#     st.session_state.is_playing = False
#     st.session_state.history = []

#     st.session_state.network = NetworkManager()
#     st.session_state.ccp = CCP()
#     st.session_state.data_engine = DataEngine()
#     st.session_state.news_analyzer = NewsAnalyzer()
#     st.session_state.predictor = PricePredictor()

#     with st.spinner("⚡ Training AI Risk Engine..."):
#         hist = st.session_state.data_engine.get_historical_data(period="1y")
#         prices = hist["JPM"]["Close"]

#         seq = st.session_state.predictor.prepare_data(prices)
#         if seq:
#             st.session_state.predictor.train_model(seq, epochs=3)

#         st.session_state.market_data = prices

# # ======================================================
# # HERO HEADER
# # ======================================================
# st.markdown(f"""
# <h1 style="font-size:2.8rem;font-weight:800;color:{accent};margin-bottom:0;">
# finance ⚡
# </h1>
# <p style="font-size:1.1rem;color:{text}aa;margin-top:0;">
# AI-Driven Systemic Risk & CCP Contagion Simulation Engine
# </p>
# """, unsafe_allow_html=True)

# # ======================================================
# # KPI TOP ROW
# # ======================================================
# k1, k2, k3, k4 = st.columns(4)

# with k1:
#     st.metric("System Health", "Stable")

# with k2:
#     st.metric("Active Banks", len(st.session_state.network.G.nodes()))

# with k3:
#     st.metric("Margin Req", f"{st.session_state.ccp.current_margin*100:.0f}%")

# with k4:
#     st.metric("Risk Score", "10 / 10")

# # ======================================================
# # SIDEBAR CONTROLS
# # ======================================================
# with st.sidebar:
#     st.markdown("### Simulation Controls")

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("▶ Run"):
#             st.session_state.is_playing = True

#     with col2:
#         if st.button("⏸ Pause"):
#             st.session_state.is_playing = False

#     st.markdown("### Stress Test Scenario")

#     hubs = [n for n, d in st.session_state.network.G.nodes(data=True)
#             if d["type"] == "hub"]

#     bank = st.selectbox("Target Institution", hubs)

#     if st.button("🔥 Trigger Failure"):
#         st.session_state.network.fail_node(bank)
#         st.warning(f"🚨 {bank} HAS FAILED")

# # ======================================================
# # SIMULATION LOOP
# # ======================================================
# if st.session_state.is_playing:
#     st.session_state.round += 1
#     time.sleep(0.4)
#     st.experimental_rerun()

# # ======================================================
# # MAIN DASHBOARD
# # ======================================================
# col_net, col_metrics = st.columns([2.3, 1])

# # ======================================================
# # NETWORK GRAPH
# # ======================================================
# with col_net:
#     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#     st.subheader("Financial Contagion Map")

#     net = Network(
#         height="520px",
#         width="100%",
#         bgcolor=bg,
#         font_color=text
#     )

#     net.set_options("""
#     {
#       "interaction": {
#         "zoomView": false,
#         "navigationButtons": true
#       }
#     }
#     """)

#     G = st.session_state.network.G

#     for node, data in G.nodes(data=True):
#         color = accent if data["type"] == "hub" else "#cbd5e1"
#         if data["status"] == "failed":
#             color = "#ff0033"

#         net.add_node(node, label=node, size=35, color=color)

#     for u, v, d in G.edges(data=True):
#         net.add_edge(u, v, width=d["weight"] * 3)

#     net.save_graph("network.html")
#     html = open("network.html", encoding="utf-8").read()
#     components.html(html, height=550)

#     st.markdown("</div>", unsafe_allow_html=True)

# # ======================================================
# # CCP INTELLIGENCE PANEL
# # ======================================================
# with col_metrics:
#     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#     st.subheader("CCP Intelligence")

#     st.metric("Cash Waterfall", f"${st.session_state.ccp.cash_waterfall/1000:.1f}B")
#     st.metric("Contracts Active", st.session_state.ccp.active_contracts)

#     st.info("System monitoring stability...")

#     st.markdown("</div>", unsafe_allow_html=True)

# # ======================================================
# # FORECASTING CHARTS
# # ======================================================
# st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# st.subheader("Pattern Recognition & Stability Forecasting")

# c1, c2 = st.columns(2)

# with c1:
#     st.info("Prediction Chart will appear once simulation runs.")

# with c2:
#     st.info("Liquidity Index chart will appear once simulation runs.")

# st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np
from pyvis.network import Network
import streamlit.components.v1 as components

from src.data_engine import DataEngine
from src.news_analyzer import NewsAnalyzer
from src.predictor import PricePredictor
from src.network_manager import NetworkManager
from src.ccp import CCP

import time

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    layout="wide",
    page_title="finance – NetRisk Nexus",
    page_icon="⚡"
)

# ======================================================
# THEME COLORS (FIGMA STYLE)
# ======================================================
BG = "#F6F3EA"          # Cream background
SIDEBAR = "#214D3A"     # Deep green sidebar
CARD = "#FFFFFF"        # White cards
ACCENT = "#D6A84A"      # Gold highlight
TEXT = "#1A1A1A"        # Main text
MUTED = "#4B5563"       # Gray muted text

# ======================================================
# GLOBAL PREMIUM CSS (FIGMA LOOK)
# ======================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body {{
    font-family: "Poppins", sans-serif;
    background: {BG} !important;
    color: {TEXT};
}}

.stApp {{
    background: {BG} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    padding: 25px !important;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

section[data-testid="stSidebar"] h1 {{
    font-size: 22px !important;
    font-weight: 800 !important;
}}

section[data-testid="stSidebar"] hr {{
    border: 1px solid rgba(255,255,255,0.15);
}}

/* Buttons */
.stButton button {{
    width: 100%;
    border-radius: 14px !important;
    padding: 12px !important;
    font-weight: 700 !important;
    border: none !important;
    background: {ACCENT} !important;
    color: black !important;
    transition: 0.25s ease;
}}

.stButton button:hover {{
    transform: scale(1.03);
    opacity: 0.92;
}}

/* Dropdown */
.stSelectbox div {{
    border-radius: 12px !important;
}}

/* Cards */
.glass-card {{
    background: {CARD};
    border-radius: 18px;
    padding: 24px;
    border: 1px solid rgba(0,0,0,0.08);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 22px;
}}

/* Metrics */
[data-testid="stMetricValue"] {{
    font-size: 30px !important;
    font-weight: 800 !important;
    color: {SIDEBAR} !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 13px !important;
    color: {MUTED} !important;
}}

footer {{
    visibility: hidden;
}}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION INIT
# ======================================================
if "round" not in st.session_state:
    st.session_state.round = 0
    st.session_state.is_playing = False

    st.session_state.network = NetworkManager()
    st.session_state.ccp = CCP()
    st.session_state.data_engine = DataEngine()
    st.session_state.news_analyzer = NewsAnalyzer()
    st.session_state.predictor = PricePredictor()

# ======================================================
# SIDEBAR CONTROLS
# ======================================================
with st.sidebar:
    st.markdown("## ⚡ finance")
    st.markdown("### Finance Control Center")
    st.divider()

    st.markdown("### Simulation Controls")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Run"):
            st.session_state.is_playing = True

    with col2:
        if st.button("⏸ Pause"):
            st.session_state.is_playing = False

    st.divider()

    st.markdown("### Stress Test Scenario")

    hubs = [n for n, d in st.session_state.network.G.nodes(data=True)
            if d["type"] == "hub"]

    bank = st.selectbox("Target institution", hubs)

    if st.button("🔥 Trigger Failure"):
        st.session_state.network.fail_node(bank)
        st.warning(f"🚨 {bank} HAS FAILED")

# ======================================================
# HERO HEADER
# ======================================================
st.markdown(f"""
<h1 style="font-size:3rem;font-weight:900;color:{SIDEBAR};margin-bottom:0;">
FINANCE ⚡
</h1>

<p style="font-size:1.2rem;font-weight:600;color:{MUTED};margin-top:6px;">
NetRisk Nexus: Game-Theoretic Modeling of Financial Infrastructure
</p>
""", unsafe_allow_html=True)

# ======================================================
# KPI TOP ROW
# ======================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("System Health", "Stable")

with k2:
    st.metric("Active Banks", len(st.session_state.network.G.nodes()))

with k3:
    st.metric("Margin Req", f"{st.session_state.ccp.current_margin*100:.0f}%")

with k4:
    st.metric("Risk Score", "10 / 10")

st.markdown("<br/>", unsafe_allow_html=True)


# ======================================================
# SIMULATION LOOP
# ======================================================
if st.session_state.is_playing:
    st.session_state.round += 1
    time.sleep(0.4)
    st.experimental_rerun()

# ======================================================
# MAIN DASHBOARD LAYOUT
# ======================================================
col_net, col_metrics = st.columns([2.3, 1])

# ======================================================
# NETWORK GRAPH PANEL
# ======================================================
with col_net:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Financial Contagion Map")

    #net = Network(
    #    height="520px",
    #    width="100%",
    #    bgcolor="#214D3A",
    #    font_color="white"
    #)

    net = Network(
        height="520px",
        width="100%",
        bgcolor=MAP_BG,
        font_color=LABEL_COLOR
    )

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
        color = ACCENT if data["type"] == "hub" else "#FDFDFD"
        if data["status"] == "failed":
            color = "#FF3333"

        net.add_node(
            node,
            label=node,
            size=35,
            color=color,
            font={"color": "black"}
        )

    for u, v, d in G.edges(data=True):
        net.add_edge(u, v, width=d["weight"] * 3, color=ACCENT)

    net.save_graph("network.html")

    html = open("network.html", encoding="utf-8").read()
    components.html(html, height=550)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# CCP INTELLIGENCE PANEL
# ======================================================
with col_metrics:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("CCP Intelligence")

    st.metric("Cash Waterfall", f"${st.session_state.ccp.cash_waterfall/1000:.1f}B")
    st.metric("Contracts Active", st.session_state.ccp.active_contracts)

    st.info("System monitoring stability...")

    st.markdown("</div>", unsafe_allow_html=True)
