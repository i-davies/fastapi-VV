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
