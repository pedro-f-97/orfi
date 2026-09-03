import datetime
import os
from pathlib import Path
from shutil import copy2, move

from . import configs


def devolveExt(pasta: Path) -> set[str]:
    ext: set[str] = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        print(f"{configs.CoresTexto.AZUL}Extensões existentes: {ext} {configs.CoresTexto.RESET}") 
    return ext

def devolveFicheiros(pasta: Path) -> list[Path]:
    listaFicheiros = []
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            listaFicheiros.append(ficheiro)
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
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        return 0
    print(f"{configs.CoresTexto.VERDE}{ficheiro.name} copiado{configs.CoresTexto.RESET}")
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
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro '{erro}' no ficheiro {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        return 0
    print(f"{configs.CoresTexto.VERDE}{ficheiro.name} movido{configs.CoresTexto.RESET}")
    return 1 

def defineDestino(ficheiro:Path, categorias: list[configs.CategoriaDePasta]) -> Path | None:
    categoria = encontraCategoria(ficheiro.suffix.lower(), categorias)
    if categoria is not None and categoria.caminho is not None:
        return categoria.caminho
    else:
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
        print(f"{configs.CoresTexto.VERMELHO}{ficheiro} apagado.{configs.CoresTexto.RESET}")
        return 1
    return 0

def ficheirosParaReverter(pastas: set[Path]) -> set[Path]:
    ficheirosParaReverter = set()
    for pasta in pastas:
        for elemento in pasta.iterdir():
            if elemento.is_dir() == False:
                ficheirosParaReverter.add(elemento)
    return ficheirosParaReverter

def datarFicheiro(ficheiro: Path) -> Path:
    data = devolveDataCriacao(ficheiro)
    formato = data.strftime("%y%m%d")

    return ficheiro.with_name(formato + "_" + ficheiro.name)

def devolveDataCriacao(ficheiro: Path) -> datetime.datetime:
    data = float
    try:
        data = os.stat(ficheiro).st_birthtime
    except AttributeError:
        data = os.stat(ficheiro).st_mtime
    
    return datetime.datetime.fromtimestamp(data, tz = None)

def reverteDatarFicheiro(ficheiro: Path) -> Path | None:
    if not verificaDatado(ficheiro):
        return None
    return ficheiro.with_name(ficheiro.name[7:])

def verificaDatado(ficheiro: Path) -> bool:
    if len(ficheiro.name) < 8 or ficheiro.name[6] != "_":
        return False
    prefixo = ficheiro.name[0:6]
    try:
        datetime.datetime.strptime(prefixo, "%y%m%d")
    except ValueError:
        return False
    return True