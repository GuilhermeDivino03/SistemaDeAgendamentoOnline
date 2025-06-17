from pydantic import BaseModel

class ServiceCreate(BaseModel):
    nome: str
    preco: float

class ServiceResponse(BaseModel):
    id: int
    nome: str
    preco: float

    class Config:
        orm_mode = True
