from configs import CategoriaDePasta
from pastas import criaPastas, devolvePastas, eliminaPastasVazias, pastasExistentes


def test_devolvePastas(tmp_path):
    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", set(), tmp_path / "Outros", True),
    ]
    extensoes = {".txt", ".jpg", ".bat"}
    pastasDevolvidas = devolvePastas(extensoes, categorias)
    
    assert pastasDevolvidas == {"Docs", "Fotos", "Outros"}

def test_criaPastas(tmp_path):
    categorias = [
        CategoriaDePasta("Docs", {".txt"}),
        CategoriaDePasta("Fotos", {".jpg"}),
        CategoriaDePasta("Outros", {""}),
    ]
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    pastasParaCriar = {"Docs", "Fotos", "Outros"}

    for categoria in categorias:
        pastaInexistente = tmp_path / "Destino" / categoria.nome
        assert not pastaInexistente.is_dir()
        assert categoria.caminho is None

    criaPastas(pastaDestino, pastasParaCriar, categorias)

    for categoria in categorias:
        pastaExistente = tmp_path / "Destino" / categoria.nome
        assert pastaExistente.is_dir()
        assert categoria.caminho == pastaExistente

def test_pastasExistentes(tmp_path):
    categorias = [
        CategoriaDePasta("Documentos", {".txt"}),
        CategoriaDePasta("Imagens", {".jpg"}),
        CategoriaDePasta("Outros", {""}),
    ]

    pastas = set()
    pastas.add(tmp_path / "Imagens")
    pastas.add(tmp_path / "Documentos")
    for pasta in pastas:
        pasta.mkdir()

    lixo = (tmp_path / "ficheiro.txt")
    lixo.touch()
    lixo = (tmp_path / "PastaIncrivel")
    lixo.mkdir()

    assert pastasExistentes(tmp_path, categorias) == pastas

def test_eliminaPastasVazias(tmp_path):
    pastasVazias = set()
    pastasVazias.add(tmp_path / "Imagens")
    pastasVazias.add(tmp_path / "Documentos")
    for pasta in pastasVazias:
        pasta.mkdir()
    
    pastasConteudo = set()
    pastasConteudo.add(tmp_path / "Coisas")
    pastasConteudo.add(tmp_path / "Projecto_A")
    for pasta in pastasConteudo:
        pasta.mkdir()
        ficheiro = (pasta / "ficheiro.txt")
        ficheiro.touch()

    pastasConjunto = pastasVazias.union(pastasConteudo)

    eliminaPastasVazias(pastasConjunto)

    for pasta in pastasVazias:
        assert not pasta.exists()
    
    for pasta in pastasConteudo:
        assert pasta.exists()