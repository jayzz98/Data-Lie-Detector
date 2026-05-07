import os
import re

def get_content(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

header = """# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import re
import time
import pandas as pd
import streamlit.components.v1 as components

# Compatibility for Query Params
def get_param(key, default=None):
    try:
        p = st.query_params
        if key in p: return p[key]
    except:
        p = st.experimental_get_query_params()
        if key in p: return p[key][0]
    return default

def clear_params():
    try:
        st.query_params.clear()
    except:
        st.experimental_set_query_params()

# Routing logic
page = get_param("page", "landing")
auth_triggers = ["login_email", "code", "login", "plan", "state"]
if any(get_param(k) for k in auth_triggers):
    page = "app"

if page == "landing":
    st.set_page_config(page_title="Data Lie Detector", page_icon="🕵️", layout="wide")
    st.markdown('<style>[data-testid="stHeader"], [data-testid="stFooter"], #MainMenu, .stDeployButton { visibility: hidden !important; height: 0 !important; } .stApp { background-color: #06060f !important; } [data-testid="stAppViewContainer"] { padding: 0 !important; } .block-container { padding: 0 !important; max-width: 100% !important; } iframe { position: fixed !important; top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important; border: none !important; z-index: 9999 !important; }</style>', unsafe_allow_html=True)
    
    landing_dir = os.path.join(os.path.dirname(__file__), "landing")
    try:
        with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
            html = f.read()
        if os.path.exists(os.path.join(landing_dir, "style.css")):
            with open(os.path.join(landing_dir, "style.css"), "r", encoding="utf-8") as f:
                css = f.read()
            html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')
        if os.path.exists(os.path.join(landing_dir, "logo.png")):
            with open(os.path.join(landing_dir, "logo.png"), "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

        app_base = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app"
        html = re.sub(r'href="/app[^"]*"', lambda m: f'href="{app_base}/?page=app" target="_top" onclick="window.open(\'{app_base}/?page=app\', \'_top\'); return false;"', html)
        
        overrides = "<style>.feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; } html, body { background: #06060f !important; overflow-y: auto !important; }</style>"
        html = html.replace("</head>", f"{overrides}</head>")
        components.html(html, height=2000, scrolling=True)
        st.stop()
    except Exception as e:
        st.error(f"Landing Error: {e}")
"""

app_content = get_content('app.py')

# Clean app.py content (remove its own set_page_config if needed, but the current app.py has it commented out)
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(header + '\n' + app_content)
print("Merge complete!")
