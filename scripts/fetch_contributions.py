import json
import requests
from bs4 import BeautifulSoup
import sys

def fetch_contributions(username, output_path):
    print(f"Fetching contributions for {username}...")
    url = f"https://github.com/users/{username}/contributions"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url} (status code {response.status_code})")
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    days = []
    # GitHub's contribution calendar structure changes sometimes.
    # Currently it uses td class="ContributionCalendar-day"
    # The 'data-date' and 'data-level' contain the info.
    
    for td in soup.find_all('td', class_='ContributionCalendar-day'):
        date = td.get('data-date')
        level = td.get('data-level')
        # Sometime the data is in tooltips, or it might be text.
        # 'data-level' usually maps to 0-4 (0=none, 4=highest).
        
        if date and level is not None:
            days.append({"date": date, "level": int(level)})
            
    if not days:
        print("Warning: Could not parse contribution days. GitHub HTML structure might have changed.")
        
    data = {
        "username": username,
        "days": days
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {output_path} with {len(days)} days of data.")

if __name__ == "__main__":
    # Ensure data dir exists
    import os
    os.makedirs("data", exist_ok=True)
    fetch_contributions("Diegolzx", "data/contributions.json")
