from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: str  # cliente, barbeiro, recepcionista

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        orm_mode = True
