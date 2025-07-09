from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime 


class ReviewCreate(BaseModel):
    author_name : str = Field(..., min_length = 3, max_length = 30)
    rating : int = Field(..., ge = 1, le=5)
    comment : Optional[str] = Field(..., max_length=300)
    company_id: int

    @field_validator("author_name")
    @classmethod
    def name_not_forbidden(cls, value):
        if value.lower() in ["admin", "moderator", "null"]:
            raise ValueError("The name is forbidden")
        return value

class ReviewRead(BaseModel):
    id: int
    author_name : str = Field(..., min_length = 3, max_length = 30)
    rating : int = Field(..., ge = 1, le=5)
    comment : Optional[str] = Field(..., max_length=300)
    created_at : datetime
    
    class Config():
        from_attributes = True

class CompanyCreate(BaseModel):
    name : str = Field(..., min_length = 2, max_length = 50)
    description : str = Field(..., max_length = 300)


class CompanyRead(BaseModel):
    id : int
    name : str
    description : str

    class Config():
        from_attributes = True




