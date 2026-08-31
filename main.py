import sys
from pathlib import Path
from tkinter import Tk, filedialog

import configs
import ficheiros
import pastas

janela = Tk()
janela.withdraw()

pastaSelecionada = filedialog.askdirectory(
    title="Selecionar pasta para organizar",
    mustexist=True
)

janela.destroy()

print(f"{configs.CoresTexto.AZUL}Pasta selecionada: {pastaSelecionada} {configs.CoresTexto.RESET}")

if not pastaSelecionada:
    print(f"{configs.CoresTexto.AMARELO}Nenhuma pasta selecionada.{configs.CoresTexto.RESET}")
    sys.exit()

if not Path(pastaSelecionada).is_dir():
    print(f"{configs.CoresTexto.AMARELO}Pasta inválida.{configs.CoresTexto.RESET}")
    sys.exit()
    
pasta = Path(pastaSelecionada)

categorias = configs.iniciarCategorias()

pastasParaCriar = pastas.devolvePastas(ficheiros.devolveExt(pasta), categorias)

if pastasParaCriar == set():
    print(f"{configs.CoresTexto.AMARELO}Nada para fazer.{configs.CoresTexto.RESET}")
    sys.exit()

confirmacao = input(f"{configs.CoresTexto.AZUL}Criar as pastas {pastasParaCriar}? (s/n): {configs.CoresTexto.RESET}")
if confirmacao.lower() == "s":
    pastas.criaPastas(pasta, pastasParaCriar, categorias)
else:
    print(f"{configs.CoresTexto.AMARELO}Operação Cancelada{configs.CoresTexto.RESET}")
    sys.exit()

ficheirosLista = ficheiros.devolveFicheiros(pasta)

total = 0
for ficheiro in ficheirosLista:
    destino = ficheiros.defineDestino(ficheiro, categorias)
    if destino is not None:
        total += ficheiros.copiaFicheiro(ficheiro, destino)
    else:
        print(f"{configs.CoresTexto.AMARELO}Categoria ou caminho não encontrados para {ficheiro.name}{configs.CoresTexto.RESET}")

print(f"{configs.CoresTexto.VERDE}Feito, {total} ficheiros copiados.{configs.CoresTexto.RESET}")