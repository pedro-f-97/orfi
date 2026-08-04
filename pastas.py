from pathlib import Path

from configs import CategoriaDePasta


def definePasta() -> Path | None:
    pasta = ""
    pasta = input("Definir pasta para organizar: ")

    vPasta = Path(pasta)
    if vPasta.is_dir() == True:
        return vPasta
    else:
        return

def devolvePastas(setExt: set[str], categorias: list[CategoriaDePasta]) -> set[str]:
    pastas = set()
    
    for ext in setExt:
        temCategoria = False
        for categoria in categorias:
            if ext in categoria.extensoes:
                pastas.add(categoria.nome)
                temCategoria = True
        if temCategoria == False:
            pastas.add("Outros")
    if len(pastas) > 0:
        print("Pastas para criar: ", pastas)
        return pastas
    else:
        print("Não vai criar pastas.")
        return pastas
        

def criaPastas(caminho: Path, pastas: set[str]):
    confirmacao = input(f"Criar as pastas {pastas}? (s/n): ")
    if confirmacao.lower() == "s":
        for pasta in pastas:
            caminhoFinal = caminho / pasta
            if not caminhoFinal.exists():
                caminhoFinal.mkdir(parents = False, exist_ok = True)
                print(f"Pasta criada - {pasta}")
            else:
                print(f"Pasta {pasta} já existe. ")
    else:
        print("Operação Cancelada")
