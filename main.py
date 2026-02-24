"""Exemplo simples de requisição à API GestãoClick.

Este script foi feito para ser o mais simples e claro possível.

Ele permite que você:
- escolha **qual endpoint** chamar (ex.: `/produtos`, `/vendas`, etc.);
- informe **parâmetros de filtro** pela linha de comando (ex.: `pagina=1`, `ativo=1`).
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any, Optional, List

import requests
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_config() -> Dict[str, str]:
    """Lê as variáveis de ambiente necessárias da API."""
    load_dotenv()

    base_url = os.getenv("GESTA_CLICK_BASE_URL", "https://api.gestaoclick.com")
    access_token = os.getenv("ACCESS_TOKEN")
    secret_access_token = os.getenv("SECRET_ACCESS_TOKEN")

    if not access_token:
        raise ValueError("ACCESS_TOKEN não configurado. Defina no arquivo .env")
    if not secret_access_token:
        raise ValueError("SECRET_ACCESS_TOKEN não configurado. Defina no arquivo .env")

    return {
        "base_url": base_url.rstrip("/"),
        "access_token": access_token,
        "secret_access_token": secret_access_token,
    }


def parse_params(param_list: Optional[List[str]]) -> Dict[str, Any]:
    """Converte uma lista do tipo ['chave=valor', ...] em dict."""
    if not param_list:
        return {}

    params: Dict[str, Any] = {}
    for raw in param_list:
        if "=" not in raw:
            logger.warning("Parâmetro ignorado (formato esperado chave=valor): %s", raw)
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            logger.warning("Parâmetro ignorado (chave vazia): %s", raw)
            continue
        params[key] = value
    return params


def make_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> None:
    """Executa uma requisição para o endpoint informado."""
    cfg = get_config()

    endpoint = endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    url = f"{cfg['base_url']}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "access-token": cfg["access_token"],
        "secret-access-token": cfg["secret_access_token"],
    }

    logger.info("Enviando requisição para %s", url)
    if params:
        logger.info("Com parâmetros: %s", params)

    response = requests.get(url, headers=headers, params=params, timeout=30, verify=False)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error("Erro HTTP na requisição: %s", e)
        logger.error("Corpo da resposta: %s", response.text)
        raise

    data = response.json()

    # A estrutura real pode mudar; aqui assumimos o formato padrão da API
    items = data.get("data", [])
    logger.info("Requisição concluída com sucesso.")
    logger.info("Total de registros retornados nesta página: %d", len(items))

    if items:
        primeiro = items[0]
        logger.info("Exemplo do primeiro item retornado:")
        for chave in list(primeiro.keys())[:10]:
            logger.info("  %s: %r", chave, primeiro[chave])
    else:
        logger.info("Nenhum registro retornado.")


def build_arg_parser() -> argparse.ArgumentParser:
    """Define os argumentos de linha de comando disponíveis."""
    parser = argparse.ArgumentParser(
        description=(
            "Exemplo de chamada à API GestãoClick.\n\n"
            "Por padrão usa o endpoint '/produtos'. "
            "Você pode trocar o endpoint e passar filtros."
        )
    )

    parser.add_argument(
        "--endpoint",
        "-e",
        default="/produtos",
        help="Endpoint da API a ser chamado (ex.: /produtos, /vendas). Padrão: /produtos",
    )

    parser.add_argument(
        "--param",
        "-p",
        action="append",
        metavar="CHAVE=VALOR",
        help=(
            "Parâmetro de filtro no formato chave=valor. "
            "Pode ser usado várias vezes. Ex.: -p pagina=1 -p ativo=1"
        ),
    )

    return parser


def main() -> None:
    """Ponto de entrada do script."""
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        params = parse_params(args.param)
        make_request(endpoint=args.endpoint, params=params)
    except Exception as exc:
        logger.error("Erro ao executar o exemplo: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

