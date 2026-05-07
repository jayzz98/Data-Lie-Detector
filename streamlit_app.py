# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# 1. Page Config (Must be first)
st.set_page_config(
    page_title="Data Lie Detector — Decision Safety AI",
    page_icon="🕵️",
    layout="wide",
)

# 2. Routing Logic
query_params = st.query_params
page = query_params.get("page", "landing")

# Auto-route triggers
if any(k in query_params for k in ["login_email", "code", "login", "plan", "state"]):
    page = "app"

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
    # Targeted CSS Overrides (Only hide UI chrome)
    st.markdown("""<style>
    header, footer, [data-testid="stHeader"], [data-testid="stFooter"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    #MainMenu, .stDeployButton, [data-testid="collapsedControl"] {
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stApp { background-color: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
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

    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    
    html = get_file_content(os.path.join(landing_dir, "index.html"))
    if not html:
        st.error("Landing page assets missing.")
        return

    # Inline Assets
    css = get_file_content(os.path.join(landing_dir, "style.css"))
    if css:
        html = html.replace('<link rel="stylesheet" href="style.css?v=2">', f'<style>{css}</style>')

    logo_b64 = get_base64(os.path.join(landing_dir, "logo.png"))
    if logo_b64:
        html = html.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')

    # ── ROBUST LINK HANDLING ──
    # We use a Javascript bridge to ensure the parent window navigates correctly.
    # This bypasses iframe sandbox restrictions that sometimes block target="_top".
    link_fix_script = """
    <script>
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a');
        if (target && target.getAttribute('href')) {
            var href = target.getAttribute('href');
            if (href.startsWith('/app') || href.startsWith('?page=app')) {
                e.preventDefault();
                var newUrl = window.parent.location.pathname + '?page=app';
                if (href.includes('plan=')) {
                    var plan = href.split('plan=')[1].split('&')[0];
                    newUrl += '&plan=' + plan;
                }
                window.parent.location.href = newUrl;
            }
        }
    }, true);
    </script>
    """
    
    # Inject Final Overrides and the Link Fix Script
    overrides = f"""
    <style>
    .feature-card, .step, .price-card {{ opacity: 1 !important; transform: none !important; }}
    html, body {{ 
        background: #06060f !important; 
        overflow-y: auto !important; 
        height: auto !important; 
        min-height: 100vh !important; 
    }}
    .navbar {{ position: fixed !important; }}
    </style>
    {link_fix_script}
    """
    html = html.replace("</head>", f"{overrides}</head>")

    # Render
    components.html(html, height=2000, scrolling=True)

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
