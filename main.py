import pastas, ficheiros

pasta = pastas.definePasta()

while pasta is None:
    pasta = pastas.definePasta()

pastas.devolvePastas(ficheiros.devolveExt(pasta))