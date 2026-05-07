# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Compatibility Layer for Query Params
def get_params():
    try:
        return st.query_params
    except AttributeError:
        return st.experimental_get_query_params()

# 2. Page Config
st.set_page_config(
    page_title="Data Lie Detector — Decision Safety AI",
    page_icon="🕵️",
    layout="wide",
)

params = get_params()
page = "landing"
if "page" in params:
    # Handle both new st.query_params (string) and old experimental (list)
    val = params["page"]
    page = val[0] if isinstance(val, list) else val
elif any(k in params for k in ["login_email", "code", "login", "plan", "state"]):
    page = "app"

def show_landing_page():
    # CSS RESET
    st.markdown("""<style>
    [data-testid="stHeader"], [data-testid="stFooter"], #MainMenu, .stDeployButton {
        visibility: hidden !important; height: 0 !important;
    }
    .stApp { background-color: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe {
        position: fixed !important; top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        border: none !important; z-index: 9999 !important;
    }
    </style>""", unsafe_allow_html=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    try:
        with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
            html = f.read()
        
        # Inline Assets
        style_path = os.path.join(landing_dir, "style.css")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                css = f.read()
            html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')
        
        logo_path = os.path.join(landing_dir, "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

        # ── ABSOLUTE REDIRECTS ──
        # We hardcode the production URL to guarantee target="_top" works.
        app_url = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app"
        
        html = html.replace('href="/app"', f'href="{app_url}/?page=app" target="_top"')
        html = html.replace('href="/app?plan=monthly"', f'href="{app_url}/?page=app&plan=monthly" target="_top"')
        html = html.replace('href="/app?plan=semi_annual"', f'href="{app_url}/?page=app&plan=semi_annual" target="_top"')
        html = html.replace('href="/app?plan=yearly"', f'href="{app_url}/?page=app&plan=yearly" target="_top"')

        # Inject Final Fixes
        overrides = """
        <style>
        .feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; }
        html, body { background: #06060f !important; overflow-y: auto !important; height: auto !important; min-height: 100vh !important; }
        .navbar { position: fixed !important; }
        </style>
        """
        html = html.replace("</head>", f"{overrides}</head>")

        components.html(html, height=2000, scrolling=True)

    except Exception as e:
        st.error(f"Error: {e}")

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("app.py not found.")

if page == "app":
    show_dashboard()
else:
    show_landing_page()
