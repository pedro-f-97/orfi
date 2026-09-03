from pathlib import Path

from . import configs, ficheiros, pastas


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

def reverteDatar(pastaSelecionada: Path, modo: configs.Modo):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados e revertidos."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "revertidos."

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            ficheiroFinal = ficheiros.reverteDatarFicheiro(ficheiro)
            total += trabalho(ficheiro, pastaSelecionada, ficheiroFinal)
        else:
            print(f"{configs.CoresTexto.AMARELO}Ficheiro ignorado: {ficheiro.name}{configs.CoresTexto.RESET}")
    print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")