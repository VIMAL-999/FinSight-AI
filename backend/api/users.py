from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User

from backend.schemas.user import UserCreate, UserResponse
from backend.schemas.login import Token

from backend.utils.security import hash_password, verify_password
from backend.utils.auth import create_access_token

from backend.api.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# -------------------------
# Register
# -------------------------
@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------
# Login
# -------------------------
@router.post("/login", response_model=Token)
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# Current Logged-in User
# -------------------------
@router.get("/me", response_model=UserResponse)
def get_current_logged_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


# -------------------------
# Get All Users
# -------------------------
@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


# -------------------------
# Get User By ID
# -------------------------
@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user