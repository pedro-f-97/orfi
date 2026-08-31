from dataclasses import dataclass
from pathlib import Path


class CoresTexto:
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    RESET = "\033[0m"


@dataclass
class CategoriaDePasta:
    nome: str
    extensoes: set[str]
    caminho: Path | None = None
    defeito: bool = False

def iniciarCategorias() -> list[CategoriaDePasta]:
    categorias: list[CategoriaDePasta] = []
    categorias.append(CategoriaDePasta("Imagens", {".jpg", ".png", ".bmp"}))
    categorias.append(CategoriaDePasta("Documentos", {".txt", ".docx", ".pdf", ".md"}))
    categorias.append(CategoriaDePasta("Excel", {".xlsx", ".xltm", ".csv"}))
    categorias.append(CategoriaDePasta("Emails", {".msg"}))
    categorias.append(CategoriaDePasta("Outros", set(),None ,True))
    return categorias