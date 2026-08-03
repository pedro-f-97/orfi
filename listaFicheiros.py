from pathlib import Path

def devolveExt(pasta):
    ext = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir(): #apenas ficheiros, não pastas
            ext.add(ficheiro.suffix.lower())
    if len(ext) > 0:
        print("Extensões existentes: ", ext) 
        return ext
    else:
        return None

def mapeiaExt(setExt):
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
        #criar pastas do set
    else:
        print("Não vai criar pastas.")
