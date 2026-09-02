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

def verificaConfiguracao(categorias: list[CategoriaDePasta]) -> bool:
    ok = True
    verificacoes = [
        verificaExtFormato,
        verificaExtDuplicadas,
        verificaCategoriasDuplicadas,
        verificaCategoriasDefeito,
    ]

    for verifica in verificacoes:
        if not verifica(categorias):
            ok = False

    return ok

def verificaExtDuplicadas(categorias: list[CategoriaDePasta]) -> bool:
    extensoesPorCategoria = dict()

    for categoria in categorias:
        for extensao in categoria.extensoes:
            if extensao not in extensoesPorCategoria:
                extensoesPorCategoria[extensao] = []

            extensoesPorCategoria[extensao].append(categoria.nome)

    erros = dict()

    for extensao, categoriasExt in extensoesPorCategoria.items():
        if len(categoriasExt) > 1:
            erros[extensao] = categoriasExt

    if erros:
        for extensao, categoriasExt in erros.items():
            print(
                f"{CoresTexto.VERMELHO}Extensão duplicada '{extensao}' nas categorias {categoriasExt}.{CoresTexto.RESET}"
            )

        return False

    return True

def verificaCategoriasDuplicadas(categorias: list[CategoriaDePasta]) -> bool:
    categoriasValidar = set()
    erros = set()
    for categoria in categorias:
        if categoria.nome in categoriasValidar:
            erros.add(categoria.nome)
        else:
            categoriasValidar.add(categoria.nome)

    if erros:
        print(f"{CoresTexto.VERMELHO}Categoria(s) duplicada(s) '{erros}'.{CoresTexto.RESET}")
        return False
    return True

def verificaCategoriasDefeito(categorias: list[CategoriaDePasta]) -> bool:
    categoriasDefeito = set()
    for categoria in categorias:
        if categoria.defeito:
            categoriasDefeito.add(categoria.nome)
    if len(categoriasDefeito) > 1:
        print(f"{CoresTexto.VERMELHO}Mais do que uma categoria por defeito: '{categoriasDefeito}'.{CoresTexto.RESET}")
        return False
    return True

def verificaExtFormato(categorias: list[CategoriaDePasta]) -> bool:
    extErros = set()
    for categoria in categorias:
        for ext in categoria.extensoes:
            if ext.count(".") != 1 or not ext.startswith("."):
                extErros.add(ext)
    if extErros:
        print(f"{CoresTexto.VERMELHO}Extensões incorretas: '{extErros}'.{CoresTexto.RESET}")
        return False
    return True