import sys

import configs
import ficheiros
import pastas

pasta = pastas.definePasta()

while pasta is None:
    pasta = pastas.definePasta()

categorias = configs.iniciarCategorias()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta), categorias)

if pastasParaCriar == set():
    print("Nada para fazer.")
    sys.exit()

cancelar = pastas.criaPastas(pasta, pastasParaCriar, categorias)
if cancelar:
    sys.exit()

ficheirosLista = ficheiros.devolveFicheiros(pasta)

ficheiros.encaminhaCopias(ficheirosLista, categorias)