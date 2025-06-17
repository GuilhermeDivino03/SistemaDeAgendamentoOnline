from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.barbeiro import BarbeiroResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Listar todos os barbeiros
@router.get("/barbeiros", response_model=list[BarbeiroResponse])
def listar_barbeiros(db: Session = Depends(get_db)):
    return db.query(User).filter(User.tipo == "barbeiro").all()
