import argparse
import logging
from importlib.metadata import version

from . import mensagens

logger = logging.getLogger(__name__)

def trataArgumentos() -> argparse.Namespace:
    """Define e processa os argumentos da linha de comandos.

    Returns:
        Os argumentos adicionados na linha de comandos.
    """
    parser = argparse.ArgumentParser(
        description=mensagens.mensagemTrataIdioma("descricao_orfi")
    )

    parser.add_argument(
        "-t",
        "--target",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_alvo")
    )

    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_copiar")
    )

    parser.add_argument(
        "-r",
        "--revert",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_reverter")
    )

    parser.add_argument(
        "-d",
        "--date",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_datar")
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_force")
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_simula")
    )

    parser.add_argument(
        "-l",
        "--language",
        help=mensagens.mensagemTrataIdioma("descricao_idioma")
    )

    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"orfi {version('orfi')}"
    )

    argumentos = parser.parse_args()

    for nome, valor in vars(argumentos).items():
        if valor:
            logger.info("Argument '--%s' set", nome)

    return argumentos