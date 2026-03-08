import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://result.election.gov.np/PRVoteChartResult2082.aspx"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://result.election.gov.np/PRVoteChartResult2082.aspx",
    "X-Requested-With": "XMLHttpRequest"
}

# Create a session to maintain cookies
session = requests.Session()
session.headers.update(headers)

# First, load the main page to get cookies
print("Loading main page to establish session...")
res = session.get(url)
print(f"Main page status: {res.status_code}")

# Get CSRF token from cookies
csrf_token = session.cookies.get('CsrfToken')
print(f"CSRF Token: {csrf_token}\n")

# Add CSRF token to session headers
if csrf_token:
    session.headers.update({'X-CSRF-Token': csrf_token})

# The correct data URL  
data_url = "https://result.election.gov.np/Handlers/SecureJson.ashx?file=JSONFiles/Election2082/Common/PRHoRPartyTop5.txt"

print(f"Fetching data from: {data_url}")
data_res = session.get(data_url)
print(f"Status: {data_res.status_code}\n")

if data_res.status_code == 200:
    print("Raw data preview:")
    print(data_res.text[:300])
    print("\n" + "="*60 + "\n")
    
    # Parse JSON
    import json
    data = json.loads(data_res.text)
    print(f"✓ Parsed {len(data)} party records\n")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    print("DataFrame loaded successfully")
    
    # Save to CSV
    df.to_csv("pr_votes.csv", index=False, encoding="utf-8-sig")
    print("\n✓ Data saved to pr_votes.csv")

    # Save selected columns to Excel
    selected = df[["PoliticalPartyName", "TotalVoteReceived"]]
    excel_file = "pr_votes_party_votes.xlsx"
    try:
        selected.to_excel(excel_file, index=False)
        print(f"✓ Data saved to {excel_file}")
    except PermissionError:
        excel_file = "pr_votes_party_votes_new.xlsx"
        selected.to_excel(excel_file, index=False)
        print(f"✓ pr_votes_party_votes.xlsx is open, saved to {excel_file} instead")
else:
    print(f"✗ Error: {data_res.status_code}")
    print(data_res.text[:300])

