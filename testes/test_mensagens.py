import orfi.mensagens


def test_definirIdioma():
    idiomaActual = orfi.mensagens.idioma
    if idiomaActual == 'pt':
        novoIdioma = 'en'
    else:
        novoIdioma = 'pt'
    
    assert orfi.mensagens.definirIdioma(novoIdioma)
    assert novoIdioma == orfi.mensagens.idioma

def test_definirIdiomaErro():
    idioma = orfi.mensagens.idioma
    assert not orfi.mensagens.definirIdioma("xx")
    assert orfi.mensagens.idioma == idioma

def test_mensagemTrataIdioma():
    orfi.mensagens.definirIdioma('pt')
    teste = orfi.mensagens.mensagemTrataIdioma('ficheiro_existente_substituir', ficheiro="teste", destino="teste")

    assert teste == "Já existe o ficheiro teste na pasta teste, substituir? (s/n): "
