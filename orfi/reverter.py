import logging
from pathlib import Path

from . import configs, ficheiros, mensagens, pastas

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
        mensagens.mensagem("modo_inesperado", "modo_inesperado", False, mensagens.CoresTexto.VERMELHO, modo=modo)
        return

    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)

    if pastasParaReverter == set():
        mensagens.mensagem("nada_para_reverter", "nada_para_reverter_simula", simula, mensagens.CoresTexto.AMARELO)
        return
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)

    if ficheirosParaReverter == set():
        mensagens.mensagem("nada_para_reverter", "nada_para_reverter_simula", simula, mensagens.CoresTexto.AMARELO)
        return
    
    total = 0
    ficheirosMovidos = set()
    for ficheiro in ficheirosParaReverter:
        resultado = trabalho(ficheiro, pastaSelecionada, force, simula)
        if resultado:
            total += resultado
            mensagens.mensagem("ficheiro_tratado", "ficheiro_seria_tratado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
            if modo == configs.Modo.MOVER:
                ficheirosMovidos.add(ficheiro)

    if modo == configs.Modo.MOVER:
        pastas.eliminaPastasVazias(pastasParaReverter, simula, ficheirosMovidos)
    if not simula:
        logger.info("Finished, %s files handled", total)
    mensagens.mensagem("ficheiros_revertidos", "ficheiros_seriam_revertidos", simula, mensagens.CoresTexto.AMARELO, total=total, tratamento=tratamento)

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
        mensagens.mensagem("modo_inesperado", "modo_inesperado", False, mensagens.CoresTexto.VERMELHO, modo=modo)
        return

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            ficheiroFinal = ficheiros.reverteDatarFicheiro(ficheiro, simula)
            resultado = trabalho(ficheiro, pastaSelecionada, force, simula, ficheiroFinal)
            if resultado:
                total += resultado
                mensagens.mensagem("ficheiro_tratado", "ficheiro_seria_tratado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
        else:
            if not simula:
                logger.info("File ignored: '%s'", ficheiro)
            mensagens.mensagem("ficheiro_ignorado", "ficheiro_seria_ignorado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
    if not simula:
        logger.info("Finished, %s files handled.", total)
    mensagens.mensagem("ficheiros_revertidos", "ficheiros_seriam_revertidos", simula, mensagens.CoresTexto.AMARELO, total=total, tratamento=tratamento)