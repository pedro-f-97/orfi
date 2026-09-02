import argparse

from . import alvo, configs, organizar, reverter


def main():
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

    argumentos = parser.parse_args()

    if argumentos.alvo:
        pastaSelecionada = alvo.defineAlvo()
    else:
        pastaSelecionada = alvo.defineAlvoAqui()

    if argumentos.copiar:
        modo = configs.Modo.COPIAR
    else:
        modo = configs.Modo.MOVER

    if pastaSelecionada is None:
        print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
        return

    print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

    categorias = configs.carregarConfiguracao() #configs.iniciarCategorias()

    if argumentos.reverter:
        reverter.reverte(pastaSelecionada, categorias, modo)

    else:
        organizar.organiza(pastaSelecionada, categorias, modo)
        

if __name__ == "__main__":
    main()    