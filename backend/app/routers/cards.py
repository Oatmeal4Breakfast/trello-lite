from app.schemas import CardBase, CardCreate, CardRead, CardUpdate
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.crud import get_card_by_id, get_cards_by_list_id, create_card, update_card, delete_card
from app.database import get_db
from sqlalchemy.orm import Session
from collections.abc import Sequence



router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Not found"}}
    )


@router.get(
    "/{card_id}",
    response_model=CardRead)
def get_card_by_id_endpoint(card_id: int, db: Session = Depends(get_db)) -> CardRead:
    card = get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return CardRead.model_validate(card)


@router.get(
    "/list/{list_id}",
    response_model=Sequence[CardRead])
def get_cards_by_list_id_endpoint(list_id: int, db: Session = Depends(get_db)) -> Sequence[CardRead]:
    cards = get_cards_by_list_id(db, list_id)
    return [CardRead.model_validate(card) for card in cards]


@router.post(
    "/",
    response_model=CardRead)
def create_card_endpoint(card: CardCreate, db: Session = Depends(get_db)) -> CardRead:
    try:
        db_card = create_card(db, card.title, card.description, card.list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CardRead.model_validate(db_card)


@router.put(
    "/{card_id}",
    response_model=CardRead)
def update_card_endpoint(card_id: int, card: CardUpdate, db: Session = Depends(get_db)) -> CardRead:
    try:
        db_card = update_card(db, card_id, card.title, card.description)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return CardRead.model_validate(db_card)


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None)
def delete_card_endpoint(card_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        delete_card(db, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)