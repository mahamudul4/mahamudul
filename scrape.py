import requests
from bs4 import BeautifulSoup
import json

# URL of your Google Scholar profile
URL = "https://scholar.google.com/citations?user=_Jit0HQAAAAJ&hl=en"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Send a request
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# --- Summary Metrics (Total Citations, h-index, i10-index) ---
indices = soup.find_all("td", class_="gsc_rsb_std")

# Extract metrics
stats = {
    "citations": {
        "total": indices[0].text if indices else "N/A",
        "since_2019": indices[1].text if len(indices) > 1 else "N/A"
    },
    "h_index": {
        "total": indices[2].text if len(indices) > 2 else "N/A",
        "since_2019": indices[3].text if len(indices) > 3 else "N/A"
    },
    "i10_index": {
        "total": indices[4].text if len(indices) > 4 else "N/A",
        "since_2019": indices[5].text if len(indices) > 5 else "N/A"
    },
    "citations_per_year": {}
}

# --- Citations Per Year ---
years = soup.find_all("span", class_="gsc_g_t")
counts = soup.find_all("span", class_="gsc_g_al")

for year, count in zip(years, counts):
    stats["citations_per_year"][year.text] = count.text

# Save to JSON file
with open("scholar_stats.json", "w") as f:
    json.dump(stats, f, indent=4)

# Print for verification
print("=== Google Scholar Summary ===")
print(f"Total Citations: {stats['citations']['total']}")
print(f"Total h-index: {stats['h_index']['total']}")
print(f"Total i10-index: {stats['i10_index']['total']}")
print(f"Since 2019 Citations: {stats['citations']['since_2019']}")
print(f"Since 2019 h-index: {stats['h_index']['since_2019']}")
print(f"Since 2019 i10-index: {stats['i10_index']['since_2019']}")

print("\n=== Citations Per Year ===")
for year in sorted(stats["citations_per_year"]):
    print(f"{year}: {stats['citations_per_year'][year]}")