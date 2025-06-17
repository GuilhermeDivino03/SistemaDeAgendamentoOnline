from pydantic import BaseModel
from datetime import datetime

class AgendamentoCreate(BaseModel):
    barbeiro_id: int
    servico_id: int
    horario: datetime  # formato ISO 8601

class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    barbeiro_id: int
    servico_id: int
    horario: datetime

    class Config:
        orm_mode = True
