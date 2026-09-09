idioma = "en"

class CoresTexto:
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    RESET = "\033[0m"

def definirIdioma(novoIdioma: str):
    """Define o idioma utilizado pelas mensagens.

    Args:
        novoIdioma: Código do idioma a utilizar.
    """
    global idioma
    idioma = novoIdioma

MENSAGENS = {
    "pt": {
        #ficheiros
        "extensao_detectada": "Extensão detectada: {ext}",
        "ficheiro_existente_substituir": "Já existe o ficheiro {ficheiro} na pasta {destino}, substituir? (s/n): ",
        "ficheiro_cancelado": "Ficheiro {ficheiro} cancelado.",
        "ficheiro_copiado": "Ficheiro {ficheiro} copiado para {destino}.",
        "ficheiro_seria_copiado": "[SIMULAÇÃO] Ficheiro {ficheiro} seria copiado para {destino}.",
        "erro_copiar_ficheiro": "Erro '{erro}' no ficheiro {ficheiro}",
        "ficheiro_movido": "Ficheiro {ficheiro} movido para {destino}.",
        "ficheiro_seria_movido": "[SIMULAÇÃO] Ficheiro {ficheiro} seria movido para {destino}.",
        "erro_mover_ficheiro": "Erro '{erro}' no ficheiro {ficheiro}",
        "ficheiro_apagado": "Ficheiro {ficheiro} apagado.",
        "ficheiro_seria_apagado": "[SIMULAÇÃO] Ficheiro {ficheiro} seria apagado.",
        "ficheiro_datado": "Ficheiro {ficheiro} datado para {ficheiroDatado}.",
        "ficheiro_seria_datado": "[SIMULAÇÃO] Ficheiro {ficheiro} seria datado para {ficheiroDatado}.",
        "ficheiro_revertido": "{ficheiro} revertido para {ficheiroRevertido}.",
        "ficheiro_seria_revertido": "[SIMULAÇÃO] {ficheiro} seria revertido para {ficheiroRevertido}.",
        #pastas
        "pasta_criada": "Pasta criada - {pasta}.",
        "pasta_seria_criada": "[SIMULAÇÃO] Pasta {pasta} seria criada.",
        "pasta_eliminada": "Pasta vazia '{pasta}' foi eliminada.",
        "pasta_seria_eliminada": "[SIMULAÇÃO] Pasta {pasta} seria eliminada.",
        "categoria_nao_encontrada": "Categoria não encontrada para {ext}.",
        "pastas_para_criar": "Pastas para criar: {pastas}",
        "nao_vai_criar_pastas": "Não vai criar pastas.",
        "pasta_existente": "Pasta {pasta} já existe.",
        #configs
        "extensao_duplicada": "Extensão duplicada '{extensao}' nas categorias {categorias}.",
        "categoria_duplicada": "Categoria(s) duplicada(s) '{categorias}'.",
        "multiplas_categorias_defeito": "Mais do que uma categoria por defeito: '{categorias}'.",
        "extensoes_incorretas": "Extensões incorretas: '{extensoes}'.",
        #main
        "inicio_simulacao": "[SIMULAÇÃO] Início de simulação.",
        "configuracao_invalida": "Configuração inválida, corrigir o config.toml.",
        "pasta_invalida": "Pasta inválida.",
        "pasta_selecionada": "Pasta selecionada: {pasta}.",
        "fim_simulacao": "[SIMULAÇÃO] Fim de simulação.",
        "idioma_invalido": "Idioma inválido, selecionar um dos idiomas existentes: '{idiomas}'",
        "idioma_alterado": "Idioma alterado para '{idioma}'.",
        #organizar
        "modo_inesperado": "Modo {modo} inesperado. Operação cancelada.",
        "nada_para_fazer": "Nada para fazer.",
        "nada_para_fazer_simula": "Não faria nada.",
        "criar_pastas": "Criar as pastas {pastas}? (s/n): ",
        "operacao_cancelada": "Operação Cancelada",
        "pastas_criadas": "{cont} pastas criadas.",
        "pastas_seriam_criadas": "[SIMULAÇÃO] {cont} pastas seriam criadas.",
        "ficheiro_tratado": "{ficheiro} tratado.",
        "ficheiro_seria_tratado": "[SIMULAÇÃO] {ficheiro} seria tratado.",
        "categoria_caminho_nao_encontrados": "Categoria ou caminho não encontrados para {ficheiro}.",
        "ficheiros_tratados": "Feito, {total} ficheiros {tratamento}",
        "ficheiros_seriam_tratados": "Feito, {total} ficheiros teriam sido {tratamento}",
        "ficheiro_ja_datado": "Ficheiro já datado: {ficheiro}.",
        #reverter
        "nada_para_reverter": "Nada para reverter.",
        "nada_para_reverter_simula": "Não revertia nada.",
        "ficheiros_revertidos": "Revertido, {total} ficheiros {tratamento}",
        "ficheiros_seriam_revertidos": "Revertido, {total} ficheiros teriam sido {tratamento}",
        "ficheiro_ignorado": "Ficheiro ignorado: {ficheiro}",
        "ficheiro_seria_ignorado": "Ficheiro seria ignorado: {ficheiro}",
        #argumentos
        "descricao_orfi": "Organiza ficheiros por categorias.",
        "descricao_alvo": "permite definir a pasta alvo",
        "descricao_copiar": "copia os ficheiros em vez de mover",
        "descricao_reverter": "reverte o processo escolhido",
        "descricao_datar": "adiciona a data de criação ao nome de cada ficheiro",
        "descricao_force": "aprova automaticamente todas as alterações",
        "descricao_simula": "simula o processo sem fazer alterações",
        "descricao_idioma": "altera o idioma para o introduzido",
    },

    "en": {
        #ficheiros
        "extensao_detectada": "Extension detected: {ext}",
        "ficheiro_existente_substituir": "File {ficheiro} already exists in folder {destino}, replace? (y/n): ",
        "ficheiro_cancelado": "File {ficheiro} cancelled.",
        "ficheiro_copiado": "File {ficheiro} copied to {destino}.",
        "ficheiro_seria_copiado": "[SIMULATION] File {ficheiro} would be copied to {destino}.",
        "erro_copiar_ficheiro": "Error '{erro}' on file {ficheiro}",
        "ficheiro_movido": "File {ficheiro} moved to {destino}.",
        "ficheiro_seria_movido": "[SIMULATION] File {ficheiro} would be moved to {destino}.",
        "erro_mover_ficheiro": "Error '{erro}' on file {ficheiro}",
        "ficheiro_apagado": "File {ficheiro} deleted.",
        "ficheiro_seria_apagado": "[SIMULATION] File {ficheiro} would be deleted.",
        "ficheiro_datado": "File {ficheiro} dated to {ficheiroDatado}.",
        "ficheiro_seria_datado": "[SIMULATION] File {ficheiro} would be dated to {ficheiroDatado}.",
        "ficheiro_revertido": "{ficheiro} reverted to {ficheiroRevertido}.",
        "ficheiro_seria_revertido": "[SIMULATION] {ficheiro} would be reverted to {ficheiroRevertido}.",
        #pastas
        "pasta_criada": "Folder created - {pasta}.",
        "pasta_seria_criada": "[SIMULATION] Folder {pasta} would be created.",
        "pasta_eliminada": "Empty folder '{pasta}' was deleted.",
        "pasta_seria_eliminada": "[SIMULATION] Folder {pasta} would be deleted.",
        "categoria_nao_encontrada": "Category not found for {ext}.",
        "pastas_para_criar": "Folders to create: {pastas}",
        "nao_vai_criar_pastas": "No folders will be created.",
        "pasta_existente": "Folder {pasta} already exists.",
        #configs
        "extensao_duplicada": "Duplicate extension '{extensao}' in categories {categorias}.",
        "categoria_duplicada": "Duplicate category/categories '{categorias}'.",
        "multiplas_categorias_defeito": "More than one default category: '{categorias}'.",
        "extensoes_incorretas": "Invalid extensions: '{extensoes}'.",
        #main
        "inicio_simulacao": "[SIMULATION] Simulation started.",
        "configuracao_invalida": "Invalid configuration, fix the config.toml.",
        "pasta_invalida": "Invalid folder.",
        "pasta_selecionada": "Selected folder: {pasta}.",
        "fim_simulacao": "[SIMULATION] Simulation ended.",
        "idioma_invalido": "Language unavailable, select one of the existing languages: '{idiomas}'",
        "idioma_alterado": "Language changed to '{idioma}'.",
        #organizar
        "modo_inesperado": "Unexpected mode {modo}. Operation cancelled.",
        "nada_para_fazer": "Nothing to do.",
        "nada_para_fazer_simula": "Wouldn't do anything.",
        "criar_pastas": "Create folders {pastas}? (y/n): ",
        "operacao_cancelada": "Operation Cancelled",
        "pastas_criadas": "{cont} folders created.",
        "pastas_seriam_criadas": "[SIMULATION] {cont} folders would be created.",
        "ficheiro_tratado": "File {ficheiro} processed.",
        "ficheiro_seria_tratado": "[SIMULATION] File {ficheiro} would be processed.",
        "categoria_caminho_nao_encontrados": "Category or path not found for {ficheiro}.",
        "ficheiros_tratados": "Done, {total} files handled",
        "ficheiros_seriam_tratados": "Done, {total} files would have been handled",
        "ficheiro_ja_datado": "File already dated: {ficheiro}.",
        #reverter
        "nada_para_reverter": "Nothing to revert.",
        "nada_para_reverter_simula": "Nothing would be reverted.",
        "ficheiros_revertidos": "Reverted, {total} files handled",
        "ficheiros_seriam_revertidos": "Reverted, {total} files would have been handled",
        "ficheiro_ignorado": "File ignored: {ficheiro}",
        "ficheiro_seria_ignorado": "File would be ignored: {ficheiro}",
        #argumentos
        "descricao_orfi": "Organizes files by category",
        "descricao_alvo": "allows selection of the target folder",
        "descricao_copiar": "copies the files instead of moving",
        "descricao_reverter": "reverts the selected process",
        "descricao_datar": "adds creation date to the name of each file",
        "descricao_force": "auto-approves all changes",
        "descricao_simula": "simulates the process without making changes",
        "descricao_idioma": "changes the language to the specified one",
    },
}

def mensagem(chaveNormal: str, chaveSimulacao: str, simula: bool, cor: str, **kwargs):
    """Imprime uma mensagem de acordo com o argumento simula.

    Args:
        chaveNormal: Chave da mensagem apresentada numa execução normal.
        chaveSimulacao: Chave da mensagem apresentada numa simulação.
        simula: Indica se é uma simulação.
        cor: Cor a utilizar para a mensagem.
        **kwargs: Valores utilizados para preencher os campos da mensagem.
    """
    chave = chaveSimulacao if simula else chaveNormal
    texto = mensagemTrataIdioma(chave, **kwargs)

    print(f"{cor}{texto}{CoresTexto.RESET}")

def mensagemTrataIdioma(chave: str, **kwargs) -> str:
    """Devolve a mensagem no idioma atualmente configurado.

    Args:
        chave: Identificador da mensagem a obter.
        **kwargs: Valores utilizados para preencher os campos da mensagem.

    Returns:
        Mensagem traduzida e formatada.
    """
    return MENSAGENS[idioma][chave].format(**kwargs)