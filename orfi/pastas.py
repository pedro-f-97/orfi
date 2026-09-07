import logging
from pathlib import Path

from . import configs, ficheiros

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
            print(f"{configs.CoresTexto.AMARELO}Categoria não encontrada para {ext}{configs.CoresTexto.RESET}")
    if len(pastas) > 0:
        print(f"{configs.CoresTexto.AMARELO}Pastas para criar: {pastas}{configs.CoresTexto.RESET}")
    else:
        print(f"{configs.CoresTexto.AMARELO}Não vai criar pastas.{configs.CoresTexto.RESET}")
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
    for pasta in pastas:
        caminhoFinal = caminho / pasta
        for categoria in categorias:
            if pasta == categoria.nome:
                categoria.caminho = caminhoFinal
        if not caminhoFinal.exists():
            if not simula:
                caminhoFinal.mkdir(parents = False, exist_ok = True)
                logger.info("Criou pasta: %s", caminhoFinal)
            configs.mensagem(f"Pasta criada - {pasta}.", f"Pasta {pasta} seria criada.", simula, configs.CoresTexto.VERDE)   
            cont += 1
        else:
            print(f"{configs.CoresTexto.AMARELO}Pasta {pasta} já existe. {configs.CoresTexto.RESET}")
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
                if pasta.stem == categoria.nome:
                    pastasParaReverter.add(pasta)
    return pastasParaReverter

def eliminaPastasVazias(pastasParaReverter: set[Path], simula: bool, ficheirosMovidos: set[Path] | None = None):
    """Elimina as pastas vazias do set de pastas indicado.

    Args:
        pastasParaReverter: As pastas a analisar.
        simula: Se é para apenas simular o processo ou não.
        ficheirosMovidos: Lista de ficheiros que seriam movidos pelo processo anterior em modo simular.
    """
    for pasta in pastasParaReverter:
        ficheirosNaPasta = set(pasta.iterdir())

        if simula and ficheirosMovidos:
            for ficheiro in ficheirosMovidos:
                ficheirosNaPasta.discard(ficheiro)

        if not ficheirosNaPasta:
            if not simula:
                pasta.rmdir()
                logger.info("Eliminou pasta: %s", pasta)
            configs.mensagem(f"Pasta vazia '{pasta}' foi eliminada.", f"Pasta {pasta} seria eliminada.", simula, configs.CoresTexto.VERMELHO)