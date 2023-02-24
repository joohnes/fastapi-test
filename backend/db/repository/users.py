from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    # user = User(hashed_password=Hasher.get_password_hash(user.password), **user.dict())
    user = User(
        **{k: i for k, i in user.dict().items() if k != "password"},
        hashed_password=Hasher.get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
