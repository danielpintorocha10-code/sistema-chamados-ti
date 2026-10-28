# Sistema de Registro e Acompanhamento de Chamados de TI

MVP acadêmico desenvolvido com Python, Flask, HTML, CSS e SQLite para registrar e acompanhar solicitações de suporte técnico.

## Objetivo

Facilitar o registro e o acompanhamento de chamados de TI, permitindo organizar solicitações e consultar seus respectivos status e prioridades.

## Funcionalidades

- Cadastro de chamados com título, descrição e prioridade de 1 a 5.
- Registro automático da data de criação.
- Definição do status inicial como **Aberto**.
- Listagem dos chamados cadastrados.
- Pesquisa e filtragem de chamados.
- Atualização da prioridade e do status.
- Armazenamento dos dados em banco SQLite.
- Interface web responsiva.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Git e GitHub

## Requisitos

- Python 3.11 ou superior.
- Git (opcional, para versionamento do projeto).

## Como executar o projeto

### 1. Obter os arquivos

Clone o repositório:

```bash
git clone https://github.com/danielpintorocha10-code/sistema-chamados-ti.git
cd sistema-chamados-ti
```

### 2. Criar um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Iniciar a aplicação

```powershell
python app.py
```

### 5. Acessar no navegador

Abra:

http://127.0.0.1:5000

O banco de dados SQLite é criado localmente pela aplicação quando necessário.

## Estrutura do projeto

```text
sistema-chamados-ti/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── chamados.db
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── form.html
    ├── editar.html
    └── 404.html
```

**Observação:** `chamados.db` é um arquivo local e está excluído do versionamento pelo `.gitignore`.

## Contexto acadêmico

Este projeto é um MVP acadêmico de um sistema de registro e acompanhamento de chamados de TI. Seu propósito é aplicar conhecimentos de desenvolvimento web, organização de dados e controle de versão.

## Repositório

https://github.com/danielpintorocha10-code/sistema-chamados-ti
