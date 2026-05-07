# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64

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
    # Load files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(landing_dir, "style.css"), "r", encoding="utf-8") as f:
        css = f.read()

    # Prepare Logo
    logo_path = os.path.join(landing_dir, "logo.png")
    logo_url = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
            logo_url = f"data:image/png;base64,{logo_b64}"

    # Process HTML for direct st.markdown injection
    # 1. Inline Logo
    html = html.replace('src="logo.png"', f'src="{logo_url}"')
    
    # 2. Fix links
    app_url = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app/?page=app"
    html = html.replace('href="/app"', f'href="{app_url}"')
    
    # 3. Extract Body Content (everything between <body> tags)
    import re
    body_match = re.search(r"<body[^>]*>(.*)</body>", html, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        body_content = html

    # 4. Global CSS Injection
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # 5. Nuclear Reset (Hide Streamlit UI)
    st.markdown("""<style>
    header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"] { display:none!important; visibility:hidden!important; }
    .stApp { margin:0!important; padding:0!important; background: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0!important; }
    [data-testid="stAppViewBlockContainer"] { padding: 0!important; max-width: none!important; }
    </style>""", unsafe_allow_html=True)

    # 6. Render Body Content Directly
    st.markdown(body_content, unsafe_allow_html=True)
    
    # 7. Animation Fix (Since scripts in st.markdown are stripped, we use a component for the JS)
    import streamlit.components.v1 as components
    components.html("""
    <script>
    const parent = window.parent.document;
    function forceShow() {
        parent.querySelectorAll('.feature-card, .step, .price-card').forEach(function(el) {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
            el.classList.add('animate-in');
        });
    }
    setTimeout(forceShow, 500);
    setTimeout(forceShow, 2000);
    </script>
    """, height=0)

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace("st.set_page_config", "# st.set_page_config")
    exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})

if page == "app":
    show_dashboard()
else:
    show_landing_page()
