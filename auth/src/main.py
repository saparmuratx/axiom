from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.api.router import auth_router

app = FastAPI()
app.include_router(auth_router)
