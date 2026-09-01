from configs import CategoriaDePasta, Modo
from organizar import organiza


def test_organizaMover(tmp_path, monkeypatch):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt", ".pdf"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg", ".png"}, tmp_path / "Fotos"),
        CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("text.txt")
    ficheiros.add("dec.pdf")
    ficheiros.add("img.jpg")
    ficheiros.add("foto.png")
    ficheiros.add("mail.msg")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    monkeypatch.setattr("builtins.input", lambda _: "s")
    organiza(pastaBase, categorias, modo)

    for path in pastaBase.iterdir():
        assert path.is_dir()
        for categoria in categorias:
            if categoria.nome == path.name:
                for ficheiro in path.iterdir():
                    extensoes = categoria.extensoes
                    assert ficheiro.suffix in extensoes
                    ficheiros.discard(ficheiro.name)
    assert not ficheiros

def test_organizaCopiar(tmp_path, monkeypatch):
    modo = Modo.COPIAR

    categorias = [
        CategoriaDePasta("Docs", {".txt", ".pdf"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg", ".png"}, tmp_path / "Fotos"),
        CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("text.txt")
    ficheiros.add("dec.pdf")
    ficheiros.add("img.jpg")
    ficheiros.add("foto.png")
    ficheiros.add("mail.msg")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    monkeypatch.setattr("builtins.input", lambda _: "s")
    organiza(pastaBase, categorias, modo)

    ficheirosBase = set()
    ficheirosCopiados = set()
    for path in pastaBase.iterdir():
        if path.is_dir():
            for categoria in categorias:
                if categoria.nome == path.name:
                    for ficheiro in path.iterdir():
                        extensoes = categoria.extensoes
                        assert ficheiro.suffix in extensoes
                        ficheirosCopiados.add(ficheiro.name)
        elif not path.is_dir():
            ficheirosBase.add(path.name)
    assert ficheirosBase == ficheiros
    assert ficheirosCopiados == ficheiros

def test_organizaOutros(tmp_path, monkeypatch):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("outro.bat")
    ficheiros.add("comp.zip")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    monkeypatch.setattr("builtins.input", lambda _: "s")
    organiza(pastaBase, categorias, modo)

    for ficheiro in ficheiros:
        assert not (pastaBase / ficheiro).exists()

    for categoria in categorias:
        if categoria.defeito:
            for path in (pastaBase / categoria.nome).iterdir():
                if path.name in ficheiros:
                    ficheiros.discard(path.name)
    assert not ficheiros

def test_organizaVazio(tmp_path):
    modo = Modo.MOVER

    categorias = [
        CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    organiza(pastaBase, categorias, modo)

    for categoria in categorias:
        assert not (pastaBase / categoria.nome).exists()