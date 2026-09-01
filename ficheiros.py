from pathlib import Path
from shutil import copy2, move

import configs


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

def copiaFicheiro(ficheiro: Path, destino: Path) -> int:
    ficheiroFinal = destino / ficheiro.name
    if ficheiroFinal.exists():
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {destino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    copy2(ficheiro, ficheiroFinal)
    print(f"{configs.CoresTexto.VERDE}{ficheiro.name} copiado{configs.CoresTexto.RESET}")
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

def moveFicheiro(ficheiro: Path, destino: Path) -> int:
    ficheiroFinal = destino / ficheiro.name
    if ficheiroFinal.exists():
        resposta = input(f"{configs.CoresTexto.AMARELO}Já existe o ficheiro {ficheiro.name} na pasta {destino}, substituir? (s/n): {configs.CoresTexto.RESET}")
        if resposta.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}{ficheiro.name} cancelado.{configs.CoresTexto.RESET}")
            return 0
    try:
        move(ficheiro, ficheiroFinal)
    except OSError as erro:
        print(f"{configs.CoresTexto.VERMELHO}Erro ao mover {ficheiro.name}: {erro}{configs.CoresTexto.RESET}")
        return 0
    print(f"{configs.CoresTexto.VERDE}{ficheiro.name} movido{configs.CoresTexto.RESET}")
    return 1 

def ficheirosParaReverter(pastas: set) -> set[Path]:
    ficheirosParaReverter = set()
    for pasta in pastas:
        for elemento in pasta.iterdir():
            if elemento.is_dir() == False:
                ficheirosParaReverter.add(elemento)
    return ficheirosParaReverter