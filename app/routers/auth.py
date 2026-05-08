from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import AdminLogin, TokenResponse
from app.utils.jwt import create_access_token
from app.utils.errors import error_response
from app.config import settings
import bcrypt

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: AdminLogin):
    if credentials.email != settings.admin_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=error_response("INVALID_CREDENTIALS", "Invalid email or password"))

    if not bcrypt.checkpw(credentials.password.encode(), settings.admin_password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=error_response("INVALID_CREDENTIALS", "Invalid email or password"))

    token = create_access_token({"email": credentials.email, "role": "admin"})
    return TokenResponse(access_token=token)
