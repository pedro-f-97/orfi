import argparse
import sys

import alvo
import configs
import organizar
import reverter

parser = argparse.ArgumentParser(
    description="Organiza ficheiros por categorias."
)

parser.add_argument(
    "-a",
    "--aqui",
    action="store_true",
    help="utiliza a pasta atual como pasta alvo"
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

if argumentos.aqui:
    pastaSelecionada = alvo.defineAlvoAqui()
else:
    pastaSelecionada = alvo.defineAlvo()

if argumentos.copiar:
    modo = configs.Modo.COPIAR
else:
    modo = configs.Modo.MOVER

if pastaSelecionada is None:
    print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
    sys.exit()

print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

categorias = configs.iniciarCategorias()

if argumentos.reverter:
    reverter.reverte(pastaSelecionada, categorias, modo)

else:
    organizar.organiza(pastaSelecionada, categorias, modo)
    
sys.exit()