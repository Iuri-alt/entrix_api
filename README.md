# Entrix API

Backend do projeto **Entrix**, 
um aplicativo de controle financeiro desenvolvido 
com **FastAPI** e integrado com um app em Flutter.

---

## 🧠 Sobre o projeto

O Entrix é um sistema simples e eficiente para gerenciamento de finanças pessoais, permitindo:

* 🔐 Autenticação de usuários (login e cadastro)
* 💸 Registro de gastos e entradas
* 🗑️ Remoção de transações
* 📊 Preparação de dados para dashboard

---

## 🛠️ Tecnologias utilizadas

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **SQLite**
* **JWT (Autenticação)**

---

## 📁 Estrutura do projeto

```
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
└── routes/
    ├── auth.py
    ├── expenses.py
```

---


## 🌐 Deploy

.

---

## 🔑 Endpoints principais

### 🔐 Autenticação

* `POST /auth/register` → Criar usuário
* `POST /auth/login` → Login e geração de token

---

### 💸 Despesas

* `GET /expenses/` → Listar despesas
* `POST /expenses/` → Criar despesa
* `DELETE /expenses/{id}` → Remover despesa

---

## 📦 Exemplo de requisição

```json
{
  "title": "Almoço",
  "value": 25.50,
  "isIncome": false
}
```

## ⚠️ Observações

* O banco de dados atual utiliza **SQLite**
* Para produção, recomenda-se usar **PostgreSQL**
* Senhas ainda não estão criptografadas (melhoria futura)

## 👨‍💻 Autor

Desenvolvido por Iuri Antonio da Silva
