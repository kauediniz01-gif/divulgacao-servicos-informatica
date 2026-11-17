
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_status_api():
    resposta = client.get("/status")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "online"}


def test_inicio_api():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "mensagem": "API de divulgação de serviços de informática funcionando!"
    }

def test_listar_categorias():
    resposta = client.get("/categorias")

    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
    assert len(resposta.json()) > 0

    for categoria in resposta.json():
        assert "id_categoria" in categoria
        assert "nome" in categoria
        assert "descricao" in categoria


def test_listar_servicos():
    resposta = client.get("/servicos")

    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
    assert len(resposta.json()) > 0

    for servico in resposta.json():
        assert "id_servico" in servico
        assert "nome" in servico
        assert "descricao" in servico
        assert "categoria_id" in servico
        assert "categoria" in servico
