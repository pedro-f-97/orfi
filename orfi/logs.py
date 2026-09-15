import logging
from logging.handlers import RotatingFileHandler

from . import configs, mensagens

logger = logging.getLogger(__name__)

def configuraLogs():
    """Define o caminho e configura o sistema dos logs."""
    caminho = configs.caminhoConfiguracao().with_name("orfi.log")
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        mensagens.mensagem("erro_criar_pasta", "erro_criar_pasta", False, mensagens.CoresTexto.VERMELHO, pasta=caminho)
        logger.exception("Error creating folder '%s'", caminho)
        return

    handler = RotatingFileHandler(
        caminho,
        maxBytes=200_000,
        backupCount=2,
        encoding="utf-8"
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

