from pathlib import Path

from . import configs, ficheiros


def devolvePastas(setExt: set[str], categorias: list[configs.CategoriaDePasta]) -> set[str]:
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
        

def criaPastas(caminho: Path, pastas: set[str], categorias: list[configs.CategoriaDePasta]):
    for pasta in pastas:
        caminhoFinal = caminho / pasta
        for categoria in categorias:
            if pasta == categoria.nome:
                categoria.caminho = caminhoFinal
        if not caminhoFinal.exists():
            caminhoFinal.mkdir(parents = False, exist_ok = True)
            print(f"{configs.CoresTexto.VERDE}Pasta criada - {pasta}{configs.CoresTexto.RESET}")
        else:
            print(f"{configs.CoresTexto.AMARELO}Pasta {pasta} já existe. {configs.CoresTexto.RESET}")

def pastasExistentes(caminho: Path, categorias: list[configs.CategoriaDePasta]) -> set[Path]:
    pastasParaReverter = set()
    for pasta in caminho.iterdir():
        if pasta.is_dir():
            for categoria in categorias:
                if pasta.stem == categoria.nome:
                    pastasParaReverter.add(pasta)
    return pastasParaReverter

def eliminaPastasVazias(pastasParaReverter: set[Path]):
    for pasta in pastasParaReverter:
            if not any(pasta.iterdir()):
                print(f"{configs.CoresTexto.VERDE}Pasta vazia '{pasta}' foi eliminada.{configs.CoresTexto.RESET}")
                pasta.rmdir()