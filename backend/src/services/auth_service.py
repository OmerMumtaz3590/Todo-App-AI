"""Authentication service for user signup, signin, and session management."""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from ..config import settings
from ..models.user import User, UserCreate, UserPublic

# Password hashing context
# Use PBKDF2 with SHA-256 for better compatibility on Python 3.14
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using PBKDF2-SHA256."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: UUID, email: str) -> str:
        """
        Create a JWT access token for a user.

        Args:
            user_id: User's UUID
            email: User's email

        Returns:
            JWT token string
        """
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        expire = datetime.utcnow() + expires_delta

        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify a JWT token and return the payload.

        Args:
            token: JWT token string

        Returns:
            Token payload dict if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def signup(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user account.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            Created user

        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = AuthService.hash_password(user_data.password)

        # Create user
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def signin(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            User if credentials are valid, None otherwise
        """
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user:
            return None

        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_current_user(session: Session, token: str) -> Optional[User]:
        """
        Get the current user from a JWT token.

        Args:
            session: Database session
            token: JWT token string

        Returns:
            User if token is valid, None otherwise
        """
        payload = AuthService.verify_token(token)

        if not payload:
            return None

        user_id = payload.get("sub")

        if not user_id:
            return None

        # Get user from database
        user = session.get(User, UUID(user_id))

        return user
