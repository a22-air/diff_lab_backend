import svgwrite
import math

def create_circles_svg(count, radius, gap):
    dwg = svgwrite.Drawing(size=("400px", "400px"))

    start_x = 50
    y = 100

    for i in range(count):
        x = start_x + i * (radius * 2 + gap)
        dwg.add(dwg.circle(center=(x, y), r=radius, fill="blue"))

    return dwg.tostring()

def create_ring_svg(count, radius, ring_radius, color):
    width = 400
    height = 400

    center_x = width // 2
    center_y = height // 2

    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))

    for i in range(count):
        angle = 2 * math.pi * i / count

        x = center_x + ring_radius * math.cos(angle)
        y = center_y + ring_radius * math.sin(angle)

        dwg.add(
            dwg.line(
                start=(center_x, center_y),
                end=(x, y),
                stroke="gray",
                stroke_width=2
            )
        )

        dwg.add(
            dwg.circle(
                center=(x, y),
                r=radius,
                fill=color
            )
        )

    # 中心の円
    dwg.add(
        dwg.circle(
            center=(center_x, center_y),
            r=10,
            fill="red"
        )
    )

    return dwg.tostring()