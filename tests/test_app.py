
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
