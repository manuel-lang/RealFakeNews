from pydantic import BaseModel
from typing import Optional


class APIInput(BaseModel):
    text: str
    summarize: Optional[bool] = True
    speaker: Optional[str] = None
    min_text_length: Optional[int] = 30
    max_text_length: Optional[int] = 120
