from . import configs


def mensagem(mensagemNormal: str, mensagemSimulacao: str, simula: bool, cor: str):
    """Imprime a mensagem correspondente ao modo de execução.

    Args:
        mensagemNormal: Mensagem apresentada numa execução normal.
        mensagemSimulacao: Mensagem apresentada numa simulação.
        simula: Se é simulação ou não.
        cor: A cor que deve ser aplicada à mensagem.
    """
    if simula:
        print(f"{configs.CoresTexto.AMARELO}[SIMULAÇÃO] {mensagemSimulacao}{configs.CoresTexto.RESET}")
    else:
        print(f"{cor}{mensagemNormal}{configs.CoresTexto.RESET}")