# Instruções para Code Review - Projeto FastAPI QTS

Este documento contém diretrizes simples para realizar code reviews neste repositório. O objetivo é garantir qualidade, segurança e manutenibilidade do código FastAPI.

## 1. **Verificação de Qualidade de Código**
- **Formatação**: O código deve seguir PEP 8. Execute `black .` e `flake8 .` para verificar.
- **Comentários**: Adicione comentários claros em funções complexas ou lógicas não óbvias.
- **Nomes**: Use nomes descritivos para variáveis, funções e endpoints (ex.: `read_user` em vez de `get_u`).

## 2. **Funcionalidade e Testes**
- **Testes**: Certifique-se de que novos endpoints têm testes correspondentes em `tests/test_main.py`.
- **Cobertura**: Execute `pytest` para verificar se todos os testes passam.
- **Funcionalidade**: Teste manualmente os endpoints para garantir que retornam os dados esperados.

## 3. **Segurança**
- **Vulnerabilidades**: Verifique por SQL injection, XSS ou outros riscos. Evite concatenar strings em queries SQL.
- **Validação**: Use Pydantic para validar entradas de usuários.
- **Dependências**: Não adicione bibliotecas desnecessárias; verifique por vulnerabilidades conhecidas.

## 4. **Estrutura e Boas Práticas**
- **Endpoints**: Mantenha endpoints simples e focados em uma responsabilidade.
- **Erros**: Trate exceções adequadamente (ex.: divisão por zero, tipos inválidos).
- **Duplicação**: Evite código duplicado; refatore se necessário.

## 5. **Checklist Rápido para Review**
- [ ] Código formatado com Black?
- [ ] Sem erros no Flake8?
- [ ] Testes passando?
- [ ] Segurança verificada?
- [ ] Documentação atualizada (se aplicável)?

Essas instruções ajudam a manter o código limpo e funcional. Para dúvidas, consulte o README.md do projeto.