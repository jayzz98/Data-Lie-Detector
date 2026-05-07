# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# DEBUG: Ensure script is running
st.write("DEBUG: Streamlit script initialized")

# 1. Routing
query_params = st.query_params
page = query_params.get("page", "landing")

auth_triggers = ["login_email", "code", "login", "plan", "state"]
if any(k in query_params for k in auth_triggers):
    page = "app"

st.write(f"DEBUG: Current page is {page}")

# 2. Page Config
try:
    st.set_page_config(
        page_title="Data Lie Detector",
        page_icon="🕵️",
        layout="wide",
    )
except Exception as e:
    st.error(f"Page Config Error: {e}")

def show_landing_page():
    st.write("DEBUG: Entering show_landing_page")
    
    # Simple CSS to hide only the top bar and footer, but keep content visible for now
    st.markdown("""<style>
    header, footer { visibility: hidden !important; height: 0 !important; }
    .block-container { padding-top: 0 !important; }
    </style>""", unsafe_allow_html=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")

    try:
        index_path = os.path.join(landing_dir, "index.html")
        style_path = os.path.join(landing_dir, "style.css")
        
        if not os.path.exists(index_path):
            st.error(f"Missing index.html at {index_path}")
            return
        
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
        with open(style_path, "r", encoding="utf-8") as f:
            css = f.read()
        
        # Inline Logo
        logo_path = os.path.join(landing_dir, "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

        # Inline CSS
        html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

        # Fix Links
        html = html.replace('href="/app"', 'href="?page=app" target="_top"')
        
        # Render
        st.write("DEBUG: Rendering component...")
        components.html(html, height=1200, scrolling=True)

    except Exception as e:
        st.error(f"Error: {e}")

def show_dashboard():
    st.write("DEBUG: Entering show_dashboard")
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            code = f.read()
        code = code.replace("st.set_page_config", "# st.set_page_config")
        exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})
    else:
        st.error("Dashboard (app.py) not found.")

if page == "app":
    show_dashboard()
else:
    show_landing_page()
