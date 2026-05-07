# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# SET PAGE CONFIG FIRST (Must be the first Streamlit command)
try:
    st.set_page_config(
        page_title="Data Lie Detector",
        page_icon="🕵️",
        layout="wide",
    )
except Exception as e:
    pass # If already set, ignore

# 1. Routing
query_params = st.query_params
page = query_params.get("page", "landing")

auth_triggers = ["login_email", "code", "login", "plan", "state"]
if any(k in query_params for k in auth_triggers):
    page = "app"

def show_landing_page():
    # ── NUCLEAR RESET ──
    # We hide Streamlit's UI elements to make it look like a pure landing page
    st.markdown("""<style>
    header, footer, [data-testid="stFooter"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], #MainMenu, [data-testid="collapsedControl"],
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    html, body, .stApp {
        background: #06060f !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 9999 !important;
    }
    </style>""", unsafe_allow_html=True)

    # ── LOAD ASSETS ──
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    index_path = os.path.join(landing_dir, "index.html")
    style_path = os.path.join(landing_dir, "style.css")
    logo_path = os.path.join(landing_dir, "logo.png")

    if not os.path.exists(index_path):
        st.error(f"Missing index.html at {index_path}")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            css = f.read()
        html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

    # ── LINK REPLACEMENT ──
    # Ensure links trigger the Streamlit app routing
    html = html.replace('href="/app"', 'href="?page=app" target="_top"')
    html = html.replace('href="/app?plan=monthly"', 'href="?page=app&plan=monthly" target="_top"')
    html = html.replace('href="/app?plan=semi_annual"', 'href="?page=app&plan=semi_annual" target="_top"')
    html = html.replace('href="/app?plan=yearly"', 'href="?page=app&plan=yearly" target="_top"')

    # ── IFRAME FIXES ──
    iframe_fixes = """
    <style>
    .feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; }
    .feature-card.animate-in, .step.animate-in, .price-card.animate-in { opacity: 1 !important; transform: none !important; }
    html, body { overflow-x: hidden !important; overflow-y: auto !important; height: auto !important; min-height: 100vh !important; background: #06060f !important; }
    .navbar { position: fixed !important; }
    </style>
    """
    html = html.replace("</head>", f"{iframe_fixes}</head>")

    # Render
    components.html(html, height=2000, scrolling=True)

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("Dashboard (app.py) not found.")

# Routing
if page == "app":
    show_dashboard()
else:
    show_landing_page()
