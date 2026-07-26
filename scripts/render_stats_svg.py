import json
import os

# GitHub's official language colors (approximate)
LANG_COLORS = {
    "Python": "#3572A5",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Java": "#b07219",
    "JavaScript": "#f1e05a",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "TypeScript": "#3178c6",
    "C": "#555555"
}

def render_top_languages(data, output_path):
    languages = data.get("languages", [])
    if not languages:
        return
        
    width = 300
    height = 200
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<style>
    .bg {{ fill: #0d1117; rx: 10px; }}
    .text {{ fill: #c9d1d9; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; }}
    .title {{ fill: #58a6ff; font-weight: bold; font-size: 14px; }}
    .bar {{ animation: slideRight 1s forwards; }}
    @keyframes slideRight {{
        from {{ transform: scaleX(0); }}
        to {{ transform: scaleX(1); }}
    }}
</style>
<rect width="100%" height="100%" class="bg" />
<text x="15" y="30" class="text title">Top Languages</text>
<text x="15" y="45" class="text">----------------------</text>
'''
    
    max_count = max([l["count"] for l in languages]) if languages else 1
    y = 70
    
    for i, lang in enumerate(languages):
        name = lang["name"]
        count = lang["count"]
        color = LANG_COLORS.get(name, "#8b949e")
        
        bar_width = int((count / max_count) * 150)
        if bar_width < 10: bar_width = 10
        
        delay = i * 0.1
        
        svg += f'''<g style="animation-delay: {delay}s; opacity: 0; animation: fadeIn 0.5s forwards;">
    <text x="15" y="{y+10}" class="text">{name[:10]}</text>
    <rect x="90" y="{y}" width="{bar_width}" height="12" fill="{color}" rx="3" class="bar" style="transform-origin: left;" />
</g>
'''
        y += 25
        
    svg += '''<style>
    @keyframes fadeIn {
        to { opacity: 1; }
    }
</style>
</svg>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Saved {output_path}")


def render_latest_projects(data, output_path):
    projects = data.get("latest_projects", [])
    if not projects:
        return
        
    width = 540
    height = 200
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<style>
    .bg {{ fill: #0d1117; rx: 10px; }}
    .text {{ fill: #c9d1d9; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; }}
    .title {{ fill: #58a6ff; font-weight: bold; font-size: 14px; }}
    .repo {{ fill: #3fb950; font-weight: bold; }}
    .desc {{ fill: #8b949e; font-size: 11px; }}
    .item {{ opacity: 0; animation: fadeUp 0.5s forwards; }}
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
<rect width="100%" height="100%" class="bg" />
<text x="20" y="30" class="text title">Latest Projects</text>
<text x="20" y="45" class="text">----------------------------------------</text>
'''
    
    y = 70
    for i, proj in enumerate(projects):
        name = proj["name"]
        desc = proj["description"]
        if len(desc) > 60:
            desc = desc[:57] + "..."
            
        delay = i * 0.15
        
        svg += f'''<g class="item" style="animation-delay: {delay}s;">
    <text x="20" y="{y}" class="text repo">📁 {name}</text>
    <text x="40" y="{y+18}" class="desc">{desc}</text>
</g>
'''
        y += 45
        
    svg += '</svg>'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    input_file = "data/github_stats.json"
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        render_top_languages(data, "top-languages.svg")
        render_latest_projects(data, "latest-projects.svg")
    else:
        print(f"{input_file} not found.")
