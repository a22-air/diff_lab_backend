from fastapi import APIRouter
from fastapi.responses import Response
from services.circle_service import create_circles_svg, create_ring_svg

router = APIRouter()

@router.get("/circles")
def circles(count: int = 5, radius: int = 30, gap: int = 10):
    svg = create_circles_svg(count, radius, gap)
    return Response(content=svg, media_type="image/svg+xml")


@router.get("/ring")
def ring(count: int = 8, radius: int = 30, ring_radius: int = 150, color: str = "blue"):
    svg = create_ring_svg(count, radius, ring_radius, color)
    return Response(content=svg, media_type="image/svg+xml")