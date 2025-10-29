"""
TDD - Test-Driven Development - Desenvolvimento Orientado a Testes

- Melhor design de código
- Cobertura alta desde o início
- Refatoração segura
- Documentação viva

Ciclo do TDD

- Teste falha
- Teste passa
- Melhora

Requisitos da funcionalidade
"Como usuário da API, quero obter estatísticas de um usuário específico
(quantidade de posts, comentários médios por post, e post mais comentado)
 para ter insights sobre sua atividade."

 Endpoint: GET /users/{user_id}/stats

 {
  "user_id": 1,
  "total_posts": 10,
  "average_comments_per_post": 5.2,
  "most_commented_post": {
    "id": 5,
    "title": "Post com mais comentários",
    "comments_count": 15
  }
}

Casos de Uso:
1. Retornar estatisticas do usuário válido
2. Retornar 404 se usuário não existe
3. Retornar 500 se API externa falhar
4. Lidar com usuários sem comentários
"""
