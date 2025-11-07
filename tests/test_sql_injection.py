"""
Testes para SQL Injection - Endpoints Seguros
Aula: Testando Vulnerabilidades - SQL Injection

Estes testes verificam que os endpoints seguros BLOQUEIAM ataques SQL Injection
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# TESTES: Error-Based SQL Injection - Endpoint Seguro


def test_search_users_secure_blocks_or_injection():
    """Verifica que OR 1=1 é bloqueado"""
    # Ataque: ' OR '1'='1
    response = client.get("/users/search-secure?username=' OR '1'='1")

    assert response.status_code == 200
    data = response.json()

    # Não deve encontrar usuários (ataque bloqueado)
    assert data["total"] == 0
    assert len(data["users"]) == 0


def test_search_users_secure_blocks_comment_injection():
    """Verifica que comentário SQL é bloqueado"""
    # Ataque: admin' --
    response = client.get("/users/search-secure?username=admin' --")

    assert response.status_code == 200
    data = response.json()

    # Não deve encontrar usuário (ataque bloqueado)
    assert data["total"] == 0


def test_search_users_secure_valid_username():
    """Verifica que busca legítima funciona"""
    response = client.get("/users/search-secure?username=admin")

    assert response.status_code == 200
    data = response.json()

    # Deve encontrar apenas o admin
    assert data["total"] == 1
    assert data["users"][0]["username"] == "admin"


# TESTES: Union-Based SQL Injection - Endpoint Seguro


def test_search_products_secure_blocks_union_injection():
    """Verifica que UNION SELECT é bloqueado"""
    # Ataque: extração de senhas via UNION
    payload = "' UNION SELECT id, username, password, email, null, null FROM users --"
    response = client.get(f"/products/search-secure?category={payload}")

    assert response.status_code == 200
    data = response.json()

    # Não deve encontrar produtos (ataque bloqueado)
    assert data["total"] == 0


def test_search_products_secure_valid_category():
    """Verifica que busca legítima funciona"""
    response = client.get("/products/search-secure?category=Eletrônicos")

    assert response.status_code == 200
    data = response.json()

    # Deve retornar produtos da categoria
    assert data["total"] > 0
    assert "products" in data


# TESTES: Boolean-Based Blind SQL Injection - Endpoint Seguro


def test_check_product_secure_validates_type():
    """Verifica que endpoint seguro valida tipo (aceita apenas int)"""
    response = client.get("/products/check-secure?product_id=1")

    assert response.status_code == 200
    data = response.json()

    # Deve funcionar normalmente com ID válido
    assert "produto_existe" in data


def test_check_product_secure_valid_id():
    """Verifica que busca legítima funciona"""
    response = client.get("/products/check-secure?product_id=1")

    assert response.status_code == 200
    data = response.json()

    # Produto com ID 1 deve existir
    assert data["produto_existe"] is True


def test_check_product_secure_nonexistent_id():
    """Verifica que ID inexistente retorna False corretamente"""
    response = client.get("/products/check-secure?product_id=999")

    assert response.status_code == 200
    data = response.json()

    # Produto inexistente deve retornar False
    assert data["produto_existe"] is False


# TESTES: Time-Based Blind SQL Injection - Endpoint Seguro


def test_check_user_secure_validates_type():
    """Verifica que endpoint seguro valida tipo (aceita apenas int)"""
    response = client.get("/users/check-secure?user_id=1")

    assert response.status_code == 200
    data = response.json()

    # Deve funcionar normalmente com ID válido
    assert data["usuario_existe"] is True
    assert "tempo_resposta" in data


def test_check_user_secure_valid_id():
    """Verifica que busca legítima funciona"""
    response = client.get("/users/check-secure?user_id=1")

    assert response.status_code == 200
    data = response.json()

    # Usuário com ID 1 deve existir
    assert data["usuario_existe"] is True


def test_check_user_secure_nonexistent_id():
    """Verifica que ID inexistente retorna False corretamente"""
    response = client.get("/users/check-secure?user_id=999")

    assert response.status_code == 200
    data = response.json()

    # Usuário inexistente deve retornar False
    assert data["usuario_existe"] is False


# TESTES: Login Bypass - Endpoint Seguro


def test_login_secure_blocks_comment_bypass():
    """Verifica que bypass com comentário SQL é bloqueado"""
    # Ataque: admin' --
    response = client.get(
        "/auth/login-secure?username=admin' --&password=qualquer"
    )

    assert response.status_code == 200
    data = response.json()

    # Login deve falhar (ataque bloqueado)
    assert data["sucesso"] is False


def test_login_secure_blocks_or_bypass():
    """Verifica que bypass com OR 1=1 é bloqueado"""
    # Ataque: ' OR '1'='1' --
    response = client.get(
        "/auth/login-secure?username=' OR '1'='1' --&password="
    )

    assert response.status_code == 200
    data = response.json()

    # Login deve falhar (ataque bloqueado)
    assert data["sucesso"] is False


def test_login_secure_valid_credentials():
    """Verifica que login legítimo funciona"""
    response = client.get(
        "/auth/login-secure?username=admin&password=admin123"
    )

    assert response.status_code == 200
    data = response.json()

    # Login deve ter sucesso
    assert data["sucesso"] is True
    assert data["usuario"]["username"] == "admin"
    # Senha não deve estar na resposta (segurança adicional)
    assert "password" not in data["usuario"]


def test_login_secure_invalid_credentials():
    """Verifica que credenciais inválidas são rejeitadas"""
    response = client.get(
        "/auth/login-secure?username=admin&password=senha_errada"
    )

    assert response.status_code == 200
    data = response.json()

    # Login deve falhar
    assert data["sucesso"] is False


def test_login_secure_nonexistent_user():
    """Verifica que usuário inexistente é rejeitado"""
    response = client.get(
        "/auth/login-secure?username=usuario_fake&password=qualquer"
    )

    assert response.status_code == 200
    data = response.json()

    # Login deve falhar
    assert data["sucesso"] is False
