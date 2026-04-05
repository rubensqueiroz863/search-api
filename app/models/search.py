import uuid
from sqlalchemy import Column, String, JSON, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.connection import Base

class Search(Base):
    __tablename__ = "search"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(String, nullable=False)
    filters = Column(JSON, nullable=True)
    fields = Column(JSON, nullable=True)
    fuzzy = Column(Boolean, default=False)
    min_score = Column(String, nullable=True)
    sort_by = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)