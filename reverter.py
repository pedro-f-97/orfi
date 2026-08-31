import sys
from collections.abc import Callable
from pathlib import Path

import configs
import ficheiros
import pastas


def reverte(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], trabalho: Callable[[Path, Path], int], tratamento: str):
    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)

    if pastasParaReverter == set():
        print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        sys.exit()
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)

    if ficheirosParaReverter == set():
        print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        sys.exit()
    
    total = 0
    for ficheiro in ficheirosParaReverter:
        total += trabalho(ficheiro, pastaSelecionada)
    print(f"{configs.CoresTexto.VERDE}Revertido, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
