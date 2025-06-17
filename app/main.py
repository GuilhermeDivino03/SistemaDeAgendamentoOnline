from fastapi import FastAPI
from app.routes import user, service, agendamento
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(service.router)
app.include_router(agendamento.router)
@app.get("/")
def root():
    return {"mensagem": "API da Barbearia funcionando!"}
