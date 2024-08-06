from fastapi import APIRouter
from requests import session

from app.config.database import get_session

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses= {404:{"discription":"Not found !"}}
)