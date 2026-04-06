from pydantic import BaseModel
from typing import Optional, Dict, Any

class SearchCreate(BaseModel):
  query: str
  email: str
  performed_by: str

  filters: Optional[Dict[str, Any]] = None
  fields: Optional[Dict[str, Any]] = None
  fuzzy: Optional[bool] = False
  min_score: Optional[str] = None
  sort_by: Optional[str] = None

class SearchResponse(BaseModel):
  id: str
  user_id: str

class LastSearchHistoryDTO(BaseModel):
    query: str
