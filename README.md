# Template de Requisição à API do GestãoClick

Este diretório contém um **exemplo mínimo e independente** de como fazer uma requisição à API GestãoClick,
pensado para que qualquer pessoa que acesse o repositório no GitHub consiga testar rapidamente
(desde que tenha credenciais válidas da API).

## Resumo rápido (para quem tem pressa)

- **1. Configurar credenciais**: copiar `.env.example` para `.env` e preencher `ACCESS_TOKEN` e `SECRET_ACCESS_TOKEN`.
- **2. Instalar dependências**: `pip install -r requirements.txt`.
- **3. Chamada mais comum (produtos ativos)**:

  ```bash
  python main.py -e /produtos -p pagina=1 -p ativo=1
  ```

- **4. Chamada de exemplo para vendas em um período**:

  ```bash
  python main.py -e /vendas -p data_inicio=2025-01-01 -p data_fim=2025-01-31
  ```

Depois, leia as seções abaixo para entender os detalhes.

## Estrutura

- `main.py` — script principal que faz requisições para a API, permitindo:
  - escolher o **endpoint** (`/produtos`, `/vendas`, etc.);
  - passar **parâmetros de filtro** pela linha de comando.
- `.env.example` — modelo de variáveis de ambiente necessárias para autenticação.
- `requirements.txt` — dependências Python mínimas para executar o exemplo.
- `.gitignore` — garante que o arquivo `.env` com credenciais não seja versionado.

## Pré-requisitos

- Python 3.10+ instalado.
- Credenciais válidas da API GestãoClick:
  - `ACCESS_TOKEN`
  - `SECRET_ACCESS_TOKEN`

## Como configurar e executar

1. **Clonar o repositório** (ou garantir que você está na pasta correta):

   ```bash
   cd "05 - MIDIA BRINDES/api_midiabrindes_example"
   ```

2. **Criar e ativar um ambiente virtual (opcional, mas recomendado)**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instalar as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar as variáveis de ambiente**:

   - Copie o arquivo `.env.example` para `.env`:

     ```bash
     copy .env.example .env
     ```

   - Edite o arquivo `.env` e preencha com os valores reais de:
     - `ACCESS_TOKEN`
     - `SECRET_ACCESS_TOKEN`
     - (opcional) `GESTA_CLICK_BASE_URL` se sua URL base for diferente.

5. **Executar o exemplo (modo padrão)**:

   Sem passar nada, ele usa o endpoint `/produtos` sem filtros:

   ```bash
   python main.py
   ```

   Se tudo estiver configurado corretamente, o script irá:

   - Fazer uma requisição GET para o endpoint `/produtos`;
   - Exibir no terminal quantos registros foram retornados na página;
   - Mostrar alguns campos do primeiro item retornado.

## Mudando o endpoint

- **Endpoint padrão**: `/produtos`
- Para mudar, use a flag `--endpoint` (ou `-e`):

```bash
python main.py --endpoint /vendas
```

Ou, sem a barra inicial (o script adiciona automaticamente):

```bash
python main.py --endpoint vendas
```

## Passando parâmetros de filtro

Você pode passar parâmetros na URL usando a flag `--param` (ou `-p`)
no formato `chave=valor`. Pode repetir a flag várias vezes.

Exemplos:

- **Página e flag de ativo**:

  ```bash
  python main.py -e /produtos -p pagina=1 -p ativo=1
  ```

- **Filtros para vendas (exemplo ilustrativo)**:

  ```bash
  python main.py -e /vendas -p data_inicio=2025-01-01 -p data_fim=2025-01-31
  ```

Regras importantes:

- O formato deve ser exatamente `chave=valor`;
- Espaços em volta de `=` são ignorados;
- Parâmetros com formato inválido são ignorados e um aviso é exibido no log.

Os nomes de parâmetros aceitos (ex.: `pagina`, `ativo`, `data_inicio`, `data_fim`, etc.)
dependem da **documentação oficial da API GestãoClick**.

Assim, este diretório serve como **modelo claro e isolado** para que outros desenvolvedores
possam entender rapidamente:

- como autenticar na API (via `.env`);
- como escolher o endpoint na linha de comando;
- como testar filtros rapidamente passando parâmetros pelo terminal.


