from dataclasses import dataclass
from pathlib import Path


@dataclass
class CategoriaDePasta:
    nome: str
    extensoes: set[str]
    caminho: Path | None = None

def iniciarCategorias() -> list[CategoriaDePasta]:
    categorias: list[CategoriaDePasta] = []
    categorias.append(CategoriaDePasta("Imagens", {".jpg", ".png", ".bmp"}))
    categorias.append(CategoriaDePasta("Documentos", {".txt", ".docx", ".pdf", ".md"}))
    categorias.append(CategoriaDePasta("Excel", {".xlsx", ".xltm", ".csv"}))
    categorias.append(CategoriaDePasta("Emails", {".msg"}))
    categorias.append(CategoriaDePasta("Outros", set()))
    return categorias