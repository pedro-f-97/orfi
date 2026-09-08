import logging
import sys
import time

from . import alvo, configs, inicializar, logs, mensagens, organizar, reverter

logger = logging.getLogger(__name__)

def main():
    """Ponto de entrada: lê os argumentos da linha de comandos e encaminha o processo."""
    inicio = time.perf_counter()
    logs.configuraLogs()
    logger.info("   --PROCESS STARTING--  ")
    logger.info("OS: %s | %s",sys.platform, sys.version)
    
    argumentos = inicializar.trataArgumentos()

    idioma = configs.carregarIdioma()
    mensagens.definirIdioma(idioma)

    if argumentos.alvo:
        pastaSelecionada = alvo.defineAlvo()
    else:
        pastaSelecionada = alvo.defineAlvoAqui()

    logger.info("Selected folder: %s", pastaSelecionada)

    if argumentos.copiar:
        modo = configs.Modo.COPIAR
    else:
        modo = configs.Modo.MOVER

    force = argumentos.force

    simula = argumentos.simula

    if simula:
        mensagens.mensagem("inicio_simulacao", "inicio_simulacao", False, mensagens.CoresTexto.AMARELO)

    categorias = configs.carregarConfiguracao()
    if not configs.verificaConfiguracao(categorias):
        mensagens.mensagem("configuracao_invalida", "configuracao_invalida", False, mensagens.CoresTexto.AMARELO)
        return

    if pastaSelecionada is None:
        mensagens.mensagem("pasta_invalida", "pasta_invalida", False, mensagens.CoresTexto.AMARELO)
        return

    mensagens.mensagem("pasta_selecionada", "pasta_selecionada", False, mensagens.CoresTexto.AZUL, pasta=pastaSelecionada)

    if argumentos.reverter:
        if not argumentos.datar:
            reverter.reverte(pastaSelecionada, categorias, modo, force, simula)
        else:
            reverter.reverteDatar(pastaSelecionada, modo, force, simula)

    elif argumentos.datar:
        organizar.datar(pastaSelecionada, modo, force, simula)
        
    else:
        organizar.organiza(pastaSelecionada, categorias, modo, force, simula)

    if simula:
        mensagens.mensagem("fim_simulacao", "fim_simulacao", False, mensagens.CoresTexto.AMARELO)
    duracao = time.perf_counter() - inicio
    logger.info("   --PROCESS ENDED--  ")
    logger.info("   --%.2f SECONDS--   ", duracao)
        
if __name__ == "__main__":
    main()    