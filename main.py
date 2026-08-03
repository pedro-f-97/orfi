import definePasta, listaFicheiros

pasta = definePasta.inserirPasta()

while pasta is None:
    pasta = definePasta.inserirPasta()

listaFicheiros.mapeiaExt(listaFicheiros.devolveExt(pasta))