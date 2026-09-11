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
        "-a",
        "--alvo",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_alvo")
    )

    parser.add_argument(
        "-c",
        "--copiar",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_copiar")
    )

    parser.add_argument(
        "-r",
        "--reverter",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_reverter")
    )

    parser.add_argument(
        "-d",
        "--datar",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_datar")
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_force")
    )

    parser.add_argument(
        "-s",
        "--simula",
        action="store_true",
        help=mensagens.mensagemTrataIdioma("descricao_simula")
    )

    parser.add_argument(
        "-i",
        "--idioma",
        help=mensagens.mensagemTrataIdioma("descricao_idioma")
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"orfi {version('orfi')}"
    )

    argumentos = parser.parse_args()

    if argumentos.alvo:
        logger.info("Argument '--alvo' set")
    if argumentos.copiar:
        logger.info("Argument '--copiar' set")
    if argumentos.reverter:
        logger.info("Argument '--reverter' set")
    if argumentos.datar:
        logger.info("Argument '--datar' set")
    if argumentos.force:
        logger.info("Argument '--force' set")
    if argumentos.simula:
        logger.info("Argument '--simula' set")

    return argumentos