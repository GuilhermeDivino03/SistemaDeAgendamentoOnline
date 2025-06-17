from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from app.db.session import SessionLocal
from app.models.user import User
from app.models.service import Service
from app.models.agendamento import Agendamento
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from app.services.auth_bearer import get_current_user

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar agendamento
@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    dados: AgendamentoCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    # Somente cliente pode agendar
    if usuario.tipo != "cliente":
        raise HTTPException(status_code=403, detail="Somente clientes podem agendar.")

    # Validação: horário deve ser no futuro
    agora = datetime.now()
    if dados.horario < agora + timedelta(minutes=30):
        raise HTTPException(status_code=400, detail="O agendamento deve ser feito com pelo menos 30 minutos de antecedência.")

    # Validação: agendamentos só após 08h
    # if dados.horario.time() < time(8, 0):
    #     raise HTTPException(status_code=400, detail="O horário de agendamento deve ser após 08:00.")

    # Verifica se o barbeiro já tem agendamento nesse horário
    conflito = db.query(Agendamento).filter(
        Agendamento.barbeiro_id == dados.barbeiro_id,
        Agendamento.horario == dados.horario
    ).first()

    if conflito:
        raise HTTPException(status_code=400, detail="Este horário já está ocupado para o barbeiro escolhido.")

    # Verifica se barbeiro e serviço existem
    barbeiro = db.query(User).filter(User.id == dados.barbeiro_id, User.tipo == "barbeiro").first()
    servico = db.query(Service).filter(Service.id == dados.servico_id).first()

    if not barbeiro or not servico:
        raise HTTPException(status_code=404, detail="Barbeiro ou serviço não encontrado.")

    novo_agendamento = Agendamento(
        cliente_id=usuario.id,
        barbeiro_id=dados.barbeiro_id,
        servico_id=dados.servico_id,
        horario=dados.horario
    )

    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)

    # "Notificação" simulada
    print(f"📧 Notificação enviada: Agendamento confirmado para {usuario.email} às {dados.horario}")

    return novo_agendamento
