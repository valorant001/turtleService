from pydantic import BaseModel, Extra

class User(BaseModel):
    name: str
    email: str
    created_at:  None = None  
    updated_at: None = None

