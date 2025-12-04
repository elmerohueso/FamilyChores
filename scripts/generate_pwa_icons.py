#!/usr/bin/env python3
"""
Generate placeholder PWA icons for Family Chores
Creates simple gradient icons in required sizes until custom icons are designed
"""

from PIL import Image, ImageDraw, ImageFont
import os

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
OUTPUT_DIR = os.path.join('static', 'icons')
COLOR_START = (102, 126, 234)  # #667eea
COLOR_END = (240, 147, 251)    # #f093fb

def interpolate_color(color1, color2, factor):
    """Interpolate between two RGB colors"""
    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

def create_gradient_icon(size):
    """Create a gradient icon with checkmark"""
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # Draw vertical gradient
    for y in range(size):
        factor = y / size
        color = interpolate_color(COLOR_START, COLOR_END, factor)
        draw.line([(0, y), (size, y)], fill=color)
    
    # Add rounded corners
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    corner_radius = size // 8
    mask_draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=255
    )
    
    # Apply mask for rounded corners
    output = Image.new('RGBA', (size, size))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Draw simple checkmark symbol
    check_color = (255, 255, 255, 255)
    stroke_width = max(2, size // 32)
    
    # Checkmark coordinates (scaled to size)
    scale = size / 512
    points = [
        (180 * scale, 280 * scale),
        (230 * scale, 330 * scale),
        (350 * scale, 200 * scale)
    ]
    
    check_draw = ImageDraw.Draw(output)
    for i in range(len(points) - 1):
        check_draw.line(
            [points[i], points[i + 1]],
            fill=check_color,
            width=stroke_width
        )
    
    return output

def main():
    """Generate all required icon sizes"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Generating PWA icons in {OUTPUT_DIR}/")
    
    for size in SIZES:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        print(f"  Creating {filename}...", end=' ')
        
        try:
            icon = create_gradient_icon(size)
            icon.save(filepath, 'PNG', optimize=True)
            print("Done")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nIcon generation complete!")
    print("Icons created with purple gradient and checkmark symbol")
    print("Replace these with custom-designed icons when ready")

if __name__ == '__main__':
    main()
