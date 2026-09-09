import logging
from pathlib import Path

from . import configs, ficheiros, mensagens, pastas

logger = logging.getLogger(__name__)

def organiza(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo, force: bool, simula: bool):
    """Organiza os ficheiros contidos na pasta indicada.

    Args:
        pastaSelecionada: A pasta que contém os ficheiros a organizar.
        categorias: A lista de categorias utilizadas para organizar os ficheiros.
        modo: Define se os ficheiros são movidos ou copiados.
        force: Se aceita automaticamente todas as verificações ou não.
        simula: Se é para apenas simular o processo ou não.
    """
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_organizar_copia")
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_organizar_movimento")
    else:
        mensagens.mensagem("modo_inesperado", "modo_inesperado", False, mensagens.CoresTexto.VERMELHO, modo=modo)
        return

    pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pastaSelecionada), categorias)

    if pastasParaCriar == set():
        mensagens.mensagem("nada_para_fazer", "nada_para_fazer_simula", simula, mensagens.CoresTexto.AMARELO)
        return

    if not force:
        confirmacao = input(f"{mensagens.CoresTexto.AZUL}{mensagens.mensagemTrataIdioma('criar_pastas', pastas=pastasParaCriar)}{mensagens.CoresTexto.RESET}")
        if confirmacao.lower() not in ("s", "y"):
            mensagens.mensagem("operacao_cancelada", "operacao_cancelada", False, mensagens.CoresTexto.AMARELO)
            return
    cont = pastas.criaPastas(pastaSelecionada, pastasParaCriar, categorias, simula)
    if not simula:
        logger.info("Finished, %s folders created.", cont)
    mensagens.mensagem("pastas_criadas", "pastas_seriam_criadas", simula, mensagens.CoresTexto.VERDE, cont=cont)

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        destino = ficheiros.defineDestino(ficheiro, categorias)
        if destino is not None:
            resultado = trabalho(ficheiro, destino, force, simula)
            if resultado:
                total += resultado
                mensagens.mensagem("ficheiro_tratado", "ficheiro_seria_tratado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
        else:
            mensagens.mensagem("categoria_caminho_nao_encontrados", "categoria_caminho_nao_encontrados", False, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
    if not simula:
        logger.info("Finished, %s files handled.", total)
    mensagens.mensagem("ficheiros_tratados", "ficheiros_seriam_tratados", simula, mensagens.CoresTexto.AMARELO, total=total, tratamento=tratamento)

def datar(pastaSelecionada: Path, modo: configs.Modo, force: bool, simula: bool):
    """Adiciona um prefixo com data aos ficheiros contidos na pasta indicada.

    Args:
        pastaSelecionada: A pasta que contém os ficheiros a datar.
        modo: Define se os ficheiros são movidos ou copiados.
        force: Se aceita automaticamente todas as verificações ou não.
        simula: Se é para apenas simular o processo ou não.
    """
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_datar_copia")
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = mensagens.mensagemTrataIdioma("tratamento_datar_movimento")
    else:
        mensagens.mensagem("modo_inesperado", "modo_inesperado", False, mensagens.CoresTexto.VERMELHO, modo=modo)
        return

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            mensagens.mensagem("ficheiro_ja_datado", "ficheiro_ja_datado", False, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
        else:
            ficheiroFinal = ficheiros.datarFicheiro(ficheiro, simula)
            resultado = trabalho(ficheiro, pastaSelecionada, force, simula, ficheiroFinal)
            if resultado:
                total += resultado
                mensagens.mensagem("ficheiro_tratado", "ficheiro_seria_tratado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
    if not simula:
        logger.info("Finished, %s files handled.", total)
    mensagens.mensagem("ficheiros_tratados", "ficheiros_seriam_tratados", simula, mensagens.CoresTexto.AMARELO, total=total, tratamento=tratamento)