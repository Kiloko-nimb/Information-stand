from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import schedule, staff, rooms

app = FastAPI(
    title="KKRIT Interactive Board API",
    description="API для интерактивного информационного стенда ККРИТ",
    version="1.0.0"
)

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "KKRIT Interactive Board API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
