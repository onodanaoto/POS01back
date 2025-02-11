from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.auth import UserCreate, UserLogin, Token
from ..security.password import verify_password, get_password_hash
from ..security.jwt import create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # ユーザー名の重複チェック
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # メールアドレスの重複チェック
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # ユーザーの作成
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # アクセストークンの生成
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token) 