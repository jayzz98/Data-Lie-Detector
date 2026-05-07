# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Page Config (Must be first)
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="🕵️",
    layout="wide",
)

# 2. Routing Logic
query_params = st.query_params
page = query_params.get("page", "landing")

# If auth code, plan, or login trigger is present, default to app page
auth_triggers = ["login_email", "code", "login", "plan", "state"]
if any(k in query_params for k in auth_triggers):
    page = "app"

def show_landing_page():
    # ── NUCLEAR RESET (Safe Version) ──
    # Hide Streamlit UI elements without breaking the layout
    st.markdown("""<style>
    header, footer, [data-testid="stHeader"], [data-testid="stFooter"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    #MainMenu, .stDeployButton, [data-testid="collapsedControl"] {
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remove padding and set background */
    .stApp {
        background-color: #06060f !important;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* The Iframe must fill the entire viewport */
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 1000 !important;
    }
    </style>""", unsafe_allow_html=True)

    # ── LOAD ASSETS ──
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    try:
        # Load index.html
        with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
            html = f.read()
        
        # Inline CSS
        style_path = os.path.join(landing_dir, "style.css")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                css = f.read()
            html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')
        
        # Inline Logo
        logo_path = os.path.join(landing_dir, "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

        # Link Replacement for Streamlit Cloud
        html = html.replace('href="/app"', 'href="?page=app" target="_top"')
        html = html.replace('href="/app?plan=monthly"', 'href="?page=app&plan=monthly" target="_top"')
        html = html.replace('href="/app?plan=semi_annual"', 'href="?page=app&plan=semi_annual" target="_top"')
        html = html.replace('href="/app?plan=yearly"', 'href="?page=app&plan=yearly" target="_top"')

        # Inject Iframe Fixes
        iframe_fixes = """
        <style>
        .feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; }
        .feature-card.animate-in, .step.animate-in, .price-card.animate-in { opacity: 1 !important; transform: none !important; }
        html, body { 
            background: #06060f !important; 
            overflow-x: hidden !important; 
            overflow-y: auto !important; 
            height: auto !important; 
            min-height: 100vh !important; 
        }
        .navbar { position: fixed !important; }
        </style>
        """
        html = html.replace("</head>", f"{iframe_fixes}</head>")

        # Render Component
        components.html(html, height=4000, scrolling=True)

    except Exception as e:
        st.error(f"Error loading landing page: {e}")

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        # Suppress nested page_config
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("Dashboard (app.py) not found.")

# Main Execution
if page == "app":
    show_dashboard()
else:
    show_landing_page()
