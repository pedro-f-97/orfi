import sys
from pathlib import Path

import configs
import ficheiros
import pastas


def reverte(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "movidos."

    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)

    if pastasParaReverter == set():
        print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        return
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)

    if ficheirosParaReverter == set():
        print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        return
    
    total = 0
    for ficheiro in ficheirosParaReverter:
        total += trabalho(ficheiro, pastaSelecionada)

    if modo == configs.Modo.MOVER:
        pastas.eliminaPastasVazias(pastasParaReverter)
    print(f"{configs.CoresTexto.VERDE}Revertido, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
