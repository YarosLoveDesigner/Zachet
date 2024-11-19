from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Подключение к базе данных PostgreSQL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/asd"
engine = create_engine(DATABASE_URL)

# Создание сессии
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Определение базового класса
Base = declarative_base()

# Таблица категорий
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="category")

# Таблица товаров
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="items")

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
