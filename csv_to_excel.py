import pandas as pd

# Convert CSV data to Excel format
input_csv = "pr_votes.csv"
output_excel = "pr_votes_party_votes.xlsx"

df = pd.read_csv(input_csv)
selected = df[["PoliticalPartyName", "TotalVoteReceived"]]
selected.to_excel(output_excel, index=False)

print(f"Converted '{input_csv}' to '{output_excel}' successfully.")
