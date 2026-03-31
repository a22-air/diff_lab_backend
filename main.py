import math
from fastapi import FastAPI
from fastapi.responses import Response
import svgwrite
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from fastapi import Request
from pydantic import BaseModel
from db.database import get_cursor
from services.settings_service import save_setting, get_settings, delete_setting, update_setting
from services.circle_service import create_circles_svg
from services.diff_service import create_diff_svg

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
    svg = create_circles_svg(count, radius, gap)
    return Response(content=svg, media_type="image/svg+xml")

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
    save_setting(data)

    return {"message": "saved"} # レスポンスを返す（Reactに成功！と返す）

# DBから全部取ってJSONに変換
@app.get("/settings")
def get_settings():

    return get_settings()

@app.delete("/settings/{id}")
def delete_setting(id: int):
    delete_setting(id)
    return {"message": "deleted"}

@app.put("/settings/{id}")
def update_setting(id: int, data: CircleRequest):
    update_setting(id, data)
    return {"message": "updated"}

@app.get("/diff")
def diff(id1: int, id2: int):
    svg = create_diff_svg(id1, id2)

    if not svg:
        return {"error": "not found"}

    return Response(content=svg, media_type="image/svg+xml")