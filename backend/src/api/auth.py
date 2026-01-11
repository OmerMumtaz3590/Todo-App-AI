"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session

from ..database import get_session
from ..schemas.auth_schemas import (
    SignupRequest,
    SignupResponse,
    SigninRequest,
    SigninResponse,
    MessageResponse,
)
from ..services.auth_service import AuthService
from .middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    session: Session = Depends(get_session),
):
    """
    Create a new user account.

    - **email**: Valid email address (unique)
    - **password**: Minimum 8 characters

    Returns the created user ID and success message.
    """
    try:
        user = AuthService.signup(session, signup_data)
        return SignupResponse(user_id=user.id)
    except ValueError as e:
        if "already registered" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/signin", response_model=SigninResponse)
async def signin(
    signin_data: SigninRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    """
    Authenticate a user and establish a session.

    - **email**: User email address
    - **password**: User password

    Returns user information and sets an HTTP-only session cookie.
    """
    user = AuthService.signin(session, signin_data.email, signin_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create access token
    access_token = AuthService.create_access_token(user.id, user.email)

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=86400,  # 24 hours
    )

    return SigninResponse(
        user={"id": str(user.id), "email": user.email}
    )


@router.post("/signout", response_model=MessageResponse)
async def signout(
    response: Response,
    current_user: User = Depends(get_current_user),
):
    """
    Sign out the authenticated user and clear the session.

    Requires authentication.
    """
    # Clear the cookie
    response.delete_cookie(key="access_token")

    return MessageResponse(message="Signed out successfully")
