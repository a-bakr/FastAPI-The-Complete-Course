from typing import Annotated

from auth import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Todos
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["admin"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo")
async def read_all(user: user_dependency, db: db_dependency):
    pass


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    pass
