from pathlib import Path

from configs import CategoriaDePasta
from ficheiros import (
    copiaFicheiro,
    defineDestino,
    devolveExt,
    devolveFicheiros,
    encontraCategoria,
)


def test_devolveExt(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "excel.xlsx").touch()
    (tmp_path / "texto.txt").touch()
    (tmp_path / "excel.xlsx").touch()
    resultado = devolveExt(tmp_path)

    assert resultado == {".jpg", ".txt", ".xlsx"}

def test_devolveFicheiros(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "excel.xlsx").touch()
    (tmp_path / "texto.txt").touch()
    (tmp_path / "excel2.xlsx").touch()
    resultado = devolveFicheiros(tmp_path)

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
    assert copiaFicheiro(paraCopiar, pastaDestino) == 1

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
    assert copiaFicheiro(paraCopiar, pastaDestino) == 0

    ficheiroCopia = Path(pastaDestino / "texto.txt")
    assert ficheiroCopia.exists()
    assert ficheiroCopia.is_file()
    

def test_defineDestino(tmp_path):
    categorias = [
        CategoriaDePasta("Fotos", {".jpg"}, tmp_path / "Fotos"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros"),
    ]

    ficheiro = (tmp_path / "img.jpg")
    ficheiro.touch()

    destinoDefinido = defineDestino(ficheiro, categorias)
    assert destinoDefinido is not None
    assert destinoDefinido == tmp_path  / "Fotos"

def test_encaminhaCopias():
    
    print()

def test_encontraCategoria(tmp_path):
    categorias = [
        CategoriaDePasta("Notas", {".txt"}, tmp_path / "Notas"),
        CategoriaDePasta("Outros", {""}, tmp_path / "Outros"),
    ]

    categoria = encontraCategoria(".txt", categorias)

    assert categoria is not None
    assert categoria.nome == "Notas"