from fastapi import APIRouter
from fastapi.responses import Response
from services.diff_service import create_diff_svg

router = APIRouter()

@router.get("/diff")
def diff(id1: int, id2: int):
    svg = create_diff_svg(id1, id2)

    if not svg:
        return {"error": "not found"}

    return Response(content=svg, media_type="image/svg+xml")