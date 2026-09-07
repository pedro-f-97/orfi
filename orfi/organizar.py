import logging
from pathlib import Path

from . import configs, ficheiros, pastas

logger = logging.getLogger(__name__)

def organiza(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo, force: bool, simula: bool):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "movidos."
    else:
        print(f"{configs.CoresTexto.VERMELHO}Modo {modo} inesperado. Operação cancelada.{configs.CoresTexto.RESET}")
        return

    pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pastaSelecionada), categorias)

    if pastasParaCriar == set():
        configs.mensagem("Nada para fazer.", "Não faria nada.", simula, configs.CoresTexto.AMARELO)
        return

    if not force:
        confirmacao = input(f"{configs.CoresTexto.AZUL}Criar as pastas {pastasParaCriar}? (s/n): {configs.CoresTexto.RESET}")
        if confirmacao.lower() != "s":
            print(f"{configs.CoresTexto.AMARELO}Operação Cancelada{configs.CoresTexto.RESET}")
            return
    cont = pastas.criaPastas(pastaSelecionada, pastasParaCriar, categorias, simula)
    if not simula:
        logger.info("Terminou, %s pastas criadas.", cont)
    configs.mensagem(f"{cont} pastas criadas.", f"{cont} pastas seriam criadas.", simula, configs.CoresTexto.VERDE)

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        destino = ficheiros.defineDestino(ficheiro, categorias)
        if destino is not None:
            resultado = trabalho(ficheiro, destino, force, simula)
            if resultado:
                total += resultado
                configs.mensagem(f"{ficheiro.name} tratado.", f"{ficheiro.name} seria tratado.", simula, configs.CoresTexto.AMARELO)
        else:
            print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
    configs.mensagem(f"Feito, {total} ficheiros {tratamento}", f"Feito, {total} ficheiros teriam sido {tratamento}", simula, configs.CoresTexto.AMARELO)

def datar(pastaSelecionada: Path, modo: configs.Modo, force: bool, simula: bool):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados e datados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "datados."
    else:
        print(f"{configs.CoresTexto.VERMELHO}Modo {modo} inesperado. Operação cancelada.{configs.CoresTexto.RESET}")
        return

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            print(f"{configs.CoresTexto.AMARELO}Ficheiro já datado: {ficheiro.name}{configs.CoresTexto.RESET}")
        else:
            ficheiroFinal = ficheiros.datarFicheiro(ficheiro, simula)
            resultado = trabalho(ficheiro, pastaSelecionada, force, simula, ficheiroFinal)
            if resultado:
                total += resultado
                configs.mensagem(f"{ficheiro.name} tratado.", f"{ficheiro.name} seria tratado.", simula, configs.CoresTexto.AMARELO)
    if not simula:
        logger.info("Terminou, %s ficheiros %s", total, tratamento)
    configs.mensagem(f"Feito, {total} ficheiros {tratamento}", f"Feito, {total} ficheiros teriam sido {tratamento}", simula, configs.CoresTexto.AMARELO)