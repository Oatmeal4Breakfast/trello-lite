from app.schemas import ListBase, ListCreate, ListRead, ListUpdate
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.crud import get_list_by_id, get_lists_by_board_id, create_list, update_list, delete_list
from app.database import get_db
from sqlalchemy.orm import Session
from collections.abc import Sequence



router = APIRouter(
    prefix="/lists",
    tags=["lists"],
    responses={404: {"description": "Not found"}}
    )


@router.get(
    "/{list_id}",
    response_model=ListRead)
def get_list_by_id_endpoint(list_id: int, db: Session = Depends(get_db)) -> ListRead:
    lst = get_list_by_id(db, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")
    return ListRead.model_validate(lst)


@router.get(
    "/board/{board_id}",
    response_model=Sequence[ListRead])
def get_lists_by_board_id_endpoint(board_id: int, db: Session = Depends(get_db)) -> Sequence[ListRead]:
    lists = get_lists_by_board_id(db, board_id)
    return [ListRead.model_validate(lst) for lst in lists]


@router.post(
    "/",
    response_model=ListRead)
def create_list_endpoint(lst: ListCreate, db: Session = Depends(get_db)) -> ListRead:
    try:
        db_list = create_list(db, lst.title, lst.board_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ListRead.model_validate(db_list)


@router.put(
    "/{list_id}",
    response_model=ListRead)
def update_list_endpoint(list_id: int, lst: ListUpdate, db: Session = Depends(get_db)) -> ListRead:
    try:
        db_list = update_list(db, list_id, lst.title)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ListRead.model_validate(db_list)


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None)
def delete_list_endpoint(list_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        delete_list(db, list_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

