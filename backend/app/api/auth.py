from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from app.database import get_db
from app.models.dataset import User
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.api.deps import get_current_user

router = APIRouter(tags=["auth"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {str(e)}")
    
    user_info = token.get('userinfo')
    if not user_info:
        user_info = await oauth.google.userinfo(token=token)
        
    email = user_info.get('email')
    google_id = user_info.get('sub')
    name = user_info.get('name')
    picture = user_info.get('picture')
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Create new user
        user = User(
            email=email,
            username=email.split('@')[0], # Simple username generation
            full_name=name,
            google_id=google_id,
            avatar_url=picture,
            is_active=True,
            balance=1000.0 # Starting balance for demo
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user info
        if not user.google_id:
            user.google_id = google_id
        if not user.avatar_url:
            user.avatar_url = picture
        db.commit()
        
    # Create access token
    access_token = create_access_token(subject=user.id)
    
    # Redirect to frontend with token
    from fastapi.responses import RedirectResponse
    import urllib.parse
    import json
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "avatar_url": user.avatar_url,
        "balance": user.balance
    }
    
    params = {
        "access_token": access_token,
        "user": json.dumps(user_data)
    }
    
    query_string = urllib.parse.urlencode(params)
    return RedirectResponse(url=f"http://localhost:3000/auth/callback?{query_string}")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
            "balance": user.balance
        }
    }

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
