# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Routing
page = st.query_params.get("page", "landing")
if any(k in st.query_params for k in ["login_email", "code", "login", "plan"]):
    page = "app"

# 2. Page Config
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="landing/logo.png",
    layout="wide",
    initial_sidebar_state="expanded" if page == "app" else "collapsed"
)

def show_landing_page():
    # Hide Streamlit UI elements for the landing page
    st.markdown("""<style>
    header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"] { display:none!important; }
    .stApp { margin:0!important; padding:0!important; background: #06060f !important; }
    iframe { border: none !important; }
    </style>""", unsafe_allow_html=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(landing_dir, "style.css"), "r", encoding="utf-8") as f:
        css = f.read()

    # Inline Logo
    logo_path = os.path.join(landing_dir, "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
            html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

    # Replace CSS link with inline style
    html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

    # Fix links for Streamlit Cloud
    app_url = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app/?page=app"
    html = html.replace('href="/app"', f'href="{app_url}"')
    html = html.replace('href="/app?plan=monthly"', f'href="{app_url}&plan=monthly"')
    html = html.replace('href="/app?plan=semi_annual"', f'href="{app_url}&plan=semi_annual"')
    html = html.replace('href="/app?plan=yearly"', f'href="{app_url}&plan=yearly"')

    # Render - Huge height to ensure all content is visible
    components.html(html, height=10000, scrolling=False)

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    # Remove conflicting set_page_config
    code = code.replace("st.set_page_config", "# st.set_page_config")
    exec(code, {"__name__": "__main__", "__file__": app_path})

if page == "app":
    show_dashboard()
else:
    show_landing_page()
