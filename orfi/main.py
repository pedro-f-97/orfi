from . import alvo, configs, inicializar, organizar, reverter


def main():

    argumentos = inicializar.trataArgumentos()

    if argumentos.alvo:
        pastaSelecionada = alvo.defineAlvo()
    else:
        pastaSelecionada = alvo.defineAlvoAqui()

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
        reverter.reverte(pastaSelecionada, categorias, modo)

    else:
        organizar.organiza(pastaSelecionada, categorias, modo)
        

if __name__ == "__main__":
    main()    