from pathlib import Path

from configs import CATEGORIAS


def definePasta() -> Path | None:
    pasta = ""
    pasta = input("Definir pasta para organizar: ")

    vPasta = Path(pasta)
    if vPasta.is_dir() == True:
        return vPasta
    else:
        return

def devolvePastas(setExt: set[str]) -> set[str]:
    pastas = set()

    for ext in setExt:
        pastas.add(CATEGORIAS.get(ext, "Outros"))
    if len(pastas) > 0:
        print("Pastas para criar: ", pastas)
        return pastas
        #criar pastas do set
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
