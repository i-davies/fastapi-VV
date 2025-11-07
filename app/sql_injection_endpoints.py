"""
Endpoints de SQL Injection
Aula: Testando Vulnerabilidades - SQL Injection
"""

import sqlite3
import time
from fastapi import APIRouter

router = APIRouter()

# Caminho do banco de dados
DB_PATH = "database.db"


def get_db_connection():
    """Cria conexão com o banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =============================================================================
# EXEMPLO 1: SQL Injection - Error-Based (VULNERÁVEL)
# =============================================================================


@router.get("/users/search-vulnerable")
def search_users_vulnerable(username: str):
    """
    VULNERÁVEL - SQL Injection (Error-Based)

    Explora mensagens de erro do banco para extrair informações sobre a
    estrutura do banco de dados


    Problema: Concatena diretamente o input do usuário na query

    Ataques possíveis:
    - username=' OR '1'='1
    - username=' OR '1'='1' --
    - username=admin' --
    - username=' UNION SELECT null, username, password, email,
      null, null FROM users --
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERÁVEL: Concatenação de string
    query = f"SELECT * FROM users WHERE username = '{username}'"

    try:
        cursor.execute(query)
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return {
            "aviso": "ENDPOINT VULNERÁVEL - apenas para demonstração",
            "query_executada": query,
            "total": len(users),
            "users": users,
        }
    except Exception as e:
        conn.close()
        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "erro": str(e),
            "query_executada": query,
        }


@router.get("/users/search-secure")
def search_users_secure(username: str):
    """
    SEGURO - Usa Prepared Statement (Parameterized Query)

    Proteção: Usa placeholders (?) que impedem SQL Injection

    Mesmo testando ataques, não funciona:
    - username=' OR '1'='1
    - username=admin' --
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # SEGURO: Prepared statement com placeholder
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    users = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "tipo": "SEGURO - Prepared Statement",
        "query": query,
        "parametros": [username],
        "total": len(users),
        "users": users,
    }


# =============================================================================
# EXEMPLO 2: SQL Injection - Union-Based (VULNERÁVEL)
# =============================================================================


@router.get("/products/search-vulnerable")
def search_products_vulnerable(category: str):
    """
    VULNERÁVEL - SQL Injection Union-Based

    Permite extrair dados de outras tabelas

    Ataques possíveis:
    - category=' UNION SELECT id, username, password, email,
      null, null FROM users --
    - category=' UNION SELECT id, username, email, role,
      null, null FROM users WHERE role='admin' --
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERÁVEL
    query = f"SELECT * FROM products WHERE category = '{category}'"

    try:
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "query_executada": query,
            "total": len(results),
            "results": results,
        }
    except Exception as e:
        conn.close()
        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "erro": str(e),
            "query_executada": query,
        }


@router.get("/products/search-secure")
def search_products_secure(category: str):
    """
    SEGURO - Union-Based não funciona com prepared statements
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE category = ?"
    cursor.execute(query, (category,))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"tipo": "SEGURO", "total": len(results), "products": results}


# =============================================================================
# EXEMPLO 3: SQL Injection - Boolean-Based Blind (VULNERÁVEL)
# =============================================================================


@router.get("/products/check-vulnerable")
def check_product_vulnerable(product_id: str):
    """
    VULNERÁVEL - Boolean-Based Blind SQL Injection

    Aceita string ao invés de int (simulando API sem validação)
    Retorna apenas True/False, atacante deduz informações

    Ataques:
    - product_id=1 AND 1=1  (retorna True)
    - product_id=1 AND 1=2  (retorna False)
    - product_id=1 AND (SELECT COUNT(*) FROM users) > 0
      (testa se tabela existe)
    - product_id=1 AND (SELECT LENGTH(password) FROM users WHERE id=1) > 5
      (descobre tamanho da senha)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERÁVEL - usa string diretamente sem validação
    query = f"SELECT COUNT(*) as count FROM products WHERE id = {product_id}"

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        exists = result["count"] > 0

        return {
            "aviso": "ENDPOINT VULNERÁVEL - aceita string sem validação",
            "query_executada": query,
            "produto_existe": exists,
        }
    except Exception as e:
        conn.close()
        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "erro": str(e),
            "query_executada": query,
        }


@router.get("/products/check-secure")
def check_product_secure(product_id: int):
    """
    SEGURO - Boolean-Based blind não funciona
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) as count FROM products WHERE id = ?"
    cursor.execute(query, (product_id,))

    result = cursor.fetchone()
    conn.close()

    exists = result["count"] > 0

    return {"tipo": "SEGURO", "produto_existe": exists}


# =============================================================================
# EXEMPLO 4: SQL Injection - Time-Based Blind (VULNERÁVEL)
# =============================================================================


@router.get("/users/check-vulnerable")
def check_user_vulnerable(user_id: str):
    """
    VULNERÁVEL - Time-Based Blind SQL Injection

    Aceita string ao invés de int (simulando API sem validação)
    Usa delays para deduzir informações

    Ataques (SQLite usa diferentes funções):
    - user_id=1 AND (SELECT CASE WHEN (1=1) THEN 1
      ELSE (SELECT 1 UNION SELECT 2) END)
    - user_id=1 AND (SELECT COUNT(*) FROM users WHERE username='admin') > 0

    Nota: SQLite não tem SLEEP(), mas é possível usar queries pesadas
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERÁVEL - usa string diretamente sem validação
    query = f"SELECT COUNT(*) as count FROM users WHERE id = {user_id}"

    start_time = time.time()

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        elapsed = time.time() - start_time

        return {
            "aviso": "ENDPOINT VULNERÁVEL - aceita string sem validação",
            "query_executada": query,
            "usuario_existe": result["count"] > 0,
            "tempo_resposta": f"{elapsed:.3f}s",
        }
    except Exception as e:
        conn.close()
        elapsed = time.time() - start_time

        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "erro": str(e),
            "query_executada": query,
            "tempo_resposta": f"{elapsed:.3f}s",
        }


@router.get("/users/check-secure")
def check_user_secure(user_id: int):
    """
    SEGURO - Time-Based blind não funciona
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    start_time = time.time()

    query = "SELECT COUNT(*) as count FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()
    conn.close()

    elapsed = time.time() - start_time

    return {
        "tipo": "SEGURO",
        "usuario_existe": result["count"] > 0,
        "tempo_resposta": f"{elapsed:.3f}s",
    }


# =============================================================================
# EXEMPLO 5: Login Vulnerável vs Seguro
# =============================================================================


@router.get("/auth/login-vulnerable")
def login_vulnerable(username: str, password: str):
    """
    VULNERÁVEL - Bypass de autenticação

    Ataques clássicos:
    - username=admin' --&password=qualquer
    - username=' OR '1'='1' --&password=
    - username=admin' OR '1'='1&password=admin' OR '1'='1
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERÁVEL
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                "aviso": "ENDPOINT VULNERÁVEL",
                "query_executada": query,
                "sucesso": True,
                "mensagem": "Login realizado",
                "usuario": dict(user),
            }
        else:
            return {
                "aviso": "ENDPOINT VULNERÁVEL",
                "query_executada": query,
                "sucesso": False,
                "mensagem": "Credenciais inválidas",
            }
    except Exception as e:
        conn.close()
        return {
            "aviso": "ENDPOINT VULNERÁVEL",
            "erro": str(e),
            "query_executada": query,
        }


@router.get("/auth/login-secure")
def login_secure(username: str, password: str):
    """
    SEGURO - Prepared statement + hash de senha (simulado)

    Nota: Em produção, use bcrypt ou argon2 para senhas
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        user_dict = dict(user)
        # Remover senha da resposta
        user_dict.pop("password", None)

        return {
            "tipo": "SEGURO",
            "sucesso": True,
            "mensagem": "Login realizado",
            "usuario": user_dict,
        }
    else:
        return {
            "tipo": "SEGURO",
            "sucesso": False,
            "mensagem": "Credenciais inválidas",
        }
