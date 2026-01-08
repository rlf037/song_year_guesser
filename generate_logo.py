#!/usr/bin/env python3
"""
GitHub Logo Generator for Richard Friedman (rlf037)
Professional, minimalist logo design for data engineer/ML portfolio
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_hexagon_points(center_x, center_y, size):
    """Create points for a regular hexagon"""
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6  # Start from top
        x = center_x + size * math.cos(angle)
        y = center_y + size * math.sin(angle)
        points.append((x, y))
    return points

def create_logo(output_file='github_logo.png', size=800):
    """Generate professional GitHub logo"""

    # Color palette
    charcoal = '#2C3E50'
    slate = '#34495E'
    silver = '#7F8C8D'
    blue_accent = '#3498DB'
    white = '#FFFFFF'

    # Create canvas
    img = Image.new('RGB', (size, size), white)
    draw = ImageDraw.Draw(img)

    center = size // 2
    hex_size = size // 3

    # Draw outer hexagon (main shape)
    hex_points = create_hexagon_points(center, center, hex_size)
    draw.polygon(hex_points, fill=charcoal, outline=slate)

    # Draw inner hexagon (border effect)
    inner_hex_points = create_hexagon_points(center, center, hex_size * 0.9)
    draw.polygon(inner_hex_points, fill=slate, outline=charcoal)

    # Draw data flow bars (representing data pipeline/analytics)
    bar_width = 12
    bar_spacing = 20
    num_bars = 5
    start_x = center - (num_bars * bar_spacing) // 2
    base_y = center + hex_size * 0.5

    # Create ascending bar chart pattern
    bar_heights = [30, 50, 70, 55, 40]

    for i, height in enumerate(bar_heights):
        x = start_x + i * bar_spacing
        y_top = base_y - height

        # Gradient effect using multiple rectangles
        for j in range(int(height)):
            alpha_factor = 1 - (j / height) * 0.3
            if i % 2 == 0:
                color = blue_accent
            else:
                color = silver

            draw.rectangle(
                [x, y_top + j, x + bar_width, y_top + j + 1],
                fill=color
            )

    # Draw initials "RF" or data symbol
    try:
        # Try to use a clean font
        font_size = hex_size // 2
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw "RF" initials
    text = "RF"

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = center - text_width // 2
    text_y = center - text_height // 2 - hex_size * 0.2

    # Draw text with slight shadow for depth
    shadow_offset = 3
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill=charcoal, font=font)
    draw.text((text_x, text_y), text, fill=white, font=font)

    # Add subtle data points/connections
    point_size = 4
    points_coords = [
        (center - hex_size * 0.6, center - hex_size * 0.3),
        (center + hex_size * 0.6, center - hex_size * 0.3),
        (center - hex_size * 0.5, center + hex_size * 0.1),
        (center + hex_size * 0.5, center + hex_size * 0.1),
    ]

    for px, py in points_coords:
        draw.ellipse(
            [px - point_size, py - point_size, px + point_size, py + point_size],
            fill=blue_accent
        )

    # Draw connecting lines between points (data flow concept)
    draw.line([points_coords[0], points_coords[2]], fill=blue_accent, width=2)
    draw.line([points_coords[1], points_coords[3]], fill=blue_accent, width=2)

    # Save the image
    img.save(output_file, 'PNG', quality=95)
    print(f"✓ Logo saved to: {output_file}")
    print(f"✓ Size: {size}x{size} pixels")
    print(f"✓ Format: PNG")

    return output_file

def create_multiple_versions():
    """Create multiple size versions"""
    sizes = {
        'github_logo_large.png': 1200,
        'github_logo_medium.png': 800,
        'github_logo_small.png': 400,
        'github_logo_favicon.png': 128,
    }

    print("Generating logo versions...\n")
    for filename, size in sizes.items():
        create_logo(filename, size)
        print()

    print("✓ All versions generated successfully!")

if __name__ == '__main__':
    # Generate multiple versions
    create_multiple_versions()
