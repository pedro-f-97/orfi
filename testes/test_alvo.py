import tkinter
from tkinter import filedialog

import orfi.alvo


class JanelaTeste:
    def withdraw(self):
        pass

    def destroy(self):
        pass

def test_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(tkinter, "Tk", lambda: JanelaTeste())
    monkeypatch.setattr(filedialog, "askdirectory", lambda **kwargs: str(tmp_path))

    resultado = orfi.alvo.defineAlvo()

    assert resultado == tmp_path

def test_cancela_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(tkinter, "Tk", lambda: JanelaTeste())
    monkeypatch.setattr(filedialog, "askdirectory", lambda title, mustexist: "")

    resultado = orfi.alvo.defineAlvo()

    assert resultado == None

def test_defineAlvoSemTkinter(monkeypatch, capsys):
    import builtins
    original_import = builtins.__import__
    def import_falso(nome, *args, **kwargs):
        if nome == "tkinter":
            raise ImportError
        return original_import(nome, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", import_falso)

    resultado = orfi.alvo.defineAlvo()
    assert resultado == None