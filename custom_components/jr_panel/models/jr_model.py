"""Data model for JR Touch Panel entities."""
from pydantic import BaseModel

class JREntityModel(BaseModel):
    """Data model for JR Touch Panel entities."""
    dp_id: int
    identifier: str
    name: str
    value: int
