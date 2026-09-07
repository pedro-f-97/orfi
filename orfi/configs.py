import logging
import os
import sys
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

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
class CoresTexto:
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    RESET = "\033[0m"

def mensagem(mensagemNormal: str, mensagemSimulacao: str, simula: bool, cor: str):
    """Imprime a mensagem correspondente ao modo de execução.

    Args:
        mensagemNormal: Mensagem apresentada numa execução normal.
        mensagemSimulacao: Mensagem apresentada numa simulação.
        simula: Se é simulação ou não.
        cor: A cor que deve ser aplicada à mensagem.
    """
    if simula:
        print(f"{CoresTexto.AMARELO}[SIMULAÇÃO] {mensagemSimulacao}{CoresTexto.RESET}")
    else:
        print(f"{cor}{mensagemNormal}{CoresTexto.RESET}")

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
    """Cria e devolve as categorias de pasta."""
    categorias: list[CategoriaDePasta] = []
    categorias.append(CategoriaDePasta("Imagens", {".jpg", ".png", ".bmp"}))
    categorias.append(CategoriaDePasta("Documentos", {".txt", ".docx", ".pdf", ".md"}))
    categorias.append(CategoriaDePasta("Excel", {".xlsx", ".xltm", ".csv"}))
    categorias.append(CategoriaDePasta("Emails", {".msg"}))
    categorias.append(CategoriaDePasta("Outros", set(),None ,True))
    return categorias

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
    
    logger.info("Caminho configs: %s", caminho)

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
            logger.error("Erro config: %s", verifica)
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
            print(
                f"{CoresTexto.VERMELHO}Extensão duplicada '{extensao}' nas categorias {categoriasExt}.{CoresTexto.RESET}"
            )

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
        print(f"{CoresTexto.VERMELHO}Categoria(s) duplicada(s) '{erros}'.{CoresTexto.RESET}")
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
        print(f"{CoresTexto.VERMELHO}Mais do que uma categoria por defeito: '{categoriasDefeito}'.{CoresTexto.RESET}")
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
        print(f"{CoresTexto.VERMELHO}Extensões incorretas: '{extErros}'.{CoresTexto.RESET}")
        return False
    return True