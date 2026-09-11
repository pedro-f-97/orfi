from pathlib import Path

from . import mensagens


def defineAlvo() -> Path | None:
    """Abre uma janela para selecionar uma pasta e devolve a pasta selecionada.

    Returns:
        A pasta selecionada ou None caso tenha sido cancelado ou o
        tkinter não esteja disponível no sistema.
    """
    try:
        from tkinter import Tk, filedialog
    except ImportError:
        mensagens.mensagem("tkinter_nao_disponivel", "tkinter_nao_disponivel", False, mensagens.CoresTexto.VERMELHO)
        return None

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