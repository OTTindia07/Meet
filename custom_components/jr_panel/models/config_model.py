"""Configuration model for JR Touch Panel."""
from pydantic import BaseModel

class ConfigModel(BaseModel):
    """Configuration model for JR Touch Panel."""
    host: str
    port: int
    name: str
