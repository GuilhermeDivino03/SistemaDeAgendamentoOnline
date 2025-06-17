from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceResponse
from app.services.auth_bearer import get_current_user
from app.models.user import User

router = APIRouter(prefix="/servicos", tags=["Serviços"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceResponse)
def criar_servico(
        servico: ServiceCreate,
        db: Session = Depends(get_db),
        usuario: User = Depends(get_current_user)
):
    if usuario.tipo != "recepcionista":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para recepcionistas.")

    existente = db.query(Service).filter(Service.nome == servico.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Serviço já cadastrado.")

    novo_servico = Service(nome=servico.nome, preco=servico.preco)
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico


@router.get("/", response_model=list[ServiceResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.nome).all()
