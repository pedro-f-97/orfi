import logging
from pathlib import Path

from . import configs, ficheiros, mensagens

logger = logging.getLogger(__name__)

def devolvePastas(setExt: set[str], categorias: list[configs.CategoriaDePasta]) -> set[str]:
    """Devolve um set com as pastas correspondentes às extensões de acordo com as categorias.

    Args:
        setExt: O set de extensões a avaliar.
        categorias: A lista de categorias utilizadas para obter as pastas.

    Returns:
        Um set com os nomes das pastas identificadas.
    """
    pastas = set()
    
    for ext in setExt:
        categoria = ficheiros.encontraCategoria(ext, categorias)
        if categoria is not None:
            pastas.add(categoria.nome)
        else:
            mensagens.mensagem("categoria_nao_encontrada", "categoria_nao_encontrada", False, mensagens.CoresTexto.AMARELO, ext=ext)
    if configs.verbose:
        if len(pastas) > 0:
            mensagens.mensagem("pastas_para_criar", "pastas_para_criar", False, mensagens.CoresTexto.AMARELO, pastas=pastas)
        else:
            mensagens.mensagem("nao_vai_criar_pastas", "nao_vai_criar_pastas", False, mensagens.CoresTexto.AMARELO)
    return pastas
        

def criaPastas(caminho: Path, pastas: set[str], categorias: list[configs.CategoriaDePasta], simula: bool) -> int:
    """Cria as pastas dadas no caminho indicado e preenche o caminho correspondente a cada categoria.

    Args:
        caminho: O caminho onde devem ser criadas as pastas.
        pastas: O set com as pastas a serem criadas.
        categorias: A lista de categorias utilizadas para preencher o caminho correspondente a cada categoria.
        simula: Se é para apenas simular o processo ou não.

    Returns:
        O número de pastas criadas.
    """
    cont = 0

    for pasta in sorted(pastas):
        caminhoFinal = caminho / pasta
        jaExistia = caminhoFinal.exists()

        # Preenche a categoria uma única vez, independentemente do que aconteça depois.
        for categoria in categorias:
            if pasta == categoria.nome:
                categoria.caminho = caminhoFinal
                break

        if jaExistia:
            if configs.verbose:
                mensagens.mensagem("pasta_existente", "pasta_existente", False, mensagens.CoresTexto.AMARELO, pasta=pasta)

        elif simula:
            if configs.verbose:
                mensagens.mensagem("pasta_criada", "pasta_seria_criada", True, mensagens.CoresTexto.VERDE, pasta=pasta)
            cont += 1

        else:
            try:
                caminhoFinal.mkdir(parents=True, exist_ok=True)
                logger.info("Created folder: %s", caminhoFinal)
                cont += 1

                if configs.verbose:
                    mensagens.mensagem("pasta_criada", "pasta_criada", False, mensagens.CoresTexto.VERDE, pasta=pasta)

            except OSError as erro:
                mensagens.mensagem("erro_criar_pasta", "erro_criar_pasta", False, mensagens.CoresTexto.VERMELHO, pasta=caminhoFinal, erro=erro)
                logger.exception("Error creating folder '%s'", caminhoFinal)
    return cont

def pastasExistentes(caminho: Path, categorias: list[configs.CategoriaDePasta]) -> set[Path]:
    """Devolve as pastas dentro do caminho indicado que correspondem a categorias.

    Args:
        caminho: O caminho onde procurar.
        categorias: A lista de categorias utilizadas para procurar.

    Returns:
        Um set com as pastas identificadas.
    """
    pastasParaReverter = set()
    for pasta in caminho.iterdir():
        if pasta.is_dir():
            for categoria in categorias:
                if pasta.name == categoria.nome:
                    pastasParaReverter.add(pasta)
    return pastasParaReverter

def eliminaPastasVazias(pastasParaReverter: set[Path], simula: bool, ficheirosMovidos: set[Path] | None = None) -> int:
    """Elimina as pastas vazias do set de pastas indicado.

    Args:
        pastasParaReverter: As pastas a analisar.
        simula: Se é para apenas simular o processo ou não.
        ficheirosMovidos: Lista de ficheiros que seriam movidos pelo processo anterior em modo simular.

    Returns:
        O número de pastas que foram ou seriam eliminadas.
    """
    pastasEliminadas = 0
    for pasta in pastasParaReverter:
        ficheirosNaPasta = set(pasta.iterdir())

        if simula and ficheirosMovidos:
            for ficheiro in ficheirosMovidos:
                ficheirosNaPasta.discard(ficheiro)

        if not ficheirosNaPasta:
            if not simula:
                try:
                    pasta.rmdir()
                    logger.info("Deleted folder: %s", pasta)
                except OSError:
                    mensagens.mensagem("erro_eliminar_pasta", "erro_eliminar_pasta", False, mensagens.CoresTexto.VERMELHO, pasta=pasta)
                    logger.exception("Error deleting folder '%s'", pasta)
                    continue
            pastasEliminadas += 1
            if configs.verbose:
                mensagens.mensagem("pasta_eliminada", "pasta_seria_eliminada", simula, mensagens.CoresTexto.VERMELHO, pasta=pasta)
    return pastasEliminadas