from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.crud import get_list_by_id, get_lists_by_board_id, create_list, update_list, delete_list, get_board_by_id
from app.database import get_db
from app.dependencies import get_current_user
from sqlalchemy.orm import Session
from collections.abc import Sequence
from app.schemas import ListCreate, ListRead, ListUpdate
from app.models import User, List, Board



router = APIRouter(
    prefix="/lists",
    tags=["lists"],
    responses={404: {"description": "Not found"}}
    )
#--- Helper functions to validate users ---
def check_list_ownership(db_list:List, current_user: User) -> None:
    if db_list.board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to acces this list.")


def check_board_ownership(board: Board, current_user: User) -> None:
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this board.")


#--- API Router Functions ---
@router.get(
    "/{list_id}",
    response_model=ListRead)
def get_list_by_id_endpoint(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ListRead:
    lst = get_list_by_id(db, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")
    check_list_ownership(lst, current_user)
    return ListRead.model_validate(lst)


@router.get(
    "/board/{board_id}",
    response_model=Sequence[ListRead])
def get_lists_by_board_id_endpoint(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[ListRead]:
    board = get_board_by_id(db, board_id)
    check_board_ownership(board, current_user)
    lists = get_lists_by_board_id(db, board_id)
    return [ListRead.model_validate(lst) for lst in lists]


@router.post(
    "/",
    response_model=ListRead)
def create_list_endpoint(lst: ListCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ListRead:
    board = get_board_by_id(db, lst.board_id)
    check_board_ownership(board, current_user)
    try:
        db_list = create_list(db, lst.title, lst.board_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ListRead.model_validate(db_list)


@router.put(
    "/{list_id}",
    response_model=ListRead)
def update_list_endpoint(list_id: int, lst: ListUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ListRead:
    check_lst = get_list_by_id(db, list_id)
    check_list_ownership(check_lst, current_user)
    try:
        db_list = update_list(db, list_id, lst.title)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ListRead.model_validate(db_list)


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None)
def delete_list_endpoint(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Response:
    lst = get_list_by_id(db, list_id)
    check_list_ownership(lst, current_user)
    try:
        delete_list(db, list_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

