from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from models import StoryRequest, ImageRequest, UserCreate, User as UserSchema, Token, UserUpdatePoints
from api import generate_story_logic, generate_image_logic
import uvicorn
import db_models
from database import engine, get_db
import auth
import os
import logging
from fastapi.responses import JSONResponse
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
try:
    db_models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    logger.error(traceback.format_exc())

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Directory contents: {os.listdir('.')}")
    if os.path.exists("data"):
        logger.info(f"Data directory contents: {os.listdir('data')}")
    else:
        logger.info("Data directory does not exist.")
    
    # Check DB connection
    try:
        with engine.connect() as connection:
            logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()},
    )

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def get_client_ip(request: Request):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    user = db.query(db_models.User).filter(db_models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin_user(current_user: db_models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限 (Admin privileges required)")
    return current_user

@app.post("/api/register", response_model=UserSchema)
def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    client_ip = get_client_ip(request)
    
    # Check IP limit - Exclude localhost for testing purposes
    if client_ip not in ["127.0.0.1", "localhost", "::1"]:
        existing_ip_user = db.query(db_models.User).filter(db_models.User.registration_ip == client_ip).first()
        if existing_ip_user:
            raise HTTPException(status_code=400, detail="此 IP 已注册过账号 (IP address already registered)")
    
    # Check username
    db_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在 (Username already registered)")
    
    hashed_password = auth.get_password_hash(user.password)
    
    # First registered user becomes admin automatically
    is_admin = db.query(db_models.User).count() == 0
    
    new_user = db_models.User(
        username=user.username,
        hashed_password=hashed_password,
        points=80,
        registration_ip=client_ip,
        is_admin=is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserSchema)
async def read_users_me(current_user: db_models.User = Depends(get_current_user)):
    return current_user

# Admin endpoints
@app.get("/api/admin/users", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, current_user: db_models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    users = db.query(db_models.User).offset(skip).limit(limit).all()
    return users

@app.post("/api/admin/users/{user_id}/points", response_model=UserSchema)
async def update_user_points(user_id: int, points_data: UserUpdatePoints, current_user: db_models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.points = points_data.points
    db.commit()
    db.refresh(user)
    return user

@app.post("/api/story")
async def generate_story(request: StoryRequest, current_user: db_models.User = Depends(get_current_user)):
    # Story generation requires login
    data = generate_story_logic(request.character, request.plot, request.page_count)
    return data

@app.post("/api/image")
async def generate_image(request: ImageRequest, current_user: db_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.points < 10:
        raise HTTPException(status_code=400, detail="积分不足，需要10积分 (Insufficient points, need 10)")
    
    # Combine character design with page prompt
    full_prompt = request.prompt
    if request.character_design:
        full_prompt = f"Character Design: {request.character_design}. \n\n" + full_prompt
        
    image_base64 = generate_image_logic(full_prompt)
    
    # Deduct points
    current_user.points -= 10
    db.commit()
    
    return {"image_data": image_base64, "remaining_points": current_user.points}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
