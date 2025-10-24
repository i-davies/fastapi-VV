import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_deve_retornar_erro_500_ao_buscar_post(mocker, client):
    """Linha 39"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/posts/1")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_retornar_erro_500_ao_buscar_comentarios_do_post(mocker, client):
    """Linha 48"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/posts/1/comments")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_listar_usuarios(mocker, client):
    """Linha 55-58"""
    mock_users = [
        {"id": 1, "nome": "User 1", "email": "user1@email.com"},
        {"id": 2, "nome": "User 2", "email": "user2@email.com"},
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_users
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == mock_users
    assert len(response.json()) == 2


def test_deve_retornar_erro_500_ao_listar_usuarios(mocker, client):
    """Linha 57"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_retornar_usuario_por_id(mocker, client):
    """Linha 64-69"""
    mock_user = {
        "id": 1,
        "name": "User 1",
        "email": "user1@email.com",
        "username": "usuario1",
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_user
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == mock_user
    assert response.json()["name"] == "User 1"


def test_deve_retornar_erro_404_quando_usuario_nao_existe(mocker, client):
    """Linha 66"""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users/99999")

    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()


def test_deve_retornar_erro_500_ao_buscar_usuario(mocker, client):
    """Linha 68"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users/1")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_listar_posts_do_usuario(mocker, client):
    """Linha 75-78"""
    mock_posts = [
        {"id": 1, "userId": 1, "title": "Post 1", "body": "Content 1"},
        {"id": 2, "userId": 1, "title": "Post 2", "body": "Content 2"},
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_posts
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users/1/posts")

    assert response.status_code == 200
    assert response.json() == mock_posts
    assert len(response.json()) == 2


def test_deve_retornar_erro_500_ao_listar_posts_do_usuario(mocker, client):
    """Linha 77"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/users/1/posts")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_listar_comentarios(mocker, client):
    """Linha 84-88"""
    mock_coments = [
        {"id": i, "email": f"user{i}@example.com", "body": f"Comment {i}"}
        for i in range(1, 21)
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_coments
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/comments")

    assert response.status_code == 200
    assert len(response.json()) == 20


def test_deve_retornar_erro_500_ao_listar_comentarios(mocker, client):
    """Linha 86"""

    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/comments")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_retornar_todo_por_id(mocker, client):
    """Linha 94-99"""
    mock_todo = {
        "id": 1,
        "userId": 1,
        "title": "Buy groceries",
        "completed": False,
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_todo
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json() == mock_todo
    assert response.json()["title"] == "Buy groceries"


def test_deve_retornar_404_quando_todo_nao_existe(mocker, client):
    """Linha 94-95"""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/todos/99999")

    assert response.status_code == 404
    assert "não encontrad" in response.json()["detail"].lower()


def test_deve_retornar_erro_500_ao_buscar_todo(mocker, client):
    """Linha 98"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/todos/1")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_deve_listar_fotos_de_album(mocker, client):
    """
    Testa endpoint GET /albums/{album_id}/photos que lista fotos de um álbum.

    Cobre: Linhas 102-108 (get_album_photos - sucesso)
    """
    mock_photos = [
        {
            "id": i,
            "albumId": 1,
            "title": f"Photo {i}",
            "url": f"https://example.com/photo{i}.jpg",
        }
        for i in range(1, 11)
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_photos
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/albums/1/photos")

    assert response.status_code == 200
    assert len(response.json()) == 10  # limite padrão


def test_deve_listar_fotos_com_limite_customizado(mocker, client):
    """
    Testa endpoint GET /albums/{album_id}/photos com limit customizado.

    Cobre: Linhas 102-108 (get_album_photos - sucesso com limit)
    """
    mock_photos = [
        {
            "id": i,
            "albumId": 1,
            "title": f"Photo {i}",
            "url": f"https://example.com/photo{i}.jpg",
        }
        for i in range(1, 6)
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_photos
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/albums/1/photos?limit=5")

    assert response.status_code == 200
    assert len(response.json()) == 5


def test_deve_retornar_erro_500_ao_listar_fotos(mocker, client):
    """
    Testa tratamento de erro 500 no endpoint GET /albums/{album_id}/photos.

    Cobre: Linhas 105-106 (get_album_photos - erro 500)
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    response = client.get("/albums/1/photos")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()
