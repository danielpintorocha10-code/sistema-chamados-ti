
import pytest

import app as sistema


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Usa um banco temporário para não alterar os chamados reais.
    banco_teste = tmp_path / "chamados_teste.db"
    monkeypatch.setattr(sistema, "DB", banco_teste)

    sistema.inicializar()

    sistema.app.config["TESTING"] = True

    with sistema.app.test_client() as cliente:
        yield cliente


def test_pagina_inicial_carrega(cliente):
    resposta = cliente.get("/")

    assert resposta.status_code == 200


def test_pagina_de_novo_chamado_carrega(cliente):
    resposta = cliente.get("/chamados/novo")

    assert resposta.status_code == 200


def test_cadastrar_chamado_com_dados_validos(cliente):
    resposta = cliente.post(
        "/chamados/novo",
        data={
            "titulo": "Computador não liga",
            "descricao": "O computador não liga após pressionar o botão.",
            "prioridade": "4",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert b"Computador n" in resposta.data
    assert b"cadastrado com sucesso" in resposta.data


def test_rejeitar_chamado_sem_titulo(cliente):
    resposta = cliente.post(
        "/chamados/novo",
        data={
            "titulo": "",
            "descricao": "Teste de validação do cadastro.",
            "prioridade": "3",
        },
    )

    assert resposta.status_code == 400
    assert b"120 caracteres" in resposta.data


def test_editar_chamado_atualiza_status_e_prioridade(cliente):
    cliente.post(
        "/chamados/novo",
        data={
            "titulo": "Internet lenta",
            "descricao": "Conexão instável no setor.",
            "prioridade": "2",
        },
    )

    with cliente.application.app_context():
        with sistema.conectar() as con:
            numero = con.execute(
                "SELECT id FROM chamados WHERE titulo = ?",
                ("Internet lenta",),
            ).fetchone()["id"]

    resposta = cliente.post(
        f"/chamados/{numero}/editar",
        data={
            "status": "Em andamento",
            "prioridade": "5",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert b"atualizado com sucesso" in resposta.data

    with cliente.application.app_context():
        with sistema.conectar() as con:
            chamado = con.execute(
                "SELECT status, prioridade FROM chamados WHERE id = ?",
                (numero,),
            ).fetchone()

    assert chamado["status"] == "Em andamento"
    assert chamado["prioridade"] == 5


def test_editar_chamado_inexistente_retorna_404(cliente):
    resposta = cliente.get("/chamados/999999/editar")

    assert resposta.status_code == 404
