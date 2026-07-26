from PIL import Image
import numpy as np

RAMP = " .`:-=+*cs#%@"
W = 100
H = 53

def make_ascii(input_path, output_path):
    print(f"Generating ASCII SVG from {input_path}...")
    img = Image.open(input_path).convert('L')
    
    # Calculate target dimensions maintaining aspect ratio
    aspect_ratio = img.height / img.width
    # A character in monospace is typically ~ 1/2 as wide as it is tall
    # So to keep aspect ratio: target_h / target_w = aspect_ratio * (char_width / char_height) => target_h = target_w * aspect_ratio * 0.5
    target_w = W
    target_h = int(target_w * aspect_ratio * 0.5)
    
    if target_h > H:
        target_h = H
        target_w = int(target_h / (aspect_ratio * 0.5))
        
    img = img.resize((target_w, target_h))
    
    ascii_rows = []
    pixels = np.array(img)
    for row in pixels:
        ascii_row = ""
        for p in row:
            # Map pixel value (0-255) to RAMP (0 to len(RAMP)-1)
            # p=255 is white (sparse/empty), p=0 is black (dense)
            # But in prep_photo, white bg is 255. So we want 255 to map to " " (index 0).
            # Therefore, we invert the pixel value or just map 255 -> 0.
            idx = int((255 - p) / 255.0 * (len(RAMP) - 1))
            ascii_row += RAMP[idx]
        ascii_rows.append(ascii_row)
        
    # Generate SVG
    font_size = 12
    line_height = 14
    svg_width = target_w * 7.2 # approx char width
    svg_height = target_h * line_height + 20
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
<style>
    .ascii {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: {font_size}px;
        fill: #c9d1d9; /* light gray for dark mode compatibility, or use currentColor */
        white-space: pre;
    }}
    .bg {{
        fill: #0d1117;
    }}
</style>
<rect width="100%" height="100%" class="bg" />
'''
    
    # Define clip paths
    svg += '<defs>\n'
    for i in range(len(ascii_rows)):
        delay = i * 0.05
        svg += f'''<clipPath id="clip-{i}">
    <rect x="0" y="{i * line_height}" width="0" height="{line_height}">
        <animate attributeName="width" from="0" to="{svg_width}" begin="{delay}s" dur="0.3s" fill="freeze" />
    </rect>
</clipPath>
'''
    svg += '</defs>\n'
    
    # Draw text
    for i, row in enumerate(ascii_rows):
        # Escape xml chars
        row = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg += f'<text x="10" y="{i * line_height + font_size}" class="ascii" clip-path="url(#clip-{i})">{row}</text>\n'
        
    svg += '</svg>'
    
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    make_ascii("source-prepped.png", "avi-ascii.svg")
