# Endpoints para testes com mocking e fixtures
# API externa: JSONPlaceholder (https://jsonplaceholder.typicode.com)

from fastapi import FastAPI, HTTPException
import requests

from app.sql_injection_endpoints import router as sql_injection_router

app = FastAPI()

# Registrar rotas de SQL Injection
app.include_router(sql_injection_router, tags=["SQL Injection"])

# URL base da API externa
BASE_URL = "https://jsonplaceholder.typicode.com"


# ENDPOINTS


@app.get("/")
def root():
    """Endpoint raiz"""
    return {"message": "Endpoints para testes com mocking e fixtures"}


@app.get("/posts")
def get_posts(limit: int = 10):
    """Lista posts (com limite opcional)"""
    response = requests.get(f"{BASE_URL}/posts")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    posts = response.json()
    return posts[:limit]


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """Obtém um post específico por ID"""
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/posts/{post_id}/comments")
def get_post_comments(post_id: int):
    """Obtém comentários de um post específico"""
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/users")
def get_users():
    """Lista todos os usuários"""
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Obtém um usuário específico por ID"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    """Obtém todos os posts de um usuário específico"""
    response = requests.get(f"{BASE_URL}/users/{user_id}/posts")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/comments")
def get_comments(limit: int = 20):
    """Lista comentários (com limite opcional)"""
    response = requests.get(f"{BASE_URL}/comments")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    comments = response.json()
    return comments[:limit]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """Obtém uma tarefa específica por ID"""
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.get("/albums/{album_id}/photos")
def get_album_photos(album_id: int, limit: int = 10):
    """Obtém fotos de um álbum específico"""
    response = requests.get(f"{BASE_URL}/albums/{album_id}/photos")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    photos = response.json()
    return photos[:limit]


@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: int):
    """
    Obtém estatísticas de atividade de um usuário:
    - Total de posts
    - Média de comentários por post
    - Post mais comentado
    """
    # 1. Buscar posts do usuário
    response = requests.get(f"{BASE_URL}/users/{user_id}/posts")

    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Erro ao buscar posts do usuário"
        )

    posts = response.json()

    # 2. Verificar se usuário tem posts
    if not posts:
        raise HTTPException(
            status_code=404, detail=f"Usuário {user_id} não possui posts"
        )

    # 3. Buscar comentários de cada post
    total_comments = 0
    post_comments_count = {}

    for post in posts:
        post_id = post["id"]
        comments_response = requests.get(
            f"{BASE_URL}/posts/{post_id}/comments"
        )

        if comments_response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Erro ao buscar comentários"
            )

        comments = comments_response.json()
        comments_count = len(comments)

        total_comments += comments_count
        post_comments_count[post_id] = {
            "count": comments_count,
            "title": post["title"],
        }

    # 4. Calcular estatísticas
    total_posts = len(posts)
    average_comments = total_comments / total_posts if total_posts > 0 else 0.0

    # 5. Encontrar post mais comentado
    most_commented = max(
        post_comments_count.items(),
        key=lambda x: x[1]["count"],
        default=(None, None),
    )

    most_commented_post = {
        "id": most_commented[0] if most_commented[0] else None,
        "title": most_commented[1]["title"] if most_commented[1] else "",
        "comments_count": (
            most_commented[1]["count"] if most_commented[1] else 0
        ),
    }

    # 6. Retornar estatísticas
    return {
        "user_id": user_id,
        "total_posts": total_posts,
        "average_comments_per_post": round(average_comments, 2),
        "most_commented_post": most_commented_post,
    }
