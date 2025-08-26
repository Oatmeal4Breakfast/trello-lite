import bcrypt
from models import User, Board, List, Card
from sqlalchemy.orm import Session

#----- User CRUD operations -----#

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    else:
        raise ValueError("User not found")
    return user


def update_user(db: Session, user_id: int, email: str | None = None, password: str | None = None):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if email:
            user.email = email
        if password:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            user.hashed_password = hashed_password.decode('utf-8')
        db.commit()
        db.refresh(user)
    return user


def create_user(db: Session, username: str, email: str, password: str):
    if get_user_by_email(db, email) or get_user_by_username(db, username):
        raise ValueError("Email or username already registered")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    db_user = User(username=username, email=email, hashed_password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#----- Board CRUD operations -----#

def get_board_by_id(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


def get_boards_by_owner_id(db: Session, owner_id: int):
    return db.query(Board).filter(Board.owner_id == owner_id).all()


def update_board(db: Session, board_id: int, title: str | None = None, description: str | None = None):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board:
        if title:
            board.title = title
        if description:
            board.description = description
        db.commit()
        db.refresh(board)
    else:
        raise ValueError("Board not found")
    return board


def delete_board(db: Session, board_id: int):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board:
        db.delete(board)
        db.commit()
    else:
        raise ValueError("Board not found")
    return board


def create_board(db: Session, title: str, description: str, owner_id: int):
    db_board = Board(title=title, description=description, owner_id=owner_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


#----- Lists CRUD operations -----#

def get_list_by_id(db: Session, list_id: int):
    return db.query(List).filter(List.id == list_id).first()


def get_lists_by_board_id(db: Session, board_id: int):
    return db.query(List).filter(List.board_id == board_id).all()


def update_list(db: Session, list_id: int, title: str | None = None):
    lst = db.query(List).filter(List.id == list_id).first()
    if lst:
        if title:
            lst.title = title
        db.commit()
        db.refresh(lst)
    else:
        raise ValueError("List not found")
    return lst


def delete_list(db: Session, list_id: int):
    lst = db.query(List).filter(List.id == list_id).first()
    if lst:
        db.delete(lst)
        db.commit()
    else:
        raise ValueError("List not found")
    return lst


def create_list(db: Session, title: str, board_id: int):
    db_list = List(title=title, board_id=board_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


#----- Cards CRUD operations -----#

def get_card_by_id(db: Session, card_id: int):
    return db.query(Card).filter(Card.id == card_id).first()


def get_cards_by_list_id(db: Session, list_id: int):
    return db.query(Card).filter(Card.list_id == list_id).all()


def update_card(db: Session, card_id: int, title: str | None = None, description: str | None = None):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        if title:
            card.title = title
        if description:
            card.description = description
        db.commit()
        db.refresh(card)
    else:
        raise ValueError("Card not found")
    return card


def delete_card(db: Session, card_id: int):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    else:
        raise ValueError("Card not found")
    return card


def create_card(db: Session, title: str, description: str, list_id: int):
    db_card = Card(title=title, description=description, list_id=list_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

