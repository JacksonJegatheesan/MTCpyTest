from pydantic import BaseModel
from typing import List, Optional

class ImageMeta(BaseModel):
    id: str
    filename: str
    title: str
    description: str
    tags: List[str]