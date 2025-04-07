import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Configure PyMySQL to be used with SQLAlchemy
pymysql.install_as_MySQLdb()

# Format: mysql://username:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:root@localhost:3306/test_db")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    def create_tables():
        Base.metadata.create_all(bind=engine)
        
except Exception as e:
    print(f"Database connection error: {e}")
