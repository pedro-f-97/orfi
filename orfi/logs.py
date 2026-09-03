import logging
from logging.handlers import RotatingFileHandler

from . import configs


def configuraLogs():
    caminho = configs.caminhoConfiguracao().with_name("orfi.log")

    caminho.parent.mkdir(parents=True, exist_ok=True)

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

