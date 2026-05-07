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

    # 1. Kill EVERYTHING Streamlit-related to allow for a true full-screen landing page.
    st.markdown("""<style>
    header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stDecoration"], #MainMenu, [data-testid="stSidebar"], 
    [data-testid="collapsedControl"] {
        display:none!important; visibility:hidden!important; height:0!important; width:0!important;
    }
    .stApp { margin:0!important; padding:0!important; background: #06060f !important; }
    [data-testid="stAppViewContainer"] { padding: 0!important; margin: 0!important; }
    [data-testid="stAppViewBlockContainer"] { padding: 0!important; margin: 0!important; max-width: none!important; width: 100vw!important; }
    .main .block-container { padding-top: 0 !important; padding-bottom: 0 !important; margin: 0 !important; }
    html { font-size: 16px !important; }
    html, body { overflow-x: hidden !important; background: #06060f !important; }
    </style>""", unsafe_allow_html=True)

    # 2. Prepare paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(base_dir, "landing")
    html_path = os.path.join(landing_dir, "index.html")
    css_path = os.path.join(landing_dir, "style.css")

    # 3. Load HTML and CSS
    if not os.path.exists(html_path):
        st.error("Landing page index.html not found.")
        return
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # 4. Inline Images (Logo, Favicon, and any other assets)
    def get_b64(rel_path):
        full_path = os.path.join(landing_dir, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return None

    logo_b64 = get_b64("logo.png")
    if logo_b64:
        html_content = html_content.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')
        html_content = html_content.replace('href="favicon.ico"', f'href="data:image/png;base64,{logo_b64}"')

    # 5. Route Dashboard Links
    app_url = "https://data-lie-detector-icjvsdmt7y7zystrxhqy5r.streamlit.app/?page=app"
    html_content = html_content.replace('href="/app"', f'href="{app_url}"')
    html_content = html_content.replace('href="/app?plan=monthly"', f'href="{app_url}&plan=monthly"')
    html_content = html_content.replace('href="/app?plan=semi_annual"', f'href="{app_url}&plan=semi_annual"')
    html_content = html_content.replace('href="/app?plan=yearly"', f'href="{app_url}&plan=yearly"')

    # 6. Final Polish & Animation Fallback
    # In Streamlit's iframe, IntersectionObserver can be flaky. We add a script to force trigger animations.
    animation_fix = """
    <script>
    function forceShow() {
        document.querySelectorAll('.feature-card, .step, .price-card').forEach(function(el) {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0) scale(1)';
            el.classList.add('animate-in');
        });
    }
    document.addEventListener("DOMContentLoaded", forceShow);
    window.addEventListener("load", forceShow);
    setTimeout(forceShow, 500);
    setTimeout(forceShow, 1500);
    setTimeout(forceShow, 3000);
    </script>
    """
    
    # 7. Inject Styles and Scripts
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>{css_content}</style>
    </head>
    <body>
        <svg width="0" height="0" style="position: absolute;">
            <defs>
                <linearGradient id="icon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff6bcb" />
                    <stop offset="100%" stop-color="#7b2ff7" />
                </linearGradient>
            </defs>
        </svg>
        {html_content}
        {animation_fix}
    </body>
    </html>
    """

    # 8. Render using components.html for better iframe control and height
    import streamlit.components.v1 as components
    components.html(full_html, height=5000, scrolling=False)




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
