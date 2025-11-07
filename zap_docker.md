## Pré‑requisitos
- Docker Desktop instalado e em execução
- Seu servidor FastAPI rodando localmente (uvicorn)
- Porta 8000 exposta (http://localhost:8000)

---


## 1 Baixar a imagem do ZAP Proxy

```powershell
docker pull zaproxy/zap-stable
```
## 2 Baseline Scan (rápido, seguro)
O baseline faz um spider e checagens passivas (sem ataques intrusivos). Gera um relatório HTML.

```powershell
# Salva o relatório na pasta atual (mapeada para /zap/wrk)
docker run --rm -t `
  -v "${PWD}:/zap/wrk" `
  zaproxy/zap-stable zap-baseline.py `
  -t http://host.docker.internal:8000 `
  -r zap_baseline.html `
  -l WARN
```

- -v "${PWD}:/zap/wrk": monta a pasta atual no container
- -t: alvo (use host.docker.internal:8000)
- -r: arquivo de relatório HTML
- -l WARN: falha somente em achados WARN/FAIL (ajuste conforme necessidade)

Resultado: um arquivo zap_baseline.html será criado no diretório do projeto.

---

## 3 Full Scan (mais agressivo)
Faz ataques ativos. Use apenas em ambientes controlados (como sua máquina local de aulas).

```powershell
docker run --rm -t `
  -v "${PWD}:/zap/wrk" `
  zaproxy/zap-stable zap-full-scan.py `
  -t http://host.docker.internal:8000 `
  -r zap_full.html `
  -m 10 `
  -l WARN
```

- -m 10: limita o tempo de ataques ativos (minutos)
- -l WARN: nível mínimo para marcar falha

Resultado: zap_full.html com achados detalhados.

---

## 4 API Scan via OpenAPI (recomendado para APIs)
Importa seu contrato OpenAPI e gera requisições a partir dele (perfeito para FastAPI).

```powershell
docker run --rm -t `
  -v "${PWD}:/zap/wrk" `
  zaproxy/zap-stable zap-api-scan.py `
  -t http://host.docker.internal:8000/openapi.json `
  -f openapi `
  -r zap_api.html `
  -l WARN
```

- -t: URL do contrato OpenAPI exposto pelo FastAPI
- -f openapi: formato do contrato

Resultado: zap_api.html com issues específicas para endpoints do contrato.

---

