# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Routing logic
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
    # Target styles for Streamlit container to make the landing page full-width
    st.markdown("""<style>
    header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"] { display:none!important; visibility:hidden!important; }
    .stApp { margin:0!important; padding:0!important; background: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0!important; }
    [data-testid="stAppViewBlockContainer"] { padding: 0!important; max-width: none!important; }
    iframe { border: none !important; margin: 0 !important; padding: 0 !important; }
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

    # Inject Visibility Script into the HTML content itself to bypass Cross-Origin limits
    visibility_script = """
    <script>
    function forceShow() {
        document.querySelectorAll('.feature-card, .step, .price-card').forEach(function(el) {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
            el.classList.add('animate-in');
        });
    }
    window.addEventListener("load", forceShow);
    setTimeout(forceShow, 500);
    setTimeout(forceShow, 1500);
    </script>
    """
    if "</body>" in html:
        html = html.replace("</body>", f"{visibility_script}</body>")
    else:
        html += visibility_script

    # Render with a huge height to prevent scrollbars and ensure all content is loaded
    components.html(html, height=8000, scrolling=False)

def show_dashboard():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if not os.path.exists(app_path):
        st.error("Dashboard app.py not found.")
        return
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    # Remove conflicting set_page_config
    code = code.replace("st.set_page_config", "# st.set_page_config")
    # Clean execution environment
    exec(code, {"__name__": "__main__", "__file__": app_path, "st": st})

if page == "app":
    show_dashboard()
else:
    show_landing_page()
