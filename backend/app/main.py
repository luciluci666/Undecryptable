from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router
from app.utils.db_config import BASE, ENGINE


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)

BASE.metadata.create_all(ENGINE)
