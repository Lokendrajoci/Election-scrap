# Nepal Election Data Pipeline (Flask + Railway)

Architecture implemented in this exact order:

1. Target Website
2. Python Scraper (`scraper.py`)
3. Data Processing (`processing.py`)
4. Flask API + Web UI (`app.py`)
5. Railway Deployment (`Procfile`, `railway.json`)
6. Public Website/API + Excel download

## Project Files

- `scraper.py`: fetches raw records from target website
- `processing.py`: selects and cleans `PoliticalPartyName`, `TotalVoteReceived`
- `app.py`: Flask web app + API + file downloads
- `templates/index.html`: website view with chart and table
- `requirements.txt`: dependencies
- `Procfile`, `railway.json`, `runtime.txt`: Railway deployment config

## Run Locally

1. Create and activate venv
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run Flask app
   ```bash
   python app.py
   ```
4. Open in browser
   - `http://127.0.0.1:5000`

## API Endpoints

- `GET /health`: health check
- `GET /api/v1/votes`: latest processed party votes JSON
- `GET /api/v1/votes/refresh`: force refresh and return JSON
- `GET /download/csv`: download CSV
- `GET /download/excel`: download Excel

## Railway Deployment

1. Push this project to GitHub.
2. In Railway, create a new project from the GitHub repo.
3. Railway auto-detects Python app and uses:
   - start command: `gunicorn app:app`
4. After deploy, open your public Railway URL.

## Notes

- Data cache refreshes every 10 minutes in Flask (`CACHE_TTL_SECONDS = 600`).
