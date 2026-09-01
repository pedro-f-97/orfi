from pathlib import Path

import orfi.configs


def test_caminhoConfiguracaoWindows(monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    monkeypatch.setenv("APPDATA", r"C:\Teste\AppData")

    caminho = orfi.configs.caminhoConfiguracao()

    assert caminho == Path(r"C:\Teste\AppData") / "orfi" / "config.toml"


def test_caminhoConfiguracaoLinux(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")

    caminho = orfi.configs.caminhoConfiguracao()

    assert caminho == Path.home() / ".config" / "orfi" / "config.toml"