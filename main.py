import sys

import ficheiros
import pastas

pasta = pastas.definePasta()

while pasta is None:
    pasta = pastas.definePasta()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta))

if pastasParaCriar == set():
    print("Nada para fazer.")
    sys.exit()

pastas.criaPastas(pasta, pastasParaCriar)

