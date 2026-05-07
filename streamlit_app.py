# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Routing & State Management
# Check query params for page or auth/plan triggers
query_params = st.query_params
page = query_params.get("page", "landing")

# If auth code, plan, or login trigger is present, default to app page
auth_triggers = ["login_email", "code", "login", "plan", "state"]
if any(k in query_params for k in auth_triggers):
    page = "app"

# 2. Page Config
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="landing/logo.png",
    layout="wide",
    initial_sidebar_state="expanded" if page == "app" else "collapsed"
)

def show_landing_page():
    # ── NUCLEAR RESET: Hide ALL Streamlit chrome ──
    # This ensures the landing page feels like a native site, not a Streamlit app.
    st.markdown("""<style>
    header, footer, [data-testid="stFooter"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], #MainMenu, [data-testid="collapsedControl"],
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    html, body, .stApp {
        background: #06060f !important;
        overflow: hidden !important;
    }
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        overflow: hidden !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }
    /* Iframe must fill viewport */
    iframe[title="streamlit_components.v1.components.html"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 9999 !important;
    }
    </style>""", unsafe_allow_html=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")

    # Load assets
    try:
        with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
            html = f.read()
        with open(os.path.join(landing_dir, "style.css"), "r", encoding="utf-8") as f:
            css = f.read()
    except FileNotFoundError:
        st.error("Landing page files not found. Please ensure the 'landing' directory exists.")
        return

    # ── INLINE ASSETS ──
    # Logo
    logo_path = os.path.join(landing_dir, "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

    # CSS
    html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

    # ── LINK REPLACEMENT (For Streamlit query params) ──
    # Force all app links to use target="_top" so they navigate the parent window
    html = html.replace('href="/app"', 'href="?page=app" target="_top"')
    html = html.replace('href="/app?plan=monthly"', 'href="?page=app&plan=monthly" target="_top"')
    html = html.replace('href="/app?plan=semi_annual"', 'href="?page=app&plan=semi_annual" target="_top"')
    html = html.replace('href="/app?plan=yearly"', 'href="?page=app&plan=yearly" target="_top"')

    # ── IFRAME OPTIMIZATIONS ──
    # Inside an iframe, IntersectionObserver often fails. We force animations to be visible.
    iframe_fixes = """
    <style>
    .feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; }
    .feature-card.animate-in, .step.animate-in, .price-card.animate-in { opacity: 1 !important; transform: none !important; }
    html, body { overflow-x: hidden !important; overflow-y: auto !important; height: auto !important; min-height: 100vh !important; }
    .navbar { position: fixed !important; }
    </style>
    """
    html = html.replace("</head>", f"{iframe_fixes}</head>")

    # Render
    components.html(html, height=10000, scrolling=True)

def show_dashboard():
    # Load and execute the main dashboard app.py
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        # Prevent double page_config
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("Dashboard (app.py) not found.")

# Main Execution Flow
if page == "app":
    show_dashboard()
else:
    show_landing_page()
