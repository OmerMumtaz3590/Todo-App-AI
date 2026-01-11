"""Initialize database tables for testing."""
from sqlmodel import SQLModel
from src.database import engine
from src.models.user import User
from src.models.todo import Todo

# Import models to register them with SQLModel
print("Creating database tables...")
SQLModel.metadata.create_all(engine)
print("Database tables created successfully!")
print(f"Database file: {engine.url}")
