# 🚀 Deployment Guide for Agentic Honeypot

For a hackathon, the easiest way to deploy a Python FastAPI application for free is **Render** or **Railway**.

## Option 1: Render (Recommended & Free)
**Pros**: Free tier, simple setup, native Python support.

### Steps:
1.  **Push your code to GitHub**:
    Ensure your repository contains:
    -   `main.py`
    -   `requirements.txt`
    -   (Optional) `runtime.txt` with `python-3.11.0`

2.  **Sign up at [render.com](https://render.com/)**.

3.  Click **New +** -> **Web Service**.

4.  Connect your GitHub repository.

5.  **Configure the Service**:
    -   **Name**: `honeypot-api`
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

6.  **Environment Variables** (Advanced -> Add Environment Variable):
    -   `HONEYPOT_API_KEY`: `secret-hackathon-key` (or your chosen key)

7.  Click **Deploy Web Service**.
    -   Render will build and start your app.
    -   Once done, you will get a URL like `https://honeypot-api.onrender.com`.

---

## Option 2: Ngrok (Instant Local Hosting)
If you don't want to push to GitHub yet, use **ngrok** to expose your *currently running* local server.

### Steps:
1.  **Start your local server**:
    ```bash
    uvicorn main:app --reload
    ```
2.  **Download & Install ngrok** from [ngrok.com](https://ngrok.com/).
3.  **Run ngrok**:
    ```bash
    ngrok http 8000
    ```
4.  Copy the HTTPS URL (e.g., `https://random-name.ngrok-free.app`).
5.  Use this URL in the GUVI Tester.

---

## Deployment Checklist
- [ ] **requirements.txt**: Ensure `fastapi`, `uvicorn`, `requests`, `httpx` are listed.
- [ ] **Host IP**: Ensure uvicorn runs on `0.0.0.0` (Render requires this).
- [ ] **Port**: Render uses port `10000` by default or sets a `$PORT` env var. The start command `uvicorn main:app --host 0.0.0.0 --port 10000` usually works best.
