from pathlib import Path
from tkinter import Tk, filedialog


def defineAlvo() -> Path | None:
    """Abre uma janela para selecionar uma pasta e devolve a pasta selecionada.

    Returns:
        A pasta selecionada ou None caso tenha sido cancelado.
    """
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
    """Devolve a pasta actual.

    Returns:
        A pasta actual.
    """
    return Path.cwd()