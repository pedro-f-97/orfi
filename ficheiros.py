from pathlib import Path
from shutil import copy2

from configs import CategoriaDePasta


def devolveExt(pasta: Path) -> set[str]:
    ext: set[str] = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        print("Extensões existentes: ", ext) 
    return ext

def devolveFicheiros(pasta: Path) -> list[Path]:
    listaFicheiros = []
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            listaFicheiros.append(ficheiro)
    return listaFicheiros

def copiaFicheiro(ficheiro: Path, destino: Path):
    # 1º tem de preparar o caminho inteiro do ficheiro no destino, juntando destino / ficheiro, ex "C:\Users\pedroferreira\Documents\exemplo.jpg"
    ficheiroFinal = destino / ficheiro.name
    # 2º condição se, caso já exista um ficheiro com o mesmo nome no destino, pergunta se quer substituir o existente
    if ficheiroFinal.exists():
        resposta = input(f"Já existe o ficheiro {ficheiro.name} na pasta {destino}, substituir? (s/n): ")
        if resposta.lower() != "s":
            print("Cancelado")
            return
    # 3º se resposta for sim ou condição se for falsa, copia o ficheiro
    copy2(ficheiro, ficheiroFinal)
    print(f"{ficheiro.name} copiado") 

def defineDestino(ficheiro:Path, categorias: list[CategoriaDePasta]) -> Path | None:
    categoria = encontraCategoria(ficheiro.suffix.lower(), categorias)
    if categoria is not None and categoria.caminho is not None:
        return categoria.caminho
    else:
        return None

def encontraCategoria(extensao: str, categorias: list[CategoriaDePasta]) -> CategoriaDePasta | None:
    for categoria in categorias:
        if extensao in categoria.extensoes:
            return categoria
    for categoria in categorias:
        if categoria.nome=="Outros":
            return categoria
            
            
