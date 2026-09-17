import logging
import os
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from . import mensagens

logger = logging.getLogger(__name__)

idiomasExistentes = {"pt", "en"}

def escreverAtomico(caminho: Path, dados: bytes) -> None:
    """Escreve dados num ficheiro de forma atómica.

    Escreve primeiro para um ficheiro temporário no mesmo diretório,
    força a sincronização para o disco e só depois substitui o destino.

    Args:
        caminho: Caminho do ficheiro de destino.
        dados: Conteúdo a escrever, em bytes.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp = tempfile.mkstemp(dir=caminho.parent, prefix=".tmp-", suffix=caminho.suffix)
    try:
        with os.fdopen(fd, "wb") as ficheiro:
            ficheiro.write(dados)
            ficheiro.flush()
            os.fsync(ficheiro.fileno())
        os.replace(tmp, caminho)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise

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

@dataclass
class ResultadosOperacao:
    ficheirosTratados: int = 0
    pastasCriadas: int = 0
    pastasEliminadas: int = 0

@dataclass
class CategoriaDePasta:
    nome: str
    extensoes: set[str]
    caminho: Path | None = None
    defeito: bool = False

@dataclass(frozen=True)
class Configuracao:
    idioma: str
    categorias: list[CategoriaDePasta]
    avisos: set

def criarConfiguracaoStandard(caminho: Path):
    """Cria um ficheiro .toml com as configurações predefinidas na pasta indicada.

    Args:
        caminho: Caminho onde vai ser criado o ficheiro de configuração.
    """
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        mensagens.mensagem("erro_criar_pasta", "erro_criar_pasta", False, mensagens.CoresTexto.VERMELHO, pasta=caminho)
        logger.exception("Error creating folder '%s'", caminho)
        return

    configuracaoStandard = Path(__file__).parent / "config.toml"
    escreverAtomico(caminho, configuracaoStandard.read_bytes())
    logger.info("Standard config created: %s", caminho)

def carregarConfiguracao(caminho: Path | None = None) -> Configuracao:
    """Carrega e devolve as configurações.
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

    avisos = set()

    if not data.get("language"):
        avisos.add("nenhum_idioma")
    idioma = data.get("language", "en")
    if not data.get("categories"):
        avisos.add("nenhuma_categoria")
    categorias = [
        CategoriaDePasta(
            nome=c["name"],
            extensoes=set(c["extensions"]),
            defeito=c.get("default", False),
        )
        for c in data.get("categories", [])
    ]

    return Configuracao(idioma=idioma, categorias=categorias, avisos=avisos)

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

def alterarIdioma(idioma: str, caminho: Path | None = None) -> bool:
    """Altera o idioma da configuração para o indicado.

    Args:
        idioma: o idioma selecionado.

    Returns:
        True se válido, False se inválido.
    """
    if idioma not in idiomasExistentes:
        return False

    if not caminho:
        caminho = caminhoConfiguracao()

    conteudo = caminho.read_text(encoding="utf-8")
    linhas = conteudo.splitlines()
    for i, linha in enumerate(linhas):
        if linha.strip().startswith("language ="):
            linhas[i] = f'language = "{idioma}"'
            break

    novoConteudo = ("\n".join(linhas) + "\n").encode("utf-8")
    escreverAtomico(caminho, novoConteudo)
    logger.info("Changed language to '%s' in: %s", idioma, caminho)
    return True

