from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database.database import SessionLocal, init_db
from src.database.models import User
from src.utils.password import verify_password, hash_password
from src.utils.jwt import create_access_token, verify_token
from src.api.gemini import get_chat_response
from datetime import timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI()

# Initialize database
init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel, Field, EmailStr

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

class ChatMessage(BaseModel):
    text: str

import logging
logger = logging.getLogger(__name__)

@app.post("/register")
def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        logger.warning(f"Registration attempt for existing username: {user_data.username}")
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        logger.warning(f"Registration attempt for existing email: {user_data.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    logger.info(f"Successfully registered user: {user_data.username}")
    return {"message": "User created successfully"}

@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "This is a protected route", "user": payload["sub"]}

@app.post("/chat")
def chat_endpoint(message: ChatMessage, token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get response from Gemini
    response_text = get_chat_response(message.text)
    return {"response": response_text}
