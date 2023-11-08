import os
from dotenv import load_dotenv
from typing import Annotated
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.database import Session, engine, get_db
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    oauth2_scheme,
)

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/roles/", response_model=list[schemas.Role])
def read_roles(
    token: Annotated[str, Depends(oauth2_scheme)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if not get_current_user(db=db, token=token):
        return HTTPException(status_code=401, detail="Invalid credentials")
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles


@app.post("/roles/", response_model=schemas.Role)
def create_role(
    token: Annotated[str, Depends(oauth2_scheme)],
    role: schemas.RoleBase,
    db: Session = Depends(get_db),
):
    if not get_current_user(db=db, token=token):
        return HTTPException(status_code=401, detail="Invalid credentials")
    db_role = crud.get_role_by_role(db=db, role=role.role)
    if db_role:
        raise HTTPException(status_code=400, detail="Role name already registered")
    return crud.create_role(db=db, role=role)


@app.get("/users/", response_model=list[schemas.User])
def read_users(
    token: Annotated[str, Depends(oauth2_scheme)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if not get_current_user(db=db, token=token):
        return HTTPException(status_code=401, detail="Invalid credentials")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_badge_number(db, badge_number=user.badge_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Badge number already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return current_user


@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(
    token: Annotated[str, Depends(oauth2_scheme)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if not get_current_user(db=db, token=token):
        return HTTPException(status_code=401, detail="Invalid credentials")
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@app.post("/employees/", response_model=schemas.Employee)
def create_employee(
    token: Annotated[str, Depends(oauth2_scheme)],
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    current_user = get_current_user(db=db, token=token)
    if not current_user:
        return HTTPException(status_code=401, detail="Invalid credentials")
    db_employee = crud.get_employee_by_user_id(db=db, user_id=current_user.id)
    if db_employee:
        raise HTTPException(
            status_code=400,
            detail=f"Employee with user id {current_user.id} already registered",
        )
    for manager_id in employee.managers:
        db_manager = crud.get_user_by_id(db=db, user_id=manager_id)
        if not db_manager:
            raise HTTPException(
                status_code=400, detail=f"Manager with id {manager_id} does not exist"
            )
        if manager_id == current_user.id:
            raise HTTPException(
                status_code=400,
                detail=f"Employee cannot be their own manager",
            )
    return crud.create_employee(db=db, employee=employee, current_user=current_user)


@app.patch("/employees/{employee_id}", response_model=schemas.Employee)
def patch_employee(
    token: Annotated[str, Depends(oauth2_scheme)],
    employee_id: str,
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    current_user = get_current_user(db=db, token=token)
    if not current_user:
        return HTTPException(status_code=401, detail="Invalid credentials")
    db_employee = crud.get_employee_by_id(db=db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {employee_id} does not exist"
        )
    if db_employee.user_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail=f"Employee with id {employee_id} does not belong to current user",
        )
    return crud.patch_employee(db=db, employee_id=employee_id, employee=employee)
