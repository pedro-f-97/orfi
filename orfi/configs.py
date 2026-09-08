import logging
import os
import sys
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from . import mensagens

logger = logging.getLogger(__name__)


def caminhoConfiguracao() -> Path:
    """Devolve o caminho onde vão ser guardados os ficheiros de configuração, de acordo com o sistema operativo.

    Returns:
        O caminho onde vai guardar as configurações.
    """
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "orfi" / "config.toml"
    else:
        return Path.home() / ".config" / "orfi" / "config.toml"

class Modo(Enum):
    COPIAR = "copiar"
    MOVER = "mover"

idiomasExistentes = {"pt", "en"}

@dataclass
class CategoriaDePasta:
    nome: str
    extensoes: set[str]
    caminho: Path | None = None
    defeito: bool = False

def criarConfiguracaoStandard(caminho: Path):
    """Cria um ficheiro .toml com as configurações predefinidas na pasta indicada.

    Args:
        caminho: Caminho onde vai ser criado o ficheiro de configuração.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)

    configuracaoStandard = Path(__file__).parent / "config.toml"

    configuracao = configuracaoStandard.read_bytes()
    caminho.write_bytes(configuracao)

def carregarConfiguracao(caminho: Path | None = None) -> list[CategoriaDePasta]:
    """Carrega as configurações e devolve as categorias de pasta.
    Se o ficheiro de configuração não existir, é criado com as configurações predefinidas.

    Args:
        caminho: Caminho do ficheiro de configuração, caso None utiliza o caminho predefinido.
    """
    if caminho is None:
        caminho = caminhoConfiguracao()

    if not caminho.exists():
        criarConfiguracaoStandard(caminho)
    
    logger.info("Config path: %s", caminho)

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

def carregarIdioma(caminho: Path | None = None) -> str:
    """Carrega as configurações e devolve o idioma.
    Se o ficheiro de configuração não existir, é criado com as configurações predefinidas.

    Args:
        caminho: Caminho do ficheiro de configuração, caso None utiliza o caminho predefinido.
    """
    if caminho is None:
        caminho = caminhoConfiguracao()

    if not caminho.exists():
        criarConfiguracaoStandard(caminho)

    with caminho.open("rb") as ficheiro:
        data = tomllib.load(ficheiro)

    idioma = data.get("idioma", "en")

    return idioma

def verificaConfiguracao(categorias: list[CategoriaDePasta]) -> bool:
    """Verifica se a lista de categorias de pasta indicada é válida.

    Args:
        categorias: Lista de categorias de pasta a analisar.

    Returns:
        True caso seja válida, False caso haja algum erro.
    """

    ok = True
    verificacoes = [
        verificaExtFormato,
        verificaExtDuplicadas,
        verificaCategoriasDuplicadas,
        verificaCategoriasDefeito,
    ]

    for verifica in verificacoes:
        if not verifica(categorias):
            logger.error("Config error: %s", verifica.__name__)
            ok = False

    return ok

def verificaExtDuplicadas(categorias: list[CategoriaDePasta]) -> bool:
    """Verifica se a lista de categorias de pasta indicada contém extensões duplicadas.

    Args:
        categorias: Lista de categorias de pasta a analisar.

    Returns:
        True caso seja válida, False caso haja algum erro.
    """
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
            mensagens.mensagem("extensao_duplicada", "extensao_duplicada", False, mensagens.CoresTexto.VERMELHO, extensao=extensao, categorias=categoriasExt)

        return False

    return True

def verificaCategoriasDuplicadas(categorias: list[CategoriaDePasta]) -> bool:
    """Verifica se a lista de categorias de pasta indicada contém categorias duplicadas.

    Args:
        categorias: Lista de categorias de pasta a analisar.

    Returns:
        True caso seja válida, False caso haja algum erro.
    """
    categoriasValidar = set()
    erros = set()
    for categoria in categorias:
        if categoria.nome in categoriasValidar:
            erros.add(categoria.nome)
        else:
            categoriasValidar.add(categoria.nome)

    if erros:
        mensagens.mensagem("categoria_duplicada", "categoria_duplicada", False, mensagens.CoresTexto.VERMELHO, categorias=erros)
        return False
    return True

def verificaCategoriasDefeito(categorias: list[CategoriaDePasta]) -> bool:
    """Verifica se a lista de categorias de pasta indicada contém mais do que uma categoria por defeito.

    Args:
        categorias: Lista de categorias de pasta a analisar.

    Returns:
        True caso seja válida, False caso haja algum erro.
    """
    categoriasDefeito = set()
    for categoria in categorias:
        if categoria.defeito:
            categoriasDefeito.add(categoria.nome)
    if len(categoriasDefeito) > 1:
        mensagens.mensagem("multiplas_categorias_defeito", "multiplas_categorias_defeito", False, mensagens.CoresTexto.VERMELHO, categorias=categoriasDefeito)
        return False
    return True

def verificaExtFormato(categorias: list[CategoriaDePasta]) -> bool:
    """Verifica se a lista de categorias de pasta indicada contém extensões mal formatadas.

    Args:
        categorias: Lista de categorias de pasta a analisar.

    Returns:
        True caso seja válida, False caso haja algum erro.
    """
    extErros = set()
    for categoria in categorias:
        for ext in categoria.extensoes:
            if ext.count(".") != 1 or not ext.startswith("."):
                extErros.add(ext)
    if extErros:
        mensagens.mensagem("extensoes_incorretas", "extensoes_incorretas", False, mensagens.CoresTexto.VERMELHO, extensoes=extErros)
        return False
    return True