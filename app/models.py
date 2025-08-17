from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderIn(BaseModel):
    items: List[str] = Field(default_factory=list)
    total_amount: float = Field(ge=0)

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    items: List[str]
    total_amount: float
    status: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
