import argparse
import logging

logger = logging.getLogger(__name__)

def trataArgumentos() -> argparse.Namespace:
    """Define e processa os argumentos da linha de comandos.

    Returns:
        Os argumentos adicionados na linha de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Organiza ficheiros por categorias."
    )

    parser.add_argument(
        "-a",
        "--alvo",
        action="store_true",
        help="permite definir a pasta alvo"
    )

    parser.add_argument(
        "-c",
        "--copiar",
        action="store_true",
        help="copia os ficheiros em vez de mover"
    )

    parser.add_argument(
        "-r",
        "--reverter",
        action="store_true",
        help="reverte o processo de organização"
    )

    parser.add_argument(
        "-d",
        "--datar",
        action="store_true",
        help="adiciona a data de criação ao nome"
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="aprova automaticamente todas as confirmações"
    )

    parser.add_argument(
        "-s",
        "--simula",
        action="store_true",
        help="simula o processo sem fazer alterações"
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