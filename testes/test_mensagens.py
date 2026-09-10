import orfi.mensagens


def test_definirIdioma():
    idiomaActual = orfi.mensagens.idioma
    if idiomaActual == 'pt':
        novoIdioma = 'en'
    else:
        novoIdioma = 'pt'
    
    orfi.mensagens.definirIdioma(novoIdioma)
    assert novoIdioma == orfi.mensagens.idioma

def test_mensagemTrataIdioma():
    orfi.mensagens.definirIdioma('pt')
    teste = orfi.mensagens.mensagemTrataIdioma('ficheiro_existente_substituir', ficheiro="teste", destino="teste")

    assert teste == "Já existe o ficheiro teste na pasta teste, substituir? (s/n): "

def test_mensagem(capsys):
    orfi.mensagens.definirIdioma('pt')
    orfi.mensagens.mensagem("ficheiro_cancelado", "ficheiro_cancelado", False, orfi.mensagens.CoresTexto.AMARELO, ficheiro="teste")
    teste = capsys.readouterr()
    assert "Ficheiro teste cancelado." in teste.out