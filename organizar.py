import sys
from collections.abc import Callable
from pathlib import Path

import configs
import ficheiros
import pastas


def organiza(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], trabalho: Callable[[Path, Path], int], tratamento: str):
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
