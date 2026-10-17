# Entrix API

Backend do **Entrix** (FastAPI + SQLAlchemy). Guarda, por usuário, os dados da planilha
*Controle Financeiro*: lançamentos, produtos e configurações do plano. Os cálculos da
planilha rodam no app Flutter; a API persiste os dados e importa/exporta o `.xlsx`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Cria conta (senha com bcrypt) |
| POST | `/auth/login` | Retorna token JWT (`Bearer`) |
| GET | `/auth/me` | Usuário do token |
| GET/POST | `/transactions/` | Lista (filtro `start`/`end`) e cria lançamentos |
| PUT/DELETE | `/transactions/{id}` | Edita / exclui lançamento |
| GET/POST | `/products/` | Lista e cria produtos |
| PUT/DELETE | `/products/{id}` | Edita / exclui produto |
| GET/PUT | `/settings/` | Config, orçamento (Renda) e cenários (Simulação) |
| POST | `/spreadsheet/import?dry_run=true` | Valida/importa o `.xlsx` sem duplicar |
| GET | `/spreadsheet/export` | Baixa os dados no layout da planilha |
| GET | `/health` | Verificação de saúde |

Todas as rotas, exceto `/auth/register`, `/auth/login` e `/health`, exigem o token e só
enxergam os dados do próprio usuário.

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | sim, em produção | PostgreSQL (`postgres://…` é aceito). Sem ela usa `sqlite:///./entrix.db` (só para desenvolvimento) |
| `SECRET_KEY` | sim, em produção | Chave do JWT (32+ caracteres aleatórios) |
| `ACCESS_TOKEN_DAYS` | não | Validade do token em dias (padrão 30) |

## Deploy no Render

1. Crie um PostgreSQL no Render (ou em outro provedor, como Neon ou Supabase).
2. No serviço web `entrix-api`, defina `DATABASE_URL` e `SECRET_KEY` em *Environment*.
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

O `render.yaml` descreve essa configuração como Blueprint. As tabelas são criadas na
primeira inicialização. Usuários antigos com senha em texto puro continuam entrando:
a senha é convertida para hash no primeiro login.

## Desenvolvimento

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest
```
