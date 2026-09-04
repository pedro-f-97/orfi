import orfi.configs
import orfi.organizar


def test_organizaMover(tmp_path, monkeypatch):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt", ".pdf"}, pastaBase / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg", ".png"}, pastaBase / "Fotos"),
        orfi.configs.CategoriaDePasta("Emails", {".msg"}, pastaBase / "Emails"),
    ]

    ficheiros = set()
    ficheiros.add("text.txt")
    ficheiros.add("dec.pdf")
    ficheiros.add("img.jpg")
    ficheiros.add("foto.png")
    ficheiros.add("mail.msg")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    monkeypatch.setattr("builtins.input", lambda _: "s")
    orfi.organizar.organiza(pastaBase, categorias, modo, False)

    for path in pastaBase.iterdir():
        assert path.is_dir()
        for categoria in categorias:
            if categoria.nome == path.name:
                for ficheiro in path.iterdir():
                    extensoes = categoria.extensoes
                    assert ficheiro.suffix in extensoes
                    ficheiros.discard(ficheiro.name)
    assert not ficheiros

def test_organizaForce(tmp_path):
    modo = orfi.configs.Modo.MOVER
    force = True
    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()
    pastaDocs = pastaBase / "Docs"

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt", ".pdf"}, pastaDocs),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg", ".png"}, pastaBase / "Fotos"),
        orfi.configs.CategoriaDePasta("Emails", {".msg"}, pastaBase / "Emails"),
    ]



    ficheiros = set()
    ficheiros.add("text.txt")
    ficheiros.add("dec.pdf")
    ficheiros.add("img.jpg")
    ficheiros.add("foto.png")
    ficheiros.add("mail.msg")

    ficheiroExistente = (pastaDocs / "text.txt")
    ficheiroExistente.parent.mkdir()
    ficheiroExistente.write_text("antigo")

    (pastaBase / "text.txt").write_text("organizado")

    for ficheiro in ficheiros:
        if ficheiro != "text.txt":
            (pastaBase / ficheiro).touch()

    orfi.organizar.organiza(pastaBase, categorias, modo, force)

    for path in pastaBase.iterdir():
        assert path.is_dir()
        for categoria in categorias:
            if categoria.nome == path.name:
                for ficheiro in path.iterdir():
                    extensoes = categoria.extensoes
                    assert ficheiro.suffix in extensoes
                    ficheiros.discard(ficheiro.name)
    assert (pastaDocs / "text.txt").read_text() == "organizado"
    assert not ficheiros

def test_organizaCopiar(tmp_path, monkeypatch):
    modo = orfi.configs.Modo.COPIAR

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt", ".pdf"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg", ".png"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
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
    orfi.organizar.organiza(pastaBase, categorias, modo, False)

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
    modo = orfi.configs.Modo.MOVER

    categorias = [
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("outro.bat")
    ficheiros.add("comp.zip")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    monkeypatch.setattr("builtins.input", lambda _: "s")
    orfi.organizar.organiza(pastaBase, categorias, modo, False)

    for ficheiro in ficheiros:
        assert not (pastaBase / ficheiro).exists()

    for categoria in categorias:
        if categoria.defeito:
            for path in (pastaBase / categoria.nome).iterdir():
                if path.name in ficheiros:
                    ficheiros.discard(path.name)
    assert not ficheiros

def test_organizaVazio(tmp_path):
    modo = orfi.configs.Modo.MOVER

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    orfi.organizar.organiza(pastaBase, categorias, modo, False)

    for categoria in categorias:
        assert not (pastaBase / categoria.nome).exists()

def test_datar(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("notas.txt")
    ficheiros.add("doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    orfi.organizar.datar(pastaBase, modo, False)

    for ficheiro in ficheiros:
        assert not (pastaBase / ficheiro).exists()

    cont = 0
    for ficheiro in pastaBase.iterdir():
        if ficheiro.name[7:] in ficheiros:
            cont += 1
    assert cont == 2


def test_datarCopiar(tmp_path):
    modo = orfi.configs.Modo.COPIAR

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("notas.txt")
    ficheiros.add("doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    orfi.organizar.datar(pastaBase, modo, False)

    for ficheiro in ficheiros:
        assert (pastaBase / ficheiro).exists()

    cont = 0
    contAlterado = 0
    for ficheiro in pastaBase.iterdir():
        if ficheiro.name in ficheiros:
            cont += 1
        else:
            contAlterado += 1
    assert cont == 2
    assert contAlterado == 2