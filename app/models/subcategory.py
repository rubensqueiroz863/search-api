import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.category import Category

class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)

    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="subcategories")

    products = relationship("Product", back_populates="subcategory")