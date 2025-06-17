from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    preco = Column(Float, nullable=False)
