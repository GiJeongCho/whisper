from fastapi import APIRouter, status, Request
from pydantic import BaseModel
from .main import process_text

router_v1 = APIRouter(
    prefix="/v1",
    tags=["whisper"],
    responses={
        status.HTTP_200_OK: {"description": "Successful Response"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"}
    },
)
