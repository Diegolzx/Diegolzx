import os

def make_info_card():
    # Card Data
    title = "diego@github"
    separator = "------------"
    
    fields = [
        {"key": "Role", "value": "Full Stack Developer"},
        {"key": "Languages", "value": "Python, C++, C#, Java, JavaScript"},
        {"key": "Technologies", "value": "React, Node.js, SQL Server, Git, Linux"},
        {"key": "Hardware/IoT", "value": "Arduino, ESP32, Raspberry Pi"},
        {"key": "Other", "value": "LaTeX"},
        {"key": "Certs", "value": "HCIA-IoT V3.0, CCNA (ITN, SRWE), Kaggle Python, Intro to Cybersec"}
    ]
    
    # Dimensions
    svg_width = 490
    svg_height = 300
    line_height = 24
    font_size = 14
    
    # SVG start
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
<style>
    .text {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: {font_size}px;
        fill: #c9d1d9;
    }}
    .key {{
        fill: #58a6ff;
        font-weight: bold;
    }}
    .title {{
        fill: #58a6ff;
        font-weight: bold;
    }}
    .bg {{
        fill: #0d1117;
        rx: 10px;
    }}
    .animated-row {{
        opacity: 0;
        animation: fadeIn 0.5s forwards;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateX(-10px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
</style>
<rect width="100%" height="100%" class="bg" />
'''

    # Add Title
    y = 30
    svg += f'<text x="20" y="{y}" class="text title animated-row" style="animation-delay: 0.1s">{title}</text>\n'
    y += line_height
    svg += f'<text x="20" y="{y}" class="text animated-row" style="animation-delay: 0.2s">{separator}</text>\n'
    y += line_height
    
    # Add fields
    for i, field in enumerate(fields):
        delay = 0.3 + (i * 0.1)
        svg += f'''
<g class="animated-row" style="animation-delay: {delay}s">
    <text x="20" y="{y}" class="text key">{field["key"]}</text>
    <text x="120" y="{y}" class="text">:</text>
    <text x="140" y="{y}" class="text">{field["value"]}</text>
</g>
'''
        y += line_height

    # Terminal color blocks
    colors = ["#ff7b72", "#3fb950", "#d2a8ff", "#a5d6ff", "#ffa657", "#ffc11a"]
    y += line_height
    svg += f'<g class="animated-row" style="animation-delay: {0.3 + len(fields)*0.1 + 0.1}s">\n'
    for i, color in enumerate(colors):
        svg += f'    <rect x="{20 + i*30}" y="{y-10}" width="20" height="20" fill="{color}" rx="3" />\n'
    svg += '</g>\n'
    
    svg += '</svg>'
    
    with open("info-card.svg", 'w') as f:
        f.write(svg)
    print("Saved info-card.svg")

if __name__ == "__main__":
    make_info_card()
