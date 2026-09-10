import logging
from pathlib import Path

from . import configs, ficheiros, mensagens, pastas

logger = logging.getLogger(__name__)

def reverte(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo, force: bool, simula: bool) -> configs.ResultadosOperacao:
    """Reverte a organização dos ficheiros contidos nas pastas categorizadas dentro da pasta indicada.

    Args:
        pastaSelecionada: A pasta que contém as pastas categorizadas.
        categorias: A lista de categorias utilizadas para organizar os ficheiros.
        modo: Define se os ficheiros são movidos ou copiados.
        force: Se aceita automaticamente todas as verificações ou não.
        simula: Se é para apenas simular o processo ou não.

    Returns:
        O resultado da operação, número de ficheiros tratados e
        de pastas eliminadas (0 em ambos se nada foi feito).
    """
    resultados = configs.ResultadosOperacao()

    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_reverter_copia")
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_reverter_movimento")
    else:
        mensagens.mensagem("modo_inesperado", "modo_inesperado", False, mensagens.CoresTexto.VERMELHO, modo=modo)
        return resultados

    pastasParaReverter = pastas.pastasExistentes(pastaSelecionada, categorias)

    if pastasParaReverter == set():
        mensagens.mensagem("nada_para_reverter", "nada_para_reverter_simula", simula, mensagens.CoresTexto.AMARELO)
        return resultados
    
    ficheirosParaReverter = ficheiros.ficheirosParaReverter(pastasParaReverter)
    
    ficheirosMovidos = set()
    for ficheiro in ficheirosParaReverter:
        resultado = trabalho(ficheiro, pastaSelecionada, force, simula)
        if resultado:
            resultados.ficheirosTratados += resultado
            mensagens.mensagem("ficheiro_tratado", "ficheiro_seria_tratado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
            if modo == configs.Modo.MOVER:
                ficheirosMovidos.add(ficheiro)

    if modo == configs.Modo.MOVER:
        resultados.pastasEliminadas = pastas.eliminaPastasVazias(pastasParaReverter, simula, ficheirosMovidos)
        if resultados.pastasEliminadas > 0:
            mensagens.mensagem("pastas_eliminadas", "pastas_eliminadas_simula", simula, mensagens.CoresTexto.VERMELHO, numero=resultados.pastasEliminadas)
    if not simula:
        logger.info("Finished, %s files handled", resultados.ficheirosTratados)
    mensagens.mensagem("ficheiros_revertidos", "ficheiros_seriam_revertidos", simula, mensagens.CoresTexto.AMARELO, total=resultados.ficheirosTratados, tratamento=tratamento)

    return resultados

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
        tratamento = mensagens.mensagemTrataIdioma("tratamento_reverter_datar_copia")
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_reverter_datar_movimento")
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