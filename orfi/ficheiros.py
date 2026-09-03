import datetime
import logging
import os
from pathlib import Path
from shutil import copy2, move

from . import configs

logger = logging.getLogger(__name__)


def devolveExt(pasta: Path) -> set[str]:
    ext: set[str] = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        for ex in ext:
            logger.info("Extensãos detectada: %s", ex)
            print(f"{configs.CoresTexto.AZUL}Extensão detectada: {ex} {configs.CoresTexto.RESET}") 
    return ext

def devolveFicheiros(pasta: Path) -> list[Path]:
    listaFicheiros = []
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            listaFicheiros.append(ficheiro)
    if listaFicheiros:
        for ficheiro in listaFicheiros:
            logger.info("Ficheiro detectado: %s", ficheiro)
    else:
        logger.info("Não detectou nenhum ficheiro.")
    return listaFicheiros

def copiaFicheiro(ficheiro: Path, pastaDestino: Path, ficheiroFinal: Path | None = None) -> int:
    ficheiroFinal = pastaDestino / (ficheiroFinal.name if ficheiroFinal else ficheiro.name)
    if ficheiroFinal.exists():
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {pastaDestino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    try:
        copy2(ficheiro, ficheiroFinal)
        logger.info("Copiou o ficheiro '%s' para '%s'", ficheiro, ficheiroFinal)
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        logger.error("Erro a copiar o ficheiro '%s' para '%s' : '%s'", ficheiro, ficheiroFinal, erro)
        return 0
    return 1

def moveFicheiro(ficheiro: Path, pastaDestino: Path, ficheiroFinal: Path | None = None) -> int:
    ficheiroFinal = pastaDestino / (ficheiroFinal.name if ficheiroFinal else ficheiro.name)
    if ficheiroFinal.exists():
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {pastaDestino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    try:
        move(ficheiro, ficheiroFinal)
        logger.info("Moveu o ficheiro '%s' para '%s'", ficheiro, ficheiroFinal)
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        logger.error("Erro a mover o ficheiro '%s' para '%s' : '%s'", ficheiro, ficheiroFinal, erro)
        return 0
    return 1 

def defineDestino(ficheiro:Path, categorias: list[configs.CategoriaDePasta]) -> Path | None:
    categoria = encontraCategoria(ficheiro.suffix.lower(), categorias)
    if categoria is not None and categoria.caminho is not None:
        return categoria.caminho
    else:
        logger.error("Não detectou caminho para a categoria '%s' da extensão '%s'", categoria, ficheiro.suffix.lower())
        return None

def encontraCategoria(extensao: str, categorias: list[configs.CategoriaDePasta]) -> configs.CategoriaDePasta | None:
    for categoria in categorias:
        if extensao in categoria.extensoes:
            return categoria
    for categoria in categorias:
        if categoria.defeito:
            return categoria

def apagaFicheiro(ficheiro:Path) -> int:
    if ficheiro.exists():
        ficheiro.unlink()
        logger.info("Eliminou o ficheiro '%s'", ficheiro)
        print(f"{configs.CoresTexto.VERMELHO}{ficheiro} apagado.{configs.CoresTexto.RESET}")
        return 1
    return 0

def ficheirosParaReverter(pastas: set[Path]) -> set[Path]:
    ficheirosParaReverter = set()
    for pasta in pastas:
        for elemento in pasta.iterdir():
            if elemento.is_dir() == False:
                ficheirosParaReverter.add(elemento)
    logger.info("Vai reverter os ficheiros: '%s'", ficheirosParaReverter)
    return ficheirosParaReverter

def datarFicheiro(ficheiro: Path) -> Path:
    data = devolveDataCriacao(ficheiro)
    formato = data.strftime("%y%m%d")
    ficheiroDatado = ficheiro.with_name(formato + "_" + ficheiro.name)

    logger.info("Datou o ficheiro '%s' para '%s'", ficheiro, ficheiroDatado)
    return ficheiroDatado

def devolveDataCriacao(ficheiro: Path) -> datetime.datetime:
    try:
        data = os.stat(ficheiro).st_birthtime
    except AttributeError:
        logger.error("Data de criação indisponível para '%s', vai usar data de modificação.", ficheiro)
        data = os.stat(ficheiro).st_mtime
    
    return datetime.datetime.fromtimestamp(data, tz = None)

def reverteDatarFicheiro(ficheiro: Path) -> Path | None:
    if not verificaDatado(ficheiro):
        return None
    logger.info("Vai reverter o ficheiro '%s'", ficheiro)
    return ficheiro.with_name(ficheiro.name[7:])

def verificaDatado(ficheiro: Path) -> bool:
    if len(ficheiro.name) < 8 or ficheiro.name[6] != "_":
        return False
    prefixo = ficheiro.name[0:6]
    try:
        datetime.datetime.strptime(prefixo, "%y%m%d")
    except ValueError:
        logger.error("Erro a verificar datado ficheiro: '%s'", ficheiro)
        return False
    return True