# Deployment Guide: Streamlit Community Cloud

Follow these exact steps to deploy the **Data Lie Detector** to Streamlit Community Cloud. 

This repository has been structured as a unified, single-link application (`streamlit_app.py`). It seamlessly serves the landing page, login page, and analysis dashboard from a single URL!

## 1. Push to GitHub
If you haven't already, push this entire project folder to a GitHub repository:
1. Initialize git (`git init`)
2. Commit all files (`git add .` then `git commit -m "Ready for Streamlit Cloud"`)
3. Push to your GitHub account.

## 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app** -> **Deploy a public app from GitHub**.
3. Fill in the details:
   - **Repository:** `your-username/your-repo-name`
   - **Branch:** `main` (or `master`)
   - **Main file path:** `streamlit_app.py` *(This is critical! Do not select `app.py`)*
4. Click **Deploy!**

## 3. Environment Variables (Secrets)
Once the app is deploying or deployed, you need to set up the environment variables so that Authentication works properly.
1. Click the **⋮ (three dots)** menu in the bottom right corner of your deployed app and select **Settings**.
2. Go to the **Secrets** section.
3. Paste the following configuration (replace with your actual API keys):

```toml
# ── Google OAuth ──
GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-google-client-secret"

# ── Microsoft OAuth ──
MICROSOFT_CLIENT_ID = "your-microsoft-client-id"
MICROSOFT_CLIENT_SECRET = "your-microsoft-client-secret"
MICROSOFT_TENANT_ID = "common"

# ── Streamlit Public URL ──
# CRITICAL: This must exactly match the public URL Streamlit gave you!
REDIRECT_URI = "https://your-custom-name.streamlit.app"
HOME_URL = "https://your-custom-name.streamlit.app"
```

## 4. Redirect URI Configuration (Google / Microsoft Consoles)
Ensure that the `REDIRECT_URI` you just pasted in the Secrets perfectly matches the **Authorized Redirect URIs** configured in your Google Cloud / Microsoft Azure app consoles. If they do not match, the login will fail with a `redirect_uri_mismatch` error.

## 5. You're Done!
Your app will now run on a single Streamlit link:
- **`https://your-custom-name.streamlit.app/`** -> Serves the custom HTML Landing Page.
- **`https://your-custom-name.streamlit.app/?page=app`** -> Serves the Login Page / SaaS Dashboard.
