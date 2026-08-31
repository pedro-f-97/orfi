import argparse
import sys

import alvo
import configs
import ficheiros
import pastas

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

argumentos = parser.parse_args()

if argumentos.aqui:
    pastaSelecionada = alvo.defineAlvoAqui()
else:
    pastaSelecionada = alvo.defineAlvo()

if pastaSelecionada is None:
    print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
    sys.exit()

print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

categorias = configs.iniciarCategorias()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pastaSelecionada), categorias)

if pastasParaCriar == set():
    print(f"{configs.CoresTexto.AMARELO}Nada para fazer.{configs.CoresTexto.RESET}")
    sys.exit()

confirmacao = input(f"{configs.CoresTexto.AZUL}Criar as pastas {pastasParaCriar}? (s/n): {configs.CoresTexto.RESET}")
if confirmacao.lower() == "s":
    pastas.criaPastas(pastaSelecionada, pastasParaCriar, categorias)
else:
    print(f"{configs.CoresTexto.AMARELO}Operação Cancelada{configs.CoresTexto.RESET}")
    sys.exit()

ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

if argumentos.copiar:
    trabalho = ficheiros.copiaFicheiro
    tratamento = "copiados."
else:
    trabalho = ficheiros.moveFicheiro
    tratamento = "movidos."

total = 0
for ficheiro in ficheirosLista:
    destino = ficheiros.defineDestino(ficheiro, categorias)
    if destino is not None:
        total += trabalho(ficheiro, destino)
    else:
        print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")

print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")