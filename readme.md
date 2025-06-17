Sistema de Agendamento de Barbearia

🔄 Como iniciar o ambiente

Ative o ambiente virtual:

# Windows
./venv/Scripts/activate

Instale as dependências:

pip install -r requirements.txt

(Inclui: fastapi, uvicorn, sqlalchemy, passlib[bcrypt], python-jose, python-multipart)

Inicie o servidor:

uvicorn app.main:app --reload

Acesse a documentação da API (Swagger):
http://localhost:8000/docs

🔧 Funcionalidades implementadas

✅ 1. Cadastro de usuários (POST /usuarios/)

Campos: nome, email, senha, tipo (cliente, barbeiro, recepcionista)

Senha criptografada com bcrypt

✅ 2. Login com token JWT (POST /usuarios/login)

Requisição via form-data

Retorna: access_token, token_type

✅ 3. Proteção de rotas com autenticação

Dependência: get_current_user

Token deve ser enviado em Authorization: Bearer <token>

✅ 4. Listagem de barbeiros (GET /usuarios/barbeiros)

Retorna apenas usuários com tipo barbeiro

✅ 5. Cadastro de serviços (POST /servicos/)

Apenas recepcionistas podem cadastrar

Campos: nome, preco

Evita nomes duplicados

✅ 6. Listagem de serviços (GET /servicos/)

Ordenado por nome

✅ 7. Agendamento de serviços (POST /agendamentos/)

Apenas clientes podem agendar

Campos: barbeiro_id, servico_id, horario

Regras de negócio:

Min. 30 minutos de antecedência

Apenas após 08:00h

Verifica se o barbeiro já está ocupado no horário

Notifica por print() simulando e-mail

📋 Como testar no Swagger

Cadastre um usuário (cliente ou recepcionista)

Realize login e copie o token

Clique em "Authorize" no topo da Swagger UI

Cole: Bearer <token>

Use os endpoints conforme o tipo de usuário

Recepcionista: pode usar POST /servicos/

Cliente: pode usar POST /agendamentos/

🔹 Arquivos criados/modificados principais

app/
├── main.py
├── models/
│   ├── user.py
│   ├── service.py
│   └── agendamento.py
├── schemas/
│   ├── user.py
│   ├── service.py
│   ├── barbeiro.py
│   └── agendamento.py
├── routes/
│   ├── user.py
│   ├── service.py
│   └── agendamento.py
└── services/
    ├── auth.py
    └── auth_bearer.py

📅 Status atual do projeto

Ambiente virtual configurado e rodando ✅

Autenticação JWT implementada ✅

Controle de acesso por tipo de usuário ✅

Cadastro e listagem de serviços ✅

Agendamento com regras ✅

Testado via Swagger ✅

Próximos passos sugeridos:

Listagem de agendamentos por cliente/barbeiro

Cancelamento/edição de agendamento

Relatórios por dia/semana/mês

Integração com e-mail real (ou log)

Interface frontend (opcional no futuro)

