import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.subcategory import SubCategory

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    price = Column(Float)
    photo = Column(String)

    subcategory_id = Column(String, ForeignKey("subcategories.id"), nullable=False)
    subcategory = relationship("SubCategory", back_populates="products")