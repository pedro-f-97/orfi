from pathlib import Path
from tkinter import Tk, filedialog


def defineAlvo() -> Path | None:
    janela = Tk()
    janela.withdraw()

    pastaSelecionada = filedialog.askdirectory(
        title="Selecionar pasta para organizar",
        mustexist=True
    )

    janela.destroy()

    if not pastaSelecionada:
        return None

    if not Path(pastaSelecionada).is_dir():
        return None

    pasta = Path(pastaSelecionada)
    return pasta

def defineAlvoAqui() -> Path:
    return Path.cwd()