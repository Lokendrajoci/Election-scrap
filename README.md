# Nepal Election Results Scraper

## Production Files
- `main.py` - Main scraper script
- `requirements.txt` - Python dependencies

## Setup on Production Server

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper:**
   ```bash
   python main.py
   ```

## Output Files
- `pr_votes.csv` - Full election data (CSV format)
- `pr_votes_party_votes.xlsx` - Party names & votes only (Excel format)

## Deployment Notes
- Exclude `venv/` folder from version control (add to `.gitignore`)
- Output files (`.csv`, `.xlsx`) are auto-generated and don't need to be deployed
