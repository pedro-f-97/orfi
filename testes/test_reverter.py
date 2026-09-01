from configs import CategoriaDePasta, Modo
from reverter import reverte


def test_reverteMover(tmp_path):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    pastasCriadas = set()
    ficheirosCriados = set()

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        pasta.mkdir()
        pastasCriadas.add(pasta)
        assert pasta.exists()
        for ext in categoria.extensoes:
            ficheiro = (pasta / ("abc" + ext))
            ficheiro.touch()
            ficheirosCriados.add(ficheiro)
            assert ficheiro.exists()

    reverte(pastaBase, categorias, modo)

    for pasta in pastasCriadas:
        assert not pasta.exists()
    
    for ficheiro in ficheirosCriados:
        assert not ficheiro.exists()
        assert (pastaBase / ficheiro.name).exists()

def test_reverteCopiar(tmp_path):
    modo = Modo.COPIAR

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    pastasCriadas = set()
    ficheirosCriados = set()

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        pasta.mkdir()
        pastasCriadas.add(pasta)
        assert pasta.exists()
        for ext in categoria.extensoes:
            ficheiro = (pasta / ("abc" + ext))
            ficheiro.touch()
            ficheirosCriados.add(ficheiro)
            assert ficheiro.exists()
    
    reverte(pastaBase, categorias, modo)

    for pasta in pastasCriadas:
        assert pasta.exists()
    
    for ficheiro in ficheirosCriados:
        assert ficheiro.exists()
        assert (pastaBase / ficheiro.name).exists()

def test_reverteSemPastas(tmp_path):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    reverte(pastaBase, categorias, modo)

    assert not any(pastaBase.iterdir())

def test_reverteSemFicheiros(tmp_path):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        pasta.mkdir()
        assert pasta.exists()
    
    reverte(pastaBase, categorias, modo)

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        assert pasta.exists()
        assert not any(pasta.iterdir())

def test_reverteConflito(tmp_path, monkeypatch):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        pasta.mkdir()
        if categoria.nome == "Docs":
            ficheiro = (pasta / "notas.txt")
            ficheiro.touch()
        if categoria.nome == "Fotos":
            ficheiro = (pasta / "img.jpg")
            ficheiro.touch()
        if categoria.nome == "Outros":
            ficheiro = (pasta / "notas.txt")
            ficheiro.touch()

    monkeypatch.setattr("builtins.input", lambda _: "n")
    reverte(pastaBase, categorias, modo)

    tipos = set()
    for path in pastaBase.iterdir():
        tipos.add(path.is_dir())
    assert True in tipos and False in tipos