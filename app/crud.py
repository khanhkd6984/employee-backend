from sqlalchemy.orm import Session
from . import models
from . import schemas
from . import auth


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def get_role_by_role(db: Session, role: str):
    return db.query(models.Role).filter(models.Role.role == role).first()

def create_role(db: Session, role: schemas.RoleBase):
    db_role = models.Role(role=role.role)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
