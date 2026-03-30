import math
from fastapi import FastAPI
from fastapi.responses import Response
import svgwrite
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from fastapi import Request
from pydantic import BaseModel

app = FastAPI()

class CircleRequest(BaseModel):
    count: int
    radius: int
    ringRadius: int
    color: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/circles")

def create_circles(count: int = 5, radius: int = 30, gap: int = 10):

    dwg = svgwrite.Drawing(size=("400px", "400px"))

    start_x = 50
    y = 100

    for i in range(count):
        x = start_x + i * (radius * 2 + gap)

        dwg.add(
            dwg.circle(
                center=(x, y),
                r=radius,
                fill="blue"
            )
        )

    return Response(content=dwg.tostring(), media_type="image/svg+xml")

@app.get("/ring")
def create_ring(
    count: int = 8,
    radius: int = 30,
    ring_radius: int = 150,
    color: str = "blue"
    ):

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
                end=(x, y,),
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

    dwg.add(
        dwg.circle(
            center=(center_x, center_y),
            r=10,
            fill="red"
        )
    )

    return Response(content=dwg.tostring(), media_type="image/svg+xml")

@app.post("/save")
def save_setting(data: CircleRequest):

    count = data.count
    radius = data.radius
    ring_radius = data.ringRadius
    color = data.color

# circle_settings = DBで作成したテーブル名
    cur.execute(
        """
        INSERT INTO circle_settings (count, radius, ring_radius, color)
        VALUES (%s, %s, %s, %s)
        """,
        (count, radius, ring_radius, color)
    )

    conn.commit() #  DBに保存

    return {"message": "saved"} # レスポンスを返す（Reactに成功！と返す）

# DBから全部取ってJSONに変換
@app.get("/settings")
def get_settings():
    cur.execute("SELECT * FROM circle_settings ORDER BY id DESC")
    rows = cur.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "count": row[1],
            "radius": row[2],
            "ring_radius": row[3],
            "color": row[4],
            "created_at": str(row[5])
        })

    return result

@app.delete("/settings/{id}")
def delete_setting(id: int):
    cur.execute(
        "DELETE FROM circle_settings WHERE id = %s",
        (id,)
    )
    conn.commit()

    return {"message": "deleted"}

@app.put("/settings/{id}")
def update_setting(id: int, data: CircleRequest):
    cur.execute(
        """
        UPDATE circle_settings
        SET count = %s, radius = %s, ring_radius = %s, color = %s
        WHERE id = %s
        """,
        (data.count, data.radius, data.ringRadius, data.color, id)
    )
    conn.commit()

    return {"message": "updated"}

@app.get("/diff")
def diff(id1: int, id2: int):
    # ① DBから取得
    cur.execute("SELECT * FROM circle_settings WHERE id = %s", (id1,))
    a = cur.fetchone()

    cur.execute("SELECT * FROM circle_settings WHERE id = %s", (id2,))
    b = cur.fetchone()

    if not a or not b:
        return {"error": "not found"}

    # ② パラメータ取得
    countA, radiusA, ringA = a[1], a[2], a[3]
    countB, radiusB, ringB = b[1], b[2], b[3]

    # ③ SVG作成
    width = 400
    height = 400
    center_x = width // 2
    center_y = height // 2

    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))

    # ④ 差分チェック

    for i in range(countA):
        angle = 2 * math.pi * i / countA

        x = center_x + ringA * math.cos(angle)
        y = center_y + ringA * math.sin(angle)

        dwg.add(
            dwg.circle(
                center=(x, y),
                r=radiusA,
                fill="none",
                stroke="blue",
                stroke_width=2
            )
        )

    for i in range(countB):
            angle = 2 * math.pi * i / countB

            x = center_x + ringB * math.cos(angle)
            y = center_y + ringB * math.sin(angle)

            dwg.add(
                dwg.circle(
                center=(x, y),
                r=radiusB,
                fill="none",
                stroke="red",
                stroke_width=2,
                opacity=0.5
                )
            )

    return Response(content=dwg.tostring(), media_type="image/svg+xml")

conn = psycopg2.connect(
    dbname="circle_db",
    user="taniguchi.airi",
    password="",
    host="localhost"
)

cur = conn.cursor()