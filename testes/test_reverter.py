import orfi.configs
import orfi.reverter


def test_reverteMover(tmp_path):
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

    orfi.reverter.reverte(pastaBase, categorias, modo, False, False)

    for pasta in pastasCriadas:
        assert not pasta.exists()
    
    for ficheiro in ficheirosCriados:
        assert not ficheiro.exists()
        assert (pastaBase / ficheiro.name).exists()

def test_reverteCopiar(tmp_path):
    modo = orfi.configs.Modo.COPIAR

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Emails", {".msg"}, tmp_path / "Emails"),
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
    
    orfi.reverter.reverte(pastaBase, categorias, modo, False, False)

    for pasta in pastasCriadas:
        assert pasta.exists()
    
    for ficheiro in ficheirosCriados:
        assert ficheiro.exists()
        assert (pastaBase / ficheiro.name).exists()

def test_reverteSemPastas(tmp_path):
    modo = orfi.configs.Modo.MOVER

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    orfi.reverter.reverte(pastaBase, categorias, modo, False, False)

    assert not any(pastaBase.iterdir())

def test_reverteSemFicheiros(tmp_path):
    modo = orfi.configs.Modo.MOVER

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
    ]

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        pasta.mkdir()
        assert pasta.exists()
    
    orfi.reverter.reverte(pastaBase, categorias, modo, False, False)

    for categoria in categorias:
        pasta = (pastaBase / categoria.nome)
        assert pasta.exists()
        assert not any(pasta.iterdir())

def test_reverteConflito(tmp_path, monkeypatch):
    modo = orfi.configs.Modo.MOVER

    categorias = [
        orfi.configs.CategoriaDePasta("Docs", {".txt"}, tmp_path / "Docs"),
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros", True),
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
    orfi.reverter.reverte(pastaBase, categorias, modo, False, False)

    tipos = set()
    for path in pastaBase.iterdir():
        tipos.add(path.is_dir())
    assert True in tipos and False in tipos

def test_reverteDatar(tmp_path):
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("260131_notas.txt")
    ficheiros.add("250131_doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    orfi.reverter.reverteDatar(pastaBase, modo, False, False)

    for ficheiro in ficheiros:
        assert not (pastaBase / ficheiro).exists()

    cont = 0
    for ficheiro in pastaBase.iterdir():
        cont += 1
    assert cont == 2

def test_reverteDatarCopiar(tmp_path):
    modo = orfi.configs.Modo.COPIAR

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("260131_notas.txt")
    ficheiros.add("250131_doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    orfi.reverter.reverteDatar(pastaBase, modo, False, False)

    for ficheiro in ficheiros:
        assert (pastaBase / ficheiro).exists()
        ficheiroRevertido = pastaBase / ficheiro[7:]
        assert ficheiroRevertido.exists()

def test_reverteSimula(tmp_path):
    simula = True
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

    orfi.reverter.reverte(pastaBase, categorias, modo, False, simula)

    for pasta in pastasCriadas:
        assert pasta.exists()
    
    for ficheiro in ficheirosCriados:
        assert ficheiro.exists()
        assert not (pastaBase / ficheiro.name).exists()

def test_reverteDatarSimula(tmp_path):
    simula = True
    modo = orfi.configs.Modo.MOVER

    pastaBase = (tmp_path / "Base")
    pastaBase.mkdir()

    ficheiros = set()
    ficheiros.add("260131_notas.txt")
    ficheiros.add("250131_doc.pdf")

    for ficheiro in ficheiros:
        (pastaBase / ficheiro).touch()

    orfi.reverter.reverteDatar(pastaBase, modo, False, simula)

    for ficheiro in ficheiros:
        assert (pastaBase / ficheiro).exists()

    cont = 0
    for ficheiro in pastaBase.iterdir():
        cont += 1
    assert cont == 2

def test_reverteSimulacaDeveEliminarPasta(tmp_path, capsys):
    simula = True
    pasta = tmp_path / "teste"
    pasta.mkdir()

    pastaImagens = pasta / "Imagens"
    pastaImagens.mkdir()

    ficheiro = pastaImagens / "imagem.jpg"
    ficheiro.touch()

    categoria = orfi.configs.CategoriaDePasta(
        nome="Imagens",
        caminho=pastaImagens,
        extensoes={".jpg"}
    )

    orfi.reverter.reverte(
        pasta,
        [categoria],
        orfi.configs.Modo.MOVER,
        True,
        simula
    )

    resultado = capsys.readouterr().out

    assert "seria eliminada" in resultado

def test_reverteSimulacaIgnoraPastaSemCategoria(tmp_path, capsys):
    simula = True
    pasta = tmp_path / "teste"
    pasta.mkdir()

    pastaTrabalho = pasta / "Trabalho"
    pastaTrabalho.mkdir()

    ficheiro = pastaTrabalho / "apontamentos.txt"
    ficheiro.touch()

    categoria = orfi.configs.CategoriaDePasta(
        nome="Imagens",
        caminho=pasta / "Imagens",
        extensoes={".jpg"}
    )

    orfi.reverter.reverte(
        pasta,
        [categoria],
        orfi.configs.Modo.MOVER,
        True,
        simula
    )

    resultado = capsys.readouterr().out

    assert not "seria eliminada" in resultado