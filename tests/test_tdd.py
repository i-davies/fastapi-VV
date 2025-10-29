"""
Testes para funcionalidade de estatísticas de usuário
Desenvolvido com TDD (Test-Driven Development)

Casos de teste:
1. ✅ Usuário válido com posts e comentários
2. ❌ Usuário sem posts (404)
3. ❌ Erro na API externa (500)
4. ⚠️ Usuário com posts sem comentários
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste"""
    return TestClient(app)


@pytest.fixture
def mock_user_posts():
    """Mock de posts de um usuário"""
    return [
        {"id": 1, "userId": 1, "title": "Post 1", "body": "Conteúdo 1"},
        {"id": 2, "userId": 1, "title": "Post 2", "body": "Conteúdo 2"},
        {"id": 3, "userId": 1, "title": "Post 3", "body": "Conteúdo 3"},
    ]


@pytest.fixture
def mock_comments_per_post():
    """Mock de comentários por post"""
    return {
        1: [
            {"id": 1, "body": "Comentário 1"},
            {"id": 2, "body": "Comentário 2"},
        ],
        2: [{"id": 3, "body": "Comentário 3"}],
        3: [
            {"id": 4, "body": "Comentário 4"},
            {"id": 5, "body": "Comentário 5"},
            {"id": 6, "body": "Comentário 6"},
        ],
    }


# 🔴 TESTE 1: Caso de Sucesso
def test_deve_retornar_estatisticas_de_usuario_valido(
    mocker, client, mock_user_posts, mock_comments_per_post
):
    """
    Deve retornar estatísticas completas de um usuário válido

    Cenário:
    - Usuário com 3 posts
    - Post 1: 2 comentários
    - Post 2: 1 comentário
    - Post 3: 3 comentários
    - Média: 2.0 comentários/post
    - Mais comentado: Post 3
    """

    # Arrange: Configurar mocks
    def mock_get(url, *args, **kwargs):
        mock_response = mocker.Mock()
        mock_response.status_code = 200

        if "/users/1/posts" in url:
            mock_response.json.return_value = mock_user_posts
        elif "/posts/1/comments" in url:
            mock_response.json.return_value = mock_comments_per_post[1]
        elif "/posts/2/comments" in url:
            mock_response.json.return_value = mock_comments_per_post[2]
        elif "/posts/3/comments" in url:
            mock_response.json.return_value = mock_comments_per_post[3]

        return mock_response

    mocker.patch("requests.get", side_effect=mock_get)

    # Act: Chamar endpoint
    response = client.get("/users/1/stats")

    # Assert: Verificar resposta
    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == 1
    assert data["total_posts"] == 3
    assert data["average_comments_per_post"] == pytest.approx(2.0, rel=0.01)
    assert data["most_commented_post"]["id"] == 3
    assert data["most_commented_post"]["comments_count"] == 3
    assert "title" in data["most_commented_post"]


# 🔴 TESTE 2: Usuário Não Encontrado
def test_deve_retornar_404_quando_usuario_nao_existe(mocker, client):
    """
    Deve retornar 404 quando usuário não existe ou não tem posts

    Cenário: API retorna lista vazia de posts
    """
    # Arrange: Mock retornando lista vazia
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mocker.patch("requests.get", return_value=mock_response)

    # Act
    response = client.get("/users/9999/stats")

    # Assert
    assert response.status_code == 404
    assert "não possui posts" in response.json()["detail"].lower()


# 🔴 TESTE 3: Erro na API Externa
def test_deve_retornar_500_quando_api_externa_falha(mocker, client):
    """
    Deve retornar 500 quando API externa está indisponível

    Cenário: API retorna status 500
    """
    # Arrange: Mock de erro
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    # Act
    response = client.get("/users/1/stats")

    # Assert
    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


# 🔴 TESTE 4: Usuário sem Comentários
def test_deve_calcular_media_zero_quando_nao_ha_comentarios(mocker, client):
    """
    Deve retornar média 0 quando posts não têm comentários

    Cenário: Usuário com 1 post sem comentários
    """
    # Arrange: Posts sem comentários
    mock_posts = [
        {"id": 1, "userId": 1, "title": "Post Solitário", "body": "Conteúdo"}
    ]

    def mock_get(url, *args, **kwargs):
        mock_response = mocker.Mock()
        mock_response.status_code = 200

        if "/users/1/posts" in url:
            mock_response.json.return_value = mock_posts
        elif "/comments" in url:
            mock_response.json.return_value = []

        return mock_response

    mocker.patch("requests.get", side_effect=mock_get)

    # Act
    response = client.get("/users/1/stats")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["total_posts"] == 1
    assert data["average_comments_per_post"] == 0.0
    assert data["most_commented_post"]["comments_count"] == 0


# 🔴 TESTE 5: Múltiplos Usuários
def test_deve_retornar_estatisticas_diferentes_para_usuarios_diferentes(
    mocker, client
):
    """
    Deve retornar estatísticas específicas para cada usuário

    Cenário: Dois usuários com quantidades diferentes de posts
    """
    # Arrange: Mock para usuário 1
    mock_posts_user1 = [
        {"id": 1, "userId": 1, "title": "Post User 1", "body": "X"}
    ]

    # Mock para usuário 2
    mock_posts_user2 = [
        {"id": 10, "userId": 2, "title": "Post User 2 - A", "body": "Y"},
        {"id": 11, "userId": 2, "title": "Post User 2 - B", "body": "Z"},
    ]

    def mock_get(url, *args, **kwargs):
        mock_response = mocker.Mock()
        mock_response.status_code = 200

        if "/users/1/posts" in url:
            mock_response.json.return_value = mock_posts_user1
        elif "/users/2/posts" in url:
            mock_response.json.return_value = mock_posts_user2
        elif "/comments" in url:
            mock_response.json.return_value = []

        return mock_response

    mocker.patch("requests.get", side_effect=mock_get)

    # Act: Buscar estatísticas de dois usuários
    response1 = client.get("/users/1/stats")
    response2 = client.get("/users/2/stats")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    assert data1["user_id"] == 1
    assert data1["total_posts"] == 1

    assert data2["user_id"] == 2
    assert data2["total_posts"] == 2
