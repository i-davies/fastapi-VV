# Teste com Pytest (Fixtures)

"""
Fixtures são funções que rodam antes dos testes para configurar o ambiente.
Usamos fixtures para:
- Criar clientes de teste reutilizáveis
- Preparar dados de teste
- Configurar e limpar recursos
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


# Fixture - cliente basico
@pytest.fixture
def client():
    """
    Fixture que cria o client de teste do Fastapi
    """
    return TestClient(app)


@pytest.fixture
def exemplo_post_id():
    """
    Fixture que retorna ID válido
    """
    return 1


@pytest.fixture(params=[1, 2, 3])
def post_ids_multiplos(request):
    """
    Fixture parametrizada - Executa teste para cada valor
    """
    return request.param


@pytest.fixture
def post_completo(client, exemplo_post_id):
    """
    Fixture que depende de outra fixture
    busca um post completo
    """
    response = client.get(f"/post/{exemplo_post_id}")
    return response.json()


@pytest.fixture(autouse=True)
def limpa_cache():
    """
    Fixture com autouse=True - Executa automaticamente
    """
    yield


# Teste usando fixture
def test_deve_retornar_mensagem_no_endpoint_raiz(client):
    """
    Deve retornar status 200 e mensagem no endpoint raiz
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_deve_listar_posts_com_limite_padrao(client):
    """
    Deve listar no máximo 10 posts
    """
    response = client.get("/posts")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) <= 10
    assert isinstance(posts, list)


def test_deve_listar_posts_com_limite_customizado(client):
    """
    Deve retornar quantidade exata de posts
    """
    response = client.get("/posts?limit=5")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 5
    assert isinstance(posts, list)


def test_deve_retornar_posts_por_id(client, exemplo_post_id):
    """
    Deve retornar post completo por ID
    """
    response = client.get(f"/posts/{exemplo_post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == exemplo_post_id
    assert "title" in post
    assert "body" in post


def test_deve_retornar_404_quando_post_nao_existe(client):
    """
    Deve retornar status 404
    """
    response = client.get("/posts/99999")
    assert response.status_code == 404


def test_deve_retornar_comentarios_do_post(client, exemplo_post_id):
    """
    Deve retornar lista de comentários de um post
    """
    response = client.get(f"/posts/{exemplo_post_id}/comments")
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0
    assert "email" in comments[0]
    assert "body" in comments[0]


def test_deve_usar_post_ids_parametrizados(client, post_ids_multiplos):
    """
    Demonstra fixture parametrizada - executa 3 vezes
    """
    response = client.get(f"/posts/{post_ids_multiplos}")
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == post_ids_multiplos


@pytest.mark.parametrize(
    "post_id, status_esperado",
    [
        (1, 200),  # ID válido
        (2, 200),  # ID válido
        (999999, 404),  # ID inválido
        ("abc", 422),  # String (erro de validação)
    ],
)
def test_post_com_status_esperado(client, post_id, status_esperado):
    """
    Teste Parametrizado
    """
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == status_esperado
