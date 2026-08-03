from pathlib import Path

def definePasta():
    pasta = ""
    pasta = input("Definir pasta para organizar: ")

    vPasta = Path(pasta)
    if vPasta.is_dir() == True:
        return vPasta
    else:
        return

def devolvePastas(setExt):
    categorias = dict()
    pastas = set()
    categorias = {
        ".jpg": "Imagens",
        ".png": "Imagens",
        ".txt": "Documentos",
        ".docx": "Documentos",
        ".xlsx": "Folhas de cálculo"
    } 

    for ext in setExt:
        pastas.add(categorias.get(ext, "Outros"))
    if len(pastas) > 0:
        print("Pastas para criar: ", pastas)
        return pastas
        #criar pastas do set
    else:
        print("Não vai criar pastas.")

def criaPastas(caminho, pastas):
    confirmacao = input(f"Criar as pastas {pastas}? (s/n)")
    if confirmacao == "s":
        for pasta in pastas:
            caminhoFinal = caminho / pasta
            caminhoFinal.mkdir(parents = False, exist_ok = True)
            print("Pastas criadas")
    else:
        print("Operação Cancelada")