from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config

app = FastAPI(title="A4S API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
