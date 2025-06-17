from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.db.base import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("users.id"))
    barbeiro_id = Column(Integer, ForeignKey("users.id"))
    servico_id = Column(Integer, ForeignKey("services.id"))
    horario = Column(DateTime, nullable=False)
