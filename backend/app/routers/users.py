
from app.schemas import UserBase, UserCreate, UserUpdate, UserRead
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.crud import get_user_by_email, get_user_by_id, get_user_by_username, create_user, update_user, delete_user
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
    )

@router.get(
    "/{user_id}",
    response_model=UserRead
)
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get(
    "/by-username/{username}",
    response_model=UserRead
)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)) -> UserRead:
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@router.get(
    "/by-email",
    response_model=UserRead
)
def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)) -> UserRead:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.post(
    "/",
    response_model=UserRead
    )
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    try:
        db_user = create_user(db, user.username, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserRead.model_validate(db_user)


@router.put(
    "/{user_id}",
    response_model=UserRead
    )
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    db_user = update_user(db, user_id, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(db_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT, 
    response_model=None
    )
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        db_user = delete_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
