# Sistema de Registro e Acompanhamento de Chamados de TI

MVP acadêmico em Python, Flask, HTML, CSS e SQLite para registrar e acompanhar solicitações de suporte técnico.

## Funcionalidades
- Cadastro com título, descrição e prioridade de 1 a 5.
- Data e status inicial “Aberto” definidos automaticamente.
- Listagem, busca por título/descrição e filtro por status.
- Atualização de prioridade e status.
- Validação no servidor e mensagens de confirmação/erro.
- Layout responsivo, rótulos de formulário, foco visível e status apresentados por texto.
- Persistência local em SQLite.

## Requisitos
Python 3.11 ou superior.

## Executar no Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Abra `http://127.0.0.1:5000` no navegador.

## Executar no Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

## Estrutura
```text
sistema-chamados-ti-mvp/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── form.html
│   ├── editar.html
│   └── 404.html
└── static/style.css
```

## Requisitos funcionais
- RF01: cadastrar chamado.
- RF02: consultar listagem.
- RF03: alterar status.
- RF04: alterar prioridade.
- RF05: filtrar por status.

## Segurança e limitações
Este MVP é para execução local e não implementa login nem controle de permissões. Antes de publicar como serviço, implemente autenticação/autorização, use uma chave secreta por variável de ambiente, desative o modo debug, use HTTPS e revise os controles de segurança. Não coloque dados reais ou sensíveis no repositório. O arquivo SQLite é criado automaticamente e está excluído do Git pelo `.gitignore`. Em hospedagens efêmeras, o banco local pode não persistir.

## Teste manual
1. Cadastre um chamado fictício.
2. Confira o status Aberto na lista.
3. Pesquise pelo título e aplique o filtro de status.
4. Atualize prioridade e status.
5. Recarregue a página para conferir a persistência local.

A navegação por teclado, acessibilidade com tecnologias assistivas e desempenho precisam ser verificados na validação prática.
