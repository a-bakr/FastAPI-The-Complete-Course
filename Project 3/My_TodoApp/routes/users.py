from typing import Annotated

from auth import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/")
async def get_user(user: user_dependency, db: db_dependency):
    pass


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    pass
