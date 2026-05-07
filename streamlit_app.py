# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import re
import streamlit.components.v1 as components

# 1. Compatibility Layer
def get_params():
    try:
        return st.query_params
    except AttributeError:
        return st.experimental_get_query_params()

# 2. Page Config
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="🕵️",
    layout="wide",
)

params = get_params()
page = "landing"
if "page" in params:
    val = params["page"]
    page = val[0] if isinstance(val, list) else val
elif any(k in params for k in ["login_email", "code", "login", "plan", "state"]):
    page = "app"

def show_landing_page():
    # CSS RESET
    st.markdown("""<style>
    [data-testid="stHeader"], [data-testid="stFooter"], #MainMenu, .stDeployButton {
        visibility: hidden !important; height: 0 !important; padding: 0 !important;
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

        # ── HYPER-ROBUST NAVIGATION ──
        app_base = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app"
        
        def link_replacer(match):
            original_href = match.group(1) # This refers to the content within parentheses
            new_url = f"{app_base}/?page=app"
            if "plan=" in original_href:
                plan_match = re.search(r"plan=([^&\s\"']*)", original_href)
                if plan_match:
                    new_url += f"&plan={plan_match.group(1)}"
            # Return the full attribute with breakout logic
            return f'href="{new_url}" target="_top" onclick="window.open(\'{new_url}\', \'_top\'); return false;"'

        # Fixed Regex with capturing group for the href value
        html = re.sub(r'href="(/app[^"]*)"', link_replacer, html)

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
        st.error(f"Execution Error: {e}")

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
