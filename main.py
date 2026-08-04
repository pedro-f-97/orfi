import ficheiros
import pastas

pasta = pastas.definePasta()

while pasta is None:
    pasta = pastas.definePasta()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta))

pastas.criaPastas(pasta, pastasParaCriar)