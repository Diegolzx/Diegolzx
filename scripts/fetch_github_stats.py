import json
import requests
import os
import sys

def fetch_stats(username, output_path):
    print(f"Fetching GitHub stats for {username}...")
    
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Optional: if a token exists in env, use it to avoid rate limits
    if "GITHUB_TOKEN" in os.environ:
        headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"
        
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url} (status code {response.status_code})")
        sys.exit(1)
        
    repos = response.json()
    
    # Calculate Languages
    languages = {}
    latest_projects = []
    
    for repo in repos:
        # Ignore forks for language stats to be accurate to original work
        if repo.get("fork"):
            continue
            
        # Get language
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
            
        # Get latest 3 projects
        if len(latest_projects) < 3:
            latest_projects.append({
                "name": repo.get("name"),
                "description": repo.get("description") or "No description provided.",
                "url": repo.get("html_url")
            })
            
    # Sort languages by frequency descending
    sorted_langs = sorted(languages.items(), key=lambda item: item[1], reverse=True)
    
    data = {
        "username": username,
        "languages": [{"name": k, "count": v} for k, v in sorted_langs[:5]], # Top 5
        "latest_projects": latest_projects
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Saved {output_path}")

if __name__ == "__main__":
    fetch_stats("Diegolzx", "data/github_stats.json")
