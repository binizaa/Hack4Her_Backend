from pydantic import BaseModel

class UserCategory(BaseModel):
    category: str
