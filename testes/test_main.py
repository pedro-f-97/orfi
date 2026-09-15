import sys

import orfi.main


def test_executarConfigInvalida(tmp_path, monkeypatch):
    caminho = tmp_path / "config.toml"
    caminho.write_text("sintaxe invalida {{{", encoding="utf-8")
    monkeypatch.setattr(orfi.main.configs, "caminhoConfiguracao", lambda: caminho)
    monkeypatch.setattr(sys, "argv", ["orfi"])

    chamadas = []
    monkeypatch.setattr(orfi.main.mensagens, "mensagem", lambda *a, **kw: chamadas.append(a[0]))

    assert orfi.main.executar() == 1
    assert "configuracao_invalida_sintaxe" in chamadas

def test_executarIdiomaInvalido(tmp_path, monkeypatch):
    caminho = tmp_path / "config.toml"
    caminho.write_text('idioma = "xx"\n[[categorias]]\nnome = "Docs"\nextensoes = [".txt"]\n', encoding="utf-8")
    monkeypatch.setattr(orfi.main.configs, "caminhoConfiguracao", lambda: caminho)
    monkeypatch.setattr(sys, "argv", ["orfi"])

    assert orfi.main.executar() == 1

def test_executarAlteraIdioma(tmp_path, monkeypatch):
    caminho = tmp_path / "config.toml"
    caminho.write_text('idioma = "pt"\n', encoding="utf-8")
    conteudo = caminho.read_text(encoding="utf-8")
    assert 'idioma = "pt"' in conteudo
    monkeypatch.setattr(orfi.main.configs, "caminhoConfiguracao", lambda: caminho)
    monkeypatch.setattr(sys, "argv", ["orfi", "-i", "en"])

    assert orfi.main.executar() == 0

    conteudo = caminho.read_text(encoding="utf-8")
    assert 'idioma = "en"' in conteudo