from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models
from . import schemas
from . import auth


def create_role(db: Session, role: schemas.RoleBase):
    db_role = models.Role(role=role.role)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_role_by_role(db: Session, role: str):
    return db.query(models.Role).filter(models.Role.role == role).first()


def get_role_by_id(db: Session, role_id: str):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        badge_number=user.badge_number,
    )
    for role_id in user.roles:
        db_role = get_role_by_id(db=db, role_id=role_id)
        db_user.roles.append(db_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_badge_number(db: Session, badge_number: str):
    return (
        db.query(models.User).filter(models.User.badge_number == badge_number).first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# def create_employee(db: Session, employee: schemas.EmployeeBase, current_user):
#     db_employee = models.Employee(
#         user_id=current_user.id,
#         avatar_url=employee.avatar_url,
#         phone=employee.phone,
#         job_position=employee.job_position,
#         department=employee.department,
#         work_location=employee.work_location,
#         summary=employee.summary,
#     )
#     for manager_id in employee.managers:
#         db_manager = db.query(models.User).filter(models.User.id == manager_id).first()
#         db_employee.managers.append(db_manager)
#     db.add(db_employee)
#     db.commit()
#     db.refresh(db_employee)
#     return db_employee


# def get_employees(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Employee).offset(skip).limit(limit).all()


# def get_employee_by_user_id(db: Session, user_id: str):
#     return db.query(models.Employee).filter(models.Employee.user_id == user_id).first()


# def get_employee_by_id(db: Session, employee_id: str):
#     return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


# def patch_employee(db: Session, employee_id: str, employee: schemas.EmployeeCreate):
#     db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id)
#     if "managers" in employee.dict(exclude_none=True).keys():
#         # TODO: Add logic to patch managers
#         raise HTTPException(
#             status_code=401,
#             detail="Cannot patch managers",
#         )
#     else:
#         db_employee.update(employee.dict(exclude_none=True))
#         db.commit()
#         return db_employee.first()
