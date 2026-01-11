"""Database connection and session management."""
from sqlmodel import Session, create_engine
from .config import settings

# Create SQLAlchemy engine with appropriate settings
# SQLite doesn't support connection pooling parameters
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},  # Allow multiple threads for SQLite
    )
else:
    # PostgreSQL with connection pooling
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10,
    )


def get_session():
    """
    FastAPI dependency for database sessions.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
