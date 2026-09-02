import tomllib
from pathlib import Path

import orfi.configs


def simulaConfiguracao(configuracao: str, tmp_path) -> list[orfi.configs.CategoriaDePasta]:
    caminho = tmp_path / "config.toml"
    caminho.write_text(configuracao, encoding="utf-8")

    categorias = orfi.configs.carregarConfiguracao(caminho)
    return categorias

def test_caminhoConfiguracaoWindows(monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    monkeypatch.setenv("APPDATA", r"C:\Teste\AppData")

    caminho = orfi.configs.caminhoConfiguracao()

    assert caminho == Path(r"C:\Teste\AppData") / "orfi" / "config.toml"


def test_caminhoConfiguracaoLinux(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")

    caminho = orfi.configs.caminhoConfiguracao()

    assert caminho == Path.home() / ".config" / "orfi" / "config.toml"

def test_criarConfiguracaoStandard(tmp_path):

    caminho = (tmp_path / "Base" / "config.toml")
    orfi.configs.criarConfiguracaoStandard(caminho)
    assert caminho.parent.exists()
    assert caminho.exists()
    with caminho.open("rb") as ficheiro:
        data = tomllib.load(ficheiro)
        assert "categorias" in data
        assert len(data["categorias"]) > 0

def test_carregarConfiguracaoStandard(tmp_path):
    caminho = tmp_path / "config.toml"

    categorias = orfi.configs.carregarConfiguracao(caminho)

    assert caminho.exists()
    assert len(categorias) > 0

def test_configuracaoStandardExiste():
    caminho = Path(orfi.configs.__file__).parent / "config.toml"

    assert caminho.exists()

def test_carregarConfiguracaoPersonalizada(tmp_path):

    configuracao = """
    [[categorias]]
    nome = "Imagens"
    extensoes = [".jpg", ".png"]

    [[categorias]]
    nome = "Musica"
    extensoes = [".mp3", ".flac"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path)

    assert len(categorias) == 3
    assert categorias[0].nome == "Imagens"
    assert ".mp3" in categorias[1].extensoes
    assert categorias[2].nome == "Outros"
    assert categorias[2].defeito

def test_verificaExtDuplicadas(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf", ".txt"]

    [[categorias]]
    nome = "Texto"
    extensoes = [".txt", ".md"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path)

    assert not orfi.configs.verificaExtDuplicadas(categorias)

def test_verificaCategoriasDuplicadas(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf"]

    [[categorias]]
    nome = "Documentos"
    extensoes = [".txt"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path)
    
    assert not orfi.configs.verificaCategoriasDuplicadas(categorias)

def test_verificaCategoriasDefeito(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true

    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf"]

    [[categorias]]
    nome = "Diversos"
    extensoes = []
    defeito = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path)
    assert not orfi.configs.verificaCategoriasDefeito(categorias)

def test_verificaExtFormatoSemPonto(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf", "txt"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path)
    assert not orfi.configs.verificaExtFormato(categorias)

def test_verificaExtFormatoMultiplosPontos(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf", "..txt"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path)
    assert not orfi.configs.verificaExtFormato(categorias)

def test_verificaExtFormatoPontoErrado(tmp_path):
    configuracao = """
    [[categorias]]
    nome = "Documentos"
    extensoes = [".pdf", "tx.t"]

    [[categorias]]
    nome = "Outros"
    extensoes = []
    defeito = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path)
    assert not orfi.configs.verificaExtFormato(categorias)