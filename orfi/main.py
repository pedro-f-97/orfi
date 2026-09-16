import logging
import sys
import time
import tomllib

from . import alvo, configs, inicializar, logs, mensagens, organizar, reverter

logger = logging.getLogger(__name__)

def main() -> int:
    """Ponto de entrada com tratamento de erros."""
    try:
        return executar()
    except KeyboardInterrupt:
        mensagens.mensagem("interrompido", "interrompido", False, mensagens.CoresTexto.AMARELO)
        logger.warning("Interrupted by user.")
        return 130
    except Exception as erro:
        logger.exception("Unexpected error.")
        mensagens.mensagem("erro_inesperado", "erro_inesperado",False, mensagens.CoresTexto.VERMELHO, erro=erro)
        return 2

def executar() -> int:
    """Lê os argumentos da linha de comandos e encaminha o processo."""
    inicio = time.perf_counter()
    logs.configuraLogs()
    logger.info("   --PROCESS STARTING--  ")
    logger.info("OS: %s | %s",sys.platform, sys.version)
    try:
        try:
            config = configs.carregarConfiguracao()
        except tomllib.TOMLDecodeError as erro:
            mensagens.mensagem("configuracao_invalida_sintaxe", "configuracao_invalida_sintaxe",
                            False, mensagens.CoresTexto.VERMELHO, erro=erro)
            return 1

        if config.idioma not in configs.idiomasExistentes:
            mensagens.mensagem("idioma_invalido", "idioma_invalido",
                            False, mensagens.CoresTexto.AMARELO,
                            idiomas=configs.idiomasExistentes)
            return 1
        mensagens.definirIdioma(config.idioma)

        if not configs.verificaConfiguracao(config.categorias):
            mensagens.mensagem("configuracao_invalida", "configuracao_invalida",
                            False, mensagens.CoresTexto.AMARELO)
            return 1
        
        argumentos = inicializar.trataArgumentos()

        if argumentos.language:
            if not configs.alterarIdioma(argumentos.language):
                mensagens.mensagem("idioma_invalido", "idioma_invalido", False, mensagens.CoresTexto.AMARELO, idiomas=", ".join(configs.idiomasExistentes))
                return 1
            mensagens.definirIdioma(argumentos.language)
            mensagens.mensagem("idioma_alterado", "idioma_alterado", False, mensagens.CoresTexto.VERDE, idioma=argumentos.language)
            return 0

        nivel = 1
        if argumentos.depth is not None:
            if argumentos.depth <= 0:
                mensagens.mensagem("nivel_invalido", "nivel_invalido", False, mensagens.CoresTexto.AMARELO, nivel=argumentos.depth)
                return 1
            nivel = argumentos.depth

        if argumentos.target:
            pastaSelecionada = alvo.defineAlvo()
        else:
            pastaSelecionada = alvo.defineAlvoAqui()

        logger.info("Selected folder: %s", pastaSelecionada)

        if argumentos.copy:
            modo = configs.Modo.COPIAR
        else:
            modo = configs.Modo.MOVER

        force = argumentos.yes

        simula = argumentos.dry_run

        if simula:
            mensagens.mensagem("inicio_simulacao", "inicio_simulacao", False, mensagens.CoresTexto.AMARELO)

        if pastaSelecionada is None:
            mensagens.mensagem("pasta_invalida", "pasta_invalida", False, mensagens.CoresTexto.AMARELO)
            return 1

        mensagens.mensagem("pasta_selecionada", "pasta_selecionada", False, mensagens.CoresTexto.AZUL, pasta=pastaSelecionada)

        if argumentos.revert:
            if not argumentos.date:
                reverter.reverte(pastaSelecionada, config.categorias, modo, force, simula)
            else:
                reverter.reverteDatar(pastaSelecionada, modo, force, simula, nivel)

        elif argumentos.date:
            organizar.datar(pastaSelecionada, modo, force, simula, nivel)
            
        else:
            organizar.organiza(pastaSelecionada, config.categorias, modo, force, simula, nivel)

        if simula:
            mensagens.mensagem("fim_simulacao", "fim_simulacao", False, mensagens.CoresTexto.AMARELO)
        return 0

    finally:
        duracao = time.perf_counter() - inicio
        logger.info("   --PROCESS ENDED--  ")
        logger.info("   --%.2f SECONDS--   ", duracao)
        
if __name__ == "__main__":
    sys.exit(main())    