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
    trabalho = ficheiros.copiaFicheiro
    tratamento = "copiados."
else:
    trabalho = ficheiros.moveFicheiro
    tratamento = "movidos."

if pastaSelecionada is None:
    print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
    sys.exit()

print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

categorias = configs.iniciarCategorias()

if argumentos.reverter:
    #1º - no diretório definido tem de procurar pastas com nomes que coincidam com nomes nas categorias de pasta
    #2º - para cada uma dessas pastas, obter ficheiros e adicionar cada um a uma lista
    #3º - percorrer a lista, movendo ou copiando cada ficheiro para a pasta base
    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)
    if pastasParaReverter:
        ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)
        if ficheirosParaReverter:
            total = 0
            for ficheiro in ficheirosParaReverter:
                total += trabalho(ficheiro, pastaSelecionada)
            print(f"{configs.CoresTexto.VERDE}Revertido, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
        else:
            print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
    else:
        print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
    sys.exit()

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

total = 0
for ficheiro in ficheirosLista:
    destino = ficheiros.defineDestino(ficheiro, categorias)
    if destino is not None:
        total += trabalho(ficheiro, destino)
    else:
        print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")

print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")