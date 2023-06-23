import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.dependencies.database import get_session
from src.routers import house

app = FastAPI(dependencies=[Depends(get_session)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(house.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
