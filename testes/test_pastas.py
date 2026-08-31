from configs import CategoriaDePasta
from pastas import criaPastas, devolvePastas


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