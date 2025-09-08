from app.schemas import BoardCreate, BoardUpdate, BoardRead
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.crud import get_board_by_id, get_boards_by_owner_id, create_board, update_board, delete_board
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session
from collections.abc import Sequence
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/boards",
    tags=["boards"],
    responses={404: {"description": "Not found"}}
    )


@router.get(
    "/{board_id}",
    response_model=BoardRead
)
def get_board_by_id_endpoint(board_id: int, db: Session = Depends(get_db), curent_user: User = Depends(get_current_user)) -> BoardRead:
    board = get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != curent_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this board")
    return BoardRead.model_validate(board)


@router.get(
    "/owner/{owner_id}",
    response_model=Sequence[BoardRead])
def get_boards_by_owner_id_endpoint(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[BoardRead]:
    boards = get_boards_by_owner_id(db, owner_id)
    if owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access these boards")
    return [BoardRead.model_validate(board) for board in boards]


@router.post(
    "/",
    response_model=BoardRead
    )
def create_board_endpoint(board: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BoardRead:
    try:
        db_board = create_board(db, 
                                title=board.title, 
                                description=board.description, 
                                owner_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return BoardRead.model_validate(db_board)


@router.put(
    "/{board_id}",
    response_model=BoardRead
    )
def update_board_endpoint(board_id: int, board: BoardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BoardRead:
    db_board = get_board_by_id(db, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    if db_board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this board")
    try:
        updated_board = update_board(db, board_id, title=board.title, description=board.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return BoardRead.model_validate(updated_board)


@router.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
    )
def delete_board_endpoint(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Response:
    db_board = get_board_by_id(db, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    if db_board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
    try:
        delete_board(db, board_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)