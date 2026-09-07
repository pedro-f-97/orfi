import logging
import sys
import time

from . import alvo, configs, inicializar, logs, organizar, reverter

logger = logging.getLogger(__name__)

def main():
    inicio = time.perf_counter()
    logs.configuraLogs()
    logger.info("   --INÍCIO DE EXECUÇÃO--  ")
    logger.info("OS: %s | %s",sys.platform, sys.version)
    
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

    force = argumentos.force

    simula = argumentos.simula

    if simula:
        print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Início de simulação.{configs.CoresTexto.RESET}")

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
            reverter.reverte(pastaSelecionada, categorias, modo, force, simula)
        else:
            reverter.reverteDatar(pastaSelecionada, modo, force, simula)

    elif argumentos.datar:
        organizar.datar(pastaSelecionada, modo, force, simula)
        
    else:
        organizar.organiza(pastaSelecionada, categorias, modo, force, simula)

    if simula:
        print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] Fim de simulação.{configs.CoresTexto.RESET}")
    duracao = time.perf_counter() - inicio
    logger.info("   --FIM DE EXECUÇÃO--  ")
    logger.info("   --%.2f SEGUNDOS--   ", duracao)
        
if __name__ == "__main__":
    main()    