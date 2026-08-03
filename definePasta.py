from pathlib import Path

def inserirPasta():
    pasta = ""
    pasta = input("Definir pasta para organizar: ")

    vPasta = Path(pasta)
    if vPasta.is_dir() == True:
        return vPasta
    else:
        return
