import logging
from pathlib import Path

from . import configs, ficheiros, pastas

logger = logging.getLogger(__name__)

def reverte(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo, force: bool, simula: bool):
    """Reverte a organização dos ficheiros contidos nas pastas categorizadas dentro da pasta indicada.

    Args:
        pastaSelecionada: A pasta que contém as pastas categorizadas.
        categorias: A lista de categorias utilizadas para organizar os ficheiros.
        modo: Define se os ficheiros são movidos ou copiados.
        force: Se aceita automaticamente todas as verificações ou não.
        simula: Se é para apenas simular o processo ou não.
    """
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
        configs.mensagem("Nada para reverter.", "Não revertia nada.", simula, configs.CoresTexto.AMARELO)
        return
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)

    if ficheirosParaReverter == set():
        configs.mensagem("Nada para reverter.", "Não revertia nada.", simula, configs.CoresTexto.AMARELO)
        return
    
    total = 0
    for ficheiro in ficheirosParaReverter:
        resultado = trabalho(ficheiro, pastaSelecionada, force, simula)
        if resultado:
            total += resultado
            configs.mensagem(f"{ficheiro.name} tratado.", f"{ficheiro.name} seria tratado.", simula, configs.CoresTexto.AMARELO)

    if modo == configs.Modo.MOVER:
        pastas.eliminaPastasVazias(pastasParaReverter, simula)
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
    configs.mensagem(f"Revertido, {total} ficheiros {tratamento}", f"Revertido, {total} ficheiros teriam sido {tratamento}", simula, configs.CoresTexto.AMARELO)

def reverteDatar(pastaSelecionada: Path, modo: configs.Modo, force: bool, simula: bool):
    """Remove o prefixo com data dos ficheiros contidos na pasta indicada.

    Args:
        pastaSelecionada: A pasta que contém os ficheiros.
        modo: Define se os ficheiros são movidos ou copiados.
        force: Se aceita automaticamente todas as verificações ou não.
        simula: Se é para apenas simular o processo ou não.
    """
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
                configs.mensagem(f"{ficheiro.name} tratado.", f"{ficheiro.name} seria tratado.", simula, configs.CoresTexto.AMARELO)
        else:
            if not simula:
                logger.info("Ignorou o ficheiro %s", ficheiro)
            configs.mensagem(f"Ficheiro ignorado: {ficheiro.name}", f"Ficheiro seria ignorado: {ficheiro.name}", simula, configs.CoresTexto.AMARELO)
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
    configs.mensagem(f"Revertido, {total} ficheiros {tratamento}", f"Revertido, {total} ficheiros teriam sido {tratamento}", simula, configs.CoresTexto.AMARELO)