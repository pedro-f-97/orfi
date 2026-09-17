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
    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, False, False, 1)

    assert resultados.pastasCriadas == len(categorias)
    assert resultados.ficheirosTratados == len(ficheiros)

    for path in pastaBase.iterdir():
        assert path.is_dir()
        for categoria in categorias:
            if categoria.nome == path.name:
                for ficheiro in path.iterdir():
                    extensoes = categoria.extensoes
                    assert ficheiro.suffix in extensoes
                    ficheiros.discard(ficheiro.name)
    assert not ficheiros

def test_organizaForcePastaExistenteComFicheiro(tmp_path):
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

    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, force, False, 1)

    assert resultados.pastasCriadas == len(categorias) - 1
    assert resultados.ficheirosTratados == len(ficheiros)

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
    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, False, False, 1)

    assert resultados.pastasCriadas == len(categorias)
    assert resultados.ficheirosTratados == len(ficheiros)

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
    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, False, False, 1)
    
    assert resultados.pastasCriadas == len(categorias) - 1
    assert resultados.ficheirosTratados == len(ficheiros)

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

    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, False, False, 1)

    assert resultados.ficheirosTratados == 0
    assert resultados.pastasCriadas == 0

    for categoria in categorias:
        assert not (pastaBase / categoria.nome).exists()

def test_organizaSimula(tmp_path, monkeypatch):
    modo = orfi.configs.Modo.MOVER
    simula = True

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
    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, False, simula, 1)
    
    assert resultados.ficheirosTratados == len(ficheiros)
    assert resultados.pastasCriadas == len(categorias)

    for path in pastaBase.iterdir():
        assert not path.is_dir()
        ficheiros.discard(path.name)
    assert not ficheiros

def test_organizaNiveis(tmp_path, monkeypatch):
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

    pastaNivel2 = (pastaBase / "Nivel2")
    pastaNivel2.mkdir()
    (pastaNivel2 / "text2.txt").touch()
    ficheiros.add("text2.txt")

    pastaNivel3 = (pastaNivel2 / "Nivel3")
    pastaNivel3.mkdir()
    (pastaNivel3 / "foto3.jpg").touch()
    ficheiros.add("foto3.jpg")

    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, True, False, 3)

    assert resultados.pastasCriadas == len(categorias)
    assert resultados.ficheirosTratados == len(ficheiros)

    for path in pastaBase.iterdir():
        assert path.is_dir()
        for categoria in categorias:
            if categoria.nome == path.name:
                for ficheiro in path.iterdir():
                    extensoes = categoria.extensoes
                    assert ficheiro.suffix in extensoes
                    ficheiros.discard(ficheiro.name)
    assert not ficheiros

def test_organizaNiveisExtensoesRecursivas(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = tmp_path / "Base"
    pastaBase.mkdir()

    categorias = [
        orfi.configs.CategoriaDePasta(
            "Docs", {".txt", ".pdf"}, pastaBase / "Docs"
        ),
        orfi.configs.CategoriaDePasta(
            "Fotos", {".jpg", ".png"}, pastaBase / "Fotos"
        ),
    ]

    (pastaBase / "texto.txt").touch()

    subpasta = pastaBase / "Subpasta"
    subpasta.mkdir()
    (subpasta / "foto.jpg").touch()

    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, True, False, 2)

    assert resultados.pastasCriadas == 2
    assert resultados.ficheirosTratados == 2

    assert (pastaBase / "Docs" / "texto.txt").exists()
    assert (pastaBase / "Fotos" / "foto.jpg").exists()

def test_organizaPastaJaOrganizadaRecursivo(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, pastaBase / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, pastaBase / "Fotos"),
        orfi.configs.CategoriaDePasta("Emails", {".msg"}, pastaBase / "Emails"),
    ]

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

    resultados = orfi.organizar.organiza(pastaBase, categorias, modo, True, False, 2)

    assert resultados.ficheirosTratados == 0
    assert resultados.pastasCriadas == 0
    assert resultados.pastasEliminadas == 0

def test_datar(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("notas.txt")
    ficheiros.add("doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    resultados = orfi.organizar.datar(pastaBase, modo, False, False, 1)

    assert resultados.ficheirosTratados == len(ficheiros)
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

    resultados = orfi.organizar.datar(pastaBase, modo, False, False, 1)

    assert resultados.ficheirosTratados == len(ficheiros)
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

def test_datarSimula(tmp_path):
    simula = True
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("notas.txt")
    ficheiros.add("doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    resultados = orfi.organizar.datar(pastaBase, modo, False, simula, 1)

    assert resultados.ficheirosTratados == len(ficheiros)
    for ficheiro in ficheiros:
        assert (pastaBase / ficheiro).exists()

    for ficheiro in pastaBase.iterdir():
        assert not ficheiro.name[7:] in ficheiros

def test_datarDatado(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("260911_notas.txt")
    ficheiros.add("260910_doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    resultados = orfi.organizar.datar(pastaBase, modo, False, False, 1)

    assert resultados.ficheirosTratados == 0
    for ficheiro in ficheiros:
        assert (pastaBase / ficheiro).exists()

def test_datarNiveis(tmp_path):
    modo = orfi.configs.Modo.MOVER
    nivel = 3

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    pastaNivel2 = (pastaBase / "nivel2")
    pastaNivel2.mkdir()

    pastaNivel3 = (pastaNivel2 / "nivel3")
    pastaNivel3.mkdir()

    ficheiros = set()
    ficheiros.add(pastaBase / "notas.txt")
    ficheiros.add(pastaBase / "doc.pdf")
    ficheiros.add(pastaNivel2 / "img2.jpg")
    ficheiros.add(pastaNivel3 / "calc.xlsx")

    for ficheiro in ficheiros:
        ficheiro.touch()

    resultados = orfi.organizar.datar(pastaBase, modo, False, False, nivel)

    assert resultados.ficheirosTratados == len(ficheiros)
    for ficheiro in ficheiros:
        assert not ficheiro.exists()
