import orfi.alvo


class JanelaTeste:
    def withdraw(self):
        pass

    def destroy(self):
        pass

def test_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(orfi.alvo, "Tk", JanelaTeste)
    monkeypatch.setattr(
        orfi.alvo.filedialog,
        "askdirectory",
        lambda title, mustexist: str(tmp_path)
    )

    resultado = orfi.alvo.defineAlvo()

    assert resultado == tmp_path

def test_cancela_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(orfi.alvo, "Tk", JanelaTeste)
    monkeypatch.setattr(
        orfi.alvo.filedialog,
        "askdirectory",
        lambda title, mustexist: ""
    )

    resultado = orfi.alvo.defineAlvo()

    assert resultado == None