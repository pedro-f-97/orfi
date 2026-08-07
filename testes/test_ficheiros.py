from pathlib import Path

import configs
from ficheiros import copiaFicheiro, devolveExt, devolveFicheiros, encontraCategoria


def test_encontra_categoria_imagem():
    categorias = configs.iniciarCategorias()

    categoria = encontraCategoria(".jpg", categorias)

    assert categoria is not None
    assert categoria.nome == "Imagens"

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
    copiaFicheiro(paraCopiar, pastaDestino)

    ficheiroCopia = Path(pastaDestino / "texto.txt")
    assert ficheiroCopia.exists()
    assert ficheiroCopia.is_file()