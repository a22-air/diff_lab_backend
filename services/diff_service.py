import math
import svgwrite
from db.database import get_cursor

def get_setting_by_id(id):
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM circle_settings WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def create_diff_svg(id1: int, id2: int):

    a = get_setting_by_id(id1)
    b = get_setting_by_id(id2)

    if not a or not b:
        return None

    countA, radiusA, ringA = a[1], a[2], a[3]
    countB, radiusB, ringB = b[1], b[2], b[3]

    width = 400
    height = 400
    center_x = width // 2
    center_y = height // 2

    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))

    def is_close(a, b, tol=1e-3):
        return abs(a - b) < tol

    # 点生成
    def generate_points(count, ring):
        points = []
        for i in range(count):
            angle = 2 * math.pi * i / count
            x = center_x + ring * math.cos(angle)
            y = center_y + ring * math.sin(angle)
            points.append((x, y))
        return points

    pointsA = generate_points(countA, ringA)
    pointsB = generate_points(countB, ringB)

    # A描画
    for (xA, yA) in pointsA:
        matched = any(is_close(xA, xB) and is_close(yA, yB) for (xB, yB) in pointsB)

        if matched:
            color = "gray" if is_close(radiusA, radiusB) else "orange"
        else:
            color = "blue"

        dwg.add(dwg.line(start=(center_x, center_y), end=(xA, yA), stroke=color))
        dwg.add(dwg.circle(center=(xA, yA), r=radiusA, fill=color))

    # B描画
    for (xB, yB) in pointsB:
        matched = any(is_close(xA, xB) and is_close(yA, yB) for (xA, yA) in pointsA)

        if matched:
            color = "gray" if is_close(radiusA, radiusB) else "orange"
        else:
            color = "red"

        dwg.add(dwg.line(start=(center_x, center_y), end=(xB, yB), stroke=color))
        dwg.add(dwg.circle(center=(xB, yB), r=radiusB, fill=color))

    # 中心
    dwg.add(dwg.circle(center=(center_x, center_y), r=10, fill="black"))

    return dwg.tostring()