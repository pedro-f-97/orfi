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

pastas.criaPastas(pasta, pastasParaCriar, categorias)

ficheirosLista = ficheiros.devolveFicheiros(pasta)

caminhoOutros = pastas.trataCaminhoOutros(categorias)

ficheiros.encaminhaCopias(ficheirosLista, caminhoOutros, categorias)