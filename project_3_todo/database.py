from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Đường dẫn SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos_app.db" # SQLite file sẽ nằm trong thư mục hiện tại.


# Tạo kết nối với database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # Cho phép kết nối đa luồng trong SQLite.


# Tạo Session
"""
Dùng sessionmaker để tạo session tương tác với database.
Tắt autocommit và autoflush để bạn kiểm soát transaction 1 cách rõ ràng.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class để các model ORM kế thừa
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
