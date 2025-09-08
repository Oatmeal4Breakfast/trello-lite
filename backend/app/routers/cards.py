from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from collections.abc import Sequence
from app.schemas import CardCreate, CardRead, CardUpdate
from app.models import User, Card
from app.crud import get_card_by_id, get_cards_by_list_id, create_card, update_card, delete_card, get_list_by_id
from app.database import get_db
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Not found"}}
    )

#--- Helper functions to authorize ownership ---
def check_card_ownership(card: Card, current_user: User) -> None:
    if card.list.board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this card")

def check_list_ownership(db_list, current_user: User) -> None:
    if db_list.board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized to access this list")


#--- API ROUTES ---
@router.get(
    "/{card_id}",
    response_model=CardRead)
def get_card_by_id_endpoint(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> CardRead:
    card = get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    check_card_ownership(card, current_user)
    return CardRead.model_validate(card)


@router.get(
    "/list/{list_id}",
    response_model=Sequence[CardRead])
def get_cards_by_list_id_endpoint(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[CardRead]:
    db_list = get_list_by_id(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    check_list_ownership(db_list, current_user)
    cards = get_cards_by_list_id(db, list_id)
    return [CardRead.model_validate(card) for card in cards]


@router.post(
    "/",
    response_model=CardRead)
def create_card_endpoint(card: CardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> CardRead:
    db_list = get_list_by_id(db, card.list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    check_list_ownership(db_list, current_user)
    try:
        db_card = create_card(db, card.title, card.description, card.list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CardRead.model_validate(db_card)


@router.put(
    "/{card_id}",
    response_model=CardRead)
def update_card_endpoint(card_id: int, card: CardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> CardRead:
    db_card = get_card_by_id(db, card_id)
    check_card_ownership(db_card, current_user)
    try:
        db_card = update_card(db, card_id, card.title, card.description)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return CardRead.model_validate(db_card)


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None)
def delete_card_endpoint(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Response:
    db_card = get_card_by_id(db, card_id)
    check_card_ownership(db_card, current_user)    
    try:
        delete_card(db, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)