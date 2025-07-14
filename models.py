from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Message(id={self.id}, model_name='{self.model_name}', created_at='{self.created_at}')>"

# Database setup
def get_database_url():
    """Get database URL from settings or use SQLite as default"""
    return "sqlite:///./messages.db"

# Create engine
engine = create_engine(
    get_database_url(),
    connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

# Database dependency for FastAPI
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
