import datetime
import logging
import os
from pathlib import Path
from shutil import copy2, move

from . import configs, mensagens

logger = logging.getLogger(__name__)


def devolveExt(ficheiros: set[Path]) -> set[str]:
    """Devolve um set com as extensões distintas dos ficheiros presentes no set.

    Args:
        ficheiros: set a ser analisado

    Returns:
        Um set com as extensões distintas encontradas na pasta.
    """
    ext: set[str] = set()
    for ficheiro in ficheiros:
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        logger.debug("Extensions detected: %s", ext)
        mensagens.mensagem("extensao_detectada", "extensao_detectada", False, mensagens.CoresTexto.AZUL, ext=ext)
    return ext

def devolveFicheiros(pasta: Path, nivel: int = 1) -> set[Path]:
    """Devolve um set dos ficheiros presentes na pasta.

    Args:
        pasta: Pasta a ser analisada.
        nivel: nivel de subpastas a considerar

    Returns:
        Um set dos ficheiros encontrados na pasta.
    """
    listaFicheiros = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            listaFicheiros.add(ficheiro)
        elif nivel > 1:
            listaFicheiros.update(devolveFicheiros(ficheiro, nivel - 1))
    if listaFicheiros:
        for ficheiro in listaFicheiros:
            logger.debug("File detected: %s", ficheiro)
    else:
        logger.info("No file detected.")
    return listaFicheiros

def podeSubstituir(ficheiro: Path, ficheiroFinal: Path, pastaDestino: Path, force: bool) -> bool:
    """Confirma com o utilizador se pode substituir um ficheiro já existente no destino.
    Args:
        ficheiro: Ficheiro em questão.
        ficheiroFinal: O ficheiro de destino.
        pastaDestino: A pasta para onde vai o ficheiro.
        force: Se as confirmações são automaticamente aceites ou não.

    Returns:
        1 se a operação for realizada, 0 caso contrário.
    """
    if not ficheiroFinal.exists() or force:
        return True
    resposta = input(f"{mensagens.CoresTexto.AMARELO}{mensagens.mensagemTrataIdioma('ficheiro_existente_substituir', ficheiro=ficheiro.name, destino=pastaDestino)}{mensagens.CoresTexto.RESET}")
    if resposta.lower() in ("s", "y"):
        return True
    mensagens.mensagem("ficheiro_cancelado", "ficheiro_cancelado", False, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro.name)
    return False

def copiaFicheiro(ficheiro: Path, pastaDestino: Path, force: bool, simula: bool, ficheiroFinal: Path | None = None) -> int:
    """Copia o ficheiro para a pasta destino ou para o ficheiroFinal quando dado.

    Args:
        ficheiro: Ficheiro a ser copiado.
        pastaDestino: Pasta para onde vai ser copiado o ficheiro.
        force: Se as confirmações são automaticamente aceites ou não.
        simula: Se é para apenas simular o processo ou não.
        ficheiroFinal: Caminho alternativo para o ficheiro de destino.

    Returns:
        1 se a operação for realizada, 0 caso contrário.
    """
    ficheiroFinal = pastaDestino / (ficheiroFinal.name if ficheiroFinal else ficheiro.name)
    if not podeSubstituir(ficheiro, ficheiroFinal, pastaDestino, force):
        return 0
    try:
        if not simula:
            copy2(ficheiro, ficheiroFinal)
            logger.info("File '%s' copied to '%s'", ficheiro, ficheiroFinal)
        mensagens.mensagem("ficheiro_copiado", "ficheiro_seria_copiado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro, destino=ficheiroFinal)    
    except OSError as erro:
        mensagens.mensagem("erro_ficheiro", "erro_ficheiro", False, mensagens.CoresTexto.VERMELHO, ficheiro=ficheiro.name, erro=erro)
        logger.exception("Error copying file '%s' to '%s'.", ficheiro, ficheiroFinal)
        return 0
    return 1

def moveFicheiro(ficheiro: Path, pastaDestino: Path, force: bool, simula: bool, ficheiroFinal: Path | None = None) -> int:
    """Move o ficheiro para a pasta destino ou para o ficheiroFinal quando dado.

    Args:
        ficheiro: Ficheiro a ser movido.
        pastaDestino: Pasta para onde vai ser movido o ficheiro.
        force: Se as confirmações são automaticamente aceites ou não.
        simula: Se é para apenas simular o processo ou não.
        ficheiroFinal: Caminho alternativo para o ficheiro de destino.

    Returns:
        1 se a operação for realizada, 0 caso contrário.
    """
    ficheiroFinal = pastaDestino / (ficheiroFinal.name if ficheiroFinal else ficheiro.name)
    if not podeSubstituir(ficheiro, ficheiroFinal, pastaDestino, force):
        return 0
    try:
        if not simula:
            move(ficheiro, ficheiroFinal)
            logger.info("File '%s' moved to '%s'", ficheiro, ficheiroFinal)
        mensagens.mensagem("ficheiro_movido", "ficheiro_seria_movido", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro, destino=ficheiroFinal)
    except OSError as erro:
        mensagens.mensagem("erro_ficheiro", "erro_ficheiro", False, mensagens.CoresTexto.VERMELHO, ficheiro=ficheiro.name, erro=erro)
        logger.exception("Error moving file '%s' to '%s'.", ficheiro, ficheiroFinal)
        return 0
    return 1 

def defineDestino(ficheiro:Path, categorias: list[configs.CategoriaDePasta]) -> Path | None:
    """Determina a pasta de destino de um ficheiro segundo as categorias.

    Args:
        ficheiro: Ficheiro cuja extensão será analisada.
        categorias: Categorias utilizadas para determinar o destino.

    Returns:
        A pasta de destino correspondente à categoria do ficheiro, ou
        None quando não existe uma categoria correspondente nem uma
        categoria por defeito — comportamento intencional, para
        permitir excluir extensões da organização.
    """
    
    categoria = encontraCategoria(ficheiro.suffix.lower(), categorias)
    if categoria is not None and categoria.caminho is not None:
        return categoria.caminho
    else:
        logger.debug("No path detected for category '%s' of the extension '%s'", categoria, ficheiro.suffix.lower())
        return None

def encontraCategoria(extensao: str, categorias: list[configs.CategoriaDePasta]) -> configs.CategoriaDePasta | None:
    """Procura a categoria correspondente à extensão dada.

    Args:
        extensao: Extensão a procurar.
        categorias: Lista de categorias onde procurar.

    Returns:
        Categoria correspondente se existir, ou categoria por defeito quando existe, caso contrário devolve None.
    """
    for categoria in categorias:
        if extensao in categoria.extensoes:
            return categoria
    for categoria in categorias:
        if categoria.defeito:
            return categoria

def apagaFicheiro(ficheiro:Path, simula: bool) -> int:
    """Apaga o ficheiro dado.

    Args:
        ficheiro: Ficheiro a ser apagado.
        simula: Se é para apenas simular o processo ou não.

    Returns:
        1 se a operação for realizada, 0 caso contrário.
    """
    if ficheiro.exists():
        if not simula:
            try:
                ficheiro.unlink()
                logger.info("Deleted file '%s'", ficheiro)
            except OSError as erro:
                mensagens.mensagem("erro_ficheiro", "erro_ficheiro", False, mensagens.CoresTexto.VERMELHO, erro=erro,ficheiro=ficheiro)
                logger.exception("Error deleting file '%s'", ficheiro)
        mensagens.mensagem("ficheiro_apagado", "ficheiro_seria_apagado", simula, mensagens.CoresTexto.VERMELHO, ficheiro=ficheiro)
        return 1
    return 0

def ficheirosParaReverter(pastas: set[Path]) -> set[Path]:
    """Devolve os ficheiros distintos encontrados dentro do conjunto de pastas dado.

    Args:
        pastas: Conjunto de pastas a analisar.

    Returns:
        O conjunto de ficheiros distintos encontrados dentro das pastas, set vazio caso não tenha encontrado nenhum.
    """
    ficheirosParaReverter = set()
    for pasta in pastas:
        for elemento in pasta.iterdir():
            if elemento.is_dir() == False:
                ficheirosParaReverter.add(elemento)
    logger.info("Reverting %s files.", len(ficheirosParaReverter))
    return ficheirosParaReverter

def datarFicheiro(ficheiro: Path, simula: bool) -> Path:
    """Adiciona um prefixo com a data de criação no formato yymmdd_ ao ficheiro dado.

    Args:
        ficheiro: O ficheiro a datar.
        simula: Se é para apenas simular o processo ou não.

    Returns:
        O ficheiro com o prefixo da data de criação no nome.
    """
    data = devolveDataCriacao(ficheiro)
    formato = data.strftime("%y%m%d")
    ficheiroDatado = ficheiro.with_name(formato + "_" + ficheiro.name)

    if not simula:
        logger.info("File '%s' dated to '%s'", ficheiro, ficheiroDatado)
    mensagens.mensagem("ficheiro_datado", "ficheiro_seria_datado", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro, ficheiroDatado=ficheiroDatado)   
    return ficheiroDatado

def devolveDataCriacao(ficheiro: Path) -> datetime.datetime:
    """Obter a data de criação ou, quando inexistente, data de última modificação do ficheiro dado.

    Args:
        ficheiro: O ficheiro alvo.

    Returns:
        A data de criação ou última modificação do ficheiro.
    """
    try:
        data = os.stat(ficheiro).st_birthtime # pyright: ignore[reportAttributeAccessIssue]  # Não existe em Linux
    except AttributeError:                    
        logger.error("Creation date unavailable for '%s', using last modification date.", ficheiro)
        data = os.stat(ficheiro).st_mtime
    
    return datetime.datetime.fromtimestamp(data, tz = None)

def reverteDatarFicheiro(ficheiro: Path, simula: bool) -> Path | None:
    """Remove o prefixo com data de criação do nome do ficheiro dado.

    Args:
        ficheiro: O ficheiro alvo.
        simula: Se é para apenas simular o processo ou não.

    Returns:
        O ficheiro com o prefixo da data de criação removido ou None caso o ficheiro já não tivesse o prefixo.
    """
    if not verificaDatado(ficheiro):
        return None
    ficheiroRevertido = ficheiro.name[7:]
    if not simula:
        logger.info("Reverting file '%s'", ficheiro)
    mensagens.mensagem("ficheiro_revertido", "ficheiro_seria_revertido", simula, mensagens.CoresTexto.AMARELO, ficheiro=ficheiro, ficheiroRevertido=ficheiroRevertido)
    return ficheiro.with_name(ficheiroRevertido)

def verificaDatado(ficheiro: Path) -> bool:
    """Verifica se o ficheiro dado tem o prefixo com data no nome ou não.

    Args:
        ficheiro: O ficheiro alvo.

    Returns:
        True quando encontra o prefixo, False caso contrário.
    """
    if len(ficheiro.name) < 8 or ficheiro.name[6] != "_":
        return False
    prefixo = ficheiro.name[0:6]
    try:
        datetime.datetime.strptime(prefixo, "%y%m%d")
    except ValueError:
        logger.debug("Error checking if file is dated: '%s'", ficheiro)
        return False
    return True