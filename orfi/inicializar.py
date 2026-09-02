import argparse


def trataArgumentos() -> argparse.Namespace:
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

    argumentos = parser.parse_args()
    return argumentos