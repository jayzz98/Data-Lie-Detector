# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(
    page_title="Data Lie Detector — Decision Safety AI",
    page_icon="🕵️",
    layout="wide",
)

# 2. Routing Logic
query_params = st.query_params
page = query_params.get("page", "landing")

# 3. Helper Functions
def get_file_content(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# 4. Show Landing Page
def show_landing_page():
    # Targeted CSS Overrides (Only hide what's needed)
    st.markdown("""<style>
    /* Hide top bar and footer */
    [data-testid="stHeader"], [data-testid="stFooter"], #MainMenu {
        visibility: hidden !important;
        height: 0 !important;
    }
    /* Expand main container to full screen */
    .stApp { background-color: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    /* Position the iframe on top */
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

    # Resolve paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    # Load HTML
    html = get_file_content(os.path.join(landing_dir, "index.html"))
    if not html:
        st.error("Landing page index.html not found.")
        return

    # Inline CSS
    css = get_file_content(os.path.join(landing_dir, "style.css"))
    if css:
        html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

    # Inline Logo
    logo_b64 = get_base64(os.path.join(landing_dir, "logo.png"))
    if logo_b64:
        html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

    # Update Links
    html = html.replace('href="/app"', 'href="?page=app" target="_top"')
    html = html.replace('href="/app?plan=monthly"', 'href="?page=app&plan=monthly" target="_top"')
    html = html.replace('href="/app?plan=semi_annual"', 'href="?page=app&plan=semi_annual" target="_top"')
    html = html.replace('href="/app?plan=yearly"', 'href="?page=app&plan=yearly" target="_top"')

    # Inject Final Overrides
    overrides = """
    <style>
    .feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; }
    html, body { 
        background: #06060f !important; 
        overflow-y: auto !important; 
        height: auto !important; 
        min-height: 100vh !important; 
    }
    .navbar { position: fixed !important; }
    </style>
    """
    html = html.replace("</head>", f"{overrides}</head>")

    # Render
    components.html(html, height=2000, scrolling=True)

# 5. Show Dashboard
def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        # Ensure we don't call set_page_config again
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("app.py not found.")

# Routing
if page == "app":
    show_dashboard()
else:
    show_landing_page()
