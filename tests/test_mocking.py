# Teste com pytest-mock

"""
IMPORTANTE: Mocking para Evitar Requisições Reais

Mocking permite substituir dependências externas (APIs, bancos, etc)
por versões simuladas, tornando testes:
- Mais rápidos (não fazem chamadas reais)
- Mais confiáveis (não dependem de serviços externos)
- Mais previsíveis (controlamos as respostas)
- Ideais para CI/CD (GitHub Actions, GitLab CI, etc)

TODOS os testes neste arquivo usam mocks - NENHUMA requisição real é feita!
Isso significa que funcionam mesmo sem internet ou se a API externa cair.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste"""
    return TestClient(app)


# FIXTURES PARA MOCKING


@pytest.fixture
def mock_posts_data():
    """
    Fixture que retorna dados mockados de posts.
    Reutilizável em múltiplos testes.
    """
    return [
        {"id": 1, "title": "Post Mockado 1", "body": "Conteúdo fake"},
        {"id": 2, "title": "Post Mockado 2", "body": "Outro fake"},
    ]


@pytest.fixture
def mock_post_individual():
    """Fixture com dados de um post único"""
    return {
        "id": 1,
        "title": "Post de Teste",
        "body": "Este post não existe na API real",
        "userId": 1,
    }


@pytest.fixture
def mock_comments_data():
    """Fixture com dados de comentários mockados"""
    return [
        {"id": 1, "email": "test@example.com", "body": "Comentário fake 1"},
        {"id": 2, "email": "test2@example.com", "body": "Comentário fake 2"},
    ]


@pytest.fixture
def mock_requests_success(mocker):
    """
    Fixture que configura mock de sucesso para requests.get.
    Retorna uma função para customizar a resposta.
    """

    def _mock(data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = data
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


@pytest.fixture
def mock_requests_error(mocker):
    """
    Fixture que configura mock de erro para requests.get.
    """

    def _mock(status_code=500):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


# TESTES USANDO FIXTURES COM MOCKING


def test_deve_usar_fixture_de_dados_mockados(mocker, client, mock_posts_data):
    """
    Demonstra uso de fixture com dados mockados.
    A fixture fornece os dados, o teste configura o mock.

    IMPORTANTE: mocker.patch substitui requests.get por versão falsa.
    NENHUMA requisição HTTP real é feita para jsonplaceholder.typicode.com!
    """
    # Configurar mock usando dados da fixture
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_posts_data

    # Esta linha SUBSTITUI requests.get - não faz requisições reais!
    mocker.patch("requests.get", return_value=mock_response)

    # Requisição ao endpoint (que internamente chamaria requests.get)
    # MAS o mock intercepta e retorna mock_response ao invés de chamar a API
    response = client.get("/posts?limit=2")

    # Verificações
    assert response.status_code == 200
    assert response.json() == mock_posts_data
    assert len(response.json()) == 2


def test_deve_usar_fixture_de_mock_configurada(
    client, mock_posts_data, mock_requests_success
):
    """
    Demonstra uso de fixture que já configura o mock.
    Mais simples e reutilizável!

    IMPORTANTE: A fixture mock_requests_success já faz o mocker.patch,
    então NÃO há requisições reais aqui também.
    """
    # Fixture já configura tudo, só passar os dados
    mock_requests_success(mock_posts_data)

    # Requisição (interceptada pelo mock)
    response = client.get("/posts?limit=2")

    # Verificações
    assert response.status_code == 200
    assert response.json() == mock_posts_data


def test_deve_usar_fixture_para_mock_de_erro(client, mock_requests_error):
    """
    Demonstra fixture que simula erro.

    IMPORTANTE: Simulamos erro 500 SEM precisar quebrar a API real.
    Útil para testar tratamento de erros sem depender de falhas reais.
    """
    # Fixture configura erro 500 (mockado, não real)
    mock_requests_error(status_code=500)

    # Requisição
    response = client.get("/posts")

    # Verificações
    assert response.status_code == 500


def test_deve_combinar_multiplas_fixtures_com_mock(
    client, mock_post_individual, mock_requests_success
):
    """
    Demonstra combinação de múltiplas fixtures:
    - client: fixture do TestClient
    - mock_post_individual: fixture com dados
    - mock_requests_success: fixture que configura mock

    IMPORTANTE: Composição de fixtures permite testes limpos e reutilizáveis.
    """
    # Usar fixture de mock com dados de outra fixture
    mock_requests_success(mock_post_individual)

    # Requisição (mockada)
    response = client.get("/posts/1")

    # Verificações
    assert response.status_code == 200
    assert response.json()["title"] == "Post de Teste"


def test_deve_usar_fixture_de_comentarios_mockados(
    client, mock_comments_data, mock_requests_success
):
    """
    Demonstra reutilização de fixtures para diferentes endpoints.
    IMPORTANTE: A mesma fixture mock_requests_success funciona para
    qualquer endpoint que use requests.get internamente.
    """
    # Configurar mock com dados de comentários
    mock_requests_success(mock_comments_data)

    # Requisição
    response = client.get("/posts/1/comments")

    # Verificações
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "test@example.com"


def test_deve_customizar_status_code_com_fixture(
    client, mock_posts_data, mock_requests_success
):
    """
    Demonstra como customizar status code usando fixture.
    IMPORTANTE: Mock permite controlar completamente a resposta simulada.
    Neste exemplo, mockamos a API externa retornando 200, então nosso
    endpoint FastAPI também retorna 200 com os dados mockados.
    """
    # Configurar mock com status 200 (sucesso)
    mock_requests_success(mock_posts_data, status_code=200)

    # Requisição ao nosso endpoint
    response = client.get("/posts")

    # Verificações - Dados vêm do mock, não da API real
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Post Mockado 1"


def test_deve_simular_erro_404_com_fixture(client, mock_requests_error):
    """
    Demonstra como simular erro 404 (não encontrado).
    IMPORTANTE: Mock permite testar como nossa aplicação se comporta
    quando a API externa retorna erros, sem precisar forçar erros reais.
    """
    # Configurar mock para retornar erro 404
    mock_requests_error(status_code=404)

    # Requisição para endpoint que busca post específico
    response = client.get("/posts/999")

    # Verificações - Nosso endpoint transforma 404 da API em 404 local
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()


def test_deve_simular_erro_500_com_fixture(client, mock_requests_error):
    """
    Demonstra como simular erro 500 (erro interno).
    IMPORTANTE: Podemos testar tratamento de erros sem depender de
    falhas reais da API externa.
    """
    # Configurar mock para retornar erro 500
    mock_requests_error(status_code=500)

    # Requisição
    response = client.get("/posts")

    # Verificações - Nosso endpoint detecta erro e retorna 500
    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_prova_que_mock_funciona(mocker, client, mock_comments_data):
    """
    Prova que o mock intercepta chamadas reais.
    IMPORTANTE: Este teste demonstra que podemos verificar se o mock
    foi chamado corretamente, provando que interceptou a requisição.
    """
    # Configurar mock
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_comments_data

    mock_get = mocker.patch("requests.get", return_value=mock_response)

    # Fazer requisição
    response = client.get("/posts/1/comments")

    # PROVA 1: Verifica que requests.get foi chamado (mas mockado)
    mock_get.assert_called_once()  # ✅ Passa - foi chamado

    # PROVA 2: Verifica que recebemos os dados mockados
    assert response.status_code == 200
    assert response.json() == mock_comments_data

    # PROVA 3: A URL tentada foi mockada (não fez requisição real)
    call_args = mock_get.call_args
    print(f"URL mockada: {call_args}")  # Mostra a URL que seria chamada
