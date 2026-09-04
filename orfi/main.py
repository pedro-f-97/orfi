import logging
import sys
import time

from . import alvo, configs, inicializar, logs, organizar, reverter

logger = logging.getLogger(__name__)

def main():
    logs.configuraLogs()
    logger.info("   --INÍCIO DE EXECUÇÃO--  ")
    logger.info("OS: %s | %s",sys.platform, sys.version)
    inicio = time.perf_counter()

    argumentos = inicializar.trataArgumentos()

    if argumentos.alvo:
        pastaSelecionada = alvo.defineAlvo()
    else:
        pastaSelecionada = alvo.defineAlvoAqui()

    logger.info("Pasta selecionada: %s", pastaSelecionada)

    if argumentos.copiar:
        modo = configs.Modo.COPIAR
    else:
        modo = configs.Modo.MOVER

    categorias = configs.carregarConfiguracao()
    if not configs.verificaConfiguracao(categorias):
        print(f"{configs.CoresTexto.AMARELO}Configuração inválida, corrigir o config.toml.{configs.CoresTexto.RESET}")
        return

    if pastaSelecionada is None:
        print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
        return

    print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

    if argumentos.reverter:
        if not argumentos.datar:
            reverter.reverte(pastaSelecionada, categorias, modo)
        else:
            reverter.reverteDatar(pastaSelecionada, modo)

    elif argumentos.datar:
        organizar.datar(pastaSelecionada, modo)
        
    else:
        organizar.organiza(pastaSelecionada, categorias, modo)
    duracao = time.perf_counter() - inicio
    logger.info("   --FIM DE EXECUÇÃO--  ")
    logger.info("   --%.2f SEGUNDOS--   ", duracao)
        
if __name__ == "__main__":
    main()    