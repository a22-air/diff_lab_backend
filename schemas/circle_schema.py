from pydantic import BaseModel

class CircleRequest(BaseModel):
    count: int
    radius: int
    ringRadius: int
    color: str