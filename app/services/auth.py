from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Chave secreta para assinar o token (nunca exponha em produção)
SECRET_KEY = "minha-chave-super-secreta"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

# Esse contexto usa o algoritmo bcrypt para lidar com senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Função que criptografa a senha antes de salvar no banco
def hash_senha(senha: str):
    return pwd_context.hash(senha)


# Função que verifica se a senha fornecida bate com a senha salva (criptografada)
def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


# Função para criar o token JWT
def criar_token(dados: dict):
    dados_para_token = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    dados_para_token.update({"exp": expiracao})

    token = jwt.encode(dados_para_token, SECRET_KEY, algorithm=ALGORITHM)
    return token
