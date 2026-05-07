# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="🕵️",
    layout="wide",
)

# Routing
query_params = st.query_params
page = query_params.get("page", "landing")
if any(k in query_params for k in ["login_email", "code", "login", "plan", "state"]):
    page = "app"

def show_landing_page():
    # NO CSS RESET FOR DEBUGGING
    st.write("--- Landing Page Header ---")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    try:
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

        # Fix Links
        html = html.replace('href="/app"', 'href="?page=app" target="_top"')
        
        # Iframe Fixes
        iframe_fixes = "<style>.feature-card, .step, .price-card { opacity: 1 !important; transform: none !important; } html, body { background: #06060f; color: white; }</style>"
        html = html.replace("</head>", f"{iframe_fixes}</head>")

        # Render
        components.html(html, height=1500, scrolling=True)
        st.write("--- Landing Page Footer ---")

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
        st.error("Dashboard engine missing.")

if page == "app":
    show_dashboard()
else:
    show_landing_page()
