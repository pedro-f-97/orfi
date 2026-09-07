import datetime
import logging
import os
from pathlib import Path
from shutil import copy2, move

from . import configs

logger = logging.getLogger(__name__)


def devolveExt(pasta: Path) -> set[str]:
    """Devolve um set com as extensões distintas dos ficheiros presentes na pasta.

    Args:
        pasta: Pasta a ser analisada.

    Returns:
        Um set com as extensões distintas encontradas na pasta.
    """
    ext: set[str] = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        for ex in ext:
            logger.debug("Extensão detectada: %s", ex)
            print(f"{configs.CoresTexto.AZUL}Extensão detectada: {ex} {configs.CoresTexto.RESET}") 
    return ext

def devolveFicheiros(pasta: Path) -> list[Path]:
    """Devolve uma lista dos ficheiros presentes na pasta.

    Args:
        pasta: Pasta a ser analisada.

    Returns:
        Uma lista dos ficheiros encontrados na pasta.
    """
    listaFicheiros = []
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            listaFicheiros.append(ficheiro)
    if listaFicheiros:
        for ficheiro in listaFicheiros:
            logger.debug("Ficheiro detectado: %s", ficheiro)
    else:
        logger.info("Não detectou nenhum ficheiro.")
    return listaFicheiros

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
    if ficheiroFinal.exists() and not force:
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {pastaDestino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    try:
        if not simula:
            copy2(ficheiro, ficheiroFinal)
            logger.info("Copiou o ficheiro '%s' para '%s'", ficheiro, ficheiroFinal)
        configs.mensagem(f"Ficheiro {ficheiro} copiado para {ficheiroFinal}.", f"Ficheiro {ficheiro} seria copiado para {ficheiroFinal}.", simula, configs.CoresTexto.AMARELO)    
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        logger.exception("Erro a copiar o ficheiro '%s' para '%s'.", ficheiro, ficheiroFinal)
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
    if ficheiroFinal.exists() and not force:
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {pastaDestino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    try:
        if not simula:
            move(ficheiro, ficheiroFinal)
            logger.info("Moveu o ficheiro '%s' para '%s'", ficheiro, ficheiroFinal)
        configs.mensagem(f"Ficheiro {ficheiro} movido para {ficheiroFinal}.", f"Ficheiro {ficheiro} seria movido para {ficheiroFinal}.", simula, configs.CoresTexto.AMARELO)
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        logger.exception("Erro a mover o ficheiro '%s' para '%s'.", ficheiro, ficheiroFinal)
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
        logger.debug("Não detectou caminho para a categoria '%s' da extensão '%s'", categoria, ficheiro.suffix.lower())
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
            ficheiro.unlink()
            logger.info("Eliminou o ficheiro '%s'", ficheiro)
        configs.mensagem(f"Ficheiro {ficheiro} apagado.", f"Ficheiro {ficheiro} seria apagado.", simula, configs.CoresTexto.VERMELHO)
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
    logger.info("Vai reverter %s ficheiros.", len(ficheirosParaReverter))
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
        logger.info("Datou o ficheiro '%s' para '%s'", ficheiro, ficheiroDatado)
    configs.mensagem(f"{ficheiro} datado para {ficheiroDatado}.", f"Ficheiro {ficheiro} seria datado para {ficheiroDatado}.", simula, configs.CoresTexto.AMARELO)   
    return ficheiroDatado

def devolveDataCriacao(ficheiro: Path) -> datetime.datetime:
    """Obter a data de criação ou, quando inexistente, data de última modificação do ficheiro dado.

    Args:
        ficheiro: O ficheiro alvo.

    Returns:
        A data de criação ou última modificação do ficheiro.
    """
    try:
        data = os.stat(ficheiro).st_birthtime
    except AttributeError:
        logger.error("Data de criação indisponível para '%s', vai usar data de modificação.", ficheiro)
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
        logger.info("Vai reverter o ficheiro '%s'", ficheiro)
    configs.mensagem(f"{ficheiro} revertido para {ficheiroRevertido}.", f"{ficheiro} seria revertido para {ficheiroRevertido}.", simula, configs.CoresTexto.AMARELO)
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
        logger.debug("Erro a verificar datado ficheiro: '%s'", ficheiro)
        return False
    return True