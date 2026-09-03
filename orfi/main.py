import logging

from . import alvo, configs, inicializar, logs, organizar, reverter

logger = logging.getLogger(__name__)

def main():
    logs.configuraLogs()

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
    logger.info("Fim de operação.")
        

if __name__ == "__main__":
    main()    