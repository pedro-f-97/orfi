import tomllib
from pathlib import Path

import orfi.configs


def simulaConfiguracao(configuracao: str, tmp_path) -> orfi.configs.Configuracao:
    caminho = tmp_path / "config.toml"
    caminho.write_text(configuracao, encoding="utf-8")

    return orfi.configs.carregarConfiguracao(caminho)

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
        assert "categories" in data
        assert len(data["categories"]) > 0

def test_carregarConfiguracaoStandard(tmp_path):
    caminho = tmp_path / "config.toml"

    categorias = orfi.configs.carregarConfiguracao(caminho).categorias

    assert caminho.exists()
    assert len(categorias) > 0

def test_configuracaoStandardExiste():
    caminho = Path(orfi.configs.__file__).parent / "config.toml"

    assert caminho.exists()

def test_carregarConfiguracaoPersonalizada(tmp_path):

    configuracao = """
    [[categories]]
    name = "Imagens"
    extensions = [".jpg", ".png"]

    [[categories]]
    name = "Musica"
    extensions = [".mp3", ".flac"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias

    assert len(categorias) == 3
    assert categorias[0].nome == "Imagens"
    assert ".mp3" in categorias[1].extensoes
    assert categorias[2].nome == "Outros"
    assert categorias[2].defeito

def test_verificaExtDuplicadas(tmp_path):
    configuracao = """
    [[categories]]
    name = "Documentos"
    extensions = [".pdf", ".txt"]

    [[categories]]
    name = "Texto"
    extensions = [".txt", ".md"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias

    assert not orfi.configs.verificaExtDuplicadas(categorias)

def test_verificaCategoriasDuplicadas(tmp_path):
    configuracao = """
    [[categories]]
    name = "Documentos"
    extensions = [".pdf"]

    [[categories]]
    name = "Documentos"
    extensions = [".txt"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias
    
    assert not orfi.configs.verificaCategoriasDuplicadas(categorias)

def test_verificaCategoriasDefeito(tmp_path):
    configuracao = """
    [[categories]]
    name = "Outros"
    extensions = []
    default = true

    [[categories]]
    name = "Documentos"
    extensions = [".pdf"]

    [[categories]]
    name = "Diversos"
    extensions = []
    default = true
    """

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias
    assert not orfi.configs.verificaCategoriasDefeito(categorias)

def test_verificaExtFormatoSemPonto(tmp_path):
    configuracao = """
    [[categories]]
    name = "Documentos"
    extensions = [".pdf", "txt"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias
    assert not orfi.configs.verificaExtFormato(categorias)

def test_verificaExtFormatoMultiplosPontos(tmp_path):
    configuracao = """
    [[categories]]
    name = "Documentos"
    extensions = [".pdf", "..txt"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias
    assert not orfi.configs.verificaExtFormato(categorias)

def test_verificaExtFormatoPontoErrado(tmp_path):
    configuracao = """
    [[categories]]
    name = "Documentos"
    extensions = [".pdf", "tx.t"]

    [[categories]]
    name = "Outros"
    extensions = []
    default = true
    """   

    categorias = simulaConfiguracao(configuracao, tmp_path).categorias
    assert not orfi.configs.verificaExtFormato(categorias)

def test_carregarIdioma(tmp_path):
    configurar = tmp_path / "config.toml"
    carregar = orfi.configs.carregarConfiguracao(configurar).idioma
    assert carregar == "en"

def test_alterarIdioma(tmp_path):
    configurar = tmp_path / "config.toml"
    idiomaActual = orfi.configs.carregarConfiguracao(configurar).idioma
    if idiomaActual == "en":
        idiomaAlterar = "pt"
    else:
        idiomaAlterar = "en"
    
    assert orfi.configs.alterarIdioma(idiomaAlterar, configurar)
    assert orfi.configs.carregarConfiguracao(configurar).idioma == idiomaAlterar