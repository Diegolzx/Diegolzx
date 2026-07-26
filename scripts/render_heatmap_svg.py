import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_heatmap(input_path, output_path):
    print(f"Rendering heatmap from {input_path}...")
    if not os.path.exists(input_path):
        print(f"Data file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        data = json.load(f)
        
    days = data.get("days", [])
    if not days:
        print("No contribution data to render.")
        
    # Build grid: weeks (columns) and days (rows)
    # GitHub typically provides 365 or 371 days depending on year start/end.
    # So approximately 53 weeks.
    
    box_size = 10
    gap = 4
    rx = 2
    
    cols = (len(days) // 7) + 1
    width = cols * (box_size + gap) + 40
    height = 7 * (box_size + gap) + 60
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<style>
    .bg {{ fill: #0d1117; }}
    .text {{ fill: #c9d1d9; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; }}
    .box {{
        opacity: 0;
        animation: slideDown 0.6s forwards;
    }}
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
<rect width="100%" height="100%" class="bg" rx="10"/>
<text x="20" y="20" class="text">github.com/{data.get("username", "Diegolzx")}</text>
<g transform="translate(20, 30)">
'''
    
    for i, day in enumerate(days):
        col = i // 7
        row = i % 7
        x = col * (box_size + gap)
        y = row * (box_size + gap)
        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]
        
        # Diagonal delay: (col + row) gives a diagonal wave
        delay = (col * 0.03) + (row * 0.03)
        
        svg += f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" rx="{rx}" class="box" style="animation-delay: {delay}s" />\n'
        
    svg += '</g>\n'
    
    # Legend
    legend_y = 30 + 7 * (box_size + gap) + 10
    legend_x = width - (len(PALETTE) * (box_size + gap)) - 40
    svg += f'<text x="{legend_x - 30}" y="{legend_y+8}" class="text">Less</text>\n'
    for i, color in enumerate(PALETTE):
        lx = legend_x + i * (box_size + gap)
        svg += f'<rect x="{lx}" y="{legend_y}" width="{box_size}" height="{box_size}" fill="{color}" rx="{rx}" />\n'
    svg += f'<text x="{legend_x + len(PALETTE) * (box_size + gap) + 5}" y="{legend_y+8}" class="text">More</text>\n'
    
    svg += '</svg>'
    
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    render_heatmap("data/contributions.json", "contrib-heatmap.svg")
