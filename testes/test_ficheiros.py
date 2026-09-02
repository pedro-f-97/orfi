import datetime
from pathlib import Path

import orfi.configs
import orfi.ficheiros


def test_devolveExt(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "excel.xlsx").touch()
    (tmp_path / "texto.txt").touch()
    (tmp_path / "excel.xlsx").touch()
    resultado = orfi.ficheiros.devolveExt(tmp_path)

    assert resultado == {".jpg", ".txt", ".xlsx"}

def test_devolveFicheiros(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "excel.xlsx").touch()
    (tmp_path / "texto.txt").touch()
    (tmp_path / "excel2.xlsx").touch()
    resultado = orfi.ficheiros.devolveFicheiros(tmp_path)

    assert len(resultado) == 4
    assert set(resultado) == {
        tmp_path / "foto.jpg",
        tmp_path / "excel.xlsx",
        tmp_path / "texto.txt",
        tmp_path / "excel2.xlsx",
    }

def test_copiaFicheiro(tmp_path):
    paraCopiar = (tmp_path / "texto.txt")
    paraCopiar.touch()
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    assert orfi.ficheiros.copiaFicheiro(paraCopiar, pastaDestino) == 1

    ficheiroCopia = Path(pastaDestino / "texto.txt")
    assert ficheiroCopia.exists()
    assert ficheiroCopia.is_file()

def test_existente_copiaFicheiro(tmp_path, monkeypatch):
    paraCopiar = (tmp_path / "texto.txt")
    paraCopiar.touch()
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    (pastaDestino / "texto.txt").touch()
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert orfi.ficheiros.copiaFicheiro(paraCopiar, pastaDestino) == 0

    ficheiroCopia = Path(pastaDestino / "texto.txt")
    assert ficheiroCopia.exists()
    assert ficheiroCopia.is_file()
    

def test_defineDestino(tmp_path):
    categorias = [
        orfi.configs.CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros"),
    ]

    ficheiro = (tmp_path / "img.jpg")
    ficheiro.touch()

    destinoDefinido = orfi.ficheiros.defineDestino(ficheiro, categorias)
    assert destinoDefinido is not None
    assert destinoDefinido == tmp_path  / "Fotos"

def test_encontraCategoria(tmp_path):
    categorias = [
        orfi.configs.CategoriaDePasta("Notas", {".txt"}, tmp_path / "Notas"),
        orfi.configs.CategoriaDePasta("Outros", {""}, tmp_path / "Outros"),
    ]

    categoria = orfi.ficheiros.encontraCategoria(".txt", categorias)

    assert categoria is not None
    assert categoria.nome == "Notas"

def test_moveFicheiro(tmp_path):
    paraMover = (tmp_path / "texto.txt")
    paraMover.touch()
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    assert orfi.ficheiros.moveFicheiro(paraMover, pastaDestino) == 1

    ficheiroMovido = Path(pastaDestino / "texto.txt")
    assert paraMover.exists() == False
    assert ficheiroMovido.exists()
    assert ficheiroMovido.is_file()

def test_existente_moveFicheiro(tmp_path, monkeypatch):
    paraMover = (tmp_path / "texto.txt")
    paraMover.touch()
    pastaDestino = (tmp_path / "Destino")
    pastaDestino.mkdir()
    (pastaDestino / "texto.txt").touch()
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert orfi.ficheiros.moveFicheiro(paraMover, pastaDestino) == 0
    assert paraMover.exists()
    ficheiroMovido = Path(pastaDestino / "texto.txt")
    assert ficheiroMovido.exists()
    assert ficheiroMovido.is_file()

def test_apagaFicheiro(tmp_path):
    paraApagar = (tmp_path / "texto.txt")
    paraApagar.touch()
    assert paraApagar.exists()
    assert orfi.ficheiros.apagaFicheiro(paraApagar) == 1
    assert paraApagar.exists() == False

def test_ficheirosParaReverter(tmp_path):
    pastas = set()
    pastas.add(tmp_path / "Imagens")
    pastas.add(tmp_path / "Documentos")
    for pasta in pastas:
        pasta.mkdir()

    ficheirosGerados = set()
    txtCriar = (tmp_path / "Documentos" / "doc.txt")
    txtCriar.touch()
    ficheirosGerados.add(txtCriar)
    pdfCriar = (tmp_path / "Documentos" / "doc.pdf")
    pdfCriar.touch()
    ficheirosGerados.add(pdfCriar)
    pngCriar = (tmp_path / "Imagens" / "img.png")
    pngCriar.touch()
    ficheirosGerados.add(pngCriar)
    jpgCriar = (tmp_path / "Imagens" / "img.jpg")
    jpgCriar.touch()
    ficheirosGerados.add(jpgCriar)

    paraValidar = orfi.ficheiros.ficheirosParaReverter(pastas)
    assert paraValidar == ficheirosGerados

def test_devolveDataCriacao(tmp_path):
    ficheiro = (tmp_path / "img.jpg")
    ficheiro.touch()
    dataAgora = datetime.datetime.now(tz = None).strftime("%y%m%d")
    assert orfi.ficheiros.devolveDataCriacao(ficheiro).strftime("%y%m%d") == dataAgora

def test_datarFicheiro(tmp_path):
    ficheiro = (tmp_path / "img.jpg")
    ficheiro.touch()
    dataAgora = datetime.datetime.now(tz = None).strftime("%y%m%d")
    ficheiroAlterado = orfi.ficheiros.datarFicheiro(ficheiro)
    assert ficheiroAlterado.name.startswith(dataAgora)
    assert ficheiroAlterado.name.endswith("_img.jpg")