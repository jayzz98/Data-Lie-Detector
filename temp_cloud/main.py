import uvicorn
import subprocess
import sys
import os
import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import httpx

app = FastAPI(title="Data Lie Detector Unified Server")

# Get absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
landing_dir = os.path.join(project_root, "landing")

# Start Streamlit in the background when the server starts
@app.on_event("startup")
async def startup_event():
    print("Starting Streamlit background engine on port 8502...")
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", 
         "--server.port", "8502", 
         "--server.address", "127.0.0.1",
         "--server.headless", "true",
         "--server.enableCORS", "false",
         "--server.enableXsrfProtection", "false"],
        cwd=project_root
    )

# Proxy route to show the app inside the iframe portal
@app.get("/app")
async def get_app():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Lie Detector - Dashboard</title>
        <style>
            body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background: #0a0a1a; }
            iframe { width: 100%; height: 100%; border: none; }
        </style>
    </head>
    <body>
        <iframe src="/streamlit"></iframe>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Reverse Proxy for Streamlit (so it works on the same port as the landing page)
@app.api_route("/streamlit/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_streamlit(request: Request, path: str):
    url = f"http://127.0.0.1:8502/{path}"
    if request.query_params:
        url += f"?{request.query_params}"
    
    async with httpx.AsyncClient() as client:
        # Stream the response back to support large data/files
        proxy_req = client.build_request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )
        proxy_resp = await client.send(proxy_req, stream=True)
        return StreamingResponse(
            proxy_resp.aiter_raw(),
            status_code=proxy_resp.status_code,
            headers=proxy_resp.headers
        )

# Serve the static files for the landing page
app.mount("/", StaticFiles(directory=landing_dir, html=True), name="landing")

if __name__ == "__main__":
    # Use port from environment (Replit/Render) or 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Data Lie Detector Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
