from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, db, auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.UserRead, summary="Register New User", description="Create a new user with email and password.")
def register(user_in: schemas.UserCreate, db: Session = Depends(db.get_db)):
    """Register a new user."""
    user = auth.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(user_in.password)
    new_user = models.User(email=user_in.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# PUBLIC_INTERFACE
@router.post("/token", response_model=schemas.Token, summary="User Login", description="Obtain a JWT token by providing email and password.")
def login(form_data: schemas.UserCreate, db: Session = Depends(db.get_db)):
    """Authenticate user and return token."""
    user = auth.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# PUBLIC_INTERFACE
@router.get("/me", response_model=schemas.UserRead, summary="Get Current User", description="Get info on the currently authenticated user.")
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """Get current logged-in user."""
    return current_user
