from pathlib import Path

from configs import CategoriaDePasta
from ficheiros import encontraCategoria


def devolvePastas(setExt: set[str], categorias: list[CategoriaDePasta]) -> set[str]:
    pastas = set()
    
    for ext in setExt:
        categoria = encontraCategoria(ext, categorias)
        if categoria is not None:
            pastas.add(categoria.nome)
        else:
            print(f"Categoria não encontrada para {ext}")
    if len(pastas) > 0:
        print("Pastas para criar: ", pastas)
    else:
        print("Não vai criar pastas.")
    return pastas
        

def criaPastas(caminho: Path, pastas: set[str], categorias: list[CategoriaDePasta]):
    for pasta in pastas:
        caminhoFinal = caminho / pasta
        for categoria in categorias:
            if pasta == categoria.nome:
                categoria.caminho = caminhoFinal
        if not caminhoFinal.exists():
            caminhoFinal.mkdir(parents = False, exist_ok = True)
            print(f"Pasta criada - {pasta}")
        else:
            print(f"Pasta {pasta} já existe. ")