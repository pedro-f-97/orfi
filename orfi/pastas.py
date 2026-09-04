import logging
from pathlib import Path

from . import configs, ficheiros

logger = logging.getLogger(__name__)

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
        

def criaPastas(caminho: Path, pastas: set[str], categorias: list[configs.CategoriaDePasta], simula: bool) -> int:
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
                print(f"{configs.CoresTexto.AMARELO}Pasta criada - {pasta}{configs.CoresTexto.RESET}")
            else:
                print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Pasta {pasta} seria criada.{configs.CoresTexto.RESET}")
            cont += 1
        else:
            print(f"{configs.CoresTexto.AMARELO}Pasta {pasta} já existe. {configs.CoresTexto.RESET}")
    return cont

def pastasExistentes(caminho: Path, categorias: list[configs.CategoriaDePasta]) -> set[Path]:
    pastasParaReverter = set()
    for pasta in caminho.iterdir():
        if pasta.is_dir():
            for categoria in categorias:
                if pasta.stem == categoria.nome:
                    pastasParaReverter.add(pasta)
    return pastasParaReverter

def eliminaPastasVazias(pastasParaReverter: set[Path], simula: bool):
    for pasta in pastasParaReverter:
            if not any(pasta.iterdir()):
                if not simula:
                    print(f"{configs.CoresTexto.VERDE}Pasta vazia '{pasta}' foi eliminada.{configs.CoresTexto.RESET}")
                    logger.info("Eliminou pasta: %s", pasta)
                    pasta.rmdir()
                else:
                    print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Pasta {pasta} seria eliminada.{configs.CoresTexto.RESET}")