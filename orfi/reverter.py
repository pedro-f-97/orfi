import logging
from pathlib import Path

from . import configs, ficheiros, pastas

logger = logging.getLogger(__name__)

def reverte(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo, force: bool, simula: bool):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "movidos."
    else:
        print(f"{configs.CoresTexto.VERMELHO}Modo {modo} inesperado. Operação cancelada.{configs.CoresTexto.RESET}")
        return

    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)

    if pastasParaReverter == set():
        if not simula:
            print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        else:
            print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Não revertia nada.{configs.CoresTexto.RESET}")
        return
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)

    if ficheirosParaReverter == set():
        if not simula:
            print(f"{configs.CoresTexto.AMARELO}Nada para reverter.{configs.CoresTexto.RESET}")
        else:
            print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Não revertia nada.{configs.CoresTexto.RESET}")
        return
    
    total = 0
    for ficheiro in ficheirosParaReverter:
        resultado = trabalho(ficheiro, pastaSelecionada, force, simula)
        if resultado:
            total += resultado
            if not simula:
                print(f"{configs.CoresTexto.VERDE}{ficheiro.name} tratado.{configs.CoresTexto.RESET}")
            else:
                print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] {ficheiro.name} seria tratado.{configs.CoresTexto.RESET}")

    if modo == configs.Modo.MOVER:
        pastas.eliminaPastasVazias(pastasParaReverter, simula)
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
        print(f"{configs.CoresTexto.VERDE}Revertido, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
    else:
        print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Revertido, {total} ficheiros teriam sido {tratamento}{configs.CoresTexto.RESET}")

def reverteDatar(pastaSelecionada: Path, modo: configs.Modo, force: bool, simula: bool):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados e revertidos."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "revertidos."
    else:
        print(f"{configs.CoresTexto.VERMELHO}Modo {modo} inesperado. Operação cancelada.{configs.CoresTexto.RESET}")
        return

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            ficheiroFinal = ficheiros.reverteDatarFicheiro(ficheiro, simula)
            resultado = trabalho(ficheiro, pastaSelecionada, force, simula, ficheiroFinal)
            if resultado:
                total += resultado
                if not simula:
                    print(f"{configs.CoresTexto.VERDE}{ficheiro.name} tratado.{configs.CoresTexto.RESET}")
                else:
                    print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] {ficheiro.name} seria tratado.{configs.CoresTexto.RESET}")
        else:
            if not simula:
                print(f"{configs.CoresTexto.AMARELO}Ficheiro ignorado: {ficheiro.name}{configs.CoresTexto.RESET}")
                logger.info("Ignorou o ficheiro %s", ficheiro)
            else:
                print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Ficheiro seria ignorado: {ficheiro.name}{configs.CoresTexto.RESET}")
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
        print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
    else:
        print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Feito, {total} ficheiros teriam sido {tratamento}{configs.CoresTexto.RESET}")