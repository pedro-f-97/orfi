import orfi.configs
import orfi.pastas


def test_devolvePastas(tmp_path):
    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", set(), tmp_path / "Outros", True),
    ]
    extensoes = {".txt", ".jpg", ".bat"}
    pastasDevolvidas = orfi.pastas.devolvePastas(extensoes, categorias)
    
    assert pastasDevolvidas == {"Docs", "Fotos", "Outros"}

def test_criaPastas(tmp_path):
    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}),
        orfi.configs.CategoriaDePasta("Outros", {""}),
    ]
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    pastasParaCriar = {"Docs", "Fotos", "Outros"}

    for categoria in categorias:
        pastaInexistente = tmp_path / "Destino" / categoria.nome
        assert not pastaInexistente.is_dir()
        assert categoria.caminho is None

    orfi.pastas.criaPastas(pastaDestino, pastasParaCriar, categorias)

    for categoria in categorias:
        pastaExistente = tmp_path / "Destino" / categoria.nome
        assert pastaExistente.is_dir()
        assert categoria.caminho == pastaExistente

def test_pastasExistentes(tmp_path):
    categorias = [
        orfi.configs.CategoriaDePasta("Documentos", {".txt"}),
        orfi.configs.CategoriaDePasta("Imagens", {".jpg"}),
        orfi.configs.CategoriaDePasta("Outros", {""}),
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

    assert orfi.pastas.pastasExistentes(tmp_path, categorias) == pastas

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

    orfi.pastas.eliminaPastasVazias(pastasConjunto)

    for pasta in pastasVazias:
        assert not pasta.exists()
    
    for pasta in pastasConteudo:
        assert pasta.exists()