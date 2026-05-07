# -*- coding: utf-8 -*-
"""
Data Lie Detector — Unified Streamlit Cloud Entry Point
Serves both the landing page and the analysis dashboard in a single Streamlit app.
"""
import streamlit as st
import os
import base64

# ═══════════════════════════════════════════════════════════════════════
# ROUTING LOGIC (Determines Page)
# ═══════════════════════════════════════════════════════════════════════
page = st.query_params.get("page", "landing")

# If auth callbacks or login actions are in URL, route to the app
if any(k in st.query_params for k in ["login_email", "code", "login", "plan"]):
    page = "app"

# ═══════════════════════════════════════════════════════════════════════
# PAGE CONFIG (must be first Streamlit command)
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded" if page == "app" else "collapsed"
)



def _load_logo_b64():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def show_landing_page():
    """Render the full landing page HTML inside Streamlit."""

    # NUCLEAR RESET: Force the landing page to be the ONLY thing on the screen.
    # This kills all Streamlit margins, headers, and sidebars completely.
    st.markdown("""<style>
    /* 1. Kill EVERYTHING Streamlit-related */
    header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stDecoration"], #MainMenu, [data-testid="stSidebar"], 
    [data-testid="collapsedControl"] {
        display:none!important; visibility:hidden!important; height:0!important; width:0!important;
    }
    
    /* 2. Force the App container to be a transparent full-screen box */
    .stApp { 
        margin:0!important; padding:0!important; 
        background: #06060f !important;
    }
    
    /* 3. Force the main content area to start at (0,0) and take 100% space */
    [data-testid="stAppViewContainer"] {
        padding: 0!important;
        margin: 0!important;
    }
    
    [data-testid="stAppViewBlockContainer"] {
        padding: 0!important;
        margin: 0!important;
        max-width: none!important;
        width: 100vw!important;
        height: 100vh!important;
    }
    
    /* Remove any Streamlit-enforced padding at the top */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
    }
    
    /* 4. Ensure root font-size is exactly 16px */
    html { font-size: 16px !important; }
    
    /* 5. Prevent horizontal scrolling issues */
    html, body {
        overflow-x: hidden !important;
        background: #06060f !important;
    }
    </style>""", unsafe_allow_html=True)

    logo_b64 = _load_logo_b64()

    # Load CSS
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "landing", "style.css")
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # Load HTML
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "landing", "index.html")
    html_content = ""
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

    # Inline the CSS (replace the <link> tag)
    html_content = html_content.replace(
        '<link rel="stylesheet" href="style.css?v=2">',
        f'<style>{css_content}</style>'
    )

    # Inline the logo as base64
    if logo_b64:
        html_content = html_content.replace(
            'src="logo.png"',
            f'src="data:image/png;base64,{logo_b64}"'
        )
        html_content = html_content.replace(
            '<link rel="icon" href="favicon.ico">',
            f'<link rel="icon" href="data:image/png;base64,{logo_b64}">'
        )

    # Fix all /app links → absolute URL with ?page=app
    # We must use the absolute URL because target="_top" resolves relative URLs against the iframe's base URL!
    app_url = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app/?page=app"
    html_content = html_content.replace('href="/app"', f'href="{app_url}"')
    html_content = html_content.replace('href="/app?plan=monthly"', f'href="{app_url}&plan=monthly"')
    html_content = html_content.replace('href="/app?plan=semi_annual"', f'href="{app_url}&plan=semi_annual"')
    html_content = html_content.replace('href="/app?plan=yearly"', f'href="{app_url}&plan=yearly"')

    # Final "Perfect Visuals" Fix:
    # 1. Inject the SVG Gradient definition separately via st.markdown
    # This prevents the st.html sanitizer from stripping it.
    st.markdown("""
    <svg width="0" height="0" style="position: absolute;">
        <defs>
            <linearGradient id="icon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ff6bcb" />
                <stop offset="100%" stop-color="#7b2ff7" />
            </linearGradient>
        </defs>
    </svg>
    """, unsafe_allow_html=True)

    # 2. Use st.html for the main content. This ensures:
    # - Perfect Layout (No squashing or markdown bugs)
    # - Working Navigation (target="_top" works in the same tab)
    # - CSS is applied correctly
    st.html(html_content)


def show_dashboard():
    """Run the dashboard by exec'ing app.py with page config removed."""
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")

    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Remove set_page_config since we already called it
    code = code.replace(
        """st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)""",
        "# page config already set by streamlit_app.py"
    )

    exec(code, {"__name__": "__app__", "__file__": app_path})


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
if page == "app":
    show_dashboard()
else:
    show_landing_page()
