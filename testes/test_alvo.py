import alvo


class JanelaTeste:
    def withdraw(self):
        pass

    def destroy(self):
        pass

def test_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(alvo, "Tk", JanelaTeste)
    monkeypatch.setattr(
        alvo.filedialog,
        "askdirectory",
        lambda title, mustexist: str(tmp_path)
    )

    resultado = alvo.defineAlvo()

    assert resultado == tmp_path

def test_cancela_defineAlvo(monkeypatch, tmp_path):
    monkeypatch.setattr(alvo, "Tk", JanelaTeste)
    monkeypatch.setattr(
        alvo.filedialog,
        "askdirectory",
        lambda title, mustexist: ""
    )

    resultado = alvo.defineAlvo()

    assert resultado == None