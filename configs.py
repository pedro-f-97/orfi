from dataclasses import dataclass
from pathlib import Path


@dataclass
class CategoriaDePasta:
    nome: str
    extensoes: set[str]
    caminho: Path | None = None

def iniciarCategorias() -> list[CategoriaDePasta]:
    categorias: list[CategoriaDePasta] = []
    categorias.append(CategoriaDePasta("Imagens", {".jpg", ".png"}))
    categorias.append(CategoriaDePasta("Documentos", {".txt", ".docx", ".pdf"}))
    categorias.append(CategoriaDePasta("Excel", {".xlsx", ".xltm"}))
    categorias.append(CategoriaDePasta("Outros", {""}))
    return categorias