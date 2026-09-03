import logging
from pathlib import Path

from . import configs, ficheiros, pastas

logger = logging.getLogger(__name__)

def organiza(pastaSelecionada: Path, categorias: list[configs.CategoriaDePasta], modo: configs.Modo):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "movidos."

    pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pastaSelecionada), categorias)

    if pastasParaCriar == set():
        print(f"{configs.CoresTexto.AMARELO}Nada para fazer.{configs.CoresTexto.RESET}")
        return

    confirmacao = input(f"{configs.CoresTexto.AZUL}Criar as pastas {pastasParaCriar}? (s/n): {configs.CoresTexto.RESET}")
    if confirmacao.lower() == "s":
        cont = pastas.criaPastas(pastaSelecionada, pastasParaCriar, categorias)
        logger.info("Terminou, %s pastas criadas.", cont)
        print(f"{configs.CoresTexto.VERDE}{cont} pastas criadas.{configs.CoresTexto.RESET}")
    else:
        print(f"{configs.CoresTexto.AMARELO}Operação Cancelada{configs.CoresTexto.RESET}")
        return

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        destino = ficheiros.defineDestino(ficheiro, categorias)
        if destino is not None:
            resultado = trabalho(ficheiro, destino)
            if resultado:
                total += resultado
                print(f"{configs.CoresTexto.VERDE}{ficheiro.name} tratado.{configs.CoresTexto.RESET}")
        else:
            print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")

    logger.info("Terminou, %s ficheiros %s", total, tratamento)
    print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")

def datar(pastaSelecionada: Path, modo: configs.Modo):
    if modo == configs.Modo.COPIAR:
        trabalho = ficheiros.copiaFicheiro
        tratamento = "copiados e datados."
    elif modo == configs.Modo.MOVER:
        trabalho = ficheiros.moveFicheiro
        tratamento = "datados."

    ficheirosLista = ficheiros.devolveFicheiros(pastaSelecionada)

    total = 0
    for ficheiro in ficheirosLista:
        if ficheiros.verificaDatado(ficheiro):
            print(f"{configs.CoresTexto.AMARELO}Ficheiro já datado: {ficheiro.name}{configs.CoresTexto.RESET}")
        else:
            ficheiroFinal = ficheiros.datarFicheiro(ficheiro)
            resultado = trabalho(ficheiro, pastaSelecionada, ficheiroFinal)
            if resultado:
                total += resultado
                print(f"{configs.CoresTexto.VERDE}{ficheiro.name} tratado.{configs.CoresTexto.RESET}")
    logger.info("Terminou, %s ficheiros %s", total, tratamento)
    print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros {tratamento}{configs.CoresTexto.RESET}")
