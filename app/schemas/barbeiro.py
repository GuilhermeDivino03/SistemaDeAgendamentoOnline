from pydantic import BaseModel, EmailStr

class BarbeiroResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
