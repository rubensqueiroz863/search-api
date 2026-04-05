import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)

    subcategories = relationship("SubCategory", back_populates="category")