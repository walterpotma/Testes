# Aplicações de teste Hexon

Cada pasta é uma aplicação independente. Na Hexon, selecione a pasta correspondente como contexto de build e use seu `Dockerfile`.

| Pasta | Aplicação | Porta do container | Configuração |
| --- | --- | --- | --- |
| `html` | Site HTML original | 80 | Nenhuma |
| `vite` | Vite com JavaScript | 80 | Build estático com Node 24 |
| `python` | HTTP Python, sem dependências | 8080 | Volume montado em `/mnt/hexon-data` |
| `dotnet` | ASP.NET Core 10 | 8080 | Variável `HEXON_MESSAGE` |

## Execução local

Execute cada comando a partir da pasta da aplicação:

- HTML: `python3 -m http.server 8000 --directory public`
- Vite: `npm ci && npm run dev -- --port 5173` (produção: `npm run build`)
- Python: `python3 app.py` (variáveis opcionais: `PORT` e `VOLUME_PATH`)
- .NET: `HEXON_MESSAGE="Olá Hexon" dotnet run --urls http://0.0.0.0:8081` (requer SDK .NET 10)

## Volume da aplicação Python

Crie/conecte um volume persistente na Hexon/Kubernetes e monte-o em `/mnt/hexon-data`, ou defina `VOLUME_PATH` para outro caminho de montagem. Essa pasta não existe no repositório e a aplicação não a cria. Ela apenas lista os nomes dos arquivos no volume, sem ler ou alterar seus conteúdos.

`GET /` retorna JSON com `mounted: true` e os arquivos quando a pasta está acessível; retorna HTTP 503 com `mounted: false` quando está ausente ou inacessível. `GET /health` retorna HTTP 200 para testar o processo, independentemente do volume. Uma pasta acessível não prova por si só que o Kubernetes montou um PVC.

## Variável da aplicação .NET

Defina `HEXON_MESSAGE` com um texto de teste na Hexon. `GET /` mostra o valor e `configured: true`; sem a variável, mostra `configured: false`. Use apenas texto não confidencial, pois o valor aparece na resposta HTTP. `GET /health` retorna HTTP 200.
