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