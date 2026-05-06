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

    # Hide ALL Streamlit chrome for a clean landing page
    st.markdown("""<style>
    #MainMenu, footer, header, [data-testid="stToolbar"],
    [data-testid="stSidebar"], [data-testid="collapsedControl"],
    [data-testid="stHeader"], [data-testid="stDecoration"] {
        display:none!important; visibility:hidden!important;
    }
    .main .block-container {
        padding:0!important; max-width:100%!important;
    }
    html, body, .stApp {
        background: #06060f !important; overflow-x: hidden;
    }
    iframe { border: none !important; }
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

    # To restore the landing page EXACTLY, we use st.html.
    # To fix the "missing icons" issue in st.html, we must inline the gradient definition
    # into EVERY SVG so they are self-contained and don't get stripped by the sanitizer.
    gradient_def = """
    <defs>
        <linearGradient id="icon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ff6bcb" />
            <stop offset="100%" stop-color="#7b2ff7" />
        </linearGradient>
    </defs>
    """
    html_content = html_content.replace('<svg ', f'<svg>{gradient_def}')

    # We use st.html to render pure HTML. This allows target="_top" navigation
    # (single tab) and avoids all the weird markdown formatting bugs.
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
