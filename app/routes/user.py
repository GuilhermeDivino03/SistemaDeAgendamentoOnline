from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_bearer import get_current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import verificar_senha, criar_token, hash_senha


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == form_data.username).first()

    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    # Conteúdo do token (evite colocar dados sensíveis aqui)
    token_data = {
        "sub": usuario.email,
        "tipo": usuario.tipo
    }

    token = criar_token(token_data)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/", response_model=UserResponse)
def criar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    novo_usuario = User(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha),
        tipo=usuario.tipo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/me")
def obter_dados_usuario_logado(usuario: User = Depends(get_current_user)):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    }

