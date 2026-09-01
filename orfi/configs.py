import os
import sys
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


def caminhoConfiguracao() -> Path:
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "orfi" / "config.toml"
    else:
        return Path.home() / ".config" / "orfi" / "config.toml"
class CoresTexto:
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    RESET = "\033[0m"

class Modo(Enum):
    COPIAR = "copiar"
    MOVER = "mover"


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

def criarConfiguracaoStandard(caminho: Path):
    caminho.parent.mkdir(parents=True, exist_ok=True)

    configuracaoStandard = Path(__file__).parent / "config.toml"

    configuracao = configuracaoStandard.read_bytes()
    caminho.write_bytes(configuracao)

def carregarConfiguracao(caminho: Path | None = None) -> list[CategoriaDePasta]:
    if caminho is None:
        caminho = caminhoConfiguracao()

    if not caminho.exists():
        criarConfiguracaoStandard(caminho)

    with caminho.open("rb") as ficheiro:
        data = tomllib.load(ficheiro)

    categorias = []

    for categoria in data["categorias"]:
        novaCategoria = CategoriaDePasta(
            nome=categoria["nome"],
            extensoes=set(categoria["extensoes"]),
            defeito=categoria.get("defeito", False)
        )
        categorias.append(novaCategoria)

    return categorias