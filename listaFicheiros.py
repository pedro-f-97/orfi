from pathlib import Path

def leFicheiros(pasta):
    ext = set()
    for ficheiro in pasta.iterdir():
        if not ficheiro.is_dir():
            ext.add(ficheiro.suffix)
    print(ext) #apenas ficheiros, não pastas