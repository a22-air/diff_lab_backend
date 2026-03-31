from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import circle_router, settings_router, diff_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(circle_router.router)
app.include_router(settings_router.router)
app.include_router(diff_router.router)