from fastapi import APIRouter

router = APIRouter(
    prefix="/user/self",
    tags=["User"]
)
